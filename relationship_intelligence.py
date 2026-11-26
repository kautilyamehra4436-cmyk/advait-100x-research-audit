"""Owner-aligned relationship and opportunity intelligence (offline, fail-closed).

This module scores opportunities against an explicit owner profile, classifies work
into a transparent taxonomy, tracks unknown work separately, and produces reports.
It does not search the internet, contact people, store raw contact details, or execute
commercial/financial actions. Feed it opportunities collected by an authorized source.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable

WORK_CATEGORIES = {
    "digital_operations": ("website updates", "data entry", "catalog", "spreadsheet", "admin"),
    "content_and_design": ("content", "social media", "graphic", "design", "video", "caption"),
    "software_and_automation": ("automation", "python", "api", "software", "integration", "bug"),
    "research_and_analysis": ("research", "market research", "analysis", "competitor", "report"),
    "customer_support": ("customer support", "support", "helpdesk", "chat", "customer service"),
    "local_business_support": ("local business", "listing", "menu", "booking", "inventory", "shop"),
    "education_and_training": ("tutoring", "training", "lesson", "course", "education"),
}

DEFAULT_OWNER_PROFILE = {
    "profile_version": "1.0",
    "mission": "build useful relationships and identify legitimate opportunities before monetization",
    "priority_categories": ["digital_operations", "research_and_analysis", "local_business_support", "software_and_automation"],
    "avoid_categories": ["regulated_finance", "deceptive_marketing", "spam", "illegal_or_unsafe"],
    "constraints": {
        "zero_spend": True,
        "phone_first": True,
        "no_paid_hosting": True,
        "no_unapproved_outreach": True,
        "no_money_movement": True,
        "owner_approval_for_commitments": True,
    },
    "scoring_weights": {
        "owner_fit": 0.30,
        "verified_need": 0.25,
        "usefulness": 0.20,
        "feasibility": 0.15,
        "relationship_value": 0.10,
    },
}

@dataclass
class Opportunity:
    title: str
    description: str
    source: str
    category: str = "unknown"
    verified_need: int = 0
    usefulness: int = 0
    feasibility: int = 0
    relationship_value: int = 0
    owner_fit: int = 0
    budget_note: str = "unknown"
    evidence: str = ""
    status: str = "DISCOVERED"


def classify_work(title: str, description: str = "") -> str:
    text = f"{title} {description}".lower()
    matches = []
    for category, keywords in WORK_CATEGORIES.items():
        score = sum(1 for word in keywords if word in text)
        if score:
            matches.append((score, category))
    if not matches:
        return "unknown"
    matches.sort(reverse=True)
    # Ambiguous matches remain unknown rather than being force-classified.
    if len(matches) > 1 and matches[0][0] == matches[1][0]:
        return "unknown"
    return matches[0][1]


def _bounded_score(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 5:
        raise ValueError("all rating fields must be integers from 0 to 5")
    return value


def score_opportunity(item: Opportunity, owner_profile: dict | None = None) -> dict:
    profile = owner_profile or DEFAULT_OWNER_PROFILE
    weights = profile.get("scoring_weights", DEFAULT_OWNER_PROFILE["scoring_weights"])
    if set(weights) != set(DEFAULT_OWNER_PROFILE["scoring_weights"]):
        raise ValueError("scoring weights must define the complete approved score set")
    if any(not isinstance(v, (int, float)) or v < 0 for v in weights.values()):
        raise ValueError("weights must be non-negative numbers")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("scoring weights must sum to 1.0")

    category = item.category if item.category != "unknown" else classify_work(item.title, item.description)
    if category in profile.get("avoid_categories", []):
        return {"category": category, "score": 0.0, "decision": "REJECTED_BY_POLICY", "reason": "category is on owner avoid-list"}
    ratings = {
        "owner_fit": _bounded_score(item.owner_fit),
        "verified_need": _bounded_score(item.verified_need),
        "usefulness": _bounded_score(item.usefulness),
        "feasibility": _bounded_score(item.feasibility),
        "relationship_value": _bounded_score(item.relationship_value),
    }
    if not item.source.strip():
        return {"category": category, "score": 0.0, "decision": "NEEDS_EVIDENCE", "reason": "source is required"}
    if not item.evidence.strip() or item.verified_need == 0:
        return {"category": category, "score": 0.0, "decision": "NEEDS_EVIDENCE", "reason": "evidence and verified need are required"}
    score = round(sum((ratings[key] / 5) * float(weights[key]) for key in weights) * 100, 2)
    if category == "unknown":
        decision = "OWNER_REVIEW_UNKNOWN_WORK"
    elif score >= 75:
        decision = "HIGH_PRIORITY_REVIEW"
    elif score >= 50:
        decision = "NORMAL_PRIORITY_REVIEW"
    else:
        decision = "LOW_PRIORITY_REVIEW"
    return {"category": category, "score": score, "decision": decision, "reason": "rank only; owner approval required before commitments"}


def build_opportunity_report(items: Iterable[Opportunity], owner_profile: dict | None = None) -> dict:
    rows = []
    category_counts = Counter()
    unknown_items = []
    decisions = Counter()
    for item in items:
        result = score_opportunity(item, owner_profile)
        row = {**asdict(item), **result}
        rows.append(row)
        category_counts[result["category"]] += 1
        decisions[result["decision"]] += 1
        if result["category"] == "unknown":
            unknown_items.append({"title": item.title, "description": item.description, "decision": result["decision"]})
    ranked = sorted(rows, key=lambda row: row["score"], reverse=True)
    return {
        "report": "Advait Owner-Aligned Relationship & Opportunity Report",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "OFFLINE_ANALYSIS_ONLY",
        "owner_profile_version": (owner_profile or DEFAULT_OWNER_PROFILE).get("profile_version", "custom"),
        "total_opportunities": len(rows),
        "category_counts": dict(sorted(category_counts.items())),
        "most_frequent_work": category_counts.most_common(5),
        "unknown_work_count": len(unknown_items),
        "unknown_work": unknown_items,
        "decision_counts": dict(sorted(decisions.items())),
        "ranked_opportunities": ranked,
        "next_focus": [name for name, _ in category_counts.most_common(3) if name != "unknown"],
        "guardrails": [
            "No customer outreach or publishing is performed by this module.",
            "No raw phone numbers, email addresses, credentials, or payment data are stored here.",
            "No budget is treated as confirmed unless the source explicitly verifies it.",
            "Scores are recommendations, not authority to accept work or make commitments.",
            "Unknown work is preserved for owner review, never silently discarded.",
        ],
    }
