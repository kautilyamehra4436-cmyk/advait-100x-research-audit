# Source Audit Addendum — pinned snapshots, evidence and test results

Research date: 2026-11-23. Commit IDs pin reviewed snapshots; URLs use main branch unless SHA-pinned. Scope remains selected files, not full audit.

## Pinned commit IDs
- ArtCraft Launcher `storytold/craft-launcher`: `c7047d47716632414d7bf56f869f7b5ac3b3e674`
- LangGraph `langchain-ai/langgraph`: `c6335a4255dc1d8abc25a7677f9c072c7ab27b9c`
- mini-SWE-agent `SWE-agent/mini-swe-agent`: `04d809ceab9df28f9adaed044884180159172930`
- Browser Use `browser-use/browser-use`: `753d629d76eb2b670f4cf467f3355bbe750f6845`
- MCP servers `modelcontextprotocol/servers`: `c799c8552b0f27b7a33a7b9233773da144dddcf5`
- OpenHands SDK `OpenHands/software-agent-sdk`: `077f3fad6d31cd852be5c87176e0a93c3b446126`

## Deeper source observations (selected files)
### ArtCraft Launcher
- HTTP source separates agents for small requests, feeds, redirect handling and downloads; caps small/API response sizes; documents rate-limits, ETags and timeout policies. Nightly test mirror is explicitly loopback-only and confines routes to one app fixture.
- Installer docs/code indicate SHA-256 verification before unpack, avoids replacing running apps, and promotes new install only after completion; update paths preserve/restore prior copy for supported package types. Important limitation: rollback/atomicity varies by package/platform, and hash validation alone is not publisher authenticity.
- Source: `crates/native/src/http.rs`, `install.rs`.

### mini-SWE-agent
- Config exposes step limit, cost limit, wall-time limit and consecutive format-error cap; zero values mean unlimited for step/time/error limits in documented fields.
- Run loop writes trajectory in finally; trajectory stores model stats, config, messages, exit status/submission and model/environment serialization. Environment execution still needs its own isolation/permissions; limits do not imply safe side effects.
- Source: `src/minisweagent/agents/default.py`.

### Browser Use (current 1.x loop source)
- Session bounds include timeout, max steps, Python-cell timeout, and a delivery-only phase near budget end; partial checkpoint redacts secrets; tool outputs are recorded; delivery repair explicitly avoids repeating browser actions and calls out missing evidence.
- Browser task code runs in a persistent Python REPL with helpers/CDP. This is a powerful execution surface; permissions/workspace/browser isolation are critical. The source explicitly discusses killed/hung worker handling, partial output and model/API transient errors.
- Source: `browser_use/agent/loop.py`, `agent/service.py`.

### MCP filesystem
- Roots/allowed dirs, read-only checks, path validation, path-root boundary checks, path normalization, realpath timeout and recursive-walk cap are implemented.
- Source `lib.ts` defines 15-second filesystem-call timeout and 100,000-entry recursive-walk cap; caveat: timeout stops waiting but does not cancel the underlying OS call, potentially retaining a libuv thread. Pinned-directory operations are used to reduce path-swap races.
- Source: `src/filesystem/server.ts`, `lib.ts`, `path-validation.ts`.

### LangGraph
- State/checkpoint machinery is sophisticated; checkpoint durability and pending/delta writes are coordinated. A checkpoint is not by itself an exactly-once guarantee for external effects; integrations still require idempotency keys and reconciliation.
- Source: `libs/langgraph/langgraph/pregel/_loop.py`; commit's metadata/test plans indicate targeted deployment update secret-field omission, not proof of every workflow behavior.

### OpenHands SDK
- Only commit snapshot and repository-level source anchor were reviewed in this pass. Deeper file-by-file review, security tests and issue history are still outstanding; do not score it as audited.

## Advait findings / design changes
1. Treat filesystem timeouts as *wait timeout*, not cancellation; track orphaned operations and avoid concurrent repeated calls to same blocked resource.
2. Make tool adapters declare side-effect class, idempotency support, cancellation semantics and evidence contract.
3. Maintain two separate statuses: execution result and independently verified result.
4. A hash-linked local ledger detects accidental edits/reordering if prior hashes remain; it is **not cryptographically tamper-proof** against an editor who can recompute the chain. For authenticity, anchor signatures/hashes externally or use signing keys protected from the writer.
5. Test limits for steps, calls, wall time, tokens/cost, output bytes, memory/storage and tool-specific action counts; fail closed when unknown.
6. User approval gate must bind to exact action/target/amount/content, expire, and not be transferable to a changed action.
7. Self-evolution candidate code cannot edit its policy/approval rules; candidate runs in isolation and promotion/rollback requires external owner authority.

## GitHub Actions verified
Workflow `Offline tests`, run ID `45232080774`, head commit `499f83393fcac21d10cda4e60df5804644c6bceb`: completed, conclusion **success**. Job `python-tests`: checkout, setup Python, `python test_harness.py` all completed successfully. Link: https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit/actions/runs/45232080774

## Test harness caveat
These are unit tests of a toy/mock policy model, not the real Advait engine or third-party projects. Passing does not establish system security or business-task capability. The hash-chain test only catches modification while original chain hashes remain unchanged.
