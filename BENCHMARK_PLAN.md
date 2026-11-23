# Advait architecture benchmark plan
Benchmark variants (all receive the same task fixtures and deterministic adapters):
1. Flat sequential executor (baseline)
2. Priority-ordered bounded executor
3. Dependency-aware bounded executor (reference Advait design)

Measure: completed tasks, verified tasks, policy denials, reconciliation count, calls, steps, elapsed wall time. Correctness is primary; timings from a phone/CI environment are noisy and must not be presented as performance proof. Each fixture is repeated 30 times locally when possible; compare median and p95. No network, accounts, money, or irreversible operations.
Initial acceptance: no unauthorized action; no task marked done without evidence; exact approval binds to payload; unknown outcome enters reconciliation; hard limits stop work.
