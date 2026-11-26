import unittest

from relationship_intelligence import (
    DEFAULT_OWNER_PROFILE, Opportunity, build_opportunity_report,
    classify_work, score_opportunity,
)


class RelationshipIntelligenceTests(unittest.TestCase):
    def test_classifies_known_work_and_keeps_unknown(self):
        self.assertEqual(classify_work("Python API automation"), "software_and_automation")
        self.assertEqual(classify_work("Something completely unusual"), "unknown")

    def test_requires_evidence_before_priority(self):
        item = Opportunity("Spreadsheet cleanup", "data entry", "public listing")
        result = score_opportunity(item, evidence_verifier=lambda _: True)
        self.assertEqual(result["decision"], "NEEDS_EVIDENCE")

    def test_owner_fit_affects_priority_and_unknown_is_reported(self):
        good = Opportunity(
            "Python API automation", "integrate an API", "verified brief",
            verified_need=5, usefulness=5, feasibility=4,
            relationship_value=4, owner_fit=5, evidence="client brief reference",
        )
        unknown = Opportunity(
            "Unusual specialist task", "novel workflow", "public listing",
            verified_need=3, usefulness=3, feasibility=2,
            relationship_value=3, owner_fit=2, evidence="listing reference",
        )
        report = build_opportunity_report([good, unknown], DEFAULT_OWNER_PROFILE, evidence_verifier=lambda _: True)
        self.assertEqual(report["total_opportunities"], 2)
        self.assertEqual(report["unknown_work_count"], 1)
        self.assertIn("software_and_automation", report["category_counts"])
        self.assertEqual(report["mode"], "OFFLINE_ANALYSIS_ONLY")

    def test_rejects_invalid_ratings_and_bad_weights(self):
        item = Opportunity("Task", "description", "source", verified_need=6, evidence="x")
        with self.assertRaises(ValueError):
            score_opportunity(item)
        profile = dict(DEFAULT_OWNER_PROFILE)
        profile["scoring_weights"] = dict(DEFAULT_OWNER_PROFILE["scoring_weights"])
        profile["scoring_weights"]["owner_fit"] = 0.9
        with self.assertRaises(ValueError):
            score_opportunity(Opportunity("Task", "description", "source", verified_need=1, evidence="x"), profile)

    def test_evidence_string_alone_is_not_accepted(self):\n        item = Opportunity(\n            \"Python API automation\", \"integrate an API\", \"public source\",\n            verified_need=5, usefulness=5, feasibility=4,\n            relationship_value=4, owner_fit=5, evidence=\"unverified claim\",\n        )\n        result = score_opportunity(item)\n        self.assertEqual(result[\"decision\"], \"NEEDS_EVIDENCE\")\n        self.assertIn(\"verifier is not configured\", result[\"reason\"])\n\n    def test_verifier_exception_fails_closed(self):\n        item = Opportunity(\n            \"Python API automation\", \"integrate an API\", \"public source\",\n            verified_need=5, usefulness=5, feasibility=4,\n            relationship_value=4, owner_fit=5, evidence=\"source reference\",\n        )\n        def broken_verifier(_):\n            raise RuntimeError(\"verifier unavailable\")\n        result = score_opportunity(item, evidence_verifier=broken_verifier)\n        self.assertEqual(result[\"decision\"], \"NEEDS_EVIDENCE\")\n\n    def test_avoid_list_is_fail_closed(self):
        item = Opportunity("Task", "description", "source", category="spam")
        result = score_opportunity(item)
        self.assertEqual(result["decision"], "REJECTED_BY_POLICY")


if __name__ == "__main__":
    unittest.main()
