# ADVAIT Unified Integration Registry
Date: 2026-11-26
Canonical design: UNIFIED_MASTER_BLUEPRINT.md

## Repository baselines
| Repository | Main baseline SHA | Role |
|---|---|---|
| my-brain | 797f3ee2b277d891102bf8f2dafb1609a0738a91 | Central Brain / ATC |
| advait_os | 04552a7db46db45af817a1afa68720684f1d392f | Security Gate |
| advait_pure_sharp | 2fafd1971340b056f3e37de9c08a5cedc42ad065 | Governance / Living Fabric / PanchTatva |
| advait-100x-research-audit | c553a0f7235e1b092cae7810b8c97ba4fd640192 | Execution / B2B / Research / Master Hub |

## Module register
| Module | Source | State | Integration rule |
|---|---|---|---|
| SOUL / Governance | my-brain + pure_sharp | Docs | One owner-authority hierarchy; canonical conflicts recorded |
| ATC Planner v1.2 | my-brain/core | Merged, rule-based | Drafts only; no external execution |
| Task Queue | my-brain/core | Local SQLite queue | Stored plan is not execution |
| Zero Cost Guard | my-brain/core | Helper exists; global wiring unverified | Fail closed at every cost-bearing boundary |
| ATC Handoff | my-brain/core | Contract helper | REVIEWED_NOT_AUTHORIZED only |
| Advait OS Gate v0.2 | advait_os | Offline gate | HIGH/CRITICAL blocked without authenticated verifier |
| Bounded Execution Core v0.2 | 100X | Offline reference | No live adapters; independent verifier not deployed |
| B2B Reconciliation | 100X | CSV worker | CSV-only; benchmark expansion required |
| PanchTatva C10 | pure_sharp | Scenario harness | Simulated checks only |
| Living Fabric / AELI | pure_sharp | Architecture proposal | Not a deployed orchestrator |
| SMV | 100X PR #6 | Open PR | Inspect diff before merge; no live payment |
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
