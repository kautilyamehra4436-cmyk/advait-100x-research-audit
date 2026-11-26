#!/usr/bin/env python3
"""Advait B2B reconciliation prototype — CSV-only, deterministic, no external dependencies.

This tool flags potential issues; it does not make accounting/tax decisions or
silently alter source data. The original CSV is never overwritten.
"""
from __future__ import annotations
import argparse, csv, io, re, sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

MAX_INPUT_BYTES = 1_048_576
MAX_OUTPUT_BYTES = 4_194_304
MAX_ROWS = 10_000
MAX_COLUMNS = 100
REQUIRED = ("invoice_id", "vendor", "amount")
OUTPUT_FINDINGS = ("row_number", "invoice_id", "rule", "severity", "field", "observed", "expected", "detail")

def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip()).casefold()

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

def _serialize_csv(headers, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def reconcile_text(csv_text: str):
    """Pure, bounded CSV reconciliation API; performs no filesystem or network I/O."""
    if not isinstance(csv_text, str):
        raise TypeError("csv_text must be a string")
    encoded = csv_text.encode("utf-8")
    if not encoded or len(encoded) > MAX_INPUT_BYTES:
        raise ValueError("CSV input is empty or exceeds the 1 MiB limit")
    csv_text = csv_text.lstrip("\ufeff")
    if "\x00" in csv_text:
        raise ValueError("CSV contains a NUL character")

    reader = csv.DictReader(io.StringIO(csv_text, newline=""))
    if not reader.fieldnames:
        raise ValueError("CSV has no header row.")
    fields = [str(name).strip() if name is not None else "" for name in reader.fieldnames]
    if len(fields) > MAX_COLUMNS:
        raise ValueError("CSV exceeds the 100-column limit")
    if any(not name for name in fields):
        raise ValueError("CSV contains a blank header")
    normalized_headers = [name.casefold() for name in fields]
    if len(set(normalized_headers)) != len(normalized_headers):
        raise ValueError("CSV contains duplicate headers")
    reader.fieldnames = fields
    missing = [name for name in REQUIRED if name not in fields]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    rows = []
    for row_number, row in enumerate(reader, start=2):
        if None in row:
            raise ValueError(f"CSV row {row_number} has more values than the header")
        if any(value is None for value in row.values()):
            raise ValueError(f"CSV row {row_number} has fewer values than the header")
        rows.append(row)
        if len(rows) > MAX_ROWS:
            raise ValueError("CSV exceeds the 10000-row limit")

    findings = analyze_rows(rows)
    normalized = []
    for row_number, row in enumerate(rows, start=2):
        copy = {key: value.strip() if isinstance(value, str) else value
                for key, value in row.items()}
        for field, value in list(copy.items()):
            if field in {"amount", "po_amount"} or not isinstance(value, str):
                continue
            if value.lstrip(" \u00a0").startswith(("=", "+", "-", "@", "\t", "\r")):
                findings.append({
                    "row_number": row_number,
                    "invoice_id": (row.get("invoice_id") or "").strip(),
                    "rule": "formula_injection_risk",
                    "severity": "high",
                    "field": field,
                    "observed": value,
                    "expected": "literal text",
                    "detail": "Spreadsheet formula-like value was escaped in the normalized output.",
                })
                copy[field] = "'" + value
        normalized.append(copy)

    findings.sort(key=lambda item: (item["row_number"], item["field"], item["rule"]))
    severity_counts = Counter(item["severity"] for item in findings)
    rule_counts = Counter(item["rule"] for item in findings)
    summary = (
        "Advait CSV Validation Summary\n"
        f"Rows checked: {len(rows)}\nFlags: {len(findings)}\n"
        "Severity counts: " + ", ".join(f"{key}={value}" for key, value in sorted(severity_counts.items())) + "\n"
        "Rule counts: " + ", ".join(f"{key}={value}" for key, value in sorted(rule_counts.items())) + "\n"
        "Limit: flags are review suggestions, not accounting/tax conclusions.\n"
    )
    normalized_csv = _serialize_csv(fields, normalized)
    safe_findings = []
    for finding in findings:
        safe = dict(finding)
        for field, value in safe.items():
            if isinstance(value, str) and value.lstrip(" \u00a0").startswith(("=", "+", "-", "@", "\t", "\r")):
                safe[field] = "'" + value
        safe_findings.append(safe)
    exceptions_csv = _serialize_csv(OUTPUT_FINDINGS, safe_findings)
    output_bytes = (
        len(normalized_csv.encode("utf-8"))
        + len(exceptions_csv.encode("utf-8"))
        + len(summary.encode("utf-8"))
    )
    if output_bytes > MAX_OUTPUT_BYTES:
        raise ValueError("reconciliation output exceeds the 4 MiB limit")
    return {
        "rows_checked": len(rows),
        "flags": len(findings),
        "severity_counts": dict(sorted(severity_counts.items())),
        "rule_counts": dict(sorted(rule_counts.items())),
        "findings": findings,
        "normalized_csv": normalized_csv,
        "exceptions_csv": exceptions_csv,
        "summary": summary,
    }


def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def run(input_path, output_prefix):
    input_path, prefix = Path(input_path), Path(output_prefix)
    raw = input_path.read_bytes()
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("CSV input exceeds the 1 MiB limit")
    csv_text = raw.decode("utf-8-sig")
    report = reconcile_text(csv_text)

    findings_path = Path(str(prefix) + "_exceptions.csv")
    clean_path = Path(str(prefix) + "_normalized.csv")
    summary_path = Path(str(prefix) + "_summary.txt")
    targets = (clean_path, findings_path, summary_path)
    if not prefix.parent.exists() or not prefix.parent.is_dir() or prefix.parent.is_symlink():
        raise ValueError("output directory must be an existing non-symlink directory")
    if any(path.exists() or path.is_symlink() for path in targets):
        raise FileExistsError("refusing to overwrite an existing output artifact")

    for path, content, encoding in (
        (clean_path, report["normalized_csv"], "utf-8-sig"),
        (findings_path, report["exceptions_csv"], "utf-8-sig"),
        (summary_path, report["summary"], "utf-8"),
    ):
        with path.open("x", encoding=encoding, newline="") as stream:
            stream.write(content)
    return report["findings"], (clean_path, findings_path, summary_path)

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
