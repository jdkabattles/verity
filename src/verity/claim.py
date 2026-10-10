"""A claim is invalid unless it cites evidence already in the ledger."""

from __future__ import annotations

from typing import Any

from .ledger import Ledger


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
    kinds = {entries[i].payload.get("kind") for i in evidence_ids}
    if "observation" not in kinds and "tool_result" not in kinds:
        raise ValueError("claim must cite an observation or tool_result")
    return {"kind": "claim", "statement": statement, "evidence": evidence_ids}
