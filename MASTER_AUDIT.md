# Advait 100X — Cross-System Audit Master Matrix

**Status:** Partial research baseline; not exhaustive line-by-line. **Date:** 2026-11-23. Observations are not security proofs; proposals remain hypotheses.

## Scope
- ArtCraft Launcher — `storytold/craft-launcher`: catalog, platform selection, install/update.
- LangGraph — `langchain-ai/langgraph`: graph execution/checkpoints.
- mini-SWE-agent — `SWE-agent/mini-swe-agent`: loop, limits, trajectory.
- Browser Use — `browser-use/browser-use`: browser automation.
- OpenHands SDK — `OpenHands/software-agent-sdk`: abstractions; deep retrieval incomplete.
- MCP servers — `modelcontextprotocol/servers`: protocol tools, filesystem permissions.

## Source anchors
- ArtCraft: https://github.com/storytold/craft-launcher ; install: https://github.com/storytold/craft-launcher/blob/main/crates/native/src/install.rs ; HTTP: https://github.com/storytold/craft-launcher/blob/main/crates/native/src/http.rs ; platform: https://github.com/storytold/craft-launcher/blob/main/crates/core/src/platform.rs
- LangGraph: https://github.com/langchain-ai/langgraph ; loop: https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/pregel/_loop.py
- mini-SWE-agent: https://github.com/SWE-agent/mini-swe-agent ; agent: https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py
- Browser Use: https://github.com/browser-use/browser-use ; service: https://github.com/browser-use/browser-use/blob/main/browser_use/agent/service.py
- OpenHands SDK: https://github.com/OpenHands/software-agent-sdk
- MCP: https://github.com/modelcontextprotocol/servers ; filesystem: https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/server.ts

## Capability / limitation / risk / Advait proposal / test matrix
| Area | Observed capability | Limit/risk | Proposed Advait improvement | Acceptance evidence |
|---|---|---|---|---|
| ArtCraft catalog | catalog/release sources | stale/incomplete catalog | provenance/license/freshness registry | reject stale metadata |
| Platform selection | OS/arch selection | compatibility != task quality | capability match + adapter health | unsupported fixture rejected |
| Install/download | installation pipeline | partial side effects/corruption | staging, verify, promote | failed integrity never promotes |
| Integrity | checksum paths | hash doesn't prove publisher | signed provenance + hash policy | untrusted provenance rejected |
| Update recovery | update/install paths | rollback gaps | recovery journal/state machine | interruption simulation |
| LangGraph state | checkpoints/stateful execution | replay duplicates effects | action journal/idempotency/reconcile | crash scenario no duplicate |
| Graph orchestration | graph loop | loops/state complexity | bounded task DAG | step/time caps |
| mini-SWE limits | step/cost/time/error controls | side effects may remain | per-tool/global budgets | budget exhaustion stops |
| Trajectory | records calls/config/cost | secret leakage; log != proof | redacted evidence ledger | redaction/integrity tests |
| Agent execution | model-driven actions | generated actions untrusted | typed tools, policy gate, sandbox | unauthorized action denied |
| Browser automation | observe/action loop | injection/UI ambiguity | observe-act-verify/site policy | hostile page fixture |
| Browser workspace | configurable access | overbroad files/accounts | least privilege, isolated task data | out-of-scope denied |
| OpenHands abstractions | tool/workspace abstractions | deep audit incomplete | adapters + independent policy | adapter contract tests |
| MCP filesystem | roots/read-only schemas | path/symlink edge cases | canonical path confinement | traversal/symlink tests |
| MCP schemas | validated inputs | valid schema != safe action | schema fingerprints/risk review | drift review required |
| Retry behavior | retry/loop patterns | duplicates/amplified errors | classify; idempotency; reconcile | unknown outcome not retried |
| Completion signal | final status/text | false success | independent verifier/evidence | missing evidence unverified |
| Self-evolution | config/checkpoints | unsafe self-approval | proposal→sandbox→review→stage→rollback | policy immutable to candidate |

## Proposed architecture (not validated)
Goal/constraints parser; capability registry; discovery adapters; benchmark harness; bounded planner; owner/policy gate; least-privilege executor; independent verifier; recovery/reconciliation; append-only redacted ledger/checkpoints; mobile-first resource manager; evolution validation with staged rollout/rollback.

## Gaps and truth gate
Pin commits/file hashes; line-numbered audit; inspect security tests/issues/releases; deep OpenHands review. No exhaustive audit, 100X superiority, or global novelty established.

## Local mock tests
10/10 passed in local sandbox (2026-11-23). Tested allowlist, approval required/approved, unknown outcome reconciliation, evidence requirement, step/call caps, ledger tamper/reordering, denied-action record prevention. Not integration tests: no real APIs, Android, performance, signatures, sandbox escape, concurrency, or durable checkpoints.
