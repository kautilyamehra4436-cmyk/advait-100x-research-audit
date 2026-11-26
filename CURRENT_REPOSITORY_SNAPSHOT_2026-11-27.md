# Advait — Current Four-Repository Snapshot

**Snapshot date:** 2026-11-27  
**Source:** GitHub recursive trees for the four repositories' `main` branches.  
**Coverage:** 213 files, 235 tree entries, no truncated trees. Gitlinks are counted as tree entries separately from blob files. This is a complete path inventory at the recorded commits, not a line-by-line semantic audit of every source line, historical branch, external setting or runtime environment.

## Main-branch source baselines inspected

| Repository | Main commit SHA inspected | Files | Tree entries | Role |
|---|---|---:|---:|---|
| [advait-100x-research-audit](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit) | `e6b52df9f7e9a2e8690217ace813e2e29b65b244` | 62 | 68 | Canonical blueprint, research, B2B engine, execution reference and SMV |
| [my-brain](https://github.com/kautilyamehra4436-cmyk/my-brain) | `a47ab5d2e1778ca3f5c44edbbe16d179db30c181` | 134 | 144 | Central Brain, ATC, queue, worker, governed runtime and B2B adapter |
| [advait_os](https://github.com/kautilyamehra4436-cmyk/advait_os) | `07f24f281fb89b189384112ed35530e3108b9d85` | 6 | 8 | Local filesystem/security gate |
| [advait_pure_sharp](https://github.com/kautilyamehra4436-cmyk/advait_pure_sharp) | `9e5927935ae3f2520e606213473b61ff87596277` | 11 | 15 | Governance, Master Operating Algorithm, Command Centre and architecture proposals |

**Snapshot commit note:** the 100X SHA above is the source commit inspected before this snapshot refresh is committed; merging this document update advances the 100X main SHA.

## Pinned cross-repository source links

| Parent repository | Gitlink path | Pinned source commit |
|---|---|---|
| my-brain | `vendor/advait_b2b` | `e6b52df9f7e9a2e8690217ace813e2e29b65b244` |

My Brain pins the B2B implementation as a Git submodule; no source copy or runtime network fetch is used. CI checks out this exact revision.

## Verified integration state at this checkpoint

- **My Brain / ATC:** ATC v1.2 remains a deterministic planner, not an LLM. The managed ATC bridge routes explicitly selected local allowlisted operations through `GovernedSelfBuildRuntimeV3` and `ManagedTaskQueueV3`. Completion/failure is fenced by active lease owner and expiry. PR #35 runtime integration CI [45906541842](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45906541842) passed.
- **B2B CSV integration:** My Brain PR #37 pins the 100X reconciler as a submodule and adds a governed adapter. CI [45908960326](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45908960326) passed 131 unit tests, compilation and the end-to-end synthetic sample smoke. The sample processed 5 rows and generated 7 review flags; source rows were not stored in the operational task queue. No real customer data was processed.
- **Financial record storage:** B2B input/output artifacts are held in a separate file vault with restrictive OS permissions and symlink checks, not in operational SQLite. It is **not encrypted at rest**; explicit acknowledgement is required. Do not stage sensitive customer data on a shared/untrusted device until encryption/Android Keystore is implemented.
- **Owner flags:** local consent/confirmation flags are manual intent checks, not authenticated owner identity. No production identity provider is deployed.
- **SQLite resource lifecycle:** My Brain PRs #33/#34 fixed legacy TaskQueue and ProviderCallLedger connection closure. 100X PR #20 fixed SMV connection closure; PR #21 fixed phone diagnostic SQLite handles. 100X CI [45906684654](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit/actions/runs/45906684654) passed.
- **B2B limits:** CSV only; 1 MiB input, 10,000 rows, 100 columns and 4 MiB output. No XLSX/PDF/OCR, accounting/tax conclusion, customer outreach, invoice submission or payment movement.
- **SMV:** Offline payment-event ledger foundation only. No live webhook receiver, PNB verifier, payout/withdrawal/transfer, bank settlement adapter or production payment collection is enabled.
- **Advait OS Gate:** Separate offline filesystem/security gate. No production authenticated owner identity provider and no proven runtime integration into My Brain.
- **Pure Sharp governance:** Living Fabric/AELI remains an architecture proposal; PanchTatva C10 is a scenario harness, not proof of intelligence or autonomy.
- **Operations:** No verified Android/Termux deployment, persistent scheduler, 24-hour runtime, live customer delivery, realized revenue or ₹10,000/day earnings.

## Canonical ownership and integration sequence

1. `advait_pure_sharp` owns governance, authority hierarchy, operating algorithm and Command Centre.
2. `my-brain` owns ATC planning, zero-cost policy implementation, queue, worker and governed local runtime.
3. `advait_os` owns the local filesystem/security gate; integrate only through a reviewed versioned contract.
4. `advait-100x-research-audit` owns the cross-project blueprint/evidence hub and specialist B2B, research, execution-reference and SMV modules.
5. Do not copy specialist implementations into competing repositories. Use pinned versioned source, contracts, tests, owner/risk gates and evidence.

## Known integration gaps

- No LLM reasoning/provider call has been verified in the Advait runtime; OpenRouter `:free` is policy-only until a real manual run is evidenced.
- B2B is code-integrated and synthetic-tested, but the financial file vault is not encrypted at rest and no real customer data has been processed.
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

### 2. my-brain — 134 files / 144 tree entries

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
.github/workflows/b2b-adapter-integration-v1.yml
.github/workflows/legacy-task-queue-regression.yml
.gitignore
.gitmodules
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
core/b2b_reconciliation_adapter_v1.py
core/engineering_lessons_v1.py
core/financial_record_vault_v1.py
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
scripts/advait_b2b_integration_smoke_v1.py
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
tests/test_b2b_reconciliation_adapter_v1.py
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
