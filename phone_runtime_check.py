"""Phone-friendly, offline runtime self-check for Advait.

Run with: python phone_runtime_check.py
Uses only Python standard-library modules and temporary files.
"""
import json
import os
import platform
import sqlite3
from contextlib import closing
import sys
import tempfile
from pathlib import Path


def sqlite_roundtrip(db_path):
    """Verify persistence and close both SQLite handles deterministically."""
    with closing(sqlite3.connect(str(db_path))) as con:
        with con:
            con.execute("CREATE TABLE probe(value TEXT NOT NULL)")
            con.execute("INSERT INTO probe(value) VALUES(?)", ("persisted",))
    with closing(sqlite3.connect(str(db_path))) as con:
        value = con.execute("SELECT value FROM probe").fetchone()[0]
    return value == "persisted"


def main():
    checks = []
    def record(name, passed, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": str(detail)})

    record("python_version_3_8_plus", sys.version_info >= (3, 8), sys.version.split()[0])
    record("sqlite_available", bool(sqlite3.sqlite_version), sqlite3.sqlite_version)
    record("monotonic_clock", hasattr(__import__("time"), "monotonic"),
           platform.system() + " / " + sys.platform)

    with tempfile.TemporaryDirectory(prefix="advait_phone_check_") as temp:
        root = Path(temp)
        file_path = root / "exclusive.txt"
        try:
            fd = os.open(str(file_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write("advait-check")
                stream.flush()
                os.fsync(stream.fileno())
            record("filesystem_write_read_fsync",
                   file_path.read_text(encoding="utf-8") == "advait-check")
        except Exception as exc:
            record("filesystem_write_read_fsync", False, type(exc).__name__)

        try:
            os.open(str(file_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            record("exclusive_create_blocks_overwrite", False, "second create unexpectedly succeeded")
        except FileExistsError:
            record("exclusive_create_blocks_overwrite", True)
        except Exception as exc:
            record("exclusive_create_blocks_overwrite", False, type(exc).__name__)

        supports_dir_fd = os.open in getattr(os, "supports_dir_fd", set())
        record("open_dir_fd_support", supports_dir_fd, "required by hardened relative file operations")

        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            record("nofollow_flag_available", False, "platform does not expose O_NOFOLLOW")
        else:
            target = root / "target.txt"
            link = root / "link.txt"
            target.write_text("safe", encoding="utf-8")
            try:
                os.symlink(str(target), str(link))
                try:
                    fd = os.open(str(link), os.O_RDONLY | nofollow)
                    os.close(fd)
                    record("nofollow_rejects_symlink", False, "symlink open unexpectedly succeeded")
                except OSError:
                    record("nofollow_rejects_symlink", True)
            except (OSError, NotImplementedError) as exc:
                record("nofollow_rejects_symlink", False, "symlink test unavailable: " + type(exc).__name__)

        db = root / "runtime.db"
        try:
            record("sqlite_commit_reopen", sqlite_roundtrip(db))
        except Exception as exc:
            record("sqlite_commit_reopen", False, type(exc).__name__)

    required = {"python_version_3_8_plus", "sqlite_available",
                "monotonic_clock", "filesystem_write_read_fsync",
                "exclusive_create_blocks_overwrite", "sqlite_commit_reopen"}
    required_pass = all(item["passed"] for item in checks if item["check"] in required)
    output = {
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform(),
                    "sqlite": sqlite3.sqlite_version},
        "required_checks_passed": required_pass,
        "checks": checks,
        "note": "Offline smoke test only. This does not prove Android background execution, 24-hour stability, or production security."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if required_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
