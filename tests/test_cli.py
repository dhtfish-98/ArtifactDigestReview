import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from cli import main


class CLITests(unittest.TestCase):
    def test_finding_json_and_invalid_path(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "owned"
            root.mkdir()
            (root / "sample").write_bytes(b"synthetic")
            path = Path(folder) / "manifest.json"
            path.write_text(json.dumps({"files": [{"path": "sample", "sha256": "0" * 64}]}))
            args = [str(path), str(root)]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(args + ["--json"]), 1)
            self.assertTrue(json.loads(output.getvalue()))
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(path) + ".missing", str(root)]), 2)
