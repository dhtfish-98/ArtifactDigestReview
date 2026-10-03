# Validation record

Scope: Missing, unsafe, oversized or digest-mismatched files.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. A matching digest checks bytes against the supplied manifest; it does not authenticate the manifest or its author. Concurrent file changes are not controlled.

## Current source result (2026-10-02)

- Python 3.14.6: 7/7 unit and CLI integration tests passed.
- Tests include the specific malformed-input, incomplete-review and declaration cases added during the source audit.
- Manifest JSON rejects duplicate keys and nonstandard numbers. Artifact reads use a bounded regular-file descriptor; parent symlinks are checked and direct root symlinks are rejected. Concurrent path changes and manifest authenticity remain outside the guarantee.
- Test input is synthetic. No external target, live credential or production cluster is exercised.
- The public commit and its corresponding GitHub workflow must be verified separately after this update.
