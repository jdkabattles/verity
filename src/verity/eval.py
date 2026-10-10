"""Score a finished run against a spec. No model call. Deterministic."""

from __future__ import annotations

from typing import Any

from .ledger import Ledger


def score(ledger: Ledger, spec: dict[str, Any]) -> dict[str, Any]:
    entries = ledger.read()
    claims = [e for e in entries if e.payload.get("kind") == "claim"]
    required = spec.get("must_claim") or []
    texts = [c.payload.get("statement", "") for c in claims]
    hit = [need for need in required if any(need.lower() in t.lower() for t in texts)]
    missing = [need for need in required if need not in hit]
    unverified = ledger.verify()
    evidenced = all(c.payload.get("evidence") for c in claims)
    passed = not unverified and not missing and evidenced and bool(claims or not required)
    return {
        "passed": passed,
        "claims": len(claims),
        "required_hit": hit,
        "required_missing": missing,
        "chain_ok": not unverified,
        "chain_errors": unverified,
    }
