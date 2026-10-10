"""Append-only hashed ledger. A later line cannot rewrite an earlier one."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(prev: str, payload: dict[str, Any]) -> str:
    return hashlib.sha256(f"{prev}\n{_canon(payload)}".encode()).hexdigest()


@dataclass
class Entry:
    index: int
    prev: str
    hash: str
    payload: dict[str, Any]


class Ledger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, payload: dict[str, Any]) -> Entry:
        entries = self.read()
        prev = entries[-1].hash if entries else "0" * 64
        digest = _hash(prev, payload)
        entry = Entry(index=len(entries), prev=prev, hash=digest, payload=payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as handle:
            handle.write(_canon({"index": entry.index, "prev": prev, "hash": digest, "payload": payload}) + "\n")
        return entry

    def read(self) -> list[Entry]:
        if not self.path.exists():
            return []
        entries: list[Entry] = []
        for line in self.path.read_text().splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            entries.append(Entry(raw["index"], raw["prev"], raw["hash"], raw["payload"]))
        return entries

    def verify(self) -> list[str]:
        errors: list[str] = []
        prev = "0" * 64
        for entry in self.read():
            expect = _hash(prev, entry.payload)
            if entry.prev != prev:
                errors.append(f"index {entry.index}: prev mismatch")
            if entry.hash != expect:
                errors.append(f"index {entry.index}: hash mismatch")
            prev = entry.hash
        return errors
