#!/usr/bin/env python3
"""Advait B2B reconciliation prototype — CSV-only, deterministic, no external dependencies.

This tool flags potential issues; it does not make accounting/tax decisions or
silently alter source data. The original CSV is never overwritten.
"""
from __future__ import annotations
import argparse, csv, re, sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ("invoice_id", "vendor", "amount")
OUTPUT_FINDINGS = ("row_number", "invoice_id", "rule", "severity", "field", "observed", "expected", "detail")

def norm_text(value: str) -> str:
    return re.sub(r"\\s+", " ", (value or "").strip()).casefold()

def parse_amount(value: str):
    raw = (value or "").strip().replace(",", "").replace("₹", "").replace("$", "")
    if raw == "":
        return None
    try:
        return Decimal(raw)
    except InvalidOperation:
        return None

def analyze_rows(rows):
    findings = []
    ids = Counter(norm_text(r.get("invoice_id", "")) for r in rows)
    for idx, row in enumerate(rows, start=2):
        invoice = (row.get("invoice_id") or "").strip()
        vendor = (row.get("vendor") or "").strip()
        amount_raw = (row.get("amount") or "").strip()
        po_ref = (row.get("po_ref") or "").strip()
        po_amount_raw = (row.get("po_amount") or "").strip()
        po_vendor = (row.get("po_vendor") or "").strip()

        def add(rule, severity, field, observed="", expected="", detail=""):
            findings.append({"row_number": idx, "invoice_id": invoice, "rule": rule,
                "severity": severity, "field": field, "observed": observed,
                "expected": expected, "detail": detail})

        if not invoice:
            add("missing_invoice_id", "high", "invoice_id", detail="Invoice ID is blank.")
        elif ids[norm_text(invoice)] > 1:
            add("duplicate_invoice_id", "high", "invoice_id", invoice,
                detail=f"Invoice ID appears {ids[norm_text(invoice)]} times; review all matching rows.")
        if not vendor:
            add("missing_vendor", "high", "vendor", detail="Vendor name is blank.")
        if amount_raw and parse_amount(amount_raw) is None:
            add("invalid_amount", "high", "amount", amount_raw,
                detail="Amount cannot be parsed as a decimal; check source.")
        elif not amount_raw:
            add("missing_amount", "high", "amount", detail="Amount is blank.")
        if not po_ref:
            add("missing_po_reference", "medium", "po_ref",
                detail="No PO reference supplied; cannot perform PO match.")

        invoice_amt, po_amt = parse_amount(amount_raw), parse_amount(po_amount_raw)
        if po_amount_raw and po_amt is None:
            add("invalid_po_amount", "high", "po_amount", po_amount_raw,
                detail="PO amount cannot be parsed.")
        elif invoice_amt is not None and po_amt is not None and invoice_amt != po_amt:
            add("amount_mismatch", "high", "amount", str(invoice_amt), str(po_amt),
                detail="Invoice amount differs from supplied PO amount; verify against source.")
        if po_vendor and vendor and norm_text(po_vendor) != norm_text(vendor):
            add("vendor_mismatch", "medium", "vendor", vendor, po_vendor,
                detail="Vendor text differs from supplied PO vendor; may be alias/formatting, review.")
    return findings

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def run(input_path, output_prefix):
    input_path, prefix = Path(input_path), Path(output_prefix)
    with input_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        fields = reader.fieldnames
        missing = [h for h in REQUIRED if h not in fields]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        rows = list(reader)
    findings = analyze_rows(rows)
    findings_path = Path(str(prefix) + "_exceptions.csv")
    clean_path = Path(str(prefix) + "_normalized.csv")
    summary_path = Path(str(prefix) + "_summary.txt")
    normalized = []
    for row in rows:
        copy = dict(row)
        for k, v in copy.items():
            if isinstance(v, str):
                copy[k] = v.strip()
        normalized.append(copy)
    write_csv(clean_path, fields, normalized)
    write_csv(findings_path, OUTPUT_FINDINGS, findings)
    severity_counts = Counter(x["severity"] for x in findings)
    rule_counts = Counter(x["rule"] for x in findings)
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("Advait CSV Validation Summary\n")
        f.write(f"Input: {input_path.name}\nRows checked: {len(rows)}\nFlags: {len(findings)}\n")
        f.write("Severity counts: " + ", ".join(f"{k}={v}" for k, v in sorted(severity_counts.items())) + "\n")
        f.write("Rule counts: " + ", ".join(f"{k}={v}" for k, v in sorted(rule_counts.items())) + "\n")
        f.write("Limit: flags are review suggestions, not accounting/tax conclusions.\n")
    return findings, (clean_path, findings_path, summary_path)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", help="Source CSV; never overwritten")
    parser.add_argument("--out-prefix", default="advait_report", help="Output filename prefix")
    args = parser.parse_args(argv)
    try:
        findings, paths = run(args.input_csv, args.out_prefix)
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Rows processed; flags={len(findings)}")
    for p in paths:
        print(f"Created: {p}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
