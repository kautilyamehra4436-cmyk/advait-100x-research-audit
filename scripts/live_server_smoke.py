"""Exercise the real Advait HTTP server over localhost; standard library only."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = "ci-only-advait-smoke-token"


def request(url: str, method: str = "GET", token: str | None = None):
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def main() -> int:
    env = os.environ.copy()
    env.update({
        "ADVAIT_SERVER_HOST": "127.0.0.1",
        "ADVAIT_SERVER_PORT": "0",
        "ADVAIT_SERVER_TOKEN": TOKEN,
    })
    proc = subprocess.Popen(
        [sys.executable, os.path.join(ROOT, "advait_sovereign_server.py")],
        cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    try:
        # Server chooses an ephemeral port when configured with port 0; read its
        # bound port from the child process output.
        line = ""
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                raise RuntimeError(f"server exited early: {proc.stderr.read()}")
            # The server prints its bound port only after binding.
            import selectors
            sel = selectors.DefaultSelector()
            sel.register(proc.stdout, selectors.EVENT_READ)
            if sel.select(timeout=0.1):
                line = proc.stdout.readline().strip()
                sel.close()
                break
            sel.close()
        if not line:
            raise RuntimeError("server did not announce startup within 8 seconds")
        port = int(line.rsplit(":", 1)[1])
        base = f"http://127.0.0.1:{port}"

        started = time.perf_counter()
        status, body = request(base + "/healthz")
        assert status == 200 and json.loads(body)["ok"] is True

        status, body = request(base + "/v1/status")
        assert status == 401 and json.loads(body)["error"] == "unauthorized"

        status, body = request(base + "/v1/status", token="wrong-token")
        assert status == 401

        status, body = request(base + "/v1/status", token=TOKEN)
        payload = json.loads(body)
        assert status == 200 and payload["owner_approval_required"] is True

        status, _ = request(base + "/unknown")
        assert status == 404

        status, _ = request(base + "/v1/status", method="POST", token=TOKEN)
        assert status == 405

        # Small bounded concurrency/stability probe, not a 24-hour soak test.
        for _ in range(100):
            status, _ = request(base + "/healthz")
            assert status == 200

        elapsed_ms = (time.perf_counter() - started) * 1000
        print(json.dumps({
            "result": "PASS",
            "checks": ["healthz", "unauthenticated_denied", "wrong_token_denied",
                       "authorized_status", "unknown_route_404", "post_rejected_405",
                       "100_repeated_health_requests"],
            "repeated_requests": 100,
            "elapsed_ms": round(elapsed_ms, 2),
            "scope": "ephemeral localhost CI smoke test; not production or 24h soak",
        }, sort_keys=True))
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)


if __name__ == "__main__":
    raise SystemExit(main())
