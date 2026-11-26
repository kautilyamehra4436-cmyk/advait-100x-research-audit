# Advait Sovereign Server — Live Open-Source Tool Scan

**Retrieved:** 2026-11-26 (one-time public GitHub metadata + README inspection)  
**Scope:** tools potentially useful to build and operate Advait's own lightweight server.  
**Live discovery feed:** not deployed.  
**Customer/maker outreach:** none.  
**Installations/execution:** none.

| Project | Purpose verified from repository | Public repo metadata | License | Advait fit / caution |
|---|---|---:|---|---|
| [Caddy](https://github.com/caddyserver/caddy) | HTTP server / reverse proxy; automatic HTTPS is a core project goal | 79,575 stars; updated 2026-11-26 | Apache-2.0 | Candidate edge proxy after domain + host exist; do not expose development server directly. |
| [Gatus](https://github.com/TwiN/gatus) | Health dashboard with HTTP, ICMP, TCP, DNS checks and alerting | 12,899 stars; updated 2026-11-26 | Apache-2.0 | Candidate low-complexity service monitor; resource use must be measured on target host. |
| [Litestream](https://github.com/benbjohnson/litestream) | SQLite WAL change replication for disaster recovery | 14,702 stars; updated 2026-11-26 | Apache-2.0 | Candidate for SQLite backups/replication; restore test is mandatory. |
| [ntfy](https://github.com/binwiederhier/ntfy) | HTTP-based push notifications to phone/desktop | 35,771 stars; updated 2026-11-26 | Apache-2.0 | Candidate private owner alerts; topic authentication/privacy and delivery must be configured. |
| [PocketBase](https://github.com/pocketbase/pocketbase) | Go backend with embedded SQLite, realtime subscriptions, users/files, admin UI and REST-style API | 61,576 stars; updated 2026-11-26; repository marked archived/moved | MIT | Do not select as default dependency until the new canonical repository, maintenance state and compatibility are verified. README warns pre-1.0 backward compatibility is not guaranteed. |

## Initial selection

For the first Advait server, keep the core custom and small: Python standard-library control plane + SQLite. Treat Caddy, Gatus, Litestream and ntfy as optional sidecars/adapters, not mandatory dependencies. This avoids coupling the core to a large stack before a real host is selected.

## What is not proven

- Stars are popularity signals, not security, quality or active-user proof.
- Public repository owners/organizations are not verified individual inventors or customer contacts.
- No individual maker identities or customer needs/budgets were verified in this scan.
- No RAM/CPU measurements were retrieved for these tools; do not infer hardware sizing from stars or language.
- No customer lead or revenue opportunity is claimed.
