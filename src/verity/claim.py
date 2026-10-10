"""A claim is invalid unless cited evidence supports the statement."""

from __future__ import annotations

import re
from typing import Any

from .ledger import Ledger

STOP = {
    "the", "a", "an", "that", "this", "with", "from", "and", "or", "for",
    "was", "were", "has", "have", "been", "is", "are", "of", "to", "in",
    "on", "it", "its", "be", "by", "at", "as",
}
PASS_WORDS = {"pass", "passed", "passing", "ok", "success", "succeeded", "green"}
FAIL_WORDS = {"fail", "failed", "failing", "error", "broken"}


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
    evidence_text = " ".join(_payload_text(e.payload) for e in cited)
    if _supports(statement, evidence_text):
        return {"kind": "claim", "statement": statement, "evidence": evidence_ids}
    raise ValueError(
        "evidence does not support the claim. "
        f"claim={statement!r} evidence={evidence_text!r}"
    )


def _supports(statement: str, evidence: str) -> bool:
    claim_words = _content_words(statement)
    evidence_words = set(_content_words(evidence))
    if not claim_words:
        return False
    # Direct overlap: every content word, or a stem of it, is in the evidence.
    if all(_present(w, evidence_words) for w in claim_words):
        return True
    # A pass claim is supported by a passing result that is not a failure.
    if _is_pass_claim(claim_words) and _is_pass_result(evidence) and not _is_fail_result(evidence):
        return True
    return False


def _is_pass_claim(words: list[str]) -> bool:
    return any(w in PASS_WORDS or w.startswith("pass") for w in words)


def _is_pass_result(text: str) -> bool:
    low = text.lower()
    if re.search(r"\b[1-9]\d*\s+passed\b", low):
        return True
    if re.search(r"\bpassed\b", low) and not re.search(r"\b[1-9]\d*\s+failed\b", low):
        return True
    return "exit 0" in low or "exit code 0" in low


def _is_fail_result(text: str) -> bool:
    low = text.lower()
    if re.search(r"\b[1-9]\d*\s+failed\b", low):
        return True
    if re.search(r"\b0\s+failed\b", low):
        return False
    return any(w in FAIL_WORDS for w in _content_words(low))


def _present(word: str, evidence_words: set[str]) -> bool:
    if word in evidence_words:
        return True
    stem = word[:5]
    return any(other.startswith(stem) or word.startswith(other[:5]) for other in evidence_words if len(other) >= 4)


def _content_words(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if len(t) >= 4 and t not in STOP]


def _payload_text(payload: dict[str, Any]) -> str:
    return " ".join(v for v in payload.values() if isinstance(v, str))
