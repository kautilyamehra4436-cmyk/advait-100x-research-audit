# Engine build checkpoint
Version: Advait bounded execution core v0.1 (reference implementation)
Built: 2026-11-23
Included: task model, allowlist, exact-action approval token, payload size cap, step/call/time limits, adapter interface, evidence-gated completion, unknown-outcome reconciliation status, hash-linked event ledger, offline demo and tests.
Not included: real adapters, autonomous bounty discovery, browser integration, account login, payment collection, persistent encrypted storage, phone background service, signed/external ledger anchoring, sandbox isolation, concurrency, performance proof.
Owner authority: high-risk actions require a token bound to the task id/tool/action/payload; any payload change invalidates it. The token helper is a local approval-binding mechanism, not a real owner authentication system.
