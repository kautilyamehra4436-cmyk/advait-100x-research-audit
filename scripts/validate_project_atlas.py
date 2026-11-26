"""Validate the checked-in cross-repository Advait context pack.

This is a deterministic integrity/scope check, not autonomous reasoning or source-code audit.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "advait_project_atlas.json"

def validate():
    data = json.loads(ATLAS.read_text(encoding="utf-8"))
    repos = data.get("repositories", [])
    modules = data.get("core_modules", [])
    required = {
        "owner_authority", "hard_zero_spend", "risk_taxonomy",
        "authenticated_exact_action_verifier", "independent_evidence_verifier",
        "license_and_security_review", "rollback", "reproducible_tests",
    }
    assert data.get("snapshot_date") == "2026-11-26"
    assert data.get("inventory", {}).get("recursive_tree_entries") == 132
    assert data.get("inventory", {}).get("truncated") is False
    assert len(repos) == 4
    assert len({r["name"] for r in repos}) == 4
    assert all(len(r["main_sha"]) == 40 for r in repos)
    assert len(modules) >= 10
    assert required.issubset(set(data.get("required_gates", [])))
    assert data.get("review_status") == "PENDING_CONNECTED_REASONING_RUNTIME"
    assert len(data.get("reading_order", [])) >= 15
    return {
        "result": "PASS",
        "repositories": len(repos),
        "modules": len(modules),
        "required_gates": len(required),
        "inventory_entries": data["inventory"]["recursive_tree_entries"],
        "review_status": data["review_status"],
        "scope": "static atlas integrity only; not source audit, LLM reasoning, Android or production validation",
    }

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
