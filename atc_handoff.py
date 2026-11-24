"""Strict, non-executing ATC -> Advait 100x handoff contract v1.

The handoff transports a reviewed candidate task. It never authorizes execution.
High-risk approval must be supplied by an authenticated host-side verifier.
"""
from __future__ import annotations
from hashlib import sha256
import json
from advait_engine import Task, Risk

SCHEMA_VERSION = "advait.task.v1"
REQUIRED = {"schema_version", "task_id", "title", "tool", "action", "payload", "risk", "state", "integrity"}

def _canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def seal(envelope: dict) -> dict:
    body = {k: v for k, v in envelope.items() if k != "integrity"}
    result = dict(body)
    result["integrity"] = sha256(_canonical(body).encode("utf-8")).hexdigest()
    return result

def validate(envelope: dict) -> None:
    if not isinstance(envelope, dict) or set(envelope) != REQUIRED:
        raise ValueError("handoff fields do not match advait.task.v1")
    if envelope["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported handoff schema")
    for key in ("task_id", "title", "tool", "action"):
        if not isinstance(envelope[key], str) or not envelope[key].strip() or len(envelope[key]) > 200:
            raise ValueError(f"invalid {key}")
    if not isinstance(envelope["payload"], dict):
        raise ValueError("payload must be an object")
    if len(_canonical(envelope["payload"]).encode("utf-8")) > 65536:
        raise ValueError("payload exceeds 65536 bytes")
    if envelope["risk"] not in ("low", "high"):
        raise ValueError("invalid risk")
    if envelope["state"] != "REVIEWED_NOT_AUTHORIZED":
        raise ValueError("handoff is not in reviewed-not-authorized state")
    expected = seal({k: v for k, v in envelope.items() if k != "integrity"})["integrity"]
    if not isinstance(envelope["integrity"], str) or envelope["integrity"] != expected:
        raise ValueError("handoff integrity mismatch")

def to_task(envelope: dict) -> Task:
    validate(envelope)
    return Task(task_id=envelope["task_id"], title=envelope["title"],
                tool=envelope["tool"], action=envelope["action"],
                payload=dict(envelope["payload"]),
                risk=Risk(envelope["risk"]))

def from_atc_candidate(*, task_id: str, title: str, tool: str, action: str,
                       payload: dict, risk: str = "low") -> dict:
    """Explicit bridge for a human-reviewed candidate; no ATC plan auto-runs."""
    body = {"schema_version": SCHEMA_VERSION, "task_id": task_id, "title": title,
            "tool": tool, "action": action, "payload": payload, "risk": risk,
            "state": "REVIEWED_NOT_AUTHORIZED"}
    return seal(body)
