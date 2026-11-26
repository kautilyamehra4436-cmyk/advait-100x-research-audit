"""Advait CEO Control Board: local, read-only project status aggregator.

This board reads known report/code artifacts from local repository checkouts.
It does not call external services, execute tasks, authenticate owners, or declare
production/live status. Missing evidence is reported as PENDING/UNKNOWN.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

WORKSTREAMS = [
    ("Unified architecture", "UNIFIED_MASTER_BLUEPRINT.md", "DOCUMENTED"),
    ("Integration registry", "UNIFIED_INTEGRATION_REGISTRY.md", "DOCUMENTED"),
    ("Queue evidence hardening", "QUEUE_EVIDENCE_HARDENING_REPORT_2026-11-26.md", "DOCUMENTED"),
    ("My Brain owner authorization policy", "authorization.md", "DOCUMENTED"),
    ("My Brain security controls", "security.md", "DOCUMENTED"),
    ("My Brain legal/compliance checklist", "compliance.md", "DOCUMENTED"),
    ("My Brain revenue and zero-spend policy", "revenue.md", "DOCUMENTED"),
    ("My Brain operational health status", "health.md", "DOCUMENTED"),
    ("Advait OS security gate", "GATE_SECURITY_V02.md", "DOCUMENTED"),
    ("Advait Pure Sharp operating algorithm", "MASTER_OPERATING_ALGORITHM.md", "DOCUMENTED"),
    ("Advait Pure Sharp living-fabric architecture", "ADVAIT_LIVING_FABRIC_ARCHITECTURE.md", "DOCUMENTED"),
    ("Execution consolidation report", "CONSOLIDATION_EXECUTION_REPORT_2026-11-26.md", "DOCUMENTED"),
    ("ATC → Queue → Executor runtime", "core/atc_planner.py", "PENDING_INTEGRATION"),
    ("My Brain task queue", "core/task_queue.py", "FOUNDATION_PRESENT"),
    ("Zero-cost guard", "core/zero_cost_guard.py", "FOUNDATION_PRESENT"),
    ("Razorpay/SMV foundation", "smv_core.py", "FOUNDATION_PRESENT"),
    ("PNB settlement adapter", "pnb_settlement_adapter.py", "PENDING"),
    ("Independent owner approval provider", "owner_approval_provider.py", "PENDING"),
    ("Independent evidence verifier", "evidence_verifier.py", "PENDING"),
    ("Android/Termux deployment", "ANDROID_DEPLOYMENT.md", "PHONE_PENDING"),
    ("24-hour target-device soak", "PHONE_24H_SOAK_EVIDENCE.json", "PHONE_PENDING"),
    ("Customer delivery and reconciled revenue", "REVENUE_EVIDENCE.json", "PENDING"),
    ("Owner-aligned relationship intelligence", "relationship_intelligence.py", "FOUNDATION_PRESENT"),
    ("Relationship intelligence tests", "tests/test_relationship_intelligence.py", "FOUNDATION_PRESENT"),
    ("Owner-fit and work-mix report specification", "RELATIONSHIP_INTELLIGENCE.md", "DOCUMENTED"),
    ("Open-source maker and customer intelligence", "open_source_intelligence.py", "FOUNDATION_PRESENT"),
    ("Open-source maker/customer test suite", "tests/test_open_source_intelligence.py", "FOUNDATION_PRESENT"),
    ("Open-source tool purpose, license and defense guide", "OPEN_SOURCE_MAKER_CUSTOMER_INTELLIGENCE.md", "DOCUMENTED"),
]

LABELS = {
    "DOCUMENTED": "Documented; not runtime proof",
    "FOUNDATION_PRESENT": "Code foundation present; deployment not verified",
    "PENDING_INTEGRATION": "Executable integration pending",
    "PHONE_PENDING": "Phone deployment/test pending",
    "PENDING": "Not implemented or not evidenced",
}


def _find_file(roots: list[Path], relative: str) -> str | None:
    for root in roots:
        candidate = root / relative
        if candidate.is_file():
            return str(candidate)
    return None


def build_board(roots: list[Path]) -> dict:
    rows = []
    for name, relative, declared in WORKSTREAMS:
        found = _find_file(roots, relative)
        # A declared foundation is not promoted to operational/live status.
        status = declared if found else ("MISSING_EVIDENCE" if declared in {"DOCUMENTED", "FOUNDATION_PRESENT"} else declared)
        rows.append({
            "workstream": name,
            "status": status,
            "meaning": LABELS.get(status, "Artifact not found; status remains unverified"),
            "artifact": relative,
            "found_at": found,
        })

    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1

    return {
        "board": "Advait CEO Control Board",
        "board_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY_LOCAL_ARTIFACT_SCAN",
        "live_status": "NOT_CLAIMED",
        "phone_deployment": "PENDING",
        "24_hour_soak": "NOT_RUN_OR_NOT_EVIDENCED",
        "revenue_status": "UNVERIFIED; do not infer income",
        "roots_scanned": [str(root.resolve()) for root in roots],
        "summary": counts,
        "workstreams": rows,
        "control_rules": [
            "No payment, withdrawal, transfer, purchase, subscription, or paid API action.",
            "No customer outreach, bid submission, contract signature, or publishing.",
            "Missing artifacts remain pending; filenames alone do not prove successful operation.",
            "24-hour live status requires target-device logs spanning at least 24 hours plus integrity checks.",
            "Owner approval and independent evidence verification must be supplied by trusted external providers.",
        ],
    }


def render_markdown(board: dict) -> str:
    lines = [
        "# Advait CEO Control Board",
        "",
        f"- Generated (UTC): {board['generated_at_utc']}",
        f"- Mode: `{board['mode']}`",
        f"- Production live: **{board['live_status']}**",
        f"- Phone deployment: **{board['phone_deployment']}**",
        f"- 24-hour soak: **{board['24_hour_soak']}**",
        f"- Revenue: **{board['revenue_status']}**",
        "",
        "## Workstream status",
        "",
        "| Workstream | Status | Meaning | Artifact |",
        "|---|---|---|---|",
    ]
    for row in board["workstreams"]:
        lines.append(f"| {row['workstream']} | `{row['status']}` | {row['meaning']} | `{row['artifact']}` |")
    lines += ["", "## Control rules", ""]
    lines += [f"- {rule}" for rule in board["control_rules"]]
    lines += ["", "## Important", "", "This is a local artifact-status board, not a running autonomous agent or a real-time cloud dashboard.", ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a read-only Advait CEO status board")
    parser.add_argument("--root", action="append", required=True, help="Repository checkout root; repeat for multiple repositories")
    parser.add_argument("--output-dir", default="reports/ceo-board")
    args = parser.parse_args(argv)
    roots = [Path(item) for item in args.root]
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    board = build_board(roots)
    (output / "ceo_control_board.json").write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "CEO_CONTROL_BOARD.md").write_text(render_markdown(board), encoding="utf-8")
    print(json.dumps({"generated": True, "output_dir": str(output), "summary": board["summary"], "live_status": board["live_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
