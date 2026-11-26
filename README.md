# Advait 100X Research Audit

Research checkpoint and offline mock harness plus a bounded execution engine.

**Research status:** partial; no 100X performance or global novelty claim is proven.
**Engine status:** hardened offline reference core; no live web/bounty/payment integrations.
**B2B discovery status:** initial market scan recorded; no customer outreach, pilot, or revenue yet.

Run:
```sh
python test_harness.py
python -m unittest -v test_advait_engine.py
python -m unittest -v test_b2b_reconcile.py
python b2b_reconcile.py b2b_sample_input.csv --out-prefix sample_report
python advait_engine.py
python phone_runtime_check.py
python soak_test.py --hours 24 --interval-seconds 60 --db advait_soak.db
```

The reference engine includes task state, allowlist, exact-task owner-verifier hook for high-risk actions, step/call/time/payload limits, adapter interface, independent evidence-verifier hook, reconciliation for unknown or unverifiable outcomes, a tamper-evident hash-linked in-memory ledger, and an optional phone-local SQLite ledger with atomic commits.

**Fail-closed behavior:** without an injected authenticated owner verifier, HIGH-risk tasks cannot execute. Without an independent evidence verifier, an adapter's claim of success cannot move a task to DONE; it remains NEEDS_RECONCILIATION. The repository ships neither verifier nor live adapters. SQLite persistence is optional and unencrypted; do not store credentials, tokens, or sensitive financial/legal source records in it.

**Phone validation:** `phone_runtime_check.py` runs offline capability checks. `soak_test.py` runs a low-load SQLite-ledger stability test and records each tick. A short CI smoke run is not a 24-hour or Android test; the 24-hour command must be run on the target phone and the result inspected.

B2B documents:
- `B2B_ENGINE_BLUEPRINT.md` — modules, boundaries, product hypothesis, experiment and acceptance criteria.
- `B2B_DISCOVERY_LOG.md` — evidence snapshot, candidates, current status, next research tasks.
- `B2B_DAILY_REPORT_2026-11-26.md` — latest dated report and next action.
- `B2B_DAILY_REPORT_2026-11-25.md` — previous report.

Phone guidance: `PHONE_RUN.md`. Build checkpoint: `ENGINE_STATUS.md`. Benchmark proposal: `BENCHMARK_PLAN.md`. Research findings/limitations: `MASTER_AUDIT.md` and `SOURCE_AUDIT_ADDENDUM.md`.

All tests are offline and use mock adapters. No account credentials, network actions, bounty submissions, money movement, or irreversible actions are performed.


## Unified project control plane

- [Unified Advait Sovereign AI CEO Master Blueprint](UNIFIED_MASTER_BLUEPRINT.md)
- [Cross-repository Integration Registry](UNIFIED_INTEGRATION_REGISTRY.md)

This repository is the canonical cross-project blueprint and evidence hub. My Brain remains the central intelligence implementation; specialized modules remain in their source repositories. The blueprint explicitly separates verified capabilities from planned integrations and untested runtime claims.

- [Live consolidation execution report](CONSOLIDATION_EXECUTION_REPORT_2026-11-26.md)
- [Queue evidence-gate hardening report](QUEUE_EVIDENCE_HARDENING_REPORT_2026-11-26.md)
- [Advait CEO Control Board setup and usage](CEO_CONTROL_BOARD_SETUP.md)
- [CEO Control Board implementation](ceo_control_board.py)

- [Owner-aligned Relationship Intelligence](RELATIONSHIP_INTELLIGENCE.md) — owner-fit scoring, work-mix and unknown-work reporting, defense boundaries.

- [Open-Source Maker & Customer Intelligence](OPEN_SOURCE_MAKER_CUSTOMER_INTELLIGENCE.md) — tool purpose, maker/customer matching, license/security review gates.
- [Advait Sovereign Server Blueprint](ADVAIT_SOVEREIGN_SERVER_BLUEPRINT.md) — local-first server architecture and safety gates.
- [Live server-tool scan](reports/ADVAIT_SERVER_TOOL_LIVE_SCAN_2026-11-26.md) — public GitHub metadata and README review.
