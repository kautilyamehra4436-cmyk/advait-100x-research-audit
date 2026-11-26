import json
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from advait_sovereign_server import build_server


class SovereignServerTests(unittest.TestCase):
    def setUp(self):
        self.server = build_server(port=0, token="test-secret",
            status_provider=lambda: {"mode": "TEST", "owner_approval_required": True})
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        time.sleep(0.01)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def get(self, path, token=None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = Request(self.base + path, headers=headers)
        try:
            with urlopen(req, timeout=2) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_health_is_minimal_and_public(self):
        status, payload = self.get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"ok": True, "service": "advait-sovereign-server"})

    def test_status_requires_bearer_token(self):
        status, _ = self.get("/v1/status")
        self.assertEqual(status, 401)
        status, payload = self.get("/v1/status", "test-secret")
        self.assertEqual(status, 200)
        self.assertEqual(payload["mode"], "TEST")

    def test_unknown_route_is_not_found(self):
        status, _ = self.get("/admin")
        self.assertEqual(status, 404)

    def test_remote_bind_requires_token(self):
        with self.assertRaises(ValueError):
            build_server(host="0.0.0.0", port=0)

    def test_status_provider_failure_fails_closed(self):
        broken = build_server(port=0, token="test-secret",
            status_provider=lambda: (_ for _ in ()).throw(RuntimeError("secret")))
        thread = threading.Thread(target=broken.serve_forever, daemon=True)
        thread.start()
        try:
            req = Request(f"http://127.0.0.1:{broken.server_port}/v1/status",
                headers={"Authorization": "Bearer test-secret"})
            with self.assertRaises(HTTPError) as ctx:
                urlopen(req, timeout=2)
            self.assertEqual(ctx.exception.code, 503)
            self.assertEqual(json.loads(ctx.exception.read()), {"error": "status_unavailable"})
        finally:
            broken.shutdown()
            broken.server_close()
            thread.join(timeout=1)


if __name__ == "__main__":
    unittest.main()
