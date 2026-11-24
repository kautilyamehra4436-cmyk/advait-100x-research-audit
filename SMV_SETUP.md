# Advait Sovereign Money Vault (SMV) — dual-gateway foundation

## Scope in this change
- Shared SQLite income ledger with provider/event idempotency.
- Razorpay webhook HMAC-SHA256 verification helper.
- Provider-neutral verification callback for PNB IPG; no PNB signature format is assumed.
- Fail-closed handling: unverified events and non-captured payments never create income entries.
- No charge creation, refund, payout, withdrawal, or bank-transfer operation is implemented.

## GitHub Actions secret names
In repository Settings → Secrets and variables → Actions, add values only after obtaining the exact credentials from each provider's merchant dashboard/onboarding pack:

- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`
- `PNB_IPG_MERCHANT_ID`
- `PNB_IPG_UAT_CREDENTIALS` (only if PNB supplies an approved UAT credential bundle; otherwise use the exact field mapping in its integration kit)

These are names only. This repository change does not create or populate GitHub secrets. Never put secret values in source files, issues, chat, logs, or test fixtures.

## Required before live integration
1. Confirm Razorpay account's approved mode, webhook URL, enabled payment methods, and settlement bank account.
2. Obtain PNB IPG UAT integration kit and confirm its authentication/signature algorithm, request fields, callback/status-query protocol, and settlement eligibility. Do not guess these details.
3. Implement and test the PNB-specific verifier from the official kit.
4. Add a hosted HTTPS webhook receiver with replay protection, request-size limits, and safe logging.
5. Reconcile captured provider payments against a verified PNB bank statement/settlement report. A gateway capture is not proof that funds have reached the bank.
6. Obtain owner approval before any live collection setup, refund, payout, transfer, or bank-account change.

## Test
Run:
```bash
python -m unittest -v test_smv.py
```

All tests use synthetic data and do not contact either gateway or move real money.
