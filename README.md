# Verity

An append-only evidence ledger for agent runs.

Agents fail in production because a fluent answer is not a proof. Verity makes the run a chain: every goal, tool call, tool result, and observation is hashed to the previous line. A claim is rejected unless it cites an observation or a tool result already in the chain. Tamper a line and `verity verify` fails.

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

## Honest ceiling

This is not a Nobel. A Nobel is years of peer-reviewed work. This is not multimillions. GitLab, Grafana, ClickHouse, and Temporal reached those numbers with teams, years, and a paid cloud on top of a free core. A new repo with zero users makes $0. The path that has worked is: free core people run, then paid hosting and audit export once the core is in real CI. Conversion from free to paid on open source is typically 0.5–3%.

## Stars

Stars follow a thing people can run in one command, a README that shows the command, and a 48-hour launch: Show HN (Tuesday–Thursday, 7–10am PT), one relevant subreddit, one X post with a 30-second demo. Respond to every comment for 24 hours. GitHub Trending reacts to velocity, not to a trickle.
