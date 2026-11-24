import unittest
from advait_engine import Engine,Policy,Limits,Ledger,Task,Risk,Status
from atc_handoff import from_atc_candidate, to_task, validate

class EngineTests(unittest.TestCase):
 def setup_engine(self,allow={"local":{"read","write"}}):
  return Engine(Policy(allow),Limits(max_steps=5,max_calls=5,max_seconds=2))
 def test_allowlist(self):
  e=self.setup_engine(); t=Task("1","x","bad","read",{})
  e.run([t],{"bad":lambda t:{"outcome":"success","evidence":"ok"}})
  self.assertEqual(t.status,Status.FAILED)
 def test_high_risk_fails_closed_without_authenticated_provider(self):
  e=self.setup_engine(); t=Task("2","write","local","write",{"path":"a"},Risk.HIGH)
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"ok"}})
  self.assertEqual(t.status,Status.NEEDS_APPROVAL)
  self.assertEqual(t.attempts,0)
 def test_authenticated_provider_can_approve_exact_task(self):
  verifier=lambda task, credential: credential=="verified-owner-session" and task.payload=={"path":"a"}
  e=Engine(Policy({"local":{"write"}},approval_verifier=verifier),Limits(max_seconds=2))
  t=Task("3","write","local","write",{"path":"a"},Risk.HIGH)
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"proof"}},{"3":"verified-owner-session"})
  self.assertEqual(t.status,Status.DONE)
 def test_wrong_or_stale_approval_denied(self):
  verifier=lambda task, credential: credential=="verified-owner-session" and task.payload=={"path":"a"}
  e=Engine(Policy({"local":{"write"}},approval_verifier=verifier),Limits(max_seconds=2))
  t=Task("4","write","local","write",{"path":"b"},Risk.HIGH)
  e.run([t],{"local":lambda t:{"outcome":"success","evidence":"proof"}},{"4":"verified-owner-session"})
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

class HandoffTests(unittest.TestCase):
 def sample(self):
  return from_atc_candidate(task_id="ATC-1",title="Review opportunity",tool="local",action="review",payload={"source":"user-approved"},risk="low")
 def test_round_trip(self):
  env=self.sample(); task=to_task(env)
  self.assertEqual(task.task_id,"ATC-1"); self.assertEqual(task.payload,{"source":"user-approved"})
 def test_tamper_detected(self):
  env=self.sample(); env["payload"]["source"]="changed"
  with self.assertRaises(ValueError): validate(env)
 def test_unknown_schema_rejected(self):
  env=self.sample(); env["schema_version"]="v99"
  with self.assertRaises(ValueError): validate(env)
 def test_auto_execute_state_rejected(self):
  env=self.sample(); env["state"]="AUTHORIZED"
  with self.assertRaises(ValueError): validate(env)
 def test_unknown_fields_rejected(self):
  env=self.sample(); env["extra"]="not-allowed"
  with self.assertRaises(ValueError): validate(env)

if __name__=="__main__": unittest.main(verbosity=2)
