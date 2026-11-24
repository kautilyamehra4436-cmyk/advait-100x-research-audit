# B2B Discovery Log — Advait
Date: 2026-11-23 | Session: initial scan | Status: evidence collected, hypotheses pending validation

## Research signals
| Signal | Evidence | Interpretation | Limit |
|---|---|---|---|
| Invoice/AP manual work | ET report says 69.6% cited invoice processing as major pain (2,400+ demos, Jan–Jul 2026) | Potential demand for invoice data extraction and exception checks | Vendor demo sample; not representative market survey |
| Supplier management friction | LocalCircles survey coverage says 67% managing multiple suppliers; procurement/invoice/credit issues reported | Supplier comparison, purchase tracking and invoice checks could be productized | Survey methodology/sample must be reviewed; press coverage only |
| Paid data-cleaning offers | Upwork listings: $49/100 rows and $150/5,000 rows examples | Existing buyers and providers; pricing benchmarks for test hypotheses | Listing prices, not sales or earnings |
| Active job posts | Freelancer search page showed Excel cleanup, inventory consolidation, invoice extraction, PDF-to-sheet tasks | Concrete job-demand signal worth collecting systematically | Search result sample, bidding competition; no job won |

## Candidate ideas (qualitative initial ranking)
1. Business data validation & reconciliation — strongest problem evidence and clear deliverable; crowded category, must differentiate with audit trail and exception evidence.
2. Supplier quotation comparison / procurement tracker — pain signal strong, but source data and buyer workflow may be more complex; requires validation.
3. Product catalogue cleanup/conversion — repeatable and phone-friendly; demand signal less directly validated in this scan.
4. B2B lead research/qualification — buyers need leads, but data freshness, platform terms, privacy, and outreach risks need stricter controls.
5. Automated recurring business reports — productizable, but depends on access to data sources and integration requirements.

## First offer hypothesis
"Upload your authorized invoice/PO/CSV files. We return a clean structured copy, a list of duplicates/missing fields/mismatches, and a source-linked exception report. We do not change the original or make accounting/tax decisions."

Pricing is not decided. Competitor listing prices are only reference points; a pilot price must be tested and include scope, time, revision, privacy, and accuracy limits.

## Next tasks
- [ ] Collect at least 10–20 current buyer-demand signals from public marketplaces, de-duplicate them, and tag buyer type, requested output, budget if explicit, deadline, competition, and source date.
- [ ] Identify 2–3 verticals (e.g. distributors, small manufacturers, ecommerce sellers) and compare recurring pain and reachable channels.
- [ ] Build a synthetic labelled dataset and a simple deterministic validation script.
- [ ] Run tests and create sample output/QA report.
- [ ] Draft outreach only; no sending until owner approves.

## Evidence discipline
No customer has been contacted. No paid pilot, revenue, conversion, or accuracy result exists. All opportunity scores/pricing remain hypotheses until tests.


## Update — 2026-11-24 (new public signals)

### New evidence
- Freelancer India direct listing **Verified Invoice Data Entry**, project 40827088: PDF invoices/receipts → analysis-ready Excel with source verification; listing showed ₹750–₹1,250/hour and 6 days remaining at capture. URL: https://www.freelancer.in/projects/data-analysis/verified-invoice-data-entry
- Freelancer India data-cleansing page showed multiple active requests: invoice PDF entry, paper/photo product-inventory digitization, and e-commerce product CSV cleanup. Some listings displayed 25–42 bids, indicating substantial competition. URL: https://www.freelancer.in/jobs/data-cleansing
- These are current listings, not confirmed awarded contracts or payment. Confidence: medium-high for listing existence at capture; medium for category demand; low for market size/conversion/revenue.

### Ranking revision (compared with 2026-11-23)
1. Invoice PDF extraction + source verification + exceptions report — sharpened/strengthened by multiple fresh listings; PDF/OCR is currently a prototype gap.
2. CSV/Excel cleaning and reconciliation — still relevant, but crowded.
3. Product/inventory/catalogue cleanup — moved above supplier comparison due new direct listings.
4. Supplier quote comparison/procurement tracker — unchanged; prior survey signal, no new direct buyer listing found today.
5. B2B lead research/enrichment — deprioritized due high competition, privacy and platform-term risk.
6. Recurring reporting automation — no new direct signal today.

### Prototype re-test (2026-11-24)
- Local unit tests: 9/9 PASS.
- Synthetic sample: 5 rows, 7 flags; original input preserved.
- CI: workflow file includes test command, but actual run data remains unverified this day.
- PDF/OCR, XLSX, real data, accuracy metrics, performance benchmark, client outreach and revenue remain pending/not done.

Daily report: `B2B_DAILY_REPORT_2026-11-24.md`.
