import unittest
from datetime import datetime, timezone

from open_source_intelligence import (
    CustomerNeed, OpenSourceProject, assess_project, build_open_source_report,
    infer_purpose, maintenance_signal, match_project_to_customer,
)


class OpenSourceIntelligenceTests(unittest.TestCase):
    def test_infers_tool_purpose_from_readme_and_topics(self):
        p = OpenSourceProject("maker", "flowtool", description="Workflow automation engine")
        self.assertEqual(infer_purpose(p), "automation")

    def test_ambiguous_or_missing_purpose_stays_unknown(self):
        self.assertEqual(infer_purpose(OpenSourceProject("maker", "blank")), "unknown")

    def test_missing_license_is_not_permission(self):
        p = OpenSourceProject("maker", "tool", description="CRM", readme_excerpt="Customer management", repository_url="https://github.com/maker/tool")
        result = assess_project(p)
        self.assertEqual(result["license_status"], "NOT_CONFIRMED")
        self.assertIn("LICENSE_NOT_CONFIRMED", result["review_signals"])

    def test_maintenance_signal(self):
        now = datetime(2026, 11, 26, tzinfo=timezone.utc)
        self.assertEqual(maintenance_signal("2026-11-01T00:00:00Z", now), "RECENT_ACTIVITY")
        self.assertEqual(maintenance_signal("", now), "UNKNOWN")

    def test_match_is_not_claimed_as_approved_tool(self):
        p = OpenSourceProject(
            "maker", "flowtool", description="Workflow automation",
            readme_excerpt="Automates repetitive workflow tasks",
            license_spdx="Apache-2.0", repository_url="https://github.com/maker/flowtool",
        )
        n = CustomerNeed("N-1", "small business", "workflow automation for repetitive work", "lead-1", verified=True)
        result = match_project_to_customer(p, n)
        self.assertEqual(result["fit"], "POTENTIAL_MATCH_REQUIRES_TECHNICAL_VALIDATION")
        self.assertIn("Review project purpose", result["next_step"])

    def test_report_counts_tool_categories_and_maker_matches(self):
        p = OpenSourceProject("maker", "flowtool", description="Workflow automation", readme_excerpt="Automates tasks", repository_url="https://github.com/maker/flowtool")
        n = CustomerNeed("N-1", "small business", "workflow automation", "lead-1", verified=True)
        report = build_open_source_report([p], [n])
        self.assertEqual(report["projects_analyzed"], 1)
        self.assertEqual(report["purpose_counts"]["automation"], 1)
        self.assertEqual(len(report["maker_customer_matches"]), 1)
        self.assertEqual(report["mode"], "OFFLINE_ANALYSIS_ONLY")


if __name__ == "__main__":
    unittest.main()
