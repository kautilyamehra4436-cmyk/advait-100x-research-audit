# Advait 100X Research Audit

Research checkpoint and offline mock harness plus the first bounded execution engine.

**Research status:** partial; no 100X performance or global novelty claim is proven.
**Engine status:** v0.1 offline reference core; no live web/bounty/payment integrations.
**B2B discovery status:** initial market scan recorded; prototype v0.1 tested locally (9/9 unit tests); no customer outreach, pilot, or revenue yet.

Run:
```
python test_harness.py
python -m unittest -v test_advait_engine.py
python -m unittest -v test_b2b_reconcile.py
python b2b_reconcile.py b2b_sample_input.csv --out-prefix sample_report
python advait_engine.py
```

The reference engine has task state, allowlist, exact-payload approval binding for high-risk actions, step/call/time/payload limits, adapter interface, evidence-gated completion, reconciliation for unknown outcomes/exceptions, and a hash-linked event ledger.

B2B documents:
- `B2B_ENGINE_BLUEPRINT.md` — modules, boundaries, first product hypothesis, experiment and acceptance criteria.
- `B2B_DISCOVERY_LOG.md` — evidence snapshot, candidates, current status, next research tasks.
- `B2B_DAILY_REPORT_2026-11-24.md` — latest dated report with new demand signals, verified local tests, CI verification limits, and next action.

Phone guidance: `PHONE_RUN.md`. Build checkpoint: `ENGINE_STATUS.md`. Benchmark proposal: `BENCHMARK_PLAN.md`. Research findings/limitations: `MASTER_AUDIT.md` and `SOURCE_AUDIT_ADDENDUM.md`.

All tests are offline and use mock adapters. No account credentials, network actions, bounty submissions, money movement, or irreversible actions are performed.
