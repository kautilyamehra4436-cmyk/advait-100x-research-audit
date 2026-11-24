import math
import unittest
from advait_engine import Engine, Policy, Limits, Ledger, Task, Risk, Status
from atc_handoff import from_atc_candidate, to_task, validate


def mock_evidence(task, output):
    value = output.get("evidence")
    return isinstance(value, str) and bool(value) and task.task_id in ("3", "5", "9", "10", "11", "12")


class EngineTests(unittest.TestCase):
    def setup_engine(self, allow=None):
        allow = allow or {"local": {"read", "write"}}
        return Engine(Policy(allow), Limits(max_steps=5, max_calls=5, max_seconds=2),
                      evidence_verifier=lambda task, output: bool(output.get("evidence")))

    def test_allowlist(self):
        e = self.setup_engine()
        t = Task("1", "x", "bad", "read", {})
        e.run([t], {"bad": lambda task: {"outcome": "success", "evidence": "ok"}})
        self.assertEqual(t.status, Status.FAILED)

    def test_high_risk_fails_closed_without_authenticated_provider(self):
        e = Engine(Policy({"local": {"write"}}),
                   evidence_verifier=lambda task, output: True)
        t = Task("2", "write", "local", "write", {"path": "a"}, Risk.HIGH)
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "ok"}})
        self.assertEqual(t.status, Status.NEEDS_APPROVAL)
        self.assertEqual(t.attempts, 0)

    def test_string_high_risk_cannot_bypass_approval(self):
        e = self.setup_engine()
        t = Task("2a", "write", "local", "write", {}, "high")
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "ok"}})
        self.assertEqual(t.status, Status.NEEDS_APPROVAL)
        self.assertEqual(t.attempts, 0)

    def test_invalid_risk_fails_closed(self):
        e = self.setup_engine()
        t = Task("2b", "write", "local", "write", {}, "critical")
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "ok"}})
        self.assertEqual(t.status, Status.FAILED)
        self.assertEqual(t.attempts, 0)

    def test_authenticated_provider_can_approve_exact_task(self):
        verifier = lambda task, credential: (
            credential == "verified-owner-session" and task.payload == {"path": "a"}
        )
        e = Engine(
            Policy({"local": {"write"}}, approval_verifier=verifier),
            Limits(max_seconds=2),
            evidence_verifier=lambda task, output: output.get("evidence") == "proof",
        )
        t = Task("3", "write", "local", "write", {"path": "a"}, Risk.HIGH)
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "proof"}},
              {"3": "verified-owner-session"})
        self.assertEqual(t.status, Status.DONE)

    def test_wrong_or_stale_approval_denied(self):
        verifier = lambda task, credential: (
            credential == "verified-owner-session" and task.payload == {"path": "a"}
        )
        e = Engine(Policy({"local": {"write"}}, approval_verifier=verifier),
                   Limits(max_seconds=2), evidence_verifier=lambda task, output: True)
        t = Task("4", "write", "local", "write", {"path": "b"}, Risk.HIGH)
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "proof"}},
              {"4": "verified-owner-session"})
        self.assertEqual(t.status, Status.NEEDS_APPROVAL)

    def test_no_evidence_not_done(self):
        e = self.setup_engine()
        t = Task("5", "read", "local", "read", {})
        e.run([t], {"local": lambda task: {"outcome": "success"}})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)

    def test_unknown_outcome_reconcile(self):
        e = self.setup_engine()
        t = Task("6", "read", "local", "read", {})
        e.run([t], {"local": lambda task: {"outcome": "unknown"}})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)

    def test_exception_reconcile(self):
        e = self.setup_engine()
        t = Task("7", "read", "local", "read", {})
        def crash(_):
            raise TimeoutError()
        e.run([t], {"local": crash})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)

    def test_payload_cap(self):
        e = self.setup_engine()
        e.limits.max_payload_bytes = 5
        t = Task("8", "large", "local", "read", {"data": "123456"})
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "x"}})
        self.assertEqual(t.status, Status.FAILED)

    def test_non_json_payload_fails_closed(self):
        e = self.setup_engine()
        t = Task("8a", "bad payload", "local", "read", {"value": object()})
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "x"}})
        self.assertEqual(t.status, Status.FAILED)
        self.assertEqual(t.result, "invalid_payload")

    def test_nan_payload_fails_closed(self):
        e = self.setup_engine()
        t = Task("8b", "nan payload", "local", "read", {"value": math.nan})
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "x"}})
        self.assertEqual(t.status, Status.FAILED)

    def test_duplicate_task_ids_rejected(self):
        e = self.setup_engine()
        a = Task("dup", "first", "local", "read", {})
        b = Task("dup", "second", "local", "read", {})
        e.run([a, b], {"local": lambda task: {"outcome": "success", "evidence": "x"}})
        self.assertEqual(a.status, Status.DONE)
        self.assertEqual(b.status, Status.FAILED)
        self.assertEqual(b.result, "duplicate_task_id")

    def test_success_without_evidence_verifier_never_done(self):
        e = Engine(Policy({"local": {"read"}}))
        t = Task("9", "read", "local", "read", {})
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "adapter says ok"}})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)
        self.assertEqual(t.result, "evidence_verifier_unavailable")

    def test_evidence_verifier_rejection_reconciles(self):
        e = Engine(Policy({"local": {"read"}}),
                   evidence_verifier=lambda task, output: False)
        t = Task("10", "read", "local", "read", {})
        e.run([t], {"local": lambda task: {"outcome": "success", "evidence": "untrusted"}})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)

    def test_non_object_adapter_output_reconciles(self):
        e = self.setup_engine()
        t = Task("11", "read", "local", "read", {})
        e.run([t], {"local": lambda task: "success"})
        self.assertEqual(t.status, Status.NEEDS_RECONCILIATION)

    def test_step_budget(self):
        e = self.setup_engine()
        e.limits.max_steps = 1
        tasks = [Task(str(i), "r", "local", "read", {}) for i in range(3)]
        e.run(tasks, {"local": lambda task: {"outcome": "success", "evidence": "ok"}})
        self.assertEqual(sum(t.status == Status.DONE for t in tasks), 1)

    def test_ledger_integrity(self):
        ledger = Ledger()
        ledger.append({"ok": 1})
        ledger.append({"ok": 2})
        self.assertTrue(ledger.verify())
        ledger.entries[0]["event"]["ok"] = 9
        self.assertFalse(ledger.verify())

    def test_ledger_rejects_nan(self):
        ledger = Ledger()
        with self.assertRaises(ValueError):
            ledger.append({"not_finite": math.nan})


class HandoffTests(unittest.TestCase):
    def sample(self):
        return from_atc_candidate(task_id="ATC-1", title="Review opportunity",
                                  tool="local", action="review",
                                  payload={"source": "user-approved"}, risk="low")

    def test_round_trip(self):
        env = self.sample()
        task = to_task(env)
        self.assertEqual(task.task_id, "ATC-1")
        self.assertEqual(task.payload, {"source": "user-approved"})

    def test_tamper_detected(self):
        env = self.sample()
        env["payload"]["source"] = "changed"
        with self.assertRaises(ValueError):
            validate(env)

    def test_unknown_schema_rejected(self):
        env = self.sample()
        env["schema_version"] = "v99"
        with self.assertRaises(ValueError):
            validate(env)

    def test_auto_execute_state_rejected(self):
        env = self.sample()
        env["state"] = "AUTHORIZED"
        with self.assertRaises(ValueError):
            validate(env)

    def test_atc_provenance_field_accepted(self):
        from atc_handoff import seal, validate, to_task
        body = {
            "schema_version": "advait.task.v1", "task_id": "ATC-2",
            "title": "Reviewed candidate", "tool": "local", "action": "review",
            "payload": {"x": 1}, "risk": "low",
            "state": "REVIEWED_NOT_AUTHORIZED", "source_atc_record": "ATC-REC-1"
        }
        envelope = seal(body)
        validate(envelope)
        self.assertEqual(to_task(envelope).task_id, "ATC-2")

    def test_unknown_fields_rejected(self):
        env = self.sample()
        env["extra"] = "not-allowed"
        with self.assertRaises(ValueError):
            validate(env)


if __name__ == "__main__":
    unittest.main(verbosity=2)
