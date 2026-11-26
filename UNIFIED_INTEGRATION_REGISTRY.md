# ADVAIT Unified Integration Registry
Date: 2026-11-27
Canonical design: UNIFIED_MASTER_BLUEPRINT.md

## Repository baselines
| Repository | Main baseline SHA | Role |
|---|---|---|
| my-brain | 497b41780ad2634ca6498460e96fe3eb739c83d6 | Central Brain / ATC |
| advait_os | 07f24f281fb89b189384112ed35530e3108b9d85 | Security Gate |
| advait_pure_sharp | 55098ab2188f324260ca233966fc8f4c6334e478 | Governance / Living Fabric / PanchTatva |
| advait-100x-research-audit | 67a1595bddab2b538d3d562e032d3a0de291878b | Execution / B2B / Research / Master Hub |

## Module register
| Module | Source | State | Integration rule |
|---|---|---|---|
| SOUL / Governance | my-brain + pure_sharp | Docs | One owner-authority hierarchy; canonical conflicts recorded |
| ATC Planner v1.2 | my-brain/core | Merged, rule-based | Drafts only; no external execution |
| Task Queue | my-brain/core | ManagedTaskQueueV3 wired to governed runtime | Lease owner + expiry fence completion/failure; local allowlisted tasks only |
| Zero Cost Guard | my-brain/core | Helper exists; global wiring unverified | Fail closed at every cost-bearing boundary |
| ATC Handoff | my-brain/core | Managed V3 bridge to governed runtime | Explicit local allowlisted operation only; no external action |
| Advait OS Gate v0.2 | advait_os | Offline gate | HIGH/CRITICAL blocked without authenticated verifier |
| Bounded Execution Core v0.2 | 100X | Offline reference | No live adapters; independent verifier not deployed |
| B2B Reconciliation | 100X | CSV worker | CSV-only; benchmark expansion required |
| PanchTatva C10 | pure_sharp | Scenario harness | Simulated checks only |
| Living Fabric / AELI | pure_sharp | Architecture proposal | Not a deployed orchestrator |
| SMV | 100X PR #8, #20 | Merged offline foundation; SQLite closure regression passed | No live payment, webhook receiver, payout, bank settlement or PNB verifier |
| PNB adapter | Intended | Not implemented/verified | Official supported route; owner configured |
| PDF/OCR/XLSX worker | 100X blueprint | Not implemented | Synthetic benchmark first |
| Android runtime | My Brain integration register | Candidate | User installation and device test required |
| n8n/Huginn/Activepieces | My Brain integration register | Candidates | Compare; do not deploy all |
| Daily 06:00 report | Project requirement | Not scheduled/verified | Requires real scheduler and delivery channel |

## Policy conflict decisions
- Controlling spend policy: my-brain/config.yml, hard ₹0, paid services disabled, stop on free-quota exhaustion. Positive caps in revenue.md conflict and are non-operative.
- Telegram/Face ID tiers in authorization.md are not active controls until an authenticated provider is implemented and tested.
- Security checkmarks and legal assertions are unverified until independently checked.
- No permission to use private customer data, credentials, outreach, contracts, money movement or destructive operations is implied by this registry.

## Consolidation rules
1. Preserve source repositories and their history.
2. This repository is the canonical cross-project blueprint and evidence hub.
3. my-brain remains the central intelligence implementation.
4. Keep specialized code in its source repository; integrate through versioned contracts, not copy-paste duplication.
5. Every capability needs an owner, input/output schema, risk class, cost envelope, evidence, tests, rollback and status label.
6. Never label candidate/planned as connected, implemented, deployed or verified.


## 2026-11-27 verified synchronization

Current recursive-tree snapshot: 213 files / 235 tree entries, no truncated trees. See `CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md` for the complete path inventory and exact main SHAs.

- My Brain PR #35 merged: governed runtime now uses the durable leased queue; worker terminal transitions require the active lease owner and an unexpired lease; the ATC smoke path uses the managed V3 bridge. CI run 45906541842 passed.
- My Brain PR #36 synchronized README/status/integration docs with the managed V3 runtime. CI run 45907097099 passed.
- Advait OS PR #4 and Pure Sharp PR #4 synchronized README/integration pointers; Pure Sharp Command Centre records the new Work Register and activity checkpoint.
- My Brain PRs #33/#34: legacy TaskQueue and ProviderCallLedger SQLite lifecycle fixes merged.
- 100X PR #20: SMV SQLite connection lifecycle fix merged and CI passed.
- 100X PR #21: phone runtime diagnostic connection lifecycle fix merged; regression test added and CI run 45906684654 passed.
- The B2B worker is CSV-only and not yet integrated as a Brain adapter; no labelled production accuracy, customer pilot or revenue is verified.
- Advait OS Gate remains a separate offline security component; authenticated identity and Brain integration are pending.
- No LLM runtime, Android/Termux validation, persistent scheduler, 24-hour operation, live payment or external customer execution is verified.


## 2026-11-27 B2B integration evidence

- My Brain PR #37 merged: pinned 100X submodule, separate financial artifact store, B2B adapter registration in GovernedSelfBuildRuntimeV3 and explicit local consent/confirmation gates.
- CI run [45908960326](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45908960326) passed 131 tests, compile and end-to-end synthetic integration smoke: 5 rows, 7 review flags, source rows absent from operational queue.
- The vault is permission-restricted but not encrypted at rest; explicit acknowledgement is required. Local owner flags are not authentication. Real customer data remains blocked pending encryption and owner identity.
