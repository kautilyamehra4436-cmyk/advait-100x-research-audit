"""Advait bounded, approval-aware task engine (offline-first reference core).

No network adapters or owner-authentication provider are included. External
actions must be injected, allowlisted, and policy-gated. A task is not DONE
until an injected evidence_verifier independently accepts its evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import copy
from enum import Enum
from hashlib import sha256
import json
import time
from typing import Callable, Any


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    NEEDS_APPROVAL = "needs_approval"
    NEEDS_RECONCILIATION = "needs_reconciliation"


class Risk(str, Enum):
    LOW = "low"
    HIGH = "high"


@dataclass
class Task:
    task_id: str
    title: str
    tool: str
    action: str
    payload: dict
    risk: Risk = Risk.LOW
    status: Status = Status.PENDING
    attempts: int = 0
    result: str = ""
    evidence: str = ""


@dataclass
class Limits:
    max_steps: int = 30
    max_calls: int = 20
    max_seconds: float = 15.0
    max_payload_bytes: int = 65536

    def __post_init__(self):
        if self.max_steps < 0 or self.max_calls < 0:
            raise ValueError("step/call budgets must be non-negative")
        if self.max_seconds < 0 or self.max_payload_bytes < 0:
            raise ValueError("time/payload budgets must be non-negative")


class Policy:
    """Allowlist plus externally authenticated, exact-task approval.

    A locally computable digest is NOT owner authentication. High-risk work is
    denied unless the host injects an approval_verifier backed by an authenticated
    owner channel. This offline engine intentionally supplies no such verifier.
    """
    def __init__(self, allowlist: dict[str, set[str]] | None = None,
                 approval_verifier: Callable[[Task, str], bool] | None = None):
        self.allowlist = allowlist or {}
        self.approval_verifier = approval_verifier

    def check(self, task: Task, approval: str | None = None):
        if not isinstance(task.tool, str) or not isinstance(task.action, str):
            raise PermissionError("Invalid tool/action type")
        if task.tool not in self.allowlist or task.action not in self.allowlist[task.tool]:
            raise PermissionError("Tool/action is not allowlisted")
        try:
            risk = Risk(task.risk)
        except (TypeError, ValueError):
            raise PermissionError("Invalid risk level")
        if risk == Risk.HIGH:
            if self.approval_verifier is None:
                raise PermissionError("Authenticated owner approval provider unavailable; fail-closed")
            try:
                valid = bool(self.approval_verifier(task, approval or ""))
            except Exception:
                valid = False
            if not valid:
                raise PermissionError("Authenticated exact-task owner approval required")


class Ledger:
    def __init__(self):
        self.entries = []

    def append(self, event: dict):
        previous = self.entries[-1]["hash"] if self.entries else "0" * 64
        body = {"previous": previous, "event": event}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False, allow_nan=False)
        digest = sha256(canonical.encode("utf-8")).hexdigest()
        self.entries.append({**body, "hash": digest})

    def verify(self):
        previous = "0" * 64
        try:
            for entry in self.entries:
                body = {"previous": previous, "event": entry["event"]}
                canonical = json.dumps(body, sort_keys=True, separators=(",", ":"),
                                       ensure_ascii=False, allow_nan=False)
                expected = sha256(canonical.encode("utf-8")).hexdigest()
                if expected != entry.get("hash"):
                    return False
                previous = entry["hash"]
            return True
        except (KeyError, TypeError, ValueError):
            return False

    def export_json(self):
        return json.dumps(self.entries, indent=2, sort_keys=True,
                          ensure_ascii=False, allow_nan=False)


class Engine:
    def __init__(self, policy: Policy, limits: Limits | None = None,
                 ledger: Ledger | None = None,
                 evidence_verifier: Callable[[Task, dict[str, Any]], bool] | None = None):
        self.policy = policy
        self.limits = limits or Limits()
        self.ledger = ledger or Ledger()
        self.evidence_verifier = evidence_verifier
        self.steps = 0
        self.calls = 0
        self.started = None

    def _reject(self, task: Task, reason: str):
        task.status = Status.FAILED
        task.result = reason
        self.ledger.append({"type": "rejected", "task": str(task.task_id),
                            "reason": reason})

    def run(self, tasks: list[Task],
            adapters: dict[str, Callable[[Task], dict[str, Any]]],
            approvals: dict[str, str] | None = None):
        approvals = approvals or {}
        self.started = time.monotonic()
        seen_ids = set()

        for task in tasks:
            if not isinstance(task, Task):
                continue
            if not isinstance(task.task_id, str) or not task.task_id.strip():
                self._reject(task, "invalid_task_id")
                continue
            if task.task_id in seen_ids:
                self._reject(task, "duplicate_task_id")
                continue
            seen_ids.add(task.task_id)

            try:
                task_status = Status(task.status)
            except (TypeError, ValueError):
                self._reject(task, "invalid_task_status")
                continue
            if task_status != Status.PENDING:
                continue
            task.status = Status.PENDING

            if (self.steps >= self.limits.max_steps or
                    self.calls >= self.limits.max_calls or
                    time.monotonic() - self.started >= self.limits.max_seconds):
                self.ledger.append({"type": "budget_stop", "task": task.task_id})
                break

            try:
                if not isinstance(task.payload, dict):
                    raise TypeError("payload must be an object")
                payload_bytes = len(json.dumps(
                    task.payload, sort_keys=True, ensure_ascii=False,
                    separators=(",", ":"), allow_nan=False
                ).encode("utf-8"))
            except (TypeError, ValueError, RecursionError):
                self._reject(task, "invalid_payload")
                continue
            if payload_bytes > self.limits.max_payload_bytes:
                self._reject(task, "payload_limit")
                continue

            self.steps += 1
            try:
                self.policy.check(task, approvals.get(task.task_id))
            except PermissionError as exc:
                message = str(exc)
                task.status = (Status.NEEDS_APPROVAL
                               if "approval" in message.lower() else Status.FAILED)
                task.result = message
                self.ledger.append({"type": "policy_denied", "task": task.task_id,
                                    "reason": message})
                continue

            adapter = adapters.get(task.tool)
            if adapter is None:
                task.status = Status.FAILED
                task.result = "adapter_missing"
                self.ledger.append({"type": "adapter_missing", "task": task.task_id})
                continue

            task.status = Status.RUNNING
            task.attempts += 1
            self.calls += 1
            try:
                # Adapters receive an isolated snapshot; they cannot mutate the
                # policy-approved task object or its payload after authorization.
                output = adapter(copy.deepcopy(task))
                if not isinstance(output, dict):
                    task.status = Status.NEEDS_RECONCILIATION
                    task.result = "adapter_output_not_object"
                    self.ledger.append({"type": "invalid_adapter_output",
                                        "task": task.task_id})
                    continue

                outcome = output.get("outcome", "unknown")
                evidence = output.get("evidence", "")
                task.evidence = evidence if isinstance(evidence, str) else ""

                if outcome == "failure":
                    task.status = Status.FAILED
                    task.result = "adapter_reported_failure"
                elif outcome == "success" and task.evidence:
                    if self.evidence_verifier is None:
                        task.status = Status.NEEDS_RECONCILIATION
                        task.result = "evidence_verifier_unavailable"
                    else:
                        try:
                            evidence_ok = bool(self.evidence_verifier(task, output))
                        except Exception:
                            evidence_ok = False
                        if evidence_ok:
                            task.status = Status.DONE
                            task.result = "evidence_independently_verified"
                        else:
                            task.status = Status.NEEDS_RECONCILIATION
                            task.result = "evidence_verification_failed"
                else:
                    task.status = Status.NEEDS_RECONCILIATION
                    task.result = "unknown_or_unverified"

                self.ledger.append({
                    "type": "task_result",
                    "task": task.task_id,
                    "outcome": str(outcome)[:80],
                    "evidence_present": bool(task.evidence),
                    "status": task.status.value,
                    "result": task.result,
                })
            except Exception as exc:
                task.status = Status.NEEDS_RECONCILIATION
                task.result = "adapter_exception; reconcile before retry"
                self.ledger.append({"type": "adapter_exception",
                                    "task": task.task_id,
                                    "exception_type": type(exc).__name__})
        return tasks

    def summary(self, tasks):
        return {status.value: sum(Status(t.status) == status for t in tasks
                                  if isinstance(t, Task))
                for status in Status}


def demo():
    tasks = [
        Task("T1", "Local calculation", "local", "calculate", {"x": 4}),
        Task("T2", "Create a file (approval-gated)", "local", "write_file",
             {"name": "example.txt", "content": "demo"}, Risk.HIGH),
    ]
    engine = Engine(
        Policy({"local": {"calculate", "write_file"}}),
        evidence_verifier=lambda task, output: (
            isinstance(output.get("evidence"), str) and bool(output["evidence"])
        ),
    )
    adapters = {
        "local": lambda task: {
            "outcome": "success",
            "evidence": "computed result: 4" if task.action == "calculate" else "dry-run only",
        }
    }
    engine.run(tasks, adapters)
    print("Status:", engine.summary(tasks))
    print("Ledger integrity:", engine.ledger.verify())
    print(engine.ledger.export_json())


if __name__ == "__main__":
    demo()
