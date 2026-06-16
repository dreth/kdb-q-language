---
name: q-language
description: Write, review, and debug q code for KX kdb+ queries, tables, functions, IPC, persistence, and q-sql using bundled Q for Mortals 3.1 chapter references.
---

# q Language

Use this skill when writing or reviewing q, kdb+, or q-sql. Prefer idiomatic array/table operations over translating row-oriented SQL or imperative loops.

## Workflow

1. Read `references/index.md` first to choose the smallest relevant chapter notes.
2. For data modeling or query work, read `chapter-08-tables.md` and `chapter-09-queries-q-sql.md` before writing code.
3. For expression bugs, read `chapter-01-q-shock-and-awe.md`, `chapter-03-lists.md`, `chapter-04-operators.md`, and `chapter-06-functions.md`.
4. For type, null, cast, or enum bugs, read `chapter-02-basic-data-types-atoms.md` and `chapter-07-transforming-data.md`.
5. For persisted kdb+ databases, read `chapter-11-io.md` and `chapter-14-introduction-to-kdb.md`.
6. If an error message is supplied, read `appendix-b-error-messages.md` early.

## q-sql Query Checklist

- Confirm whether the input is a table, keyed table, splayed table, or partitioned table.
- Check column names and types first with `meta t`, `cols t`, `key t`, and small `select[10] from t` probes when q is available.
- Use q-sql templates for readable queries: `select ... by ... from t where ...`, `update ... by ... from t where ...`, `delete ... from t where ...`.
- Use functional forms (`?[...]`, `![...]`) when column names, filters, groupings, or aggregates are dynamic.
- Remember row order matters in q. Sort explicitly with `xasc`, `xdesc`, `asc`, `desc`, or attributes when the result depends on order.

## Idiom Reminders

- q evaluates function application from right to left and has no traditional operator precedence. Add parentheses when generating code for humans.
- Lists, dictionaries, functions, and tables can all behave like maps. Indexing and function application share notation.
- Prefer vector operations, atomic functions, iterators (`each`, `over`, `scan`, `prior`, `peach`), and q-sql aggregates over explicit loops.
- Use typed empty lists in schemas: `` `sym$()``, `` `long$()``, `` `timestamp$()``.
- Use `enlist` when a single item must remain a list, row, key, or record.
- Treat symbols as interned values. Avoid unbounded conversion of arbitrary strings to symbols in long-running processes.

## Validation

When q is installed, run generated snippets against a scratch process and inspect `type`, `meta`, `count`, and representative results. Without q, do structural validation: balance brackets/braces, check q-sql phrase order, verify column names/types against schemas, and reason through atom-vs-list rank.

This skill includes `scripts/validate_skill.py` for repository structure checks. It does not validate q semantics unless a local q runtime is available.
