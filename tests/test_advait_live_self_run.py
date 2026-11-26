import unittest

from advait_engine import Status, demo


class AdvaitLiveSelfRunTests(unittest.TestCase):
    def test_real_calculation_and_owner_gate(self):
        report = demo()
        self.assertEqual(report["mode"], "offline_self_run")
        self.assertEqual(report["calculation"]["actual_result"], 9)
        self.assertEqual(report["calculation"]["status"], Status.DONE.value)
        self.assertEqual(report["high_risk_action"]["status"], Status.NEEDS_APPROVAL.value)
        self.assertEqual(report["high_risk_action"]["adapter_attempts"], 0)
        self.assertTrue(report["ledger_integrity"])
        self.assertFalse(report["external_network_actions"])
        self.assertFalse(report["payment_actions"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
