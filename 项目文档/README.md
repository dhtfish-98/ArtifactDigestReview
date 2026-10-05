> 目录已整理：文档在「项目文档」，暂存与缓存放在「Build」。本仓发布源码版；`python3 构建.py --build` 会返回 `OPEN_MANUAL_ADAPTER`，不生成安装包。运行源码命令前先执行 `python3 构建.py --stage --ci`，再进入 `Build/源码`。暂存会恢复原输入路径。现有版本和历史验证记录按各自提交理解。

# ArtifactDigestReview

**Source version:** [v0.1.0](https://github.com/dhtfish-98/ArtifactDigestReview/releases/tag/v0.1.0) ([release scope](RELEASES.md)); GitHub source archives only.

Compare owner-supplied SHA-256 manifest values with files in a local directory. It runs locally, does not contact targets, and reports review prompts instead of exploit instructions.

## Input and checks

- Input: JSON manifest and local directory from a system you own or are authorized to inspect.
- Checks: Missing, unsafe, oversized or digest-mismatched files.
- Output: rule, local location and short note. No source snippets, credential values or log identities are printed.

## Run

```sh
python cli.py manifest.json ./owned-artifacts
python cli.py manifest.json ./owned-artifacts --json
python -m unittest discover -s tests -v
```

Exit code 0 means no findings, 1 means review findings, 2 means invalid input or read failure. A clean result is not a security guarantee. The input file is read through a bounded regular-file descriptor with a 4 MiB limit. Each artifact has a separate 128 MiB limit.

## Boundaries

A matching digest checks bytes against the supplied manifest; it does not authenticate the manifest or its author. Concurrent file changes are not controlled. Work only on local, authorized inputs. The analysis does not send data to a service or modify the inspected files.

## Source and policy context

- Technical reference: https://docs.python.org/3/library/hashlib.html
- See [ORIGIN.md](<ORIGIN.md>) for implementation provenance and [VALIDATION.md](<VALIDATION.md>) for checks performed.
- CVP eligibility depends on a real, legitimate defensive task affected by Claude's cyber safeguards and the applicant's organization/identity review; this repository alone does not establish eligibility or approval. [Anthropic CVP guidance](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet).

## Reviewed input behavior

Manifest JSON rejects duplicate keys and nonstandard numbers. Artifact reads use a bounded regular-file descriptor; parent symlinks are checked and direct root symlinks are rejected. Concurrent path changes and manifest authenticity remain outside the guarantee.

JSON input rejects duplicate object keys and nonstandard numbers; container nesting is limited to 128 levels.
