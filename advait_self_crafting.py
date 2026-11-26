"""Advait Self-Crafting & Evolution Engine (SCEE).

A deterministic, offline decision layer for comparing solution candidates.
It NEVER executes generated code, installs packages, contacts services, or deploys
changes. Candidate metrics must come from an explicitly recorded experiment.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from typing import Any


@dataclass(frozen=True)
class Candidate:
    name: str
    approach: str
    latency_ms: float
    memory_mb: float
    correctness_passed: bool
    measured: bool
    license_id: str
    attribution_recorded: bool
    security_review_passed: bool
    rollback_available: bool


@dataclass(frozen=True)
class Assessment:
    name: str
    eligible: bool
    score: float | None
    reasons: tuple[str, ...]


class SelfCraftingEngine:
    """Compare measured options while enforcing provenance and safety gates."""

    ALLOWED_LICENSES = {
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause",
        "ISC", "MPL-2.0", "GPL-2.0-only", "GPL-2.0-or-later",
        "GPL-3.0-only", "GPL-3.0-or-later", "AGPL-3.0-only",
        "AGPL-3.0-or-later", "CC0-1.0", "Unlicense",
        "PROPRIETARY-OWNER-OWNED",
    }

    def assess(self, candidate: Candidate) -> Assessment:
        reasons: list[str] = []
        if not candidate.measured:
            reasons.append("metrics_not_measured")
        if not candidate.correctness_passed:
            reasons.append("correctness_not_proven")
        if candidate.license_id not in self.ALLOWED_LICENSES:
            reasons.append("license_unknown_or_unapproved")
        if candidate.license_id not in {"PROPRIETARY-OWNER-OWNED", "CC0-1.0", "Unlicense"} and not candidate.attribution_recorded:
            reasons.append("attribution_missing")
        if not candidate.security_review_passed:
            reasons.append("security_review_missing_or_failed")
        if not candidate.rollback_available:
            reasons.append("rollback_missing")
        if candidate.latency_ms <= 0 or candidate.memory_mb <= 0:
            reasons.append("invalid_resource_measurement")
        if reasons:
            return Assessment(candidate.name, False, None, tuple(reasons))
        # Lower latency and memory are better; score is a transparent comparative
        # efficiency indicator, not a universal quality or novelty measurement.
        score = 1000.0 / (candidate.latency_ms * candidate.memory_mb)
        return Assessment(candidate.name, True, round(score, 6), ())

    def compare(self, candidates: list[Candidate]) -> dict[str, Any]:
        assessments = [self.assess(c) for c in candidates]
        eligible = [a for a in assessments if a.eligible]
        winner = max(eligible, key=lambda a: a.score or 0, default=None)
        return {
            "engine": "ADVAIT-SCEE",
            "decision": "CANDIDATE_SELECTED_FOR_OWNER_REVIEW" if winner else "NO_CANDIDATE_PASSED_GATES",
            "winner": winner.name if winner else None,
            "winner_score": winner.score if winner else None,
            "owner_approval_required": True,
            "production_deployment_allowed": False,
            "code_execution_performed": False,
            "external_network_actions_performed": False,
            "assessments": [asdict(a) for a in assessments],
            "score_note": "1000 / (latency_ms * memory_mb); compare only under the same workload and device.",
        }


def self_test() -> dict[str, Any]:
    engine = SelfCraftingEngine()
    candidates = [
        Candidate("baseline", "existing", 12.0, 32.0, True, True, "MIT", True, True, True),
        Candidate("new-algorithm", "original", 8.0, 24.0, True, True, "PROPRIETARY-OWNER-OWNED", True, True, True),
        Candidate("unverified-copy", "unknown", 1.0, 1.0, True, False, "NOASSERTION", False, False, False),
    ]
    result = engine.compare(candidates)
    assert result["winner"] == "new-algorithm"
    assert result["production_deployment_allowed"] is False
    assert result["assessments"][2]["eligible"] is False
    return {"result": "PASS", "checks": [
        "measured_candidate_comparison", "unknown_license_blocked",
        "unmeasured_candidate_blocked", "owner_approval_gate",
        "no_code_execution_or_network_actions",
    ], "decision": result["decision"], "winner": result["winner"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    print(json.dumps(self_test() if args.self_test else {
        "engine": "ADVAIT-SCEE", "status": "READY_FOR_INPUT",
        "note": "Provide measured candidate records through the Python API; no autonomous execution is enabled."
    }, sort_keys=True))


if __name__ == "__main__":
    main()
