"""Advait SMV: fail-closed payment event ledger foundation.

This module does not initiate charges, refunds, payouts, or bank transfers.
A provider-specific adapter must verify each event before it is recorded.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
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
    """Verify Razorpay webhook HMAC-SHA256 against the exact raw request body."""
    if not raw_body or not signature or not secret:
        return False
    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def load_config() -> dict[str, str]:
    """Read secrets from environment; never print or persist their values."""
    names = (
        "RAZORPAY_TEST_KEY_ID",
        "RAZORPAY_TEST_KEY_SECRET",
        "RAZORPAY_TEST_WEBHOOK_SECRET",
        "PNB_IPG_UAT_MERCHANT_ID",
        "PNB_IPG_UAT_CREDENTIALS",
    )
    return {name: os.environ.get(name, "") for name in names}


class MoneyLedger:
    """SQLite idempotent ledger. Credits only provider-verified successful events."""

    def __init__(self, db_path: str | Path = "smv_ledger.sqlite3") -> None:
        self.db_path = str(db_path)
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
                    verified INTEGER NOT NULL CHECK (verified IN (0, 1)),
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

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def record(self, event: PaymentEvent, verifier: Callable[[PaymentEvent], bool]) -> str:
        if not event.provider or not event.event_id or not event.payment_id:
            raise ValueError("provider, event_id and payment_id are required")
        if event.amount_minor <= 0 or not event.currency:
            raise ValueError("positive amount_minor and currency are required")
        verified = bool(verifier(event))
        digest = hashlib.sha256(event.raw_body).hexdigest()
        with self._connect() as conn:
            try:
                conn.execute("""
                    INSERT INTO payment_events
                    (provider, event_id, payment_id, status, amount_minor, currency,
                     reference, raw_sha256, verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (event.provider, event.event_id, event.payment_id, event.status,
                      event.amount_minor, event.currency, event.reference, digest,
                      int(verified)))
            except sqlite3.IntegrityError:
                return "DUPLICATE"
            if not verified:
                return "REJECTED_UNVERIFIED"
            if event.status != "payment.captured":
                return "VERIFIED_NOT_INCOME"
            conn.execute("""
                INSERT INTO ledger_entries
                (provider, event_id, payment_id, amount_minor, currency, entry_type)
                VALUES (?, ?, ?, ?, ?, 'INCOME')
            """, (event.provider, event.event_id, event.payment_id,
                  event.amount_minor, event.currency))
            return "CREDITED_TO_LEDGER"

    def income_total_minor(self, currency: str = "INR") -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount_minor), 0) FROM ledger_entries WHERE currency = ?",
                (currency,),
            ).fetchone()
        return int(row[0])

    def bank_settled_revenue(self, _bank_statement_reference: str) -> None:
        """Deliberately unavailable until a separately verified bank statement adapter exists."""
        raise NotImplementedError(
            "Ledger credits are not bank settlement proof; reconcile against verified bank data."
        )
