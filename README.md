# kdb-q-language

[![skills.sh](https://skills.sh/b/dreth/kdb-q-language)](https://skills.sh/dreth/kdb-q-language)

Codex/OpenAI-style skills for KX q/kdb+ work:

- `q-language`: write, review, and debug q, q-sql, and kdb+ code.
- `pykx`: write, review, and debug PyKX code for Python/q/kdb+ interop, conversion, query, IPC, databases, streaming, and PyKX under q.

The q skill is grounded in the KX-hosted Q for Mortals 3.1 HTML edition: https://code.kx.com/q4m3/

The PyKX skill is grounded in the PyKX docs/source at https://github.com/KxSystems/pykx and the local docs tree used to build it.

## Contents

- `q-language/SKILL.md`: concise procedural instructions for when and how to use the skill.
- `q-language/agents/openai.yaml`: OpenAI agent UI metadata with implicit invocation enabled.
- `q-language/references/`: chapter-by-chapter agent notes for Preface, chapters 0-14, Appendix A, Appendix B, Colophon, and an index.
- `q-language/scripts/validate_skill.py`: structural validation for frontmatter, metadata, required references, and local markdown links.
- `pykx/SKILL.md`: concise procedural instructions for practical PyKX work.
- `pykx/agents/openai.yaml`: OpenAI agent UI metadata with implicit invocation enabled.
- `pykx/references/`: task-oriented PyKX notes for setup, conversion, query,
  database/IPC/streaming, under-q interop, operations, recipes, and anti-patterns.
- `pykx/scripts/validate_skill.py`: structural validation, local markdown link
  checks, secret hygiene checks, and optional PyKX conversion/query smoke tests.

The references are not a mirror of Q for Mortals. They preserve source URLs and
summarize the parts an AI agent needs for practical q/kdb+ work: syntax forms,
q-sql workflow, idioms, pitfalls, and short original examples.

The PyKX references are also not raw API docs. They preserve source paths/URLs and
summarize the behavior agents need for practical code: wrapper mental model,
conversion boundaries, q execution, query APIs, databases, IPC, streaming, PyKX
under q, and operational pitfalls.

## Install/Use

For skills.sh/Codex-style installations, install or copy either skill directory as a skill root. Required skill entry points:

```text
q-language/SKILL.md
pykx/SKILL.md
```

Invoke explicitly, or rely on implicit invocation where supported:

```text
Use $q-language to write a q-sql query that computes VWAP by symbol from a trades table.

Use $pykx to write Python code that loads a partitioned kdb+ database and queries one date and symbol.
```

Agents should read `q-language/references/index.md` first, then load only the chapter notes relevant to the task.

For PyKX, agents should read `pykx/references/index.md` first, then load only the task notes relevant to setup, conversion, query, IPC, databases, streaming, under-q interop, or troubleshooting.

If the local skills CLI supports repository discovery, inspect available skills with:

```sh
npx skills add . --list --full-depth
```

## Validation

Run:

```sh
python3 q-language/scripts/validate_skill.py
python3 pykx/scripts/validate_skill.py
python3 -m py_compile q-language/scripts/validate_skill.py pykx/scripts/validate_skill.py
```

If `q` is not installed, validation is structural only. With q installed, agents should still run generated snippets against a scratch process and inspect `type`, `meta`, `count`, and representative results.

If PyKX is not installed, `pykx/scripts/validate_skill.py` remains structural. If PyKX is importable, it runs a conversion smoke test; if licensed embedded q is available, it also runs a tiny `kx.q("1+1")` smoke test.
