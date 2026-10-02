"""Verify local file digests against an owner-supplied JSON manifest."""

from __future__ import annotations

import hashlib
from local_input import read_local_file
from strict_json import loads
from pathlib import Path, PurePosixPath

MAX_FILE = 128 * 1024 * 1024


def review_manifest(text: str, root: Path) -> list[dict[str, str]]:
    try:
        document = loads(text)
    except ValueError as exc:
        raise ValueError("invalid manifest JSON") from exc
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        raise ValueError("expected files array")
    if root.is_symlink():
        raise ValueError("root must not be a symlink")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    findings = []
    seen = set()
    for index, entry in enumerate(document["files"]):
        if not isinstance(entry, dict):
            raise ValueError("file entry must be an object")
        name, expected = entry.get("path"), entry.get("sha256")
        if not isinstance(name, str) or not isinstance(expected, str) or len(expected) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in expected):
            raise ValueError("invalid path or SHA-256 digest")
        rel = PurePosixPath(name)
        if rel.is_absolute() or rel.as_posix() != name or any(part == ".." for part in rel.parts) or name in seen or not name:
            raise ValueError("unsafe or duplicate path")
        seen.add(name)
        candidate = root.joinpath(*rel.parts)
        if any(root.joinpath(*rel.parts[:depth]).is_symlink() for depth in range(1, len(rel.parts) + 1)) or not candidate.is_file() or not candidate.resolve().is_relative_to(root):
            findings.append({"rule": "missing-or-unsafe-file", "location": name, "note": "File is missing, linked, or outside the root"})
            continue
        if candidate.stat().st_size > MAX_FILE:
            findings.append({"rule": "size-limit", "location": name, "note": "File exceeds the review limit"})
            continue
        digest = hashlib.sha256(read_local_file(candidate, MAX_FILE)).hexdigest()
        if digest != expected.lower():
            findings.append({"rule": "digest-mismatch", "location": name, "note": "Observed SHA-256 differs from the manifest"})
    return findings
