import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from review import review_manifest


class DigestTests(unittest.TestCase):
    def test_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "app.bin").write_bytes(b"owned")
            digest = hashlib.sha256(b"owned").hexdigest()
            manifest = lambda value: json.dumps({"files": [{"path": "app.bin", "sha256": value}]})
            self.assertEqual(review_manifest(manifest(digest), root), [])
            self.assertEqual(review_manifest(manifest("0" * 64), root)[0]["rule"], "digest-mismatch")

    def test_missing_and_path_traversal(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(review_manifest(json.dumps({"files": [{"path": "missing", "sha256": "0" * 64}]}), root)[0]["rule"], "missing-or-unsafe-file")
            with self.assertRaises(ValueError):
                review_manifest(json.dumps({"files": [{"path": "../outside", "sha256": "0" * 64}]}), root)

    def test_invalid_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            for value in ("{}", "bad", '{"files":[null]}'):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    review_manifest(value, Path(folder))
