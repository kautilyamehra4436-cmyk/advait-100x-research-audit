# Advait Full Project Atlas
**Snapshot date:** 2026-11-26  
**Purpose:** One authoritative map for the central Brain to understand all four accessible Advait repositories, their blueprints, code, tests, dependencies, status and unresolved work.

## Snapshot scope and truth boundary
Recursive Git trees were fetched from each repository's `main` branch; none reported truncation. This inventory contains **132 tree entries** (files plus directories). It is not a claim that every historical branch, hidden GitHub setting, external account or every source line has been audited. The detailed document/code review covered the key blueprints, integration pointers, policies, queue, gates, business, server, SCEE and tests.

## Canonical repositories
| Repository | Visibility | Main SHA inspected | Primary role |
|---|---|---|---|
| [advait-100x-research-audit](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit) | Public | `0b6c498c075136b9192123cab70f469629480843` | Canonical cross-project hub, bounded execution, B2B, research, server, SCEE, SMV and tests |
| [my-brain](https://github.com/kautilyamehra4436-cmyk/my-brain) | Public | `030a7f1b98751f24d6f5e13a15f28cb63d22b48c` | Central Brain / ATC planning, task queue, memory conventions and zero-cost policy |
| [advait_os](https://github.com/kautilyamehra4436-cmyk/advait_os) | Private | `eeb4ce2801360b2af09b44decdf8e260118eff48` | Filesystem/security Gate, fail-closed HIGH/CRITICAL actions |
| [advait_pure_sharp](https://github.com/kautilyamehra4436-cmyk/advait_pure_sharp) | Private | `ad78d8c7e84ffc7b77db7be65b05d9cc76089226` | Governance, Master Operating Algorithm, Command Centre, Living Fabric/AELI and PanchTatva C10 |

The owner prefix search returned these four repositories. The separately mentioned “PanchTatva C10” is a module in `advait_pure_sharp`, not a fifth repository under that exact name.

## Repository file inventories

### 1. advait-100x-research-audit — 61 entries
```text
.devcontainer/
.devcontainer/devcontainer.json
.github/
.github/workflows/
.github/workflows/engine-regression.yml
.github/workflows/tests.yml
ADVAIT_SELF_CRAFTING_EVOLUTION_ENGINE.md
ADVAIT_SOVEREIGN_SERVER_BLUEPRINT.md
B2B_DAILY_REPORT_2026-11-24.md
B2B_DAILY_REPORT_2026-11-25.md
B2B_DAILY_REPORT_2026-11-26.md
B2B_DISCOVERY_LOG.md
B2B_ENGINE_BLUEPRINT.md
B2B_PROTOTYPE_TEST_RESULTS.md
BENCHMARK_PLAN.md
CEO_CONTROL_BOARD_SETUP.md
CODESPACES_LIVE_SERVER.md
CONSOLIDATION_EXECUTION_REPORT_2026-11-26.md
ENGINE_STATUS.md
ENGINE_TEST_RESULTS.md
LIVE_TEST_RESULTS.txt
MASTER_AUDIT.md
OPEN_SOURCE_MAKER_CUSTOMER_INTELLIGENCE.md
PHONE_RUN.md
QUEUE_EVIDENCE_HARDENING_REPORT_2026-11-26.md
README.md
RELATIONSHIP_INTELLIGENCE.md
SCEE_PHONE_AND_CODESPACES.md
SMV_SETUP.md
SOURCE_AUDIT_ADDENDUM.md
UNIFIED_INTEGRATION_REGISTRY.md
UNIFIED_MASTER_BLUEPRINT.md
advait_engine.py
advait_self_crafting.py
advait_sovereign_server.py
atc_handoff.py
b2b_reconcile.py
b2b_sample_input.csv
ceo_control_board.py
open_source_intelligence.py
phone_runtime_check.py
relationship_intelligence.py
reports/
reports/ADVAIT_SERVER_TOOL_LIVE_SCAN_2026-11-26.md
reports/ADVait_LIVE_OPEN_SOURCE_SCAN_2026-11-26.md
scripts/
scripts/live_server_smoke.py
scripts/scee_live_smoke.py
smv_core.py
soak_test.py
test_advait_engine.py
test_b2b_reconcile.py
test_harness.py
test_smv.py
tests/
tests/test_advait_live_self_run.py
tests/test_advait_self_crafting.py
tests/test_advait_sovereign_server.py
tests/test_ceo_control_board.py
tests/test_open_source_intelligence.py
tests/test_relationship_intelligence.py
```

### 2. my-brain — 48 entries
```text
.github/
.github/workflows/
.github/workflows/atc-tests.yml
.gitignore
CHANGELOG.md
INTEGRATIONS.md
LICENSE
README.md
RUNTIME_QUICKSTART.md
SOUL.md
START_HERE.md
UNIFIED_ADVait_INTEGRATION.md
authorization.md
compliance.md
config.yml
core/
core/__init__.py
core/atc_handoff.py
core/atc_planner.py
core/task_queue.py
core/zero_cost_guard.py
dashboard.md
docs/
docs/ATC_FIR_v1.2.md
docs/ATC_INTEGRATION_MAP.md
docs/REPOSITORY_RECONCILIATION_2026-11-24.md
dreams.md
emergence.md
errors.md
free_limits.md
health.md
integrations/
integrations/registry.json
legacy.md
log.md
onboarding.md
revenue.md
rules.md
security.md
session.md
status.md
tasks.md
tests/
tests/__init__.py
tests/test_atc_handoff.py
tests/test_atc_planner.py
tests/test_runtime.py
troubleshoot.md
```

### 3. advait_os — 8 entries
```text
.github/
.github/workflows/
.github/workflows/gate-security.yml
.github/workflows/run-gate.yml
GATE_SECURITY_V02.md
README.md
UNIFIED_ADVait_INTEGRATION.md
advait_gate_v01.py
```

### 4. advait_pure_sharp — 15 entries
```text
.github/
.github/workflows/
.github/workflows/advait-panch-tatva-c10.yml
ADVAIT_COMMAND_CENTRE.md
ADVAIT_LIVING_FABRIC_ARCHITECTURE.md
ChatGPT_0.1.md
MASTER_OPERATING_ALGORITHM.md
README.md
SYNC_TEST.txt
UNIFIED_ADVait_INTEGRATION.md
advait_panch_tatva_c10.py
reports/
reports/ADVait_PanchTatva_C10_GITHUB_TEST_REPORT.md
tests/
tests/test_advait_panch_tatva_c10.py
```

## Blueprint and policy index

| Document | Repository | What it governs / contains |
|---|---|---|
| `UNIFIED_MASTER_BLUEPRINT.md` | 100X | Mission, component map, Opportunity-to-Proof-to-Profit lifecycle, My Brain, security, zero-cost, B2B, SMV, evolution, evidence, implementation sequence and conflicts |
| `UNIFIED_INTEGRATION_REGISTRY.md` | 100X | Repository baselines, module status, adapter states, dependencies and gaps |
| `MASTER_AUDIT.md`, `SOURCE_AUDIT_ADDENDUM.md` | 100X | Historical cross-repository audits and corrections |
| `CONSOLIDATION_EXECUTION_REPORT_2026-11-26.md` | 100X | Consolidation evidence/checkpoint |
| `B2B_ENGINE_BLUEPRINT.md` | 100X | Market scout, evidence ledger, opportunity scoring, CSV-first service, validation and owner-approved outreach |
| `OPEN_SOURCE_MAKER_CUSTOMER_INTELLIGENCE.md` | 100X | Understand open-source tools/makers and match capabilities to customer needs; offline-only today |
| `RELATIONSHIP_INTELLIGENCE.md` | 100X | Owner-aligned opportunity ranking; offline analysis only |
| `ADVAIT_SOVEREIGN_SERVER_BLUEPRINT.md` | 100X | Lightweight Python control plane, SQLite metadata, Caddy/Gatus/Litestream/ntfy candidates and staged deployment gates |
| `ADVAIT_SELF_CRAFTING_EVOLUTION_ENGINE.md` | 100X | SCEE experiments, metrics, license/security/rollback gates; deterministic assessor, not autonomous researcher |
| `CEO_CONTROL_BOARD_SETUP.md` | 100X | Read-only cross-repository status board |
| `SMV_SETUP.md` | 100X | Safe payment-event ledger, Razorpay HMAC helper, injected PNB verifier; no transfers/payouts |
| `ENGINE_STATUS.md`, `ENGINE_TEST_RESULTS.md`, `PHONE_RUN.md`, `LIVE_TEST_RESULTS.txt` | 100X | Execution-core status and test/device evidence; read with environment and date caveats |
| `SOUL.md`, `rules.md`, `authorization.md`, `security.md`, `compliance.md` | My Brain | Owner authority, legal/privacy rules, security and approval boundaries |
| `config.yml` | My Brain | Hard ₹0 spend, no paid services/APIs/hosting/subscriptions, stop at quota exhaustion |
| `START_HERE.md`, `RUNTIME_QUICKSTART.md`, `dashboard.md`, `health.md` | My Brain | Setup and intended local runtime/status guidance; not proof of phone deployment |
| `ATC_FIR_v1.2.md`, `ATC_INTEGRATION_MAP.md`, `REPOSITORY_RECONCILIATION_2026-11-24.md` | My Brain | Planner design, handoff mapping and earlier reconciliation |
| `INTEGRATIONS.md`, `integrations/registry.json`, `free_limits.md` | My Brain | Tool candidates, connection status and zero-cost quota policy |
| `GATE_SECURITY_V02.md` | Advait OS | Fail-closed filesystem gate; no production authenticated identity provider |
| `MASTER_OPERATING_ALGORITHM.md` | Pure Sharp | Learn-while-doing method, authority hierarchy, evidence, test loop, permission and modular evolution rules |
| `ADVAIT_COMMAND_CENTRE.md` | Pure Sharp | Capability directory, work register, project navigation and evidence status |
| `ADVAIT_LIVING_FABRIC_ARCHITECTURE.md` | Pure Sharp | Proposed multi-module routing/fabric; architecture proposal, not a running orchestrator |
| `ChatGPT_0.1.md` | Pure Sharp | Earlier governing instructions and protected-rule continuity |
| `advait_panch_tatva_c10.py` + report | Pure Sharp | 10 scenario policy simulations; not consciousness, general intelligence, device or earning proof |

## Actual implementation map

1. **Central Brain / planner:** `my-brain/core/atc_planner.py`; deterministic planning, not an LLM and not an executor.
2. **Task queue:** `my-brain/core/task_queue.py`; SQLite WAL queue, atomic claim/complete, injected verifier required for completion. No lease expiry/recovery has been demonstrated in the reviewed code.
3. **Handoff:** `my-brain/core/atc_handoff.py`; SHA-256 integrity digest, not authentication; currently LOW/HIGH only and outputs REVIEWED_NOT_AUTHORIZED.
4. **Cost policy:** `my-brain/core/zero_cost_guard.py` plus `config.yml`; helper exists, global enforcement at every adapter is not proven.
5. **Security gate:** `advait_os/advait_gate_v01.py`; fail-closed HIGH/CRITICAL absent injected authenticated exact-action verifier. No verifier is shipped/configured.
6. **Execution core:** `advait_engine.py`; allowlisted offline actions, budgets, evidence-verifier hook and ledger; no production external adapters or independent production verifier.
7. **B2B worker:** `b2b_reconcile.py`; CSV reconciliation baseline; PDF/OCR and robust XLSX workflow are not complete.
8. **Open-source intelligence:** `open_source_intelligence.py`; offline analysis of supplied repository/customer-need records; no continuous collector/crawler.
9. **Relationship intelligence:** `relationship_intelligence.py`; offline ranking; no live lead feed or outreach.
10. **SMV:** `smv_core.py`; synthetic payment-event ledger and signature/verifier hooks; no live payment collection, payout, withdrawal or PNB production adapter.
11. **Server:** `advait_sovereign_server.py`; local read-only HTTP control-plane foundation; no public production deployment or 24/7 service.
12. **SCEE:** `advait_self_crafting.py`; deterministic candidate scoring/comparison and fail-closed gates; no live code generation, isolated code execution or autonomous research agent.
13. **CEO board:** `ceo_control_board.py`; local read-only report generator; not a hosted live dashboard.
14. **PanchTatva C10:** 10 rule-based scenario simulations; no real device, cognitive or business performance benchmark.
15. **Living Fabric/AELI:** proposed architecture only; no deployed routing graph or worker scheduler.

## Non-negotiable common controls
- Owner is final authority. ₹0 spend is hard policy; no paid API, hosting, subscription, credit or auto-renewal.
- Money movement, withdrawals, bank transfers, contracts, credential disclosure, sensitive data sharing, external submissions, public outreach and production security changes remain blocked pending suitable explicit authorization and real authenticated controls.
- Never treat a plan, queue record, hash, local file, chat text, simulation or CI pass as owner authentication.
- Preserve source repositories; integrate by versioned contracts, not by flattening everything into one giant file.
- Unknown, unverified and hypothesized states remain explicit.
- No claims of 24/7 uptime, independent LLM reasoning, customer acquisition, paid delivery or revenue without evidence.

## Required next integration order
1. Pin and validate all four source SHAs; keep this atlas refreshed on repository changes.
2. Normalize shared Task, Opportunity, Evidence, Approval, Delivery and Financial Event contracts.
3. Define one authoritative queue/ledger ownership boundary; avoid competing queues and duplicate completion states.
4. Make one risk taxonomy (LOW/MEDIUM/HIGH/CRITICAL) and adapt the My Brain handoff contract without confusing integrity with identity.
5. Enforce hard-zero spend and permission checks at every adapter boundary; test bypass attempts.
6. Connect ATC draft → security/policy gate → bounded worker → independent evidence verifier → evidence ledger. Until then, keep handoff plan-only.
7. Add worker contracts for B2B, open-source intelligence, relationship intelligence, SCEE, server and SMV.
8. Add stale-running lease/recovery, idempotency, retry limits, cancellation and reconciliation.
9. Run full CI, adversarial tests and a controlled 60-minute soak; then actual Android/Termux measurement and only later 24-hour soak.
10. Production deployment remains a separate owner-reviewed gate; no live payments or outreach in this integration.

## Brain's review assignment
When an actual reasoning model/runtime is connected, it must read this file, `ADVait_BRAIN_CONTEXT.md`, `advait_project_atlas.json`, and the linked source blueprints. It must produce a versioned review containing:
- repository/commit coverage and omitted files;
- duplicate/conflicting rules and a precedence decision;
- module dependency DAG and proposed execution sequence;
- shared contracts and migration plan;
- security, privacy, license and zero-cost threats;
- measured vs estimated resource requirements;
- test matrix with pass/fail/blocked and reproducible evidence;
- the top 10 blockers ranked by impact and confidence;
- a reversible implementation plan with rollback;
- explicit questions that only the owner can decide.

Do not mark the assignment complete merely because this document exists. The review must cite file paths and line ranges, include the exact source SHAs, and distinguish direct source facts from hypotheses.
