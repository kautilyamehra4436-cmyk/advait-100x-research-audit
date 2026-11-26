import hashlib
import hmac
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from smv_core import MoneyLedger, PaymentEvent, verify_razorpay_webhook


class SMVTests(unittest.TestCase):
    def make_event(self, **changes):
        values = dict(
            provider="razorpay", event_id="evt_1", payment_id="pay_1",
            status="payment.captured", amount_minor=12500, currency="INR",
            reference="order_1", raw_body=b'{"id":"evt_1","event":"payment.captured"}',
        )
        values.update(changes)
        return PaymentEvent(**values)

    def test_every_sqlite_connection_is_closed_after_use(self):
        with tempfile.TemporaryDirectory() as tmp:
            original_connect = sqlite3.connect
            handles = []

            def tracked_connect(*args, **kwargs):
                conn = original_connect(*args, **kwargs)
                handles.append(conn)
                return conn

            def assert_all_closed():
                self.assertGreaterEqual(len(handles), 1)
                for conn in handles:
                    with self.assertRaises(sqlite3.ProgrammingError):
                        conn.execute("SELECT 1")

            with patch("smv_core.sqlite3.connect", side_effect=tracked_connect):
                ledger = MoneyLedger(Path(tmp) / "ledger.db")
                assert_all_closed()

                self.assertEqual(
                    ledger.record(self.make_event(), lambda _: True),
                    "CREDITED_TO_LEDGER",
                )
                assert_all_closed()

                self.assertEqual(ledger.income_total_minor(), 12500)
                assert_all_closed()

    def test_razorpay_hmac_valid_and_invalid(self):
        body = b'{"event":"payment.captured"}'
        secret = "test-webhook-secret"
        signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        self.assertTrue(verify_razorpay_webhook(body, signature, secret))
        self.assertFalse(verify_razorpay_webhook(body, "bad", secret))
        self.assertFalse(verify_razorpay_webhook(body, signature, ""))
        self.assertFalse(verify_razorpay_webhook(b"", signature, secret))

    def test_verified_capture_credits_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = self.make_event()
            verify = lambda e: e.provider == "razorpay" and e.raw_body.startswith(b"{")
            self.assertEqual(ledger.record(event, verify), "CREDITED_TO_LEDGER")
            self.assertEqual(ledger.record(event, verify), "DUPLICATE")
            self.assertEqual(ledger.income_total_minor(), 12500)

    def test_same_event_id_with_different_payload_is_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            verify = lambda _: True
            self.assertEqual(ledger.record(self.make_event(), verify), "CREDITED_TO_LEDGER")
            changed = self.make_event(amount_minor=99999, raw_body=b'{"changed":true}')
            self.assertEqual(ledger.record(changed, verify), "DUPLICATE_CONFLICT")
            self.assertEqual(ledger.income_total_minor(), 12500)

    def test_unverified_event_does_not_poison_valid_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = self.make_event()
            self.assertEqual(ledger.record(event, lambda _: False), "REJECTED_UNVERIFIED")
            self.assertEqual(ledger.record(event, lambda _: True), "CREDITED_TO_LEDGER")

    def test_missing_verifier_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            with self.assertRaises(PermissionError):
                ledger.record(self.make_event(), None)

    def test_non_capture_event_never_credits(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            event = self.make_event(status="payment.pending")
            self.assertEqual(ledger.record(event, lambda _: True), "VERIFIED_NOT_INCOME")
            self.assertEqual(ledger.income_total_minor(), 0)

    def test_invalid_amount_and_currency_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            with self.assertRaises(ValueError):
                ledger.record(self.make_event(amount_minor=True), lambda _: True)
            with self.assertRaises(ValueError):
                ledger.record(self.make_event(currency="inr"), lambda _: True)

    def test_empty_raw_body_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            with self.assertRaises(ValueError):
                ledger.record(self.make_event(raw_body=b""), lambda _: True)

    def test_bank_settlement_requires_separate_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = MoneyLedger(Path(tmp) / "ledger.db")
            with self.assertRaises(NotImplementedError):
                ledger.bank_settled_revenue("UTR-EXAMPLE")


if __name__ == "__main__":
    unittest.main()
