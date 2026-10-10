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
    obs = ledger.append({"kind": "observation", "text": "the suite passed, 3 passed 0 failed"})
    payload = assert_evidenced(ledger, [obs.index], "the suite passed")
    assert payload["evidence"] == [obs.index]
    weak = ledger.append({"kind": "observation", "text": "binary found"})
    try:
        assert_evidenced(ledger, [weak.index], "the suite passed")
        raise AssertionError("ungrounded claim should fail")
    except ValueError as exc:
        assert "missing" in str(exc)


def test_score_against_spec(tmp_path: Path):
    ledger = Ledger(tmp_path / "run.jsonl")
    ledger.append({"kind": "goal", "text": "confirm tests"})
    obs = ledger.append({"kind": "observation", "text": "3 passed"})
    ledger.append({"kind": "claim", "statement": "tests passed", "evidence": [obs.index]})
    result = score(ledger, {"must_claim": ["tests passed"]})
    assert result["passed"] is True
    assert result["chain_ok"] is True
