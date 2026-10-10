---
name: verity
description: Log Hermes work to a Verity evidence ledger and reject claims that cite no evidence.
version: 0.1.0
author: jdkabattles
license: Apache-2.0
metadata:
  hermes:
    tags: [verity, evidence, ledger, audit]
    requires_tools: [terminal]
---

# Verity

Use this skill when the user asks to prove a run, keep an evidence ledger, or check a claim.

Verity is a local CLI. It does not call a model. The ledger file is `~/verity/run.jsonl` unless the user names another path.

## Procedure

1. Resolve the binary with `terminal`: `command -v verity`. If that fails, use `/data/data/com.termux/files/usr/bin/verity`.
2. Before tool work, append a goal:
   `verity log --run ~/verity/run.jsonl --kind goal --data '{"text":"<goal>"}'`
3. After each tool result or observation, append it:
   `verity log --run ~/verity/run.jsonl --kind tool_result --data '{"text":"<short result>"}'`
   or `--kind observation`.
4. A claim is allowed only with evidence indexes from step 3:
   `verity claim --run ~/verity/run.jsonl --statement "<claim>" --evidence <id>`
5. Finish with `verity verify --run ~/verity/run.jsonl`.
6. If a spec exists, run `verity check --run ~/verity/run.jsonl --spec ~/verity/spec.json`.

## Rules

- Do not claim success without a `verity claim` that cites a `tool_result` or `observation`.
- If `verity` is missing, stop and tell the user to run `cd ~/verity && pip install -e .`.
- Do not put secrets in the ledger.
