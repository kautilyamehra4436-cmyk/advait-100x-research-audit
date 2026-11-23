# B2B Prototype Test Report
Date: 2026-11-23
Prototype: `b2b_reconcile.py` (CSV-only, deterministic, Python standard library)

## Tests
- Unit tests: **9/9 PASS** (local execution).
- Synthetic sample: 5 rows processed; 7 flags emitted.
- Original sample file preserved; outputs created: normalized copy, exception CSV, summary TXT.

Sample rule counts:
- duplicate_invoice_id: 2
- missing_po_reference: 1
- amount_mismatch: 1
- invalid_amount: 1
- missing_vendor: 1
- vendor_mismatch: 1

## Implemented
- Required columns: invoice_id, vendor, amount
- Duplicate invoice IDs (case/whitespace normalized)
- Missing invoice ID/vendor/amount
- Invalid amount parsing
- Missing PO reference
- Invoice-vs-PO amount mismatch (when PO amount supplied)
- Vendor text mismatch (when PO vendor supplied)
- Output files with source row numbers and reason details
- Input is not overwritten; normalized output is a separate file

## Limits / not yet tested
- CSV only; no PDF/OCR, XLSX, image ingestion, database, cloud or integrations.
- Duplicate detection is exact after basic case/whitespace normalization; it does not identify fuzzy duplicates.
- Amount equality uses exact Decimal comparison; currency, tax/discount, tolerance, and business-specific rules are not inferred.
- Vendor mismatch can be a legitimate alias and is only flagged.
- No real customer documents or customer testing; synthetic data only.
- No accuracy metric against a labelled real dataset, no pricing or revenue validation.

## Reproduce on phone/PC Python
```bash
python -m unittest -v test_b2b_reconcile.py
python b2b_reconcile.py b2b_sample_input.csv --out-prefix sample_report
```
