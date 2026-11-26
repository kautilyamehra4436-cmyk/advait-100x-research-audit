# ADVAIT SOVEREIGN AI CEO — Unified Master Blueprint
Version: 1.0-integration | Date: 2026-11-27
Status: Consolidation baseline; runtime and production verification remain staged.

## Executive mission
Advait is a phone-first, zero-spend-by-default, evidence-led business execution system. Its goal is to discover real customer problems, validate demand, produce authorized work, independently verify deliverables, reconcile actual revenue, and learn from measured outcomes. The ₹10,000/day target is an owner-set target, not a forecast or guarantee.

This is a consolidation of four existing repositories, not a destructive code merge. My Brain remains the central intelligence implementation. This repository is the canonical cross-project blueprint, integration registry, research and evidence hub. Specialized code remains in its source repository and is connected through versioned contracts.

No claim of consciousness, general autonomy, guaranteed revenue, 24/7 uptime, live payment collection or successful Android runtime is made.

## 1. Canonical component map

| Component | Source repository | Responsibility | Current verified boundary |
|---|---|---|---|
| My Brain / ATC | my-brain | Goal interpretation, planning, reflection, governed local task execution | ATC v1.2 remains deterministic; managed V3 bridge now connects selected local allowlisted tasks to lease-fenced governed runtime; no LLM or external executor |
| Governance / Soul / Command Centre | advait_pure_sharp | Owner authority, mission, policies, project navigation | Documents exist; conflicting drafts need reconciliation |
| Living Fabric / AELI | advait_pure_sharp | Proposed routing and coordination contract | Architecture proposal, not deployed orchestrator |
| Advait OS Gate | advait_os | Local filesystem gate and fail-closed high-risk decisions | v0.2 code and tests; no production identity provider |
| Bounded Execution Core | advait-100x-research-audit | Allowlist, budgets, risk checks, evidence-verifier contract, ledger | Offline reference implementation; no live adapters |
| B2B Worker | advait-100x-research-audit | CSV reconciliation and exception output | CSV worker and CI tests exist; no labelled real-world accuracy, XLSX/PDF/OCR, Brain adapter or customer pilot |
| PanchTatva C10 | advait_pure_sharp | Scenario and regression harness | 10 simulated scenarios; not proof of intelligence |
| SMV | 100X | Payment-event ledger and financial record foundation | Offline ledger; SQLite lifecycle regression passed; no live webhook, payout, bank settlement or PNB integration |
| Research and Evidence Ledger | 100X | Sources, confidence, tests, benchmarks and decisions | Research logs and reports exist |
| Owner Command Centre | my-brain docs + this blueprint | Approvals, opportunity portfolio, queue, spend and status | Documentation only; no deployed dashboard verified |

Repositories:
- https://github.com/kautilyamehra4436-cmyk/my-brain
- https://github.com/kautilyamehra4436-cmyk/advait_os
- https://github.com/kautilyamehra4436-cmyk/advait_pure_sharp
- https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit

## 2. New operating principle: Opportunity-to-Proof-to-Profit (O2P2)

The primary work object is an Opportunity Case, not a raw task. Every case has a unique ID, source evidence, uncertainty, estimated value, risk, cost, plan, acceptance criteria, delivery evidence and financial state.

Lifecycle:
1. Sense: discover public, permitted market signals.
2. Provenance: record source URL, retrieval time, claim, supporting evidence, source class, confidence and recheck date.
3. Normalize: identify user, pain, frequency, workaround, buyer, budget proxy and measurable outcome.
4. Challenge: compare at least five materially different strategies when practical: evidence-first, low-resource, risk-first, creative reframing, fallback.
5. Score: evaluate evidence strength, buyer clarity, repeatability, feasibility, value evidence, competition, cost and risk. Scores are heuristics until calibrated. Missing data remains UNKNOWN.
6. Decide: auto-advance only reversible, low-risk internal work inside owner-approved limits. Hold external, sensitive, uncertain, costly or irreversible actions.
7. Build: produce a small bounded solution and deterministic tests before adding AI/OCR complexity.
8. Verify: independent acceptance tests, source-preserving outputs, uncertainty flags and reproducible run metadata.
9. Authorize: obtain owner approval for outreach, bids, contracts, client data, paid services, credentials, external submissions and financial actions unless a narrow pre-authorization is explicitly configured.
10. Deliver: provide the agreed deliverable and retain acceptance evidence.
11. Reconcile: track quoted, contracted, delivered, invoiced, received, refunded and pending amounts separately.
12. Learn: compare prediction with outcome; record failure causes and propose tested changes.
13. Promote: proposal → isolated branch/sandbox → tests → review → owner approval → versioned release → monitoring and rollback.

Allowed case states: REJECTED, PARKED, NEEDS_OWNER, READY_FOR_TEST, TEST_FAILED, VERIFIED_READY, AUTHORIZED, DELIVERED_PENDING_ACCEPTANCE, ACCEPTED_PENDING_PAYMENT, PAID_RECONCILED, CLOSED. A worker cannot declare success without evidence.

## 3. My Brain: thinking, memory and planning
My Brain is the central thinking and memory layer, not an executor by itself.
- ATC v1.2 creates draft plans using deterministic rules and heuristic strategy scores.
- The SQLite task queue stores plan-only work; a queue entry is not execution. My Brain PR #5 additionally hardens completion: a task cannot be marked done without an injected verifier accepting explicit evidence; only the evidence digest is persisted. This is a verifier hook, not a deployed production verifier.
- Zero-cost guard exists but global wiring at every adapter boundary is not verified.
- ATC risk keyword detection can miss or over-flag; it is advisory, not a security boundary.
- Reflection must challenge assumptions, identify missing evidence, compare alternatives and state what would disprove a recommendation.
- Persistent memory distinguishes durable owner policy, project facts, hypotheses, temporary tasks and sensitive records.
- Credentials and source financial/legal records must not be stored in ordinary model memory or unencrypted operational SQLite.
- The Brain must not claim background work between sessions without an actual configured and tested runtime/scheduler.

## 4. Multi-agent and open-source tool ecosystem
Use a capability registry, not unrestricted agent access. Every worker/tool record must specify source and license, version, inputs, outputs, data permissions, network access, resource needs, cost/quota, failure modes, tests and allowed actions.

Candidate tools are not connected merely because they appear in a list:
- Termux + Python: possible Android local runtime; user installation and device validation required.
- SQLite: operational metadata only; sensitive records need a separately reviewed protected store.
- Git + GitHub Actions: versioning and CI subject to actual quota and account settings.
- n8n, Huginn, Activepieces: compare resource, licensing and phone feasibility; do not deploy all.
- PDF/OCR: evaluate offline/open-source extraction separately; low-confidence fields require human review.
- LLMs: only services with permitted, confirmed access and clear data terms. No quota evasion, credential sharing or deceptive free-tier cycling.
- Browser/marketplace research: public permitted access only; no spam, unsolicited bulk outreach, authenticated scraping or access-control bypass.

A tool moves through candidate → connected → installed → configured → runtime-tested → approved-for-use. Each transition needs evidence.

## 5. Security and owner authority
Authority order: owner policy and current explicit authorization → authenticated security gate → risk/cost policy → planner recommendation → worker suggestion. The planner cannot override the gate. A hash, phrase, local file, repo permission or connector session is not identity proof for money movement.

Risk classes:
- LOW: read permitted public data, draft, deterministic local analysis.
- MEDIUM: create a new non-sensitive project artifact in a controlled branch; log and review.
- HIGH: external communication/submission, client-data processing, delete/overwrite, account/security change; explicit owner approval and suitable authentication.
- CRITICAL: spending, payment, withdrawal, bank transfer, contract signing, credential disclosure or production security change. Block unless a genuine authenticated exact-action approval provider is deployed. Current offline code does not ship one; these actions remain blocked.

Emergency stop prevents new work; it cannot undo external effects. Every adapter needs idempotency, timeouts, bounded retries, rate limits, input validation, immutable run ID and reconciliation of uncertain outcomes.

## 6. Zero-cost and resource rules
The controlling policy in my-brain/config.yml is hard zero: ₹0 maximum spend, no paid APIs/hosting/subscriptions/credit/auto-renewal/automatic reinvestment, and stop on free-quota exhaustion. This overrides contradictory positive spend tables elsewhere.

Quota rules:
- 70%: warn and estimate remaining work.
- 80%: pause optional/high-volume jobs; switch only to a pre-verified, terms-compliant free alternative with no hidden obligation.
- 90%, unknown quota or exhaustion: pause the affected integration and report. Never silently fall back to paid.
- ₹0 does not mean zero electricity, data, device wear, human time or opportunity cost; record separately where measurable.

Phone-first means small batches, streaming, bounded memory, resumable checkpoints and no mandatory cloud server. Android background execution and 24-hour uptime must be tested on the actual device, never assumed.

## 7. Business and earning engine
Initial candidate retained from the research: small-business invoice/data validation and reconciliation. The first service is CSV-first: deterministic duplicate detection, normalization, field validation, cross-file comparison, exception report with source-row references and a QA summary. Preserve the original; no silent deletion or financial correction. Human confirms tax/legal interpretations.

The existing worker does not yet implement PDF/OCR, XLSX multi-sheet output, PO/GRN matching, GST/tax determination or bank/payment integration.

Commercial pipeline: public demand evidence → shortlist → synthetic sample → measured QA report → owner-reviewed offer → owner-approved individualized outreach → scoped pilot → delivery/acceptance → invoice/payment reconciliation → post-mortem. Never bid or contact a prospect without owner approval. A marketplace budget is not realized income. Track time, revisions, false positives/negatives, conversion and realized profit.

## 8. Sovereign Money Vault
Separate payment-provider events, internal accounting ledger, bank credentials and owner approvals. Credentials never enter repository files or ordinary logs. Razorpay and PNB are intended integrations, not verified live connections. The original PR #6 was superseded and closed; the rebased, hardened SMV foundation in PR #8 was merged on 2026-11-26. Do not enable live keys or real transfers as part of documentation consolidation.

Before production: test-mode fixtures, server-side webhook signature verification, idempotency, replay protection, amount/currency/order matching, refund/dispute handling and independent reconciliation. PNB linkage must use an officially supported, owner-configured channel. AI never receives withdrawal or transfer authority.

## 9. Self-evolution without self-authorization
Observe → detect recurring issue → falsifiable hypothesis → minimal patch proposal → regression test → isolated test → baseline comparison → security review → owner approval → versioned promotion → monitor → rollback.

The system may create research notes and sandbox patch proposals within granted repository scope. It may not alter owner policy, permissions, credentials, financial controls, legal rules or production security boundaries. No self-merge to protected production branches.

## 10. Evidence and research standard
For every claim retain claim ID, exact wording, source URL/publisher, publication date, retrieval timestamp, source class, supporting excerpt/summary, scope, confidence, caveats, verification state and recheck date. Separate direct observation, vendor claim, secondary report, assumption and hypothesis. Simulated PASS is not real-world capability proof.

## 11. Existing test evidence and next acceptance

| Layer | Existing evidence | Next required proof |
|---|---|---|
| My Brain ATC | PR #1 merged; historical 38/38 CI tests | fresh CI, queue integration, Android/Termux run |
| Advait OS Gate | fail-closed code; 15 regression tests reported | fresh CI, platform security review, authenticated verifier design |
| Bounded execution core | historical 50/50 CI suite reported | fresh CI, adversarial integration, real verifier remains external |
| B2B worker | historical 9/9 tests | 20+ labelled cases, precision/recall, false-positive/negative, XLSX output |
| PanchTatva C10 | 3/3 structural tests; 10 simulated scenarios | executable decision functions and adversarial fixtures |
| SMV | PR #6 open | inspect diff; synthetic webhook tests; no real funds |
| Phone runtime | not verified | user-side Android test with time, memory, battery, heat and offline recovery |
| 24-hour stability | not verified | actual device soak test, crash/restart and queue recovery |
| Revenue | no sale/payment evidenced | owner-approved pilot and independently reconciled receipt |

Historical test reports do not replace a fresh run. Each report records commit SHA, workflow URL, timestamp, test count, skipped tests and environment.

## 12. Conflict resolution register
1. my-brain/config.yml sets hard ₹0. Positive cost caps in revenue.md are conflicting draft content and are non-operative until corrected.
2. authorization.md describes Telegram/Face ID tiers, but no authenticated provider is deployed. They are placeholders, not functioning controls.
3. security.md checkmarks for 2FA, branch protection, Dependabot, SHA pinning, OIDC and rate limits require independent live settings verification.
4. compliance.md includes legal assertions, retention schedules and a placeholder email. They are not verified legal determinations; validate against current authoritative law and actual data flows.
5. health.md references monitoring metrics while README says 0/100 uncomputed. No health score is valid until measurements exist.
6. ATC plans, queue entries and handoff envelopes do not mean execution or authorization.
7. Local hash chains are tamper-evident only under stated assumptions; without external anchoring and authenticated writers they are not immutable proof.

## 13. Reporting and operations
Daily report: verified work, failed attempts, new/expired opportunities, tests and commit SHAs, quota/spend, queue, pending approvals, delivered work, invoices, received revenue, security events, unknowns and next three actions. A 06:00 IST report requires an actual scheduler and tested delivery channel; do not claim it is scheduled until configured.

## 14. Implementation sequence
Phase 0: preserve four repositories, record source SHAs, reconcile documents, inspect PR #6.
Phase 1: standardize Opportunity, Task, Evidence, Approval, Delivery and Financial Event schemas; add integration register and CI links.
Phase 2: connect ATC → queue → bounded executor behind allowlist; wire cost/risk gates at every adapter; add verifier, checkpoint and recovery.
Phase 3: benchmark CSV worker with labelled synthetic cases; add XLSX only after correctness; evaluate PDF/OCR after deterministic baseline.
Phase 4: review SMV PR and test provider events in test mode; design PNB only through supported official route; keep withdrawals blocked.
Phase 5: user installs phone runtime; measure resources; run bounded soak test before 24-hour claims.
Phase 6: controlled research and evolution with tests, owner-reviewed promotion and rollback.

## 15. Consolidation checkpoint — 2026-11-27

Verified repository metadata:
- Current main commits: 100X source baseline `67a1595bddab2b538d3d562e032d3a0de291878b`; My Brain `f27ca720f1c1be0fa6e2ea5e5e2916f48cf338b3`; Advait OS `07f24f281fb89b189384112ed35530e3108b9d85`; Pure Sharp `55098ab2188f324260ca233966fc8f4c6334e478`.
- Recursive trees contain 207 files / 227 entries; none of the four trees was truncated. Full paths are recorded in `CURRENT_REPOSITORY_SNAPSHOT_2026-11-27.md`.
- My Brain PR #35 is merged. `GovernedSelfBuildRuntimeV3` uses `ManagedTaskQueueV3`; worker completion/failure is fenced by the active lease owner and expiry; the ATC integration smoke uses the managed V3 bridge. CI run [45906541842](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45906541842) passed.
- My Brain PRs #33/#34 closed the SQLite connection lifecycle gaps in legacy TaskQueue and ProviderCallLedger.
- My Brain PR #36 synchronized the README, status and ATC integration map; CI run [45907097099](https://github.com/kautilyamehra4436-cmyk/my-brain/actions/runs/45907097099) passed.
- Advait OS PR #4 updated the Gate README/integration pointer. Pure Sharp PR #4 updated its README, integration pointer and Command Centre Work Register/activity log.
- 100X PR #20 fixed SMV SQLite connection closure. PR #21 fixed the phone diagnostic's SQLite handles and added a regression test. CI run [45906684654](https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit/actions/runs/45906684654) passed.
- B2B reconciliation code is CSV-only and its CI tests pass; labelled real-world accuracy, XLSX/PDF/OCR, Brain adapter integration, customer pilot and revenue remain unverified.
- ATC remains a deterministic planner, not an LLM. The managed bridge executes only explicitly selected, zero-cost, local allowlisted operations.
- SMV remains an offline event-ledger foundation; no live webhook receiver, PNB verifier, payout/withdrawal/transfer or bank settlement adapter is enabled.
- Advait OS Gate remains a separate offline gate; authenticated production owner identity and runtime integration are not verified.
- Living Fabric/AELI remains an architecture proposal; PanchTatva C10 remains a scenario harness, not proof of intelligence or autonomy.
- Android/Termux, persistent scheduling, 24-hour operation, live customer delivery and realized revenue are not verified.

Coverage: recursive path inventories are complete for the four recorded main commits. This is not a line-by-line semantic audit of every source file, historical branch, external setting or runtime environment. Each capability is labelled by its actual test boundary, not by its blueprint existence.

## 16. Definition of operational success
Advait is operational only when an authorized workflow has traceable demand evidence, approved scope and customer permission, reproducible deliverable, independent acceptance verification, customer acceptance, payment receipt independently confirmed, accurate ledger reconciliation, no policy/privacy/security/cost breach, and reproducible logs plus rollback/recovery. Until then report the exact verified stage and blockers.
