import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import portable_launcher


class PortableLauncherDiagnosticsTests(unittest.TestCase):
    def test_runtime_exception_is_logged_and_returns_failure(self):
        old_cwd = os.getcwd()
        old_executable = sys.executable
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                exe = root / "Orione.exe"
                exe.write_bytes(b"")
                (root / portable_launcher.APP_FILENAME).write_text("pass\n", encoding="utf-8")
                sys.executable = str(exe)
                try:
                    with mock.patch.object(
                        portable_launcher.runpy,
                        "run_path",
                        side_effect=RuntimeError("probe exploded"),
                    ):
                        with mock.patch.object(portable_launcher, "_show_runtime_error"):
                            result = portable_launcher.main()
                    self.assertEqual(result, 1)
                    log = root / "standalone_startup_error.log"
                    self.assertTrue(log.is_file())
                    text = log.read_text(encoding="utf-8")
                    self.assertIn("RuntimeError", text)
                    self.assertIn("probe exploded", text)
                finally:
                    os.chdir(old_cwd)
        finally:
            sys.executable = old_executable
            os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
