# Run Advait offline on Android

## 1. Install/run environment
Use Termux or a mobile Python IDE with Python 3.8+. No API key, paid hosting, server, or subscription is required for these local checks.

## 2. Download the repository files
At minimum:
- `advait_engine.py`
- `atc_handoff.py`
- `phone_runtime_check.py`
- `soak_test.py`
- `test_advait_engine.py`

## 3. Run the quick checks
```sh
python phone_runtime_check.py
python -m unittest -v test_advait_engine.py
python advait_engine.py
```

The self-check writes only inside a temporary directory and reports Python, SQLite, filesystem, exclusive-create, fsync and symlink capability observations. A platform may report optional filesystem features as unavailable; inspect the output rather than assuming compatibility.

## 4. Run a 24-hour low-load SQLite soak test
Only after the quick checks pass:
```sh
python soak_test.py --hours 24 --interval-seconds 60 --db advait_soak.db
```

This writes operational test events to a local SQLite file and checks the hash chain after every tick. Keep the phone powered and prevent the OS from stopping Termux/IDE if possible. Do not put credentials, tokens, private customer data, or legal/financial source records in this test database.

To stop manually, use Ctrl+C. If the process is force-stopped by Android, the last persisted tick remains; the absence of a final completion record means the run did not complete. Do not report a 24-hour PASS unless the final summary says `completed: true` and `ledger_integrity: true`.

## 5. What this does not prove
A CI smoke run is not an Android test. This harness does not prove background execution, battery behavior, memory stability of a full autonomous agent, live web/bounty discovery, account integration, external submissions, payment collection, owner authentication, or revenue. No external action is performed.
