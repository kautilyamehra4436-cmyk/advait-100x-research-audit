"""Open-source maker, tool-purpose, and customer-fit intelligence.

Offline analysis only. This module analyzes metadata/readme text supplied by an
authorized collector; it does not crawl, contact maintainers, install tools, or
claim that a project is safe merely because it is popular.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable

TOOL_PURPOSES = {
    "automation": ("automation", "workflow", "orchestration", "task runner", "rpa"),
    "developer_tools": ("developer tool", "sdk", "api", "debugger", "compiler", "ide"),
    "data_and_analytics": ("analytics", "database", "etl", "data pipeline", "visualization"),
    "ai_and_machine_learning": ("machine learning", "llm", "inference", "model", "ai agent"),
    "design_and_content": ("design", "image editor", "video editor", "content", "graphics"),
    "business_operations": ("crm", "inventory", "billing", "accounting", "erp", "booking"),
    "security_and_privacy": ("security", "privacy", "encryption", "scanner", "authentication"),
    "education_and_knowledge": ("learning", "education", "documentation", "knowledge base", "course"),
    "communication": ("chat", "messaging", "email", " collaboration", "video conference"),
}

CUSTOMER_NEEDS = {
    "automation": ("manual repetitive work", "workflow automation", "task orchestration"),
    "developer_tools": ("software development", "api integration", "debugging"),
    "data_and_analytics": ("reporting", "data cleanup", "business analytics"),
    "ai_and_machine_learning": ("document intelligence", "chatbot", "model inference"),
    "design_and_content": ("graphic design", "video editing", "content production"),
    "business_operations": ("customer management", "inventory management", "booking operations"),
    "security_and_privacy": ("security review", "privacy controls", "access management"),
    "education_and_knowledge": ("training", "knowledge management", "learning materials"),
    "communication": ("team communication", "customer messaging", "remote collaboration"),
}


@dataclass
class OpenSourceProject:
    owner: str
    repo: str
    description: str = ""
    readme_excerpt: str = ""
    topics: tuple[str, ...] = ()
    license_spdx: str = ""
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    updated_at: str = ""
    repository_url: str = ""
    release_url: str = ""
    latest_release: str = ""


@dataclass
class CustomerNeed:
    need_id: str
    customer_type: str
    need_description: str
    source_reference: str
    verified: bool = False


def infer_purpose(project: OpenSourceProject) -> str:
    text = " ".join((project.description, project.readme_excerpt, *project.topics)).lower()
    scores = {
        purpose: sum(1 for term in terms if term in text)
        for purpose, terms in TOOL_PURPOSES.items()
    }
    ranked = sorted(((score, purpose) for purpose, score in scores.items() if score), reverse=True)
    if not ranked:
        return "unknown"
    if len(ranked) > 1 and ranked[0][0] == ranked[1][0]:
        return "unknown"
    return ranked[0][1]


def maintenance_signal(updated_at: str, now: datetime | None = None) -> str:
    if not updated_at:
        return "UNKNOWN"
    try:
        updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        current = now or datetime.now(timezone.utc)
        days = (current - updated).days
    except (ValueError, TypeError):
        return "UNKNOWN"
    if days < 0:
        return "UNKNOWN"
    if days <= 180:
        return "RECENT_ACTIVITY"
    if days <= 365:
        return "AGING_ACTIVITY"
    return "STALE_ACTIVITY"


def assess_project(project: OpenSourceProject) -> dict:
    purpose = infer_purpose(project)
    signals = []
    if not project.license_spdx:
        signals.append("LICENSE_NOT_CONFIRMED")
    if not project.repository_url:
        signals.append("REPOSITORY_URL_MISSING")
    if maintenance_signal(project.updated_at) in ("STALE_ACTIVITY", "UNKNOWN"):
        signals.append("MAINTENANCE_REQUIRES_REVIEW")
    if not project.readme_excerpt.strip():
        signals.append("PURPOSE_EVIDENCE_INCOMPLETE")
    return {
        "purpose": purpose,
        "customer_need_examples": list(CUSTOMER_NEEDS.get(purpose, ())),
        "maintenance_signal": maintenance_signal(project.updated_at),
        "license_status": "DECLARED" if project.license_spdx else "NOT_CONFIRMED",
        "review_signals": signals,
        "suitability": "REQUIRES_HUMAN_REVIEW",
        "why_built": (
            project.description.strip()
            or (project.readme_excerpt.strip()[:500] if project.readme_excerpt else "NOT_ESTABLISHED_FROM_AVAILABLE_EVIDENCE")
        ),
    }


def match_project_to_customer(project: OpenSourceProject, need: CustomerNeed) -> dict:
    assessment = assess_project(project)
    purpose = assessment["purpose"]
    need_text = need.need_description.lower()
    expected = CUSTOMER_NEEDS.get(purpose, ())
    overlap = [phrase for phrase in expected if any(word in need_text for word in phrase.split() if len(word) > 3)]
    if purpose == "unknown" or not overlap:
        fit = "UNCONFIRMED"
    elif need.verified:
        fit = "POTENTIAL_MATCH_REQUIRES_TECHNICAL_VALIDATION"
    else:
        fit = "UNVERIFIED_NEED"
    return {
        "project": f"{project.owner}/{project.repo}",
        "project_url": project.repository_url,
        "maintainer_or_maker": project.owner,
        "customer_need_id": need.need_id,
        "customer_type": need.customer_type,
        "need_description": need.need_description,
        "fit": fit,
        "overlap_terms": overlap,
        "license_status": assessment["license_status"],
        "review_signals": assessment["review_signals"],
        "release_url": project.release_url,
        "next_step": "Review project purpose, license, security, compatibility, and customer consent before recommending or deploying.",
    }


def build_open_source_report(
    projects: Iterable[OpenSourceProject],
    customer_needs: Iterable[CustomerNeed] = (),
) -> dict:
    project_rows = []
    purpose_counts = Counter()
    matches = []
    for project in projects:
        assessment = assess_project(project)
        project_rows.append({
            "owner": project.owner,
            "repo": project.repo,
            "description": project.description,
            "repository_url": project.repository_url,
            "topics": list(project.topics),
            "license_spdx": project.license_spdx or "UNKNOWN",
            "stars": project.stars,
            "forks": project.forks,
            "latest_release": project.latest_release,
            "release_url": project.release_url,
            **assessment,
        })
        purpose_counts[assessment["purpose"]] += 1
        for need in customer_needs:
            matches.append(match_project_to_customer(project, need))
    return {
        "report": "Advait Open-Source Maker and Customer Intelligence",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "OFFLINE_ANALYSIS_ONLY",
        "projects_analyzed": len(project_rows),
        "purpose_counts": dict(sorted(purpose_counts.items())),
        "most_common_tool_purposes": purpose_counts.most_common(5),
        "projects": project_rows,
        "maker_customer_matches": matches,
        "guardrails": [
            "Repository metadata and README text are evidence inputs, not proof of safety or quality.",
            "Stars and forks are popularity signals only, never trust or compatibility scores.",
            "A missing license is NOT treated as permission to use, modify, redistribute, or sell.",
            "A purpose or customer match is a hypothesis until tested against the real need.",
            "Do not contact maintainers or customers automatically; obtain owner approval.",
            "Do not install or execute untrusted code as part of discovery.",
            "Review license, dependencies, security posture, maintenance, data handling, and fit before recommending a tool.",
        ],
    }
