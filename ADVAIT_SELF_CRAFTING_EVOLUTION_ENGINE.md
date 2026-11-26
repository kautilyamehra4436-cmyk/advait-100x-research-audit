# Advait Self-Crafting & Evolution Engine (SCEE)

## Purpose
SCEE is an offline, evidence-gated innovation workbench for Advait. It organizes
problem discovery, open-source capability analysis, candidate design, controlled
experiments, provenance/license review, security review, resource comparison,
product hypotheses, and owner-reviewed integration.

## Current implementation
- `advait_self_crafting.py`: deterministic candidate assessor and comparator.
- `tests/test_advait_self_crafting.py`: fail-closed gate and comparison tests.
- `python advait_self_crafting.py --self-test`: executable local smoke check.
- CI executes the unit tests and self-test.

## Experiment protocol
For each problem, keep a written brief: user need, workload, device/runtime,
acceptance criteria, baseline, candidate A (existing tool), candidate B (new
independent algorithm), candidate C (hybrid), test data, repeated runs, and
measurement method. Compare only results collected under the same workload and
device. Record latency, peak memory, correctness, security findings, energy or
network cost where measurable, and uncertainty.

## Hard gates
1. No candidate is eligible unless metrics are measured and correctness passes.
2. Unknown or unapproved licenses fail closed. Record source URL, exact version,
   license identifier, required notices, and attribution obligations before reuse.
3. Security review and a rollback path are mandatory.
4. A selected candidate is only a recommendation for owner review.
5. Production deployment is always disabled in this module; owner approval and
   a separate deployment process are required.
6. This module does not run generated code, install packages, crawl the web,
   contact maintainers/customers, submit work, or move money.

## Originality truth gate
A different implementation is not automatically a globally novel invention.
SCEE records independent design rationale and comparison evidence; novelty claims
require a separate prior-art and license review. Reuse functional ideas without
copying protected code unless the applicable license permits it.

## Score
Eligible candidates receive `1000 / (latency_ms * memory_mb)`. This is a
transparent local efficiency indicator only. It is not a universal quality,
security, cost, or originality score. It is meaningful only for the same workload,
device, measurement method, and correctness criteria.

## Current limitations
This is the first executable SCEE foundation, not an autonomous research agent.
Live web discovery, repository crawling, code generation, isolated execution,
Android measurements, customer validation, and product deployment are not
implemented here. Those require separately permissioned integrations and
independent security controls.
