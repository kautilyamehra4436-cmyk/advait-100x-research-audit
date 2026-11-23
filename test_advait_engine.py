import unittest
from advait_engine import Engine,Policy,Limits,Ledger,Task,Risk,Status
class EngineTests(unittest.TestCase):
 def setup_engine(self,allow={"local":{"read","write"}}):
  return Engine(Policy(allow),Limits(max_steps=5,max_calls=5,max_seconds=2))
 def test_allowlist(self):
  e=self.setup_engine(); t=Task("1","x","bad","read",{})
  e.run([t],{"bad":lambda t:{"outcome":"success","evidence":"ok"}})
  self.assertEqual(t.status,Status.FAILED)
 def test_high_risk_requires_exact_approval(self):
  e=self.setup_engine(); t=Task("2","write","local","write",{"path":"a"},Risk.HIGH)
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"ok"}})
  self.assertEqual(t.status,Status.NEEDS_APPROVAL)
 def test_exact_approval(self):
  e=self.setup_engine(); t=Task("3","write","local","write",{"path":"a"},Risk.HIGH)
  token=Policy.approval_token(t)
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"proof"}},{"3":token})
  self.assertEqual(t.status,Status.DONE)
 def test_changed_payload_invalidates_approval(self):
  e=self.setup_engine(); t=Task("4","write","local","write",{"path":"a"},Risk.HIGH)
  token=Policy.approval_token(t); t.payload["path"]="b"
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"proof"}},{"4":token})
  self.assertEqual(t.status,Status.NEEDS_APPROVAL)
 def test_no_evidence_not_done(self):
  e=self.setup_engine(); t=Task("5","read","local","read",{})
  e.run([t],{"local":lambda t:{"outcome":"success"}})
  self.assertEqual(t.status,Status.NEEDS_RECONCILIATION)
 def test_unknown_outcome_reconcile(self):
  e=self.setup_engine(); t=Task("6","read","local","read",{})
  e.run([t],{"local":lambda t:{"outcome":"unknown"}})
  self.assertEqual(t.status,Status.NEEDS_RECONCILIATION)
 def test_exception_reconcile(self):
  e=self.setup_engine(); t=Task("7","read","local","read",{})
  def crash(_): raise TimeoutError()
  e.run([t],{"local":crash})
  self.assertEqual(t.status,Status.NEEDS_RECONCILIATION)
 def test_payload_cap(self):
  e=self.setup_engine(); e.limits.max_payload_bytes=5
  t=Task("8","large","local","read",{"data":"123456"})
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"x"}})
  self.assertEqual(t.status,Status.FAILED)
 def test_step_budget(self):
  e=self.setup_engine(); e.limits.max_steps=1
  tasks=[Task(str(i),"r","local","read",{}) for i in range(3)]
  e.run(tasks,{"local":lambda t:{"outcome":"success","evidence":"ok"}})
  self.assertEqual(sum(t.status==Status.DONE for t in tasks),1)
 def test_ledger_integrity(self):
  l=Ledger(); l.append({"ok":1}); l.append({"ok":2})
  self.assertTrue(l.verify()); l.entries[0]["event"]["ok"]=9
  self.assertFalse(l.verify())
if __name__=="__main__": unittest.main(verbosity=2)
