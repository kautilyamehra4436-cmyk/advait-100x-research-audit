# Advait Sovereign Server — Foundation Blueprint

**Status (2026-11-26):** local-first server foundation proposed and added as a standard-library Python control-plane skeleton. CI tests pending. Not deployed, not internet-accessible, and not a 24-hour runtime.

## Design objective

Create an owner-controlled control plane that can host Advait's bounded modules without requiring a GPU or a heavy AI runtime. The first server should be small, auditable, portable to a phone or low-cost CPU host, and safe by default.

## Architecture

1. **Control plane:** `advait_sovereign_server.py`; Python standard library only; loopback bind by default; remote bind refused without a bearer token.
2. **Module adapters:** My Brain, Relationship Intelligence, Open-Source Maker & Customer Intelligence, CEO Control Board. Adapters expose read-only status first; no module is granted execution authority merely by registration.
3. **Local data plane:** SQLite for task metadata and evidence references; separate encrypted owner-controlled vault for secrets/legal/financial source records. Never store raw credentials in ordinary module databases.
4. **Discovery workers:** scheduled, rate-limited public-source retrieval; cache results; preserve source URL, retrieval time, license status, evidence and uncertainty. Do not scrape behind login or bypass access controls.
5. **Observability:** Gatus or a similarly lightweight health-check service can monitor endpoints; avoid adding a second monitoring stack until a host exists.
6. **Edge/network:** Caddy can provide HTTPS and reverse proxy after a public host/domain is deliberately configured. Never expose the Python development server directly to the public internet.
7. **Backup:** Litestream is a candidate for SQLite replication; test restore, not just backup creation, before relying on it.
8. **Owner channel:** ntfy can deliver private alerts after authentication, topic privacy and delivery tests. No customer outreach is enabled.

## Initial operating profile

- CPU: 1 vCPU is a reasonable first target for the control plane and light metadata jobs; 2 vCPU provides more headroom.
- RAM: start by measuring at 512 MB–1 GB for the minimal server; target 1–2 GB if running several workers and monitoring together.
- Storage: 5–10 GB initial application/log/cache allocation, with separate backup retention limits.
- GPU: none for metadata discovery, classification rules, queueing, health checks, and reports. A GPU is only relevant if a local large language model or image model is added.
- These are engineering starting estimates, not measured Advait production requirements. Measure peak RSS, CPU, disk growth and request latency under representative load before choosing a host.

## Safety model

- Liveness endpoint exposes only a fixed minimal response.
- Operational status requires a bearer token.
- Remote binding without a token is rejected.
- No task execution, payment, payout, bank transfer, external contact, or credential administration endpoint exists in this foundation.
- Owner approval remains mandatory for outreach, contracts, commitments, money movement and core security changes.
- A successful health check does not prove modules are working. Readiness, module-level tests and a 24-hour soak test are separate gates.

## Build and validation gates

1. Unit tests for authentication, route allowlisting, remote-bind protection and fail-closed provider errors.
2. CI pass on the server code and all existing regression suites.
3. Phone test on the user's Android device, with measured CPU/RAM and network behavior.
4. Controlled 1-hour soak, then 24-hour soak with restart, backup and recovery checks.
5. Only after those gates: decide whether to host on a dedicated device or a third-party server.

## Known limits

This is a foundation, not a claim of superiority over all existing servers. Advait's differentiation must be proven through measured owner-control, low-resource efficiency, cross-module evidence quality, recovery time and safe task completion—not branding or feature count.
