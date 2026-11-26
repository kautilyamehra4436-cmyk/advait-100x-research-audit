# Advait Full Project Atlas
**Snapshot date:** 2026-11-27  
**Purpose:** One authoritative map for the central Brain to understand all four accessible Advait repositories, their blueprints, code, tests, dependencies, status and unresolved work.

## Snapshot scope and truth boundary
Recursive Git trees were fetched from each repository's `main` branch; none reported truncation. This inventory is superseded by [CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md](CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md), which records **207 files and 227 tree entries** across the four current main branches. It is not a claim that every historical branch, hidden GitHub setting, external account or every source line has been audited. The detailed document/code review covered the key blueprints, integration pointers, policies, queue, gates, business, server, SCEE and tests.

## Canonical repositories
| Repository | Visibility | Main SHA inspected | Primary role |
|---|---|---|---|
| [advait-100x-research-audit](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit) | Public | `67a1595bddab2b538d3d562e032d3a0de291878b` | Canonical cross-project hub, bounded execution, B2B, research, server, SCEE, SMV and tests |
| [my-brain](https://github.com/kautilyamehra4436-cmyk/my-brain) | Public | `f27ca720f1c1be0fa6e2ea5e5e2916f48cf338b3` | Central Brain / ATC planning, task queue, memory conventions and zero-cost policy |
| [advait_os](https://github.com/kautilyamehra4436-cmyk/advait_os) | Private | `07f24f281fb89b189384112ed35530e3108b9d85` | Filesystem/security Gate, fail-closed HIGH/CRITICAL actions |
| [advait_pure_sharp](https://github.com/kautilyamehra4436-cmyk/advait_pure_sharp) | Private | `55098ab2188f324260ca233966fc8f4c6334e478` | Governance, Master Operating Algorithm, Command Centre, Living Fabric/AELI and PanchTatva C10 |

The owner prefix search returned these four repositories. The separately mentioned “PanchTatva C10” is a module in `advait_pure_sharp`, not a fifth repository under that exact name.

## Repository file inventories

The detailed, current inventory is maintained in [CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md](CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md) (207 files / 227 tree entries at capture time). The earlier inline inventories below are retained in the prior snapshot's history and should not be used as current file counts.

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


## 2026-11-27 synchronization checkpoint

See [CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md](CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md) for current main SHAs, exact file inventory, verified integration state and remaining gaps. This replaces the 2026-11-26 repository baselines; it does not assert a line-by-line audit of every source file.


The 2026-11-27 snapshot's source baselines were refreshed after My Brain PR #36 and documentation updates in Advait OS and Pure Sharp. See the linked snapshot for exact capture SHAs and the self-update note.
