# Engine test report
Date: 2026-11-23

## Local test run
- `test_advait_engine.py`: 10/10 PASS on local Python execution.
- `advait_engine.py` offline demo: 1 low-risk task completed with evidence; 1 high-risk task held for approval; ledger integrity reported valid.

Tests cover allowlist rejection, exact approval, changed payload invalidating approval, missing evidence, unknown outcome, adapter exception reconciliation, payload cap, step budget, and ledger edit detection.

## Boundaries
These are unit tests against a local reference implementation and mock adapters. They do not validate real integrations, robust owner authentication, safe sandboxing, encrypted persistence, background operation, real bounty execution, payments, or performance on the user's phone. GitHub Actions has been updated to run the previous 10-test harness, these 10 unit tests, and the demo; its latest result is pending verification.
