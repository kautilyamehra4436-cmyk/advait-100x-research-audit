# Advait Sovereign Money Vault (SMV) — Safe Foundation

## Implemented in this branch
- SQLite ledger for normalized provider events.
- Razorpay raw-body HMAC-SHA256 helper.
- Provider-specific verifier injection for Razorpay or PNB IPG; no undocumented PNB signature scheme is assumed.
- Only verified normalized payment.captured events create income ledger entries.
- Idempotency distinguishes exact duplicate events from conflicting payloads reusing the same provider event ID.
- Unverified events do not reserve an event ID and cannot poison a valid retry.
- No charge, refund, payout, withdrawal or bank transfer operation exists.

## Environment variable names (names only)
- RAZORPAY_TEST_KEY_ID
- RAZORPAY_TEST_KEY_SECRET
- RAZORPAY_TEST_WEBHOOK_SECRET
- PNB_IPG_UAT_MERCHANT_ID
- PNB_IPG_UAT_CREDENTIALS (only if supplied by the official PNB UAT kit)

Never store secret values in source files, chat, issues, logs or test fixtures. The code does not create GitHub secrets.

## Before any real integration
1. Confirm Razorpay account mode, official webhook configuration and settlement details.
2. Obtain the official PNB IPG UAT kit; implement only its documented authentication and callback/status protocol.
3. Build a hosted HTTPS webhook receiver with request-size limits, replay protection and safe logging.
4. Add provider payload normalization and exact raw-body verification.
5. Reconcile gateway events against an independently verified bank statement/settlement report.
6. Obtain explicit owner approval for live collection setup. Withdrawals, payouts and transfers remain blocked.
7. Review applicable legal, tax, privacy and merchant requirements.

A captured gateway payment is not proof of bank settlement. This ledger stores operational event metadata and hashes; it is not encrypted storage for bank statements, credentials or source financial records.

## Tests
python -m unittest -v test_smv.py

All tests use synthetic fixtures and do not contact providers or move real money.
