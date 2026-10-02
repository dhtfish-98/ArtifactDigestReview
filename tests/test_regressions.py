import json
import plistlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review import review_manifest


class RegressionTests(unittest.TestCase):

    def test_parent_symlink_and_oversized_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"actual").mkdir()
            (root/"actual"/"file").write_bytes(b"synthetic")
            (root/"linked").symlink_to(root/"actual",target_is_directory=True)
            manifest=json.dumps({"files":[{"path":"linked/file","sha256":"0"*64}]})
            self.assertEqual(review_manifest(manifest,root)[0]["rule"],"missing-or-unsafe-file")
            with patch("review.MAX_FILE",8):
                manifest=json.dumps({"files":[{"path":"actual/file","sha256":"0"*64}]})
                self.assertEqual(review_manifest(manifest,root)[0]["rule"],"size-limit")
