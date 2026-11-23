"""Offline mock tests for Advait policy and reliability controls."""
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
class Outcome(str,Enum):
 SUCCESS="confirmed_success"; FAILURE="confirmed_failure"; UNKNOWN="unknown_outcome"
@dataclass
class ToolResult:
 outcome:Outcome
 evidence:str=""
class BudgetExceeded(RuntimeError): pass
class PolicyDenied(RuntimeError): pass
class Budget:
 def __init__(self,max_steps=3,max_calls=3): self.max_steps=max_steps; self.max_calls=max_calls; self.steps=0; self.calls=0
 def step(self):
  self.steps+=1
  if self.steps>self.max_steps: raise BudgetExceeded("step limit")
 def call(self):
  self.calls+=1
  if self.calls>self.max_calls: raise BudgetExceeded("call limit")
class Policy:
 def __init__(self,allowed_tools=(),approval_actions=()): self.allowed=set(allowed_tools); self.approvals=set(approval_actions)
 def authorize(self,tool,action,approved=False):
  if tool not in self.allowed: raise PolicyDenied("tool not allowlisted")
  if action in self.approvals and not approved: raise PolicyDenied("approval required")
class Ledger:
 def __init__(self): self.events=[]
 def record(self,event):
  previous=self.events[-1]["hash"] if self.events else "0"*64
  payload={"prev":previous,"event":event}
  digest=sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
  self.events.append({**payload,"hash":digest})
 def valid(self):
  prev="0"*64
  for e in self.events:
   p={"prev":prev,"event":e["event"]}
   if sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()!=e["hash"]: return False
   prev=e["hash"]
  return True
class Engine:
 def __init__(self,policy,budget,ledger): self.policy=policy; self.budget=budget; self.ledger=ledger
 def execute(self,tool,action,result,approved=False):
  self.budget.step(); self.budget.call(); self.policy.authorize(tool,action,approved)
  self.ledger.record({"tool":tool,"action":action,"outcome":result.outcome.value,"evidence":result.evidence})
  if result.outcome==Outcome.UNKNOWN: return "needs_reconciliation"
  if result.outcome==Outcome.SUCCESS and not result.evidence: return "not_verified"
  return result.outcome.value
def test_allowlist_blocks_untrusted_tool():
 try: Policy(["safe"]).authorize("unknown","read")
 except PolicyDenied: return
 raise AssertionError("unlisted tool should be blocked")
def test_irreversible_action_requires_approval():
 try: Policy(["payments"],["transfer"]).authorize("payments","transfer")
 except PolicyDenied: return
 raise AssertionError("approval required")
def test_approval_allows_authorized_action():
 p=Policy(["payments"],["transfer"]); p.authorize("payments","transfer",approved=True)
def test_unknown_outcome_requires_reconciliation():
 e=Engine(Policy(["mock"]),Budget(),Ledger())
 assert e.execute("mock","send",ToolResult(Outcome.UNKNOWN))=="needs_reconciliation"
def test_success_without_evidence_not_verified():
 e=Engine(Policy(["mock"]),Budget(),Ledger())
 assert e.execute("mock","create",ToolResult(Outcome.SUCCESS))=="not_verified"
def test_step_budget_enforced():
 b=Budget(max_steps=1); b.step()
 try: b.step()
 except BudgetExceeded: return
 raise AssertionError("step cap should stop")
def test_call_budget_enforced():
 b=Budget(max_calls=1); b.call()
 try: b.call()
 except BudgetExceeded: return
 raise AssertionError("call cap should stop")
def test_ledger_tamper_detection():
 l=Ledger(); l.record({"v":"ok"}); l.record({"v":"verified"})
 assert l.valid(); l.events[0]["event"]["v"]="changed"; assert not l.valid()
def test_ledger_order_detection():
 l=Ledger(); l.record({"n":1}); l.record({"n":2}); l.events.reverse()
 assert not l.valid()
def test_denied_tool_not_recorded():
 l=Ledger(); e=Engine(Policy(["allowed"]),Budget(),l)
 try: e.execute("blocked","read",ToolResult(Outcome.SUCCESS,"proof"))
 except PolicyDenied: pass
 else: raise AssertionError("denial expected")
 assert l.events==[]
if __name__=="__main__":
 tests=[f for n,f in globals().items() if n.startswith("test_")]
 for f in tests: f(); print("PASS:",f.__name__)
 print(f"\n{len(tests)}/{len(tests)} passed")
