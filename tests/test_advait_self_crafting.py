import unittest

from advait_self_crafting import Candidate, SelfCraftingEngine, self_test


class SelfCraftingTests(unittest.TestCase):
    def setUp(self):
        self.engine = SelfCraftingEngine()

    def candidate(self, **overrides):
        values = dict(name="candidate", approach="new", latency_ms=10,
                      memory_mb=20, correctness_passed=True, measured=True,
                      license_id="MIT", attribution_recorded=True,
                      security_review_passed=True, rollback_available=True)
        values.update(overrides)
        return Candidate(**values)

    def test_valid_candidate_is_eligible(self):
        self.assertTrue(self.engine.assess(self.candidate()).eligible)

    def test_unknown_license_fails_closed(self):
        result = self.engine.assess(self.candidate(license_id="NOASSERTION"))
        self.assertFalse(result.eligible)
        self.assertIn("license_unknown_or_unapproved", result.reasons)

    def test_unmeasured_or_incorrect_candidate_blocked(self):
        self.assertFalse(self.engine.assess(self.candidate(measured=False)).eligible)
        self.assertFalse(self.engine.assess(self.candidate(correctness_passed=False)).eligible)

    def test_attribution_security_and_rollback_gates(self):
        result = self.engine.assess(self.candidate(
            attribution_recorded=False, security_review_passed=False,
            rollback_available=False))
        self.assertFalse(result.eligible)
        self.assertEqual(len(result.reasons), 3)

    def test_no_candidate_means_no_selection(self):
        result = self.engine.compare([self.candidate(license_id="NOASSERTION")])
        self.assertEqual(result["decision"], "NO_CANDIDATE_PASSED_GATES")
        self.assertIsNone(result["winner"])
        self.assertFalse(result["production_deployment_allowed"])

    def test_lower_resource_use_wins(self):
        result = self.engine.compare([
            self.candidate(name="slow", latency_ms=20, memory_mb=20),
            self.candidate(name="fast", latency_ms=5, memory_mb=10),
        ])
        self.assertEqual(result["winner"], "fast")
        self.assertTrue(result["owner_approval_required"])

    def test_cli_self_test(self):
        self.assertEqual(self_test()["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
