import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from phone_runtime_check import sqlite_roundtrip


class PhoneRuntimeSQLiteLifecycleTests(unittest.TestCase):
    def test_roundtrip_closes_both_connections(self):
        with tempfile.TemporaryDirectory() as tmp:
            original_connect = sqlite3.connect
            handles = []

            def tracked_connect(*args, **kwargs):
                conn = original_connect(*args, **kwargs)
                handles.append(conn)
                return conn

            with patch("phone_runtime_check.sqlite3.connect", side_effect=tracked_connect):
                self.assertTrue(sqlite_roundtrip(Path(tmp) / "runtime.db"))

            self.assertEqual(len(handles), 2)
            for conn in handles:
                with self.assertRaises(sqlite3.ProgrammingError):
                    conn.execute("SELECT 1")


if __name__ == "__main__":
    unittest.main()
