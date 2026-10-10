# Verity

An append-only evidence ledger for agent runs.

Agents fail in production because a fluent answer is not a proof. Verity makes the run a chain: every goal, tool call, tool result, and observation is hashed to the previous line. A claim is rejected unless cited evidence supports it. A passing test result supports a pass claim. An unrelated observation does not. Tamper a line and `verity verify` fails.

```bash
pip install -e .
verity init --run run.jsonl
verity log --run run.jsonl --kind goal --data '{"text":"confirm the suite passed"}'
verity log --run run.jsonl --kind observation --data '{"text":"3 passed, 0 failed"}'
verity claim --run run.jsonl --statement "the suite passed" --evidence 1
verity verify --run run.jsonl
verity check --run run.jsonl --spec spec.json
```

`spec.json`:

```json
{"must_claim": ["the suite passed"]}
```

## Why this exists

Enterprise surveys in 2026 put agent pilots at about 78% and production scale under 15%. The gap is not another chat wrapper. It is evidence, replay, and a check that fails when the chain or the claim is wrong. Verity is that check, local, with no model call in the core.

## Free and paid

| | Free (this repo) | Paid later |
|---|---|---|
| Local append-only ledger | yes | yes |
| Claim must cite evidence | yes | yes |
| Tamper detection | yes | yes |
| Spec check in CI | yes | yes |
| Hosted multi-run ledger, team audit export, retention | no | yes |

Paid is not built. The free core is the product until a hosted ledger has users. Do not star this for a promise. Star it if the check is useful.

## Install on Termux

The error `neither setup.py nor pyproject.toml found` means the command ran in home, not in this repo.

```bash
pkg install python git
cd ~
git clone https://github.com/jdkabattles/verity.git
cd verity
pip install -e .
verity init --run run.jsonl
verity log --run run.jsonl --kind goal --data '{"text":"confirm the suite passed"}'
verity log --run run.jsonl --kind observation --data '{"text":"3 passed, 0 failed"}'
verity claim --run run.jsonl --statement "the suite passed" --evidence 1
verity verify --run run.jsonl
printf '%s\n' '{"must_claim":["the suite passed"]}' > spec.json
verity check --run run.jsonl --spec spec.json
```

`verity` is on PATH only after `pip install -e .` succeeds inside the cloned directory.

## How to use

Verity does not run your tests. You or an agent run them. Verity records the result and refuses a claim the result does not support.

```bash
pip install -e .
verity init --run verity.jsonl
verity log --run verity.jsonl --kind goal --data '{"text":"run the tests and report the real result"}'
# run the real suite, then log what it printed
verity log --run verity.jsonl --kind tool_result --data '{"text":"9 passed, 0 failed"}'
verity claim --run verity.jsonl --statement "the bot tests passed" --evidence 1
verity verify --run verity.jsonl
printf '%s\n' '{"must_claim":["the bot tests passed"]}' > spec.json
verity check --run verity.jsonl --spec spec.json
```

`9 passed, 0 failed` supports a pass claim. `binary found` does not. `verity verify` fails if any line was edited after it was written.

### With Hermes on Termux

```bash
mkdir -p $HOME/.hermes/skills/verity
cp skills/verity/SKILL.md $HOME/.hermes/skills/verity/SKILL.md
hermes chat -q "Use the verity skill. Run the tests, log the real output, claim only what the output supports, then verify."
```

### What a passing check means

`verify` OK means the chain is intact. `check` passed means the required claim is present and cites supporting evidence. It does not mean the next run will pass. Run it again after the next change.
