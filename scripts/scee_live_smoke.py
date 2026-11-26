"""CI smoke test for SCEE's actual Python API and CLI."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from advait_self_crafting import self_test

result = self_test()
assert result["result"] == "PASS"
proc = subprocess.run(
    [sys.executable, str(ROOT / "advait_self_crafting.py"), "--self-test"],
    cwd=ROOT, check=True, capture_output=True, text=True, timeout=10,
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
