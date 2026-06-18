# Anti-Patterns

Source paths: pitfalls across `docs/user-guide/*`, `docs/help/{faq,troubleshooting,issues}.md`, and `src/pykx` docstrings.

## Setup and Secrets

- Setting `PYKX_*`, `QARGS`, `QHOME`, `QLIC`, or license env vars after `import pykx`.
- Committing `kc.lic`, `k4.lic`, base64 license strings, DARE passwords, IPC passwords, or support logs containing secrets.
- Assuming a vanilla kdb+ license enables PyKX licensed features. PyKX needs PyKX/embedq feature flags.
- Ignoring unlicensed mode differences while using `kx.q`, `kx.DB`, Query API with `kx.Column`, local SQL, or PyKX under q.

## Conversion

- Converting a whole large table to Pandas before filtering in q.
- Calling `.py()` by default when `.np()`/`.pd()`/`.pa()` or staying in PyKX would be better.
- Treating Python `str` as q char vectors. It defaults to symbols.
- Interning unbounded text as symbols in long-running processes.
- Guessing q null sentinels instead of using typed nulls/infinities.
- Round-tripping q nanosecond timestamps through Python native datetime and expecting nanosecond precision.
- Using `raw=True` without documenting who handles epoch, GUID, bytes, null, and infinity semantics.
- Deep-mutating nested PyKX lists as if they were Python nested lists.

## q Execution and Querying

- Building q query strings with user data interpolated into the q text.
- Passing more than 8 args to a q function through `kx.q` or IPC.
- Forgetting `debug=True`/`PYKX_QDEBUG` when diagnosing q errors.
- Using SQL for q-specific joins/attributes/window logic when raw q would be clearer.
- Using raw q strings for dynamic query construction when Query API or parameterized functions would avoid quoting/type bugs.
- Querying partitioned HDBs with `sym` before `date`/partition predicates.
- Running broad `select from trade` probes against large partitioned databases.
- Applying attributes to data that does not satisfy the asserted shape.

## Databases

- Editing persisted DB schemas without a backup.
- Adding a table to only new partitions and forgetting `db.fill_database()`.
- Expecting `update`/`delete` on splayed/partitioned tables to mutate disk data through normal Query API calls.
- Loading multiple databases into one PyKX process without explicit `overwrite=True` and understanding global state.
- Hard-coding encryption passwords or using demo key paths.

## IPC

- Leaving IPC connections open instead of using context managers.
- Using `AsyncQConnection` only to send fire-and-forget messages; `wait=False` on sync IPC is enough.
- Using `wait=False` while expecting a result.
- Sending large client-side tables over IPC SQL `$1` injection when a server-side table name can be used.
- Using the context interface on hot paths or KX Insights connections instead of `no_ctx=True`.
- Sending Python functions as ordinary IPC arguments.
- Using `RawQConnection` when normal sync/async request/response is enough.

## Streaming

- Running expensive analytics directly as a subscriber to the primary zero-latency tickerplant.
- Treating a chained tickerplant as authoritative storage. It does not keep the primary replay log.
- Starting tick/RTP/HDB processes without configured q executable in environments where `q` is not on `PATH`.
- Forgetting to stop/restart managed q subprocesses during iterative development.

## PyKX Under q

- Trying to send q foreign objects over IPC.
- Forgetting `.pykx.pyexec` is needed for side effects such as imports and function definitions.
- Passing a single `::` to a Python callable expecting `None`; use `.pykx.eval"None"`.
- Passing `<`, `>`, `*`, `` ` ``, or `` `. `` as data without declaring return type or wrapping with `.pykx.tok`.
- Expecting Python-side embedded q to behave like standalone q for timers, subscriptions, `.z.pg`, or IPC server loops.

## Threading and Subprocesses

- Importing PyKX in child processes spawned from a PyKX parent without `kx.PyKXReimport()`.
- Enabling `PYKX_THREADING` and not calling `kx.shutdown_thread()` in `finally`.
- Assuming `PYKX_THREADING` is supported on Windows.
- Letting q call back into Python while `PYKX_THREADING` is active.
- Using q `peach` to call Python without `PYKX_RELEASE_GIL` and tests for the workload.
