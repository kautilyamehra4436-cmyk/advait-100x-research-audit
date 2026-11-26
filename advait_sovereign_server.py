"""Minimal, fail-closed HTTP control plane for Advait Sovereign Server.

This is a local-first server foundation, not a production deployment. It uses only
Python's standard library, binds to loopback by default, exposes a minimal liveness
probe, and requires a bearer token for operational status. It intentionally has no
task-execution, payment, outreach, or credential-management endpoints.
"""
from __future__ import annotations

import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable
from urllib.parse import urlsplit


def _is_loopback(host: str) -> bool:
    return host in {"127.0.0.1", "::1", "localhost"}


def build_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    token: str | None = None,
    status_provider: Callable[[], dict] | None = None,
) -> ThreadingHTTPServer:
    """Build a server; remote binding is refused unless a token is configured."""
    if not _is_loopback(host) and not (token and token.strip()):
        raise ValueError("remote binding requires a non-empty ADVAIT_SERVER_TOKEN")
    if not 0 <= int(port) <= 65535:
        raise ValueError("port must be between 0 and 65535")

    provider = status_provider or (lambda: {
        "mode": "CONTROL_PLANE_SKELETON",
        "modules": {},
        "owner_approval_required": True,
        "live_integrations": False,
    })

    class Handler(BaseHTTPRequestHandler):
        server_version = "AdvaitSovereignServer/0.1"

        def _send(self, status: int, payload: dict) -> None:
            body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            path = urlsplit(self.path).path
            if path == "/healthz":
                self._send(200, {"ok": True, "service": "advait-sovereign-server"})
                return
            if path == "/v1/status":
                supplied = self.headers.get("Authorization", "")
                expected = f"Bearer {token or ''}"
                if not token or not hmac.compare_digest(supplied, expected):
                    self._send(401, {"error": "unauthorized"})
                    return
                try:
                    payload = provider()
                    if not isinstance(payload, dict):
                        raise TypeError("status provider must return a dictionary")
                    self._send(200, payload)
                except Exception:
                    self._send(503, {"error": "status_unavailable"})
                return
            self._send(404, {"error": "not_found"})

        def do_POST(self) -> None:
            self._send(405, {"error": "method_not_allowed"})

        def do_PUT(self) -> None:
            self._send(405, {"error": "method_not_allowed"})

        def do_DELETE(self) -> None:
            self._send(405, {"error": "method_not_allowed"})

        def log_message(self, format: str, *args: object) -> None:
            # Avoid writing request paths or headers (which may contain secrets) to logs.
            return

    return ThreadingHTTPServer((host, int(port)), Handler)


def main() -> None:
    host = os.environ.get("ADVAIT_SERVER_HOST", "127.0.0.1")
    port = int(os.environ.get("ADVAIT_SERVER_PORT", "8765"))
    token = os.environ.get("ADVAIT_SERVER_TOKEN")
    server = build_server(host=host, port=port, token=token)
    print(f"Advait Sovereign Server listening on {host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
