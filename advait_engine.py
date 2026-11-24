"""Advait bounded, approval-aware task engine (offline-first reference implementation).
No network adapters are included. External actions must be injected and policy-gated.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json, time
from typing import Callable, Any

class Status(str, Enum):
    PENDING="pending"; RUNNING="running"; DONE="done"; FAILED="failed"
    NEEDS_APPROVAL="needs_approval"; NEEDS_RECONCILIATION="needs_reconciliation"

class Risk(str, Enum):
    LOW="low"; HIGH="high"

@dataclass
class Task:
    task_id: str
    title: str
    tool: str
    action: str
    payload: dict
    risk: Risk=Risk.LOW
    status: Status=Status.PENDING
    attempts: int=0
    result: str=""
    evidence: str=""

@dataclass
class Limits:
    max_steps: int=30
    max_calls: int=20
    max_seconds: float=15.0
    max_payload_bytes: int=65536

class Policy:
    """Allowlist plus externally authenticated, exact-action approval.

    A locally computable digest is NOT owner authentication. High-risk work is
    denied unless the host injects an approval_verifier backed by an authenticated
    owner channel. This offline engine intentionally supplies no such verifier.
    """
    def __init__(self, allowlist: dict[str, set[str]]|None=None,
                 approval_verifier: Callable[[Task, str], bool]|None=None):
        self.allowlist=allowlist or {}
        self.approval_verifier=approval_verifier

    def check(self, task: Task, approval: str|None=None):
        if task.tool not in self.allowlist or task.action not in self.allowlist[task.tool]:
            raise PermissionError("Tool/action is not allowlisted")
        if task.risk is Risk.HIGH:
            if self.approval_verifier is None:
                raise PermissionError("Authenticated owner approval provider unavailable; fail-closed")
            try:
                valid = bool(self.approval_verifier(task, approval or ""))
            except Exception:
                valid = False
            if not valid:
                raise PermissionError("Authenticated exact-action owner approval required")

class Ledger:
    def __init__(self): self.entries=[]
    def append(self, event: dict):
        prev=self.entries[-1]["hash"] if self.entries else "0"*64
        body={"previous":prev,"event":event}
        digest=sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        self.entries.append({**body,"hash":digest})
    def verify(self):
        previous="0"*64
        for entry in self.entries:
            body={"previous":previous,"event":entry["event"]}
            expected=sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()
            if expected!=entry.get("hash"): return False
            previous=entry["hash"]
        return True
    def export_json(self):
        return json.dumps(self.entries,indent=2,sort_keys=True)

class Engine:
    def __init__(self, policy:Policy, limits:Limits|None=None, ledger:Ledger|None=None):
        self.policy=policy; self.limits=limits or Limits(); self.ledger=ledger or Ledger()
        self.steps=0; self.calls=0; self.started=None
    def run(self, tasks:list[Task], adapters:dict[str,Callable[[Task],dict[str,Any]]], approvals:dict[str,str]|None=None):
        approvals=approvals or {}; self.started=time.monotonic()
        for task in tasks:
            if task.status is not Status.PENDING: continue
            if self.steps>=self.limits.max_steps or self.calls>=self.limits.max_calls or time.monotonic()-self.started>=self.limits.max_seconds:
                self.ledger.append({"type":"budget_stop","task":task.task_id}); break
            if len(json.dumps(task.payload).encode())>self.limits.max_payload_bytes:
                task.status=Status.FAILED; task.result="payload_limit"
                self.ledger.append({"type":"rejected","task":task.task_id,"reason":"payload_limit"}); continue
            self.steps+=1
            try: self.policy.check(task, approvals.get(task.task_id))
            except PermissionError as e:
                task.status=Status.NEEDS_APPROVAL if "approval" in str(e).lower() else Status.FAILED
                task.result=str(e); self.ledger.append({"type":"policy_denied","task":task.task_id,"reason":str(e)}); continue
            adapter=adapters.get(task.tool)
            if adapter is None:
                task.status=Status.FAILED; task.result="adapter_missing"
                self.ledger.append({"type":"adapter_missing","task":task.task_id}); continue
            task.status=Status.RUNNING; task.attempts+=1; self.calls+=1
            try:
                output=adapter(task) or {}
                outcome=output.get("outcome","unknown")
                evidence=str(output.get("evidence",""))
                task.evidence=evidence
                if outcome=="success" and evidence:
                    task.status=Status.DONE; task.result="verified_by_adapter_evidence"
                elif outcome=="failure":
                    task.status=Status.FAILED; task.result="adapter_reported_failure"
                else:
                    task.status=Status.NEEDS_RECONCILIATION; task.result="unknown_or_unverified"
                self.ledger.append({"type":"task_result","task":task.task_id,"outcome":outcome,"evidence_present":bool(evidence),"status":task.status.value})
            except Exception as exc:
                task.status=Status.NEEDS_RECONCILIATION
                task.result="adapter_exception; reconcile before retry"
                self.ledger.append({"type":"adapter_exception","task":task.task_id,"exception_type":type(exc).__name__})
        return tasks
    def summary(self,tasks):
        return {s.value:sum(t.status is s for t in tasks) for s in Status}
def demo():
    tasks=[Task("T1","Local calculation","local","calculate",{"x":4}),
           Task("T2","Create a file (approval-gated)","local","write_file",{"name":"example.txt","content":"demo"},Risk.HIGH)]
    engine=Engine(Policy({"local":{"calculate","write_file"}}))
    adapters={"local":lambda t: {"outcome":"success","evidence":"computed result: 4" if t.action=="calculate" else "dry-run only"}}
    engine.run(tasks,adapters)
    print("Status:",engine.summary(tasks))
    print("Ledger integrity:",engine.ledger.verify())
    print(engine.ledger.export_json())
if __name__=="__main__": demo()
