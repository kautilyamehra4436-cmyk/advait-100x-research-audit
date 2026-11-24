"""Low-load SQLite ledger soak test for phone/desktop.

Example 24-hour run:
python soak_test.py --hours 24 --interval-seconds 60 --db advait_soak.db

Quick CI smoke:
python soak_test.py --hours 0.001 --interval-seconds 0.1 --max-iterations 3 --db /tmp/advait-soak.db
"""
import argparse
import json
import time
import tracemalloc
import uuid

from advait_engine import SQLiteLedger


def main(argv=None):
    parser = argparse.ArgumentParser(description="Low-load Advait SQLite ledger soak test")
    parser.add_argument("--hours", type=float, default=24.0)
    parser.add_argument("--interval-seconds", type=float, default=60.0)
    parser.add_argument("--db", default="advait_soak.db")
    parser.add_argument("--max-iterations", type=int, default=0,
                        help="Optional cap for smoke tests; 0 means duration-controlled")
    args = parser.parse_args(argv)
    if args.hours <= 0 or args.interval_seconds < 0 or args.max_iterations < 0:
        parser.error("hours must be positive; interval and iteration cap must be non-negative")

    run_id = "SOAK-" + uuid.uuid4().hex[:12]
    duration = args.hours * 3600.0
    started = time.monotonic()
    ticks = 0
    completed = False
    tracemalloc.start()

    with SQLiteLedger(args.db) as ledger:
        if not ledger.verify():
            raise SystemExit("Existing ledger integrity check failed; refusing to append.")
        ledger.append({"type": "soak_started", "run_id": run_id,
                       "wall_time": time.time(), "target_seconds": duration,
                       "interval_seconds": args.interval_seconds})
        try:
            while time.monotonic() - started < duration:
                current, peak = tracemalloc.get_traced_memory()
                ticks += 1
                ledger.append({"type": "soak_tick", "run_id": run_id,
                               "tick": ticks, "elapsed_seconds": time.monotonic() - started,
                               "heap_current_bytes": current, "heap_peak_bytes": peak,
                               "wall_time": time.time()})
                if not ledger.verify():
                    raise RuntimeError("Ledger integrity failed during soak run")
                print(json.dumps({"run_id": run_id, "tick": ticks,
                                  "elapsed_seconds": round(time.monotonic() - started, 2),
                                  "ledger_integrity": "PASS"}), flush=True)
                if args.max_iterations and ticks >= args.max_iterations:
                    completed = True
                    break
                remaining = duration - (time.monotonic() - started)
                if remaining <= 0:
                    break
                time.sleep(min(args.interval_seconds, remaining))
            else:
                completed = True
            if time.monotonic() - started >= duration:
                completed = True
        except KeyboardInterrupt:
            ledger.append({"type": "soak_interrupted", "run_id": run_id,
                           "ticks": ticks, "elapsed_seconds": time.monotonic() - started})
            print("Interrupted by user; prior ticks remain in the ledger.")
        ledger.append({"type": "soak_finished" if completed else "soak_stopped",
                       "run_id": run_id, "ticks": ticks,
                       "elapsed_seconds": time.monotonic() - started,
                       "ledger_integrity": ledger.verify()})
        valid = ledger.verify()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    summary = {"run_id": run_id, "ticks": ticks, "completed": completed,
               "ledger_integrity": valid, "python_heap_current_bytes": current,
               "python_heap_peak_bytes": peak, "database": args.db,
               "note": "A completed quick smoke run is not a 24-hour or Android validation."}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
