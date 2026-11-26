import stat
import tempfile
import unittest
from pathlib import Path

from ceo_control_board import build_board, write_board


class CEOControlBoardOutputTests(unittest.TestCase):
    def test_reports_are_private_and_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "reports" / "ceo-board"
            board = build_board([Path(tmp)])
            json_path, markdown_path = write_board(board, output)
            self.assertEqual(stat.S_IMODE(json_path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(markdown_path.stat().st_mode), 0o600)
            original = json_path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_board(board, output)
            self.assertEqual(json_path.read_bytes(), original)

    def test_symlinked_output_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()
            link = Path(tmp) / "linked"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(PermissionError):
                write_board(build_board([Path(tmp)]), link)


if __name__ == "__main__":
    unittest.main()
