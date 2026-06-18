# PyKX Reference Index

Source base: `/opt/data/home/projects/pykx-docs-src` cloned from `https://github.com/KxSystems/pykx`.

Public docs base: https://code.kx.com/pykx/

These notes are task guides for agents. They summarize practical behavior from PyKX docs/source and avoid mirroring raw API pages.

## Start Here

- Setup, import, environment, license modes: [getting-started-and-configuration.md](getting-started-and-configuration.md)
- PyKX objects, `kx.toq`, wrappers, text, nulls, temporals: [data-conversion-and-types.md](data-conversion-and-types.md)
- q execution, Query API, SQL, qSQL, query performance: [query-and-q-execution.md](query-and-q-execution.md)
- `kx.DB`, IPC, streaming/tick workflows: [databases-ipc-and-streaming.md](databases-ipc-and-streaming.md)
- PyKX under q, context interface, remote functions, serialization: [pykx-under-q-and-interop.md](pykx-under-q-and-interop.md)
- Environment, license, threading, subprocess, embedded q limits: [operational-pitfalls-and-troubleshooting.md](operational-pitfalls-and-troubleshooting.md)
- Common patterns to adapt: [recipes.md](recipes.md)
- Review checklist and generated-code traps: [anti-patterns.md](anti-patterns.md)

## Task Routing

| User task | Load |
| --- | --- |
| Install/import/configure PyKX or CI env | `getting-started-and-configuration.md` |
| Convert Python/Pandas/Arrow data to q or back | `data-conversion-and-types.md` |
| Explain wrapper types, symbols vs strings, nulls, temporals | `data-conversion-and-types.md` |
| Write `kx.q`, q keyword, qSQL, SQL, or Query API code | `query-and-q-execution.md` |
| Query a partitioned HDB efficiently | `query-and-q-execution.md`, then `databases-ipc-and-streaming.md` |
| Create/load/change a splayed or partitioned DB | `databases-ipc-and-streaming.md` |
| Connect to q over IPC or publish updates | `databases-ipc-and-streaming.md` |
| Use Python inside q or migrate embedPy code | `pykx-under-q-and-interop.md` |
| Diagnose license, `embedq`, `cores`, `noupdate`, timer, or main-loop bugs | `operational-pitfalls-and-troubleshooting.md` |
| Review generated PyKX code | `anti-patterns.md`, then relevant task file |

## Source Coverage Map

- Overview/setup: `README.md`, `docs/index.md`, `docs/getting-started/*`, `docs/learn/objects.md`, `docs/user-guide/configuration.md`, `docs/user-guide/advanced/modes.md`, `docs/license.md`.
- Fundamentals: `docs/user-guide/fundamentals/{creating,evaluating,indexing,conversion_considerations,text,nulls_and_infinities,temporal}.md`.
- Querying: `docs/user-guide/fundamentals/query/*`, `docs/api/{query,columns}.md`, `docs/api/pykx-execution/q.md`.
- Databases/IPC/streaming: `docs/user-guide/advanced/database/*`, `docs/user-guide/advanced/ipc.md`, `docs/user-guide/advanced/streaming/*`, `docs/api/{db,ipc,tick}.md`.
- Interop: `docs/pykx-under-q/*`, `docs/user-guide/advanced/{context_interface,remote-functions,serialization,subprocess,threading}.md`, relevant `src/pykx` docstrings.
- Operations: `docs/help/{faq,troubleshooting,issues}.md`, `docs/user-guide/advanced/{license,performance,attributes,compress-encrypt}.md`.
