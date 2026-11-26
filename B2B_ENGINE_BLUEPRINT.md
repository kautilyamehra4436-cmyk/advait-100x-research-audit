# Advait B2B Business Discovery & Execution Blueprint
Version: 0.4 | Date: 2026-11-27 | Status: CSV worker integrated into governed My Brain runtime; customer readiness pending

## Objective
Advait should own the routine cycle of finding, evaluating, prototyping, validating, and delivering B2B opportunities within owner-defined constraints. The owner should not have to manually hunt for business ideas. Owner approval remains mandatory for financial actions, binding contracts, risky data handling, policy changes, and outbound actions not explicitly pre-authorized.

## Guardrails (default)
- Zero upfront spend; no recurring paid subscriptions or paid hosting unless owner approves.
- Phone-first, low-compute; use local/offline processing where practical and free tools where viable.
- No spam, deception, unsolicited bulk outreach, unauthorized scraping, or use of private/customer data without permission.
- No financial transfers, withdrawals, contract acceptance, credential handling, or policy/core promotion without owner approval.
- For financial data: organize, extract, compare, flag exceptions only; do not make tax/accounting/legal determinations. Human approval for final interpretation.
- Never claim a market, customer, revenue, or accuracy result without evidence.
- Preserve source links, timestamp, claim, confidence, and verification status for every research assertion.
- Stop/hold if evidence is weak, cost/risk exceeds limits, data permission is unclear, or the action is irreversible.

## Modules
1. **Market Scout** — search public signals: job posts, marketplace requests, complaints, recurring operational pain, public product gaps.
2. **Evidence Ledger** — source, date, excerpt/summary, URL, evidence class, confidence, expiry/recheck date. Distinguish direct evidence, survey/report evidence, marketplace signal, and hypothesis.
3. **Problem Normalizer** — translate signals into: user, workflow, pain, frequency, consequence, current workaround, buyer, budget proxy, and measurable outcome.
4. **Opportunity Scorer** — score demand evidence, buyer clarity, repeatability, delivery feasibility, low-cost fit, competition, risk, and owner fit. Scores are heuristics, not truth.
5. **Portfolio/Decision Gate** — rank candidates; auto-select only within owner-approved low-risk envelope. Uncertain or high-risk opportunities are held for owner.
6. **Solution Factory** — generate a narrowly scoped workflow, templates/code, input/output specification, and test cases.
7. **Quality & Evidence Verifier** — validate outputs against source; preserve original; mark uncertain fields; run acceptance tests; reject unsupported claims.
8. **Customer Discovery / Outreach Drafting** — identify public, relevant prospects and draft respectful, individualized outreach. Sending requires explicit permission or a narrowly pre-approved policy, with opt-out and rate limits.
9. **Delivery & Feedback** — deliver agreed output, record customer feedback and revisions, track outcome.
10. **Revenue Ledger** — record quoted, contracted, delivered, invoiced, received, and pending amounts. This is recordkeeping only; payment/withdrawal actions require owner approval.
11. **Learning Loop** — compare estimates to actual outcomes; propose changes; run tests in a sandbox; version and rollback. No self-modification of permissions, owner policy, or security boundary.
12. **Owner Control Center** — pending approvals, current opportunities, evidence, spend (default zero), work queue, reports, and stop control.

## Opportunity ranking rubric (0–5 each; initial weights)
- Evidence of demand: 25%
- Clear buyer and reachable channel: 15%
- Repeatability/productization: 15%
- Delivery feasibility on phone/free tools: 15%
- Value / willingness-to-pay evidence: 15%
- Competition/differentiation: 10%
- Safety/legal/privacy risk: 5% (higher score = lower risk)

Weighted score = sum(score/5 * weight). Missing evidence is marked unknown, not silently scored as positive. Initial ranking is provisional and must be recalibrated after real customer tests.

## First candidate (provisional)
**Business Data Validation & Reconciliation Pack**: client-authorized PDFs/images/CSV/XLSX → structured extraction (where feasible), normalization, duplicate detection, field validation, cross-file comparison, exception list with row/source references, clean copy, QA summary. Original data is preserved. Human confirms financial/legal conclusions.
Differentiation hypothesis: evidence trail for every flagged row; no silent deletion or invented corrections; clear exception report; sample-first accuracy report; privacy-conscious processing.

## Research snapshot (not a complete market audit)
- MSME invoice/AP pain: reported 69.6% in a study based on 2,400+ demonstrations (Economic Times, Aug 2026): https://m.economictimes.com/news/company/corporate-trends/indian-businesses-still-rely-on-manual-invoicing-despite-digital-adoption-study/amp_articleshow/132825565.cms
- Supplier-management / procurement friction: LocalCircles survey coverage reports 67% managing multiple suppliers and recurring invoice compliance, price volatility, and credit issues: https://economictimes.indiatimes.com/small-biz/sme-sector/world-msme-day-2026-supplier-gaps-invoice-compliance-credit-access-continue-to-hit-5-in-10-msmes/articleshow/132013668.cms
- Marketplace signals: Upwork examples include 100-row invoice CSV checks at $49 and 5,000-row cleanup/reconciliation at $150 (listing prices, not realized earnings): https://www.upwork.com/services/product/admin-customer-support-clean-validate-and-organize-your-business-csv-data-or-pdf-documents-2114557318853676241 and https://www.upwork.com/services/product/development-it-your-excel-data-cleaned-de-duplicated-and-reconciled-to-your-source-2116232489207973539
- Data-cleaning category listing displays multiple offers and competitive starting prices: https://www.upwork.com/services/data-analysis-reports/data-entry-cleaning
- Freelancer.in search page surfaced current examples of spreadsheet cleanup, invoice extraction, inventory cleanup and consolidation tasks: https://www.freelancer.in/jobs/data-cleansing/
These sources demonstrate problem/service signals and competition, not a guaranteed buyer or income.

## First validation experiment — current state
1. Synthetic sample data is stored in the repository; CI processes 5 rows and verifies the result (7 review flags).
2. A bounded pure-text CSV API is implemented; it has 1 MiB input, 10,000-row, 100-column and 4 MiB output limits. Formula-like spreadsheet cells are flagged and escaped.
3. Unit/regression tests and end-to-end adapter smoke pass. Formal precision/recall, false-positive/negative rates and a 20+ case labelled benchmark have **not** been measured.
4. CI generates normalized CSV, exceptions CSV and summary artifacts in a temporary vault; no real customer deliverable has been produced.
5. Public buyer signals have been collected, but a verified 10-prospect shortlist is not complete.
6. No outreach has been sent; offer drafting and owner approval remain pending.
7. No paid pilot, customer acceptance or revenue has occurred.

## Acceptance criteria and verification boundary
- Source file remains unchanged.
- Every flag maps to source row and rule.
- No silent deletion or automatic financial correction.
- Unknown/ambiguous fields stay flagged.
- Reproducible results for same input.
- Verified tests cover duplicate IDs, missing required values/PO reference, vendor/amount mismatch, invalid amount, malformed row width, duplicate headers, formula injection and output no-overwrite. Date normalization and formal false-positive/negative metrics remain pending.
- Test report separates verified behavior from limitations. Current integration CI: 131 full My Brain tests and 5-row / 7-flag synthetic B2B smoke.

## Current status
- Public research snapshot: started; sources collected, not exhaustive.
- Candidate ranking: provisional; no weighted score validated yet.
- CSV reconciliation API: implemented in `b2b_reconcile.py` as bounded pure-text function; 1 MiB input, 10,000 rows, 100 columns, 4 MiB output; formula-like spreadsheet cells are flagged and escaped.
- My Brain integration: merged as PR #37 through a pinned Git submodule and governed `B2BReconciliationAdapterV1`; task queue stores only opaque artifact ID and metadata, while source/output files remain in a separate financial artifact store.
- Synthetic integration CI: 131 tests passed; end-to-end sample processed 5 rows and generated 7 review flags; source rows were not persisted in operational queue. No real customer data was processed.
- Financial artifact store: restrictive OS permissions and symlink checks, but **not encrypted at rest**. Explicit acknowledgement is required; do not use sensitive customer records until encryption/Android Keystore and authenticated owner identity are implemented.
- Owner consent/confirmation flags are manual intent checks, not authentication.
- XLSX multi-sheet, PDF/OCR and customer-system adapters: not implemented/verified.
- Customer/paid pilot: not run.
- Repo update: CSV worker and tests are integrated into My Brain's local governed adapter; no production customer integration, outreach, paid pilot or real client work has been performed.
