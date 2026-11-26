"""CI smoke test for SCEE's actual Python API and CLI."""
import json
import subprocess
import sys

from advait_self_crafting import self_test

result = self_test()
assert result["result"] == "PASS"
proc = subprocess.run(
    [sys.executable, "advait_self_crafting.py", "--self-test"],
    check=True, capture_output=True, text=True, timeout=10,
)
payload = json.loads(proc.stdout)
assert payload["result"] == "PASS"
assert payload["decision"] == "CANDIDATE_SELECTED_FOR_OWNER_REVIEW"
assert payload["winner"] == "new-algorithm"
print(json.dumps({
    "result": "PASS",
    "checks": ["python_api", "real_cli_subprocess", "license_gate",
               "owner_approval_gate", "no_production_deployment"],
    "scope": "ephemeral GitHub Actions runner; not Android, Codespaces session, or 24h soak",
}, sort_keys=True))
