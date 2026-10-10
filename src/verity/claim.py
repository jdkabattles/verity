"""A claim is invalid unless cited evidence states the claim."""

from __future__ import annotations

import re
from typing import Any

from .ledger import Ledger

STOP = {
    "the", "a", "an", "that", "this", "with", "from", "and", "or", "for",
    "was", "were", "has", "have", "been", "is", "are", "of", "to", "in",
    "on", "it", "its", "be", "by", "at", "as",
}


def assert_evidenced(ledger: Ledger, evidence_ids: list[int], statement: str) -> dict[str, Any]:
    if not statement.strip():
        raise ValueError("empty statement")
    if not evidence_ids:
        raise ValueError("claim requires at least one evidence id")
    entries = ledger.read()
    known = {e.index for e in entries}
    missing = [i for i in evidence_ids if i not in known]
    if missing:
        raise ValueError(f"unknown evidence ids: {missing}")
    cited = [entries[i] for i in evidence_ids]
    kinds = {e.payload.get("kind") for e in cited}
    if "observation" not in kinds and "tool_result" not in kinds:
        raise ValueError("claim must cite an observation or tool_result")
    words = _content_words(statement)
    if not words:
        raise ValueError("statement has no content words")
    blob = " ".join(w for e in cited for w in _content_words(_payload_text(e.payload)))
    absent = [w for w in words if w not in blob.split()]
    if absent:
        raise ValueError(f"evidence does not state the claim; missing: {absent}")
    return {"kind": "claim", "statement": statement, "evidence": evidence_ids}


def _content_words(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if len(t) >= 4 and t not in STOP]


def _payload_text(payload: dict[str, Any]) -> str:
    parts = []
    for value in payload.values():
        if isinstance(value, str):
            parts.append(value)
    return " ".join(parts)
