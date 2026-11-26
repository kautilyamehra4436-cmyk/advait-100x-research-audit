"""Advait SMV: fail-closed payment event ledger foundation.

No charge, refund, payout, withdrawal or bank-transfer operation is implemented.
Provider adapters must verify the exact raw event before calling MoneyLedger.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class PaymentEvent:
    provider: str
    event_id: str
    payment_id: str
    status: str
    amount_minor: int
    currency: str
    reference: str = ""
    raw_body: bytes = b""


def verify_razorpay_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    """Verify Razorpay HMAC-SHA256 over the exact raw request body."""
    if not isinstance(raw_body, bytes) or not raw_body:
        return False
    if not isinstance(signature, str) or not signature:
        return False
    if not isinstance(secret, str) or not secret:
        return False
    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def load_config() -> dict[str, str]:
    """Read secret values from environment; callers must never print or persist them."""
    names = (
        "RAZORPAY_TEST_KEY_ID",
        "RAZORPAY_TEST_KEY_SECRET",
        "RAZORPAY_TEST_WEBHOOK_SECRET",
        "PNB_IPG_UAT_MERCHANT_ID",
        "PNB_IPG_UAT_CREDENTIALS",
    )
    return {name: os.environ.get(name, "") for name in names}


class MoneyLedger:
    """SQLite event ledger; stores metadata and hashes, not credentials or raw bodies."""

    PROVIDERS = {"razorpay", "pnb_ipg"}
    STATUSES = {
        "payment.captured", "payment.authorized", "payment.pending",
        "payment.failed", "payment.refunded",
    }

    def __init__(self, db_path: str | Path = "smv_ledger.sqlite3") -> None:
        self.db_path = str(db_path)
        if self.db_path != ":memory:" and os.path.islink(self.db_path):
            raise ValueError("ledger database path must not be a symlink")
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS payment_events (
                    provider TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    payment_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    amount_minor INTEGER NOT NULL,
                    currency TEXT NOT NULL,
                    reference TEXT NOT NULL,
                    raw_sha256 TEXT NOT NULL,
                    verified INTEGER NOT NULL CHECK (verified = 1),
                    PRIMARY KEY (provider, event_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ledger_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    payment_id TEXT NOT NULL,
                    amount_minor INTEGER NOT NULL,
                    currency TEXT NOT NULL,
                    entry_type TEXT NOT NULL CHECK (entry_type = 'INCOME'),
                    UNIQUE (provider, event_id)
                )
            """)

    @contextmanager
    def _connect(self):
        """Commit/rollback and always close each SQLite connection.

        sqlite3.Connection's own context manager handles transactions only;
        it does not close the connection. Keep the lifecycle explicit here.
        """
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA busy_timeout = 5000")
            yield conn
            conn.commit()
        except BaseException:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass
            raise
        finally:
            conn.close()

    @staticmethod
    def _validate(event: PaymentEvent) -> None:
        if not isinstance(event, PaymentEvent):
            raise TypeError("event must be a PaymentEvent")
        if event.provider not in MoneyLedger.PROVIDERS:
            raise ValueError("unsupported provider")
        for name, value in (("event_id", event.event_id), ("payment_id", event.payment_id)):
            if not isinstance(value, str) or not value.strip() or len(value) > 200:
                raise ValueError(f"invalid {name}")
        if event.status not in MoneyLedger.STATUSES:
            raise ValueError("unsupported normalized payment status")
        if isinstance(event.amount_minor, bool) or not isinstance(event.amount_minor, int):
            raise ValueError("amount_minor must be an integer")
        if event.amount_minor <= 0 or event.amount_minor > 10**15:
            raise ValueError("amount_minor is outside the accepted range")
        if not isinstance(event.currency, str) or not re.fullmatch(r"[A-Z]{3}", event.currency):
            raise ValueError("currency must be a three-letter uppercase code")
        if not isinstance(event.raw_body, bytes) or not event.raw_body:
            raise ValueError("exact raw event body is required")
        if not isinstance(event.reference, str) or len(event.reference) > 200:
            raise ValueError("invalid reference")

    def record(self, event: PaymentEvent, verifier: Callable[[PaymentEvent], bool]) -> str:
        self._validate(event)
        if not callable(verifier):
            raise PermissionError("provider event verifier unavailable; fail-closed")
        try:
            verified = bool(verifier(event))
        except Exception:
            verified = False
        if not verified:
            # Do not reserve an event ID with an untrusted request; otherwise an
            # invalid request could poison the idempotency key before a valid retry.
            return "REJECTED_UNVERIFIED"

        digest = hashlib.sha256(event.raw_body).hexdigest()
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = conn.execute(
                "SELECT payment_id,status,amount_minor,currency,reference,raw_sha256 "
                "FROM payment_events WHERE provider=? AND event_id=?",
                (event.provider, event.event_id),
            ).fetchone()
            if existing:
                same = existing == (
                    event.payment_id, event.status, event.amount_minor,
                    event.currency, event.reference, digest,
                )
                conn.execute("ROLLBACK")
                return "DUPLICATE" if same else "DUPLICATE_CONFLICT"

            conn.execute("""
                INSERT INTO payment_events
                (provider,event_id,payment_id,status,amount_minor,currency,
                 reference,raw_sha256,verified)
                VALUES (?,?,?,?,?,?,?,?,1)
            """, (
                event.provider, event.event_id, event.payment_id, event.status,
                event.amount_minor, event.currency, event.reference, digest,
            ))
            if event.status != "payment.captured":
                conn.execute("COMMIT")
                return "VERIFIED_NOT_INCOME"

            conn.execute("""
                INSERT INTO ledger_entries
                (provider,event_id,payment_id,amount_minor,currency,entry_type)
                VALUES (?,?,?,?,?,'INCOME')
            """, (
                event.provider, event.event_id, event.payment_id,
                event.amount_minor, event.currency,
            ))
            conn.execute("COMMIT")
            return "CREDITED_TO_LEDGER"

    def income_total_minor(self, currency: str = "INR") -> int:
        if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
            raise ValueError("invalid currency")
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount_minor),0) FROM ledger_entries WHERE currency=?",
                (currency,),
            ).fetchone()
        return int(row[0])

    def bank_settled_revenue(self, _bank_statement_reference: str) -> None:
        """Unavailable until an independently verified bank-statement adapter exists."""
        raise NotImplementedError(
            "gateway event ledger is not bank settlement proof; reconcile verified bank data"
        )
