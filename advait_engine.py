"""Advait bounded, approval-aware task engine (offline-first reference core).

No network adapters or owner-authentication provider are included. External
actions must be injected, allowlisted, and policy-gated. A task is not DONE
until an injected evidence_verifier independently accepts its evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import copy
import os
import sqlite3
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


class SQLiteLedger:
    """Optional durable local event ledger using Python's standard sqlite3.

    This stores operational events, not secrets or legal/financial source records.
    It is not encrypted and its hash chain is not externally anchored.
    """
    def __init__(self, path: str):
        if not isinstance(path, str) or not path:
            raise ValueError("database path is required")
        if path != ":memory:" and os.path.islink(path):
            raise ValueError("database path must not be a symlink")
        self.path = path
        self.connection = sqlite3.connect(path, timeout=5.0, isolation_level=None)
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.execute("PRAGMA busy_timeout=5000")
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS ledger ("
            "seq INTEGER PRIMARY KEY AUTOINCREMENT, "
            "previous_hash TEXT NOT NULL, "
            "event_json TEXT NOT NULL, "
            "entry_hash TEXT NOT NULL UNIQUE)"
        )
        if path != ":memory:":
            try:
                os.chmod(path, 0o600)
            except OSError:
                self.connection.close()
                raise

    @staticmethod
    def _canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False)

    def append(self, event: dict):
        event_json = self._canonical(event)
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            row = self.connection.execute(
                "SELECT entry_hash FROM ledger ORDER BY seq DESC LIMIT 1"
            ).fetchone()
            previous = row[0] if row else "0" * 64
            body = {"previous": previous, "event": json.loads(event_json)}
            digest = sha256(self._canonical(body).encode("utf-8")).hexdigest()
            self.connection.execute(
                "INSERT INTO ledger(previous_hash,event_json,entry_hash) VALUES(?,?,?)",
                (previous, event_json, digest),
            )
            self.connection.execute("COMMIT")
        except Exception:
            self.connection.execute("ROLLBACK")
            raise

    def verify(self):
        previous = "0" * 64
        try:
            rows = self.connection.execute(
                "SELECT previous_hash,event_json,entry_hash FROM ledger ORDER BY seq"
            ).fetchall()
            for stored_previous, event_json, stored_hash in rows:
                if stored_previous != previous:
                    return False
                event = json.loads(event_json)
                body = {"previous": previous, "event": event}
                expected = sha256(self._canonical(body).encode("utf-8")).hexdigest()
                if expected != stored_hash:
                    return False
                previous = stored_hash
            return True
        except (sqlite3.Error, TypeError, ValueError, KeyError):
            return False

    def export_json(self):
        rows = self.connection.execute(
            "SELECT previous_hash,event_json,entry_hash FROM ledger ORDER BY seq"
        ).fetchall()
        entries = [
            {"previous": previous, "event": json.loads(event_json), "hash": digest}
            for previous, event_json, digest in rows
        ]
        return json.dumps(entries, indent=2, sort_keys=True,
                          ensure_ascii=False, allow_nan=False)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()


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
    """Run a real local calculation and prove a high-risk action is blocked.

    This is an offline self-run, not a live customer, network, or payment action.
    """
    tasks = [
        Task("T1", "Add two numbers", "local", "calculate",
             {"x": 4, "y": 5}),
        Task("T2", "Write a file (approval-gated)", "local", "write_file",
             {"name": "example.txt", "content": "demo"}, Risk.HIGH),
    ]

    def local_adapter(task):
        if task.action == "calculate":
            value = task.payload["x"] + task.payload["y"]
            return {"outcome": "success", "value": value,
                    "evidence": f"sum:{value}"}
        if task.action == "write_file":
            # This branch must never run without an authenticated owner verifier.
            return {"outcome": "success", "evidence": "unexpected dry-run"}
        return {"outcome": "failure", "evidence": ""}

    def verify_calculation(task, output):
        if task.action != "calculate":
            return False
        expected = task.payload["x"] + task.payload["y"]
        return output.get("value") == expected and output.get("evidence") == f"sum:{expected}"

    engine = Engine(
        Policy({"local": {"calculate", "write_file"}}),
        evidence_verifier=verify_calculation,
    )
    engine.run(tasks, {"local": local_adapter})
    report = {
        "engine": "ADVAIT",
        "mode": "offline_self_run",
        "calculation": {"input": [4, 5], "actual_result": 9,
                        "status": tasks[0].status.value},
        "high_risk_action": {"status": tasks[1].status.value,
                             "adapter_attempts": tasks[1].attempts},
        "ledger_integrity": engine.ledger.verify(),
        "summary": engine.summary(tasks),
        "external_network_actions": False,
        "payment_actions": False,
    }
    assert tasks[0].status == Status.DONE
    assert tasks[1].status == Status.NEEDS_APPROVAL
    assert tasks[1].attempts == 0
    assert report["ledger_integrity"] is True
    return report


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True))
