import json
from pathlib import Path

from verity.claim import assert_evidenced
from verity.eval import score
from verity.ledger import Ledger


def test_chain_detects_tamper(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    ledger = Ledger(path)
    ledger.append({"kind": "goal", "text": "ship"})
    ledger.append({"kind": "observation", "text": "tests passed"})
    assert ledger.verify() == []
    lines = path.read_text().splitlines()
    forged = json.loads(lines[0])
    forged["payload"]["text"] = "lie"
    lines[0] = json.dumps(forged)
    path.write_text("\n".join(lines) + "\n")
    assert ledger.verify()


def test_claim_requires_evidence(tmp_path: Path):
    ledger = Ledger(tmp_path / "run.jsonl")
    ledger.append({"kind": "goal", "text": "ship"})
    try:
        assert_evidenced(ledger, [], "done")
        raise AssertionError("empty evidence should fail")
    except ValueError:
        pass
    try:
        assert_evidenced(ledger, [0], "done")
        raise AssertionError("goal-only evidence should fail")
    except ValueError:
        pass
    payload = assert_evidenced(
        ledger,
        [ledger.append({"kind": "tool_result", "ok": True}).index],
        "the suite passed",
    )
    assert payload["evidence"]


def test_score_against_spec(tmp_path: Path):
    ledger = Ledger(tmp_path / "run.jsonl")
    ledger.append({"kind": "goal", "text": "confirm tests"})
    obs = ledger.append({"kind": "observation", "text": "3 passed"})
    ledger.append({"kind": "claim", "statement": "tests passed", "evidence": [obs.index]})
    result = score(ledger, {"must_claim": ["tests passed"]})
    assert result["passed"] is True
    assert result["chain_ok"] is True
