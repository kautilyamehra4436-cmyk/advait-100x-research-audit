# Advait — Current Four-Repository Snapshot

**Snapshot date:** 2026-11-27  
**Source:** GitHub recursive trees for the four repositories' `main` branches.  
**Coverage:** 207 files, 227 tree entries, no truncated trees. This is a complete path inventory at the recorded commits, not a claim that every source line, external setting, historical branch or runtime behavior has been audited.

## Main-branch source baselines inspected

| Repository | Main commit SHA inspected | Files | Tree entries | Role |
|---|---|---:|---:|---|
| [advait-100x-research-audit](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit) | `67a1595bddab2b538d3d562e032d3a0de291878b` | 62 | 68 | Canonical blueprint, research, B2B, execution reference and SMV |
| [my-brain](https://github.com/kautilyamehra4436-cmyk/my-brain) | `f27ca720f1c1be0fa6e2ea5e5e2916f48cf338b3` | 128 | 136 | Central Brain, ATC, task queue, worker and governed local runtime |
| [advait_os](https://github.com/kautilyamehra4436-cmyk/advait_os) | `07f24f281fb89b189384112ed35530e3108b9d85` | 6 | 8 | Local filesystem/security gate |
| [advait_pure_sharp](https://github.com/kautilyamehra4436-cmyk/advait_pure_sharp) | `55098ab2188f324260ca233966fc8f4c6334e478` | 11 | 15 | Governance, Master Operating Algorithm, Command Centre and architecture proposals |

**Snapshot commit note:** the 100X SHA above is the source commit inspected before this snapshot refresh is committed; merging this document update advances the 100X main SHA. The other three SHAs are their inspected main commits at capture time.

## Verified integration state at this checkpoint

- **My Brain / ATC:** ATC v1.2 remains a deterministic planner, not an LLM. The managed ATC bridge routes an explicitly selected local allowlisted operation through `GovernedSelfBuildRuntimeV3` and `ManagedTaskQueueV3`. Completion/failure is fenced by active lease owner and expiry. PR #35 runtime integration CI [45906541842](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45906541842) passed. PR #36 status/docs synchronization CI [45907097099](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45907097099) passed. This is bounded local execution, not external business execution.
- **SQLite resource lifecycle:** My Brain PRs #33/#34 fixed legacy TaskQueue and ProviderCallLedger connection closure. 100X PR #20 fixed SMV connection closure; PR #21 fixed the phone runtime diagnostic's SQLite handles and added a close regression test. 100X CI [45906684654](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit/actions/runs/45906684654) passed.
- **B2B reconciliation:** CSV-only deterministic reconciliation code and tests exist. Labelled real-world accuracy, XLSX/PDF/OCR support, customer pilot, outreach and revenue remain unverified/not enabled.
- **SMV:** Offline payment-event ledger foundation only. No live webhook receiver, PNB verifier, payout/withdrawal/transfer, bank settlement adapter or production payment collection is enabled.
- **Advait OS Gate:** Separate offline filesystem/security gate. Its README and integration pointer now describe scope; no production authenticated owner identity provider and no proven runtime integration into My Brain.
- **Pure Sharp governance:** README, integration pointer and Command Centre now reflect the current cross-project state. Living Fabric/AELI remains an architecture proposal; PanchTatva C10 is a scenario harness, not proof of intelligence or autonomy.
- **Operations:** No verified Android/Termux deployment, persistent scheduler, 24-hour runtime, live customer delivery, realized revenue or ₹10,000/day earnings.

## Canonical ownership and integration sequence

1. `advait_pure_sharp` owns governance, authority hierarchy, operating algorithm and Command Centre.
2. `my-brain` owns ATC planning, zero-cost policy implementation, queue, worker and governed local runtime.
3. `advait_os` owns the local filesystem/security gate; integrate only through a reviewed versioned contract.
4. `advait-100x-research-audit` owns the cross-project blueprint/evidence hub and specialist B2B, research, execution-reference and SMV modules.
5. Do not copy specialist implementations into competing repositories. Use versioned contracts, tests, owner/risk gates and evidence.

## Known integration gaps

- No LLM reasoning/provider call has been verified in the Advait runtime; OpenRouter `:free` is policy-only until a real manual run is evidenced.
- B2B CSV reconciliation and SMV are not yet exposed as governed My Brain adapters.
- Advait OS Gate is not yet wired into the worker's path/data operations.
- Global zero-cost enforcement across every future adapter is not proven.
- Independent production evidence verification and authenticated owner identity are not deployed.
- Lease heartbeat/renewal and multi-process stress testing remain pending; stale-owner fencing alone is not a complete concurrency/soak proof.
- No scheduler, background host, Android endurance run or 24-hour operation is verified.
- No real customer outreach, contract, payment movement or revenue is enabled.

## Full current file inventory

### 1. advait-100x-research-audit — 62 files / 68 tree entries

```text
.devcontainer/devcontainer.json
.github/workflows/engine-regression.yml
.github/workflows/tests.yml
ADVAIT_SELF_CRAFTING_EVOLUTION_ENGINE.md
ADVAIT_SOVEREIGN_SERVER_BLUEPRINT.md
ADVait_BRAIN_CONTEXT.md
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
CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md
ENGINE_STATUS.md
ENGINE_TEST_RESULTS.md
FULL_PROJECT_ATLAS.md
LIVE_TEST_RESULTS.txt
MASTER_AUDIT.md
OPEN_SOURCE_MAKER_CUSTOMER_INTELLIGENCE.md
PHONE_RUN.md
QUEUE_EVIDENCE_HARDENING_REPORT_2026-11-26.md
README.md
RELATIONSHIP_INTELLIGENCE.md
SCEE_PHONE_AND_CODESPACES.md
SELF_EVOLUTION_50_GAP_REGISTER.md
SMV_SETUP.md
SOURCE_AUDIT_ADDENDUM.md
UNIFIED_INTEGRATION_REGISTRY.md
UNIFIED_MASTER_BLUEPRINT.md
advait_engine.py
advait_project_atlas.json
advait_self_crafting.py
advait_sovereign_server.py
atc_handoff.py
b2b_reconcile.py
b2b_sample_input.csv
ceo_control_board.py
open_source_intelligence.py
phone_runtime_check.py
relationship_intelligence.py
reports/ADVAIT_SERVER_TOOL_LIVE_SCAN_2026-11-26.md
reports/ADVait_LIVE_OPEN_SOURCE_SCAN_2026-11-26.md
scripts/live_server_smoke.py
scripts/scee_live_smoke.py
scripts/validate_project_atlas.py
smv_core.py
soak_test.py
test_advait_engine.py
test_b2b_reconcile.py
test_harness.py
test_smv.py
tests/test_advait_live_self_run.py
tests/test_advait_self_crafting.py
tests/test_advait_sovereign_server.py
tests/test_ceo_control_board.py
tests/test_open_source_intelligence.py
tests/test_phone_runtime_check_connection_lifecycle.py
tests/test_relationship_intelligence.py
```

### 2. my-brain — 128 files / 136 tree entries

```text
.github/workflows/advait-ai-developer-ci.yml
.github/workflows/advait-ai-developer-v1.yml
.github/workflows/advait-ai-developer-v2.yml
.github/workflows/advait-core-integration-check-v1.yml
.github/workflows/advait-foundation-resource-governance-v1.yml
.github/workflows/advait-governed-self-build-v3.yml
.github/workflows/advait-one-click-start-check-v1.yml
.github/workflows/advait-one-click-start-check-v2.yml
.github/workflows/advait-one-click-start-check-v3.yml
.github/workflows/advait-one-click-start-check-v4.yml
.github/workflows/advait-open-source-discovery-v1.yml
.github/workflows/advait-openrouter-smoke-v1.yml
.github/workflows/advait-repository-vetting-v1.yml
.github/workflows/advait-self-build-worker-v1.yml
.github/workflows/advait-self-build-worker-v2.yml
.github/workflows/atc-tests.yml
.github/workflows/legacy-task-queue-regression.yml
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
config/provider_policy_v1.json
core/__init__.py
core/atc_handoff.py
core/atc_planner.py
core/atc_worker_bridge_managed_v1.py
core/atc_worker_bridge_managed_v2.py
core/atc_worker_bridge_managed_v3.py
core/atc_worker_bridge_v1.py
core/engineering_lessons_v1.py
core/governed_ai_developer_v1.py
core/governed_ai_developer_v2.py
core/governed_self_build_factory_v1.py
core/governed_self_build_runtime_v3.py
core/managed_atc_queue_adapter_v1.py
core/managed_provider_call_ledger_v2.py
core/managed_self_build_runtime_v1.py
core/managed_self_build_runtime_v2.py
core/managed_self_build_runtime_v3.py
core/managed_sqlite_v1.py
core/managed_task_queue_v1.py
core/managed_task_queue_v2.py
core/managed_task_queue_v3.py
core/opensource_discovery_v1.py
core/provider_router_v1.py
core/repository_vetting_v1.py
core/self_build_factory_v1.py
core/self_build_runtime_v1.py
core/task_queue.py
core/worker.py
core/zero_cost_guard.py
dashboard.md
docs/ATC_FIR_v1.2.md
docs/ATC_INTEGRATION_MAP.md
docs/DURABLE_TASK_LEASE_RECOVERY_V1.md
docs/FOUNDATION_RESOURCE_GOVERNANCE_V1.md
docs/FOUNDATION_RUNTIME_MIGRATION_V2.md
docs/GOVERNED_AI_DEVELOPER_V1.md
docs/GOVERNED_SELF_BUILD_V3.md
docs/MANAGED_SQLITE_RUNTIME_V1.md
docs/ONE_CLICK_START_GUIDE_HI.md
docs/ONE_CLICK_START_GUIDE_V2.md
docs/ONE_CLICK_START_GUIDE_V3_HI.md
docs/ONE_CLICK_START_GUIDE_V4_HI.md
docs/OPEN_SOURCE_DISCOVERY_V1.md
docs/PROVIDER_ROUTER_AUDIT_V1.md
docs/REPOSITORY_RECONCILIATION_2026-11-24.md
docs/REPOSITORY_VETTING_V1.md
docs/ROOT_BLOCKER_AND_BRIDGE_V1.md
docs/SELF_BUILD_FACTORY_V1.md
docs/SELF_BUILD_RUNTIME_V1.md
docs/SELF_BUILD_WORKER_V2.md
dreams.md
emergence.md
errors.md
free_limits.md
health.md
integrations/registry.json
legacy.md
log.md
onboarding.md
revenue.md
rules.md
scripts/advait_ai_developer_v1.py
scripts/advait_ai_developer_v2.py
scripts/advait_atc_worker_bridge_v1.py
scripts/advait_discover_open_source_v1.py
scripts/advait_governed_self_build_v3.py
scripts/advait_self_build_worker_v1.py
scripts/advait_self_build_worker_v2.py
scripts/advait_vet_repository_v1.py
scripts/openrouter_smoke_v1.py
scripts/openrouter_smoke_v3.py
scripts/openrouter_smoke_v4.py
security.md
session.md
status.md
tasks.md
tests/__init__.py
tests/test_atc_handoff.py
tests/test_atc_planner.py
tests/test_atc_worker_bridge_v1.py
tests/test_foundation_resource_governance_v1.py
tests/test_foundation_runtime_migration_v2.py
tests/test_governed_ai_developer_v1.py
tests/test_governed_ai_developer_v2.py
tests/test_governed_self_build_v3.py
tests/test_legacy_task_queue_connection_lifecycle.py
tests/test_managed_runtime_v1.py
tests/test_managed_self_build_runtime_v3.py
tests/test_managed_task_queue_v3.py
tests/test_opensource_discovery_v1.py
tests/test_provider_ledger_connection_lifecycle.py
tests/test_provider_router_v1.py
tests/test_repository_vetting_v1.py
tests/test_runtime.py
tests/test_self_build_factory_v1.py
tests/test_self_build_runtime_v1.py
tests/test_worker.py
troubleshoot.md
```

### 3. advait_os — 6 files / 8 tree entries

```text
.github/workflows/gate-security.yml
.github/workflows/run-gate.yml
GATE_SECURITY_V02.md
README.md
UNIFIED_ADVait_INTEGRATION.md
advait_gate_v01.py
```

### 4. advait_pure_sharp — 11 files / 15 tree entries

```text
.github/workflows/advait-panch-tatva-c10.yml
ADVAIT_COMMAND_CENTRE.md
ADVAIT_LIVING_FABRIC_ARCHITECTURE.md
ChatGPT_0.1.md
MASTER_OPERATING_ALGORITHM.md
README.md
SYNC_TEST.txt
UNIFIED_ADVait_INTEGRATION.md
advait_panch_tatva_c10.py
reports/ADVait_PanchTatva_C10_GITHUB_TEST_REPORT.md
tests/test_advait_panch_tatva_c10.py
```

## Change boundary

Historical reports remain historical evidence. This snapshot supersedes their old repository SHAs and inventory counts only; it does not silently change governance rules, authorize external actions, or claim runtime capabilities that have not been tested.
