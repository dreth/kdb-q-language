# kdb-q-language

Codex/OpenAI-style skill for helping agents write q, the KX kdb+ query and programming language.

The skill is grounded in the KX-hosted Q for Mortals 3.1 HTML edition: https://code.kx.com/q4m3/

## Contents

- `q-language/SKILL.md`: concise procedural instructions for when and how to use the skill.
- `q-language/agents/openai.yaml`: OpenAI agent UI metadata with implicit invocation enabled.
- `q-language/references/`: chapter-by-chapter agent notes for Preface, chapters 0-14, Appendix A, Appendix B, Colophon, and an index.
- `q-language/scripts/validate_skill.py`: structural validation for frontmatter, metadata, required references, and local markdown links.

The references are not a mirror of Q for Mortals. They preserve source URLs and summarize the parts an AI agent needs for practical q/kdb+ work: syntax forms, q-sql workflow, idioms, pitfalls, and short original examples.

## Install/Use

For skills.sh/Codex-style installations, install or copy the `q-language/` directory as a skill root. The required skill entry point is:

```text
q-language/SKILL.md
```

Invoke explicitly with `$q-language`, or rely on implicit invocation where supported:

```text
Use $q-language to write a q-sql query that computes VWAP by symbol from a trades table.
```

Agents should read `q-language/references/index.md` first, then load only the chapter notes relevant to the task.

## Validation

Run:

```sh
python3 q-language/scripts/validate_skill.py
```

If `q` is not installed, validation is structural only. With q installed, agents should still run generated snippets against a scratch process and inspect `type`, `meta`, `count`, and representative results.
