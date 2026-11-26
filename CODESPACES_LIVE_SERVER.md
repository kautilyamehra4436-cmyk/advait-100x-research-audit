# GitHub Codespaces: Advait Sovereign Server

This repository now has a Codespaces-ready development environment and a real HTTP smoke test.

## Open a live development server

1. Open the repository on GitHub: https://github.com/kautilyamehra4436-cmyk/advait-100x-research-audit
2. Select **Code → Codespaces → Create codespace on main**.
3. In the Codespaces terminal run:

```bash
export ADVAIT_SERVER_HOST=127.0.0.1
export ADVAIT_SERVER_PORT=8765
export ADVAIT_SERVER_TOKEN='choose-a-long-random-local-token'
python advait_sovereign_server.py
```

4. In a second terminal, verify the public liveness endpoint and protected status endpoint:

```bash
curl -i http://127.0.0.1:8765/healthz
curl -i -H "Authorization: Bearer $ADVAIT_SERVER_TOKEN" http://127.0.0.1:8765/v1/status
```

The forwarded port is configured as **private**. Do not change it to public for this local control-plane test. Do not paste tokens into chat, source files, commits, or screenshots.

## Automated real-HTTP test

GitHub Actions starts the Python server as a child process and sends real HTTP requests to it. It checks liveness, missing/wrong/valid bearer tokens, unknown routes, rejected write methods, and 100 repeated health requests. The run reports elapsed time.

The test is intentionally bounded. It is not a 24-hour endurance test, a penetration test, a production deployment, or proof of internet reachability.

## Safety boundaries

- The server binds to loopback by default.
- Operational status requires a bearer token.
- No task execution, payment, transfer, customer outreach, or credential-management endpoint is enabled.
- Codespaces is temporary development infrastructure; it may stop and is not an always-on production host.
- Never store production secrets in repository files. Use GitHub Codespaces secrets only when needed and only after reviewing their scope.

## Current validation stages

1. Unit tests in GitHub Actions.
2. Ephemeral localhost HTTP smoke test in GitHub Actions.
3. Interactive Codespaces run (requires opening a Codespace in the GitHub UI).
4. Long-duration soak test and production hardening (not yet complete).
