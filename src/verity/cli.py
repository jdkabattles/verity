"""verity init | log | claim | check | verify."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .claim import assert_evidenced
from .eval import score
from .ledger import Ledger


def _ledger(path: str) -> Ledger:
    return Ledger(path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="verity")
    sub = parser.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init")
    init.add_argument("--run", default="verity.jsonl")

    log = sub.add_parser("log")
    log.add_argument("--run", default="verity.jsonl")
    log.add_argument("--kind", required=True, choices=["goal", "tool_call", "tool_result", "observation"])
    log.add_argument("--data", required=True, help="JSON object")

    claim = sub.add_parser("claim")
    claim.add_argument("--run", default="verity.jsonl")
    claim.add_argument("--statement", required=True)
    claim.add_argument("--evidence", required=True, help="Comma-separated entry indexes")

    check = sub.add_parser("check")
    check.add_argument("--run", default="verity.jsonl")
    check.add_argument("--spec", required=True)

    verify = sub.add_parser("verify")
    verify.add_argument("--run", default="verity.jsonl")

    args = parser.parse_args()
    if args.cmd == "init":
        path = Path(args.run)
        if path.exists():
            print(f"exists {path}")
            return
        Ledger(path)  # touch on first append
        path.write_text("")
        print(f"init {path}")
        return
    ledger = _ledger(args.run)
    if args.cmd == "log":
        entry = ledger.append({"kind": args.kind, **json.loads(args.data)})
        print(f"index={entry.index} hash={entry.hash[:12]}")
        return
    if args.cmd == "claim":
        ids = [int(x) for x in args.evidence.split(",") if x]
        payload = assert_evidenced(ledger, ids, args.statement)
        entry = ledger.append(payload)
        print(f"index={entry.index} hash={entry.hash[:12]}")
        return
    if args.cmd == "verify":
        errors = ledger.verify()
        if errors:
            print("FAIL")
            for err in errors:
                print(f"- {err}")
            sys.exit(1)
        print(f"OK entries={len(ledger.read())}")
        return
    result = score(ledger, json.loads(Path(args.spec).read_text()))
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
