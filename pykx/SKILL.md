---
name: pykx
description: Write, review, and debug PyKX code for Python/q/kdb+ interop, q execution, data conversion, databases, IPC, streaming, PyKX under q, and operational troubleshooting.
---

# PyKX

Use this skill when building or reviewing PyKX code. PyKX wraps q/K objects inside Python, so keep data in PyKX/K form for q analytics and convert only at Python, NumPy, Pandas, PyArrow, or IPC boundaries.

## Workflow

1. Read `references/index.md` first and load only the relevant task notes.
2. For install, import, configuration, modes, or license setup, read `getting-started-and-configuration.md`.
3. For object creation, conversion, text, nulls, temporals, or wrapper behavior, read `data-conversion-and-types.md`.
4. For `kx.q`, q keyword wrappers, Query API, SQL, qSQL, and query performance, read `query-and-q-execution.md`.
5. For persisted kdb+ databases, IPC connections, or real-time capture, read `databases-ipc-and-streaming.md`.
6. For q processes running Python or Python functions running on q servers, read `pykx-under-q-and-interop.md`.
7. For production bugs, environment problems, subprocess/threading issues, and embedded-q limitations, read `operational-pitfalls-and-troubleshooting.md`.
8. For generated code or review, read `recipes.md` and `anti-patterns.md`.

## Core Defaults

- Import as `import pykx as kx`.
- Set environment variables or `.pykx-config` before importing PyKX. Do not include license contents or secrets; mention names only, such as `QLIC`, `KDB_LICENSE_B64`, and `KDB_K4LICENSE_B64`.
- Prefer `kx.toq(obj)` for conversion into q/PyKX. Use explicit `ktype` for schemas and columns when type matters.
- Python `str` converts to q symbol by default. Use `strings_as_char=True` or `kx.CharVector` for free text, high-cardinality strings, or mutable text.
- Use typed nulls/infinities such as `kx.LongAtom.null`, `kx.IntAtom.inf`, and temporal atom/vector classes instead of guessing sentinel values.
- Convert out with `.py()`, `.np()`, `.pd()`, or `.pa()` only when the consumer needs that representation.
- Execute q locally with `kx.q("til 10")` or `kx.q("{x+y}", 2, 4)`. Arguments are converted with `kx.toq`; q calls take at most 8 arguments.
- Use `debug=True` per `kx.q` call, or `PYKX_QDEBUG` before import, when diagnosing q errors.
- Choose the query surface by intent: Query API for structured PyKX queries, SQL for SQL-facing users, raw q/qSQL for q-specific work.
- For partitioned HDB queries, put the partition/date predicate first and avoid broad probes.
- Use `kx.SyncQConnection` by default for IPC, `kx.AsyncQConnection` for `asyncio`, `kx.SecureQConnection` for TLS, and `kx.RawQConnection` only for low-level receive/server handling.
- Use context managers for IPC connections. Use `wait=False` for fire-and-forget updates and `no_ctx=True` where context-interface overhead or KX Insights compatibility matters.

## Validation

If PyKX is importable, run a small conversion smoke test and, when licensed embedded
q is available, a tiny `kx.q("1+1")` query. Without PyKX or a license, perform
structural validation and reason from schemas, types, and q expressions.

This skill includes `scripts/validate_skill.py` for structure, local links, secret hygiene, and optional PyKX runtime smoke checks.
