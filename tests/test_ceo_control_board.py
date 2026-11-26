import tempfile
import unittest
from pathlib import Path

from ceo_control_board import build_board, render_markdown


class CEOControlBoardTests(unittest.TestCase):
    def test_missing_phone_and_soak_evidence_never_claims_live(self):
        with tempfile.TemporaryDirectory() as temp:
            board = build_board([Path(temp)])
        self.assertEqual(board["live_status"], "NOT_CLAIMED")
        self.assertEqual(board["phone_deployment"], "PENDING")
        self.assertEqual(board["24_hour_soak"], "NOT_RUN_OR_NOT_EVIDENCED")

    def test_foundation_artifact_does_not_mean_live(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "smv_core.py").write_text("# foundation")
            board = build_board([root])
        smv = next(row for row in board["workstreams"] if row["workstream"] == "Razorpay/SMV foundation")
        self.assertEqual(smv["status"], "FOUNDATION_PRESENT")
        self.assertEqual(board["live_status"], "NOT_CLAIMED")

    def test_markdown_has_clear_control_status(self):
        with tempfile.TemporaryDirectory() as temp:
            board = build_board([Path(temp)])
        output = render_markdown(board)
        self.assertIn("Production live: **NOT_CLAIMED**", output)
        self.assertIn("Phone deployment: **PENDING**", output)
        self.assertIn("24-hour soak: **NOT_RUN_OR_NOT_EVIDENCED**", output)


if __name__ == "__main__":
    unittest.main()
