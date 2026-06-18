# Operational Pitfalls and Troubleshooting

Source paths: `docs/help/{faq,troubleshooting,issues}.md`,
`docs/user-guide/advanced/{license,modes,performance,threading,subprocess,attributes,compress-encrypt}.md`,
`docs/api/{util,license,exceptions,system}.md`,
`src/pykx/{config.py,ctx.py,util.py,core.pyx}`.

Public docs: https://code.kx.com/pykx/help/troubleshooting.html

## First Diagnostic Steps

Capture environment details:

```python
import pykx as kx
kx.util.debug_environment()
```

For logs or support artifacts:

```python
info = kx.util.debug_environment(return_info=True)
```

Use `detailed=True` only when it is acceptable to reveal directory contents for `QHOME`/`QLIC`. Never print or commit license contents.

For q errors:

```python
import os
os.environ["PYKX_QDEBUG"] = "1"
import pykx as kx
```

or:

```python
kx.q("{x+1}", "bad", debug=True)
```

## License and Import Errors

Common cases:

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `embedq` during initialization | license lacks PyKX/embedq feature flags | use a PyKX-enabled license |
| `kc.lic` license error | license not found or not written correctly | check `QLIC`, `QHOME`, current directory, or reinstall |
| `cores` license error | process sees more cores than license allows | restrict CPU affinity before import |
| import falls back to unlicensed mode | embedded q could not initialize | inspect warning, `debug_environment`, modes |

Core-limit examples:

```sh
taskset -c 0-3 python script.py
```

```python
import os
os.sched_setaffinity(0, [0, 1, 2, 3])
import pykx as kx
```

License lookup order: current directory, `QLIC`, `QHOME`, then `KDB_LICENSE_B64`/`KDB_K4LICENSE_B64`.

Do not put base64 license values in examples, config snippets, logs, or committed files.

## Configuration Gotchas

- Environment variables must be set before `import pykx`.
- Environment variables override `.pykx-config`.
- PyKX source reads `PYKX_PROFILE` for selecting config profiles; docs also mention `PYKX_CONFIGURATION_PROFILE`. Prefer `PYKX_PROFILE` unless the local installed version says otherwise.
- `PYKX_LICENSED=true` should be used in CI only when failure to initialize embedded q should fail fast.
- `PYKX_UNLICENSED=true` is useful for conversion/IPC-only tests without a local license.

## Embedded q Is Not Standalone q

The q runtime embedded in a Python process does not run the normal standalone q main loop.

Consequences:

- Do not use embedded q as a normal IPC server.
- `.z.pg` callbacks set inside Python-side embedded q will not behave like a standalone q server.
- Connecting to a Python embedded q server can hang.
- q timers do not tick.
- `.z.ts` is hidden through the context interface because the main loop is inactive.

Use PyKX under q for workloads that need q timers, subscriptions, `.z.pg`, or normal q process main-loop behavior.

## Threading

Default PyKX embedded q calls are not safe from multiple Python threads.

Enable threaded mode before import only when needed:

```python
import os
os.environ["PYKX_THREADING"] = "1"
import pykx as kx

try:
    main()
finally:
    kx.shutdown_thread()
```

Caveats:

- Licensed mode only.
- Linux/macOS only.
- Single-threaded mode is faster for single-threaded work.
- q-calling-Python callbacks are not memory-safe in threading mode.
- Some under-q bridge operations are unsupported with `PYKX_THREADING`.

For multithreaded q calls without the background q thread, `PYKX_RELEASE_GIL` and `PYKX_Q_LOCK` affect safety/performance; set them deliberately before import.

## Subprocesses and Multiprocessing

If a child Python process imports PyKX, wrap launch in `PyKXReimport`:

```python
import subprocess
import pykx as kx

with kx.PyKXReimport():
    subprocess.Popen(["python", "worker.py"])
```

On Windows, multiprocessing support has known limitations. In all multiprocessing setups, import and initialize PyKX inside each child process where it is needed.

Avoid `PYKX_ALLOCATOR`/NEP-49 allocator in multiprocessing unless the installed-version docs and tests confirm it is safe for the workload.

## Performance Rules

- Avoid unnecessary conversions. Keep K objects in PyKX while q can do the work.
- Convert only needed columns/rows.
- Prefer q functions (`kx.q.avg`, `kx.q.sdev`, qSQL) for q/K data.
- Use IPC queries to prefilter on the server before data crosses the socket.
- Avoid converting large Python data to q repeatedly; Python-to-q copies.
- Use `QARGS="-s N"` before import to control q secondary threads. `-s 0` disables them.
- Do not call Python from q with `peach` unless `PYKX_RELEASE_GIL` is enabled and tested; default behavior can hang.

## Attributes

Use attributes only when the data shape is true and the query benefit is meaningful:

```python
quotes = quotes.grouped("sym")
sorted_times = times.sorted()
```

Misapplied attributes can error or be dropped by later operations. `parted` requires equal values to be contiguous. `grouped` is more flexible and survives inserts.

## Compression and Encryption

- Compression choices: IPC, gzip, snappy, lz4hc, zstd.
- Use per-write `compress=` or `encrypt=` on `DB.create` for partition-specific behavior.
- Use global init only when process-wide persistence settings are intended.
- Encryption needs a key path and password. Read passwords from a secret store or environment variable; never hard-code.
- TDE is transparent to queries but costs time.

## Pandas/Arrow Issues

- Pandas 2 behavior and Arrow-backed dtypes can change equality and dtype expectations.
- Prefer `pd.testing.assert_frame_equal` for tests instead of relying only on `DataFrame.equals`.
- PyArrow conversions require PyArrow installed; otherwise PyKX raises a PyArrow unavailable exception.

## Safe Review Checklist

- Are env vars set before import?
- Does the code assume licensed-only features in unlicensed mode?
- Are license contents, passwords, or credentials absent from examples and logs?
- Are partition predicates first for HDB queries?
- Is IPC using context managers and closing connections?
- Is `wait=False` only used when no response is expected?
- Are Python functions avoided as ordinary IPC payloads?
- Are embedded-q timers/server callbacks avoided in Python mode?
- Is `PyKXReimport` used for child processes?
- Is `kx.shutdown_thread()` called when `PYKX_THREADING` is enabled?
