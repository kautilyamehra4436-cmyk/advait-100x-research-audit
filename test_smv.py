import hashlib
import hmac
import tempfile
import unittest
from pathlib import Path

from smv_core import MoneyLedger, PaymentEvent, verify_razorpay_webhook


class SMVTests(unittest.TestCase):
    def test_razorpay_hmac_valid_and_invalid(self):
        body = b'{"event":"payment.captured"}'
        secret = "test-webhook-secret"
        sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        self.assertTrue(verify_razorpay_webhook(body, sig, secret))
        self.assertFalse(verify_razorpay_webhook(body, "bad", secret))
        self.assertFalse(verify_razorpay_webhook(body, sig, ""))

    def test_verified_capture_credits_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = PaymentEvent("razorpay", "evt_1", "pay_1",
                                 "payment.captured", 12500, "INR", raw_body=b"{}")
            self.assertEqual(ledger.record(event, lambda _: True), "CREDITED_TO_LEDGER")
            self.assertEqual(ledger.record(event, lambda _: True), "DUPLICATE")
            self.assertEqual(ledger.income_total_minor(), 12500)

    def test_unverified_capture_never_credits(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = PaymentEvent("pnb_ipg", "txn_1", "txn_1",
                                 "payment.captured", 5000, "INR")
            self.assertEqual(ledger.record(event, lambda _: False), "REJECTED_UNVERIFIED")
            self.assertEqual(ledger.income_total_minor(), 0)

    def test_non_capture_event_does_not_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = PaymentEvent("pnb_ipg", "txn_2", "txn_2",
                                 "payment.pending", 5000, "INR")
            self.assertEqual(ledger.record(event, lambda _: True), "VERIFIED_NOT_INCOME")
            self.assertEqual(ledger.income_total_minor(), 0)

    def test_bank_settlement_requires_separate_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            with self.assertRaises(NotImplementedError):
                ledger.bank_settled_revenue("UTR-EXAMPLE")


if __name__ == "__main__":
    unittest.main()
