# SCEE: Phone and Codespaces Runbook

## GitHub Codespaces
Open the repository, choose Code -> Codespaces -> Create codespace on
`main` after this change is merged. Keep forwarded ports private.

Run:
```bash
python -m unittest -v tests.test_advait_self_crafting
python advait_self_crafting.py --self-test
```

Expected self-test output includes `"result": "PASS"`,
`"winner": "new-algorithm"`, and
`"production_deployment_allowed": false`.

## Android phone
Use a trusted Python environment that supports Python 3.10+ and can access the
repository files. Run the same two commands from the repository root. The GitHub
Actions run is not an Android-device test; record the phone model, Python version,
run duration, and output separately.

## Security
Do not expose Codespaces ports publicly, paste tokens into chat, or put secrets
in candidate records. This module performs no external network actions.
