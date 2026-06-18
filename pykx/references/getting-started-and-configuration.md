# Getting Started and Configuration

Source paths: `README.md`, `docs/index.md`,
`docs/getting-started/{installing,quickstart,what_is_pykx}.md`,
`docs/learn/objects.md`, `docs/user-guide/configuration.md`,
`docs/user-guide/advanced/{modes,license}.md`,
`docs/help/{faq,troubleshooting}.md`.

Public docs: https://code.kx.com/pykx/getting-started/installing.html

## Mental Model

- PyKX is Python-first access to q/kdb+. It supports local embedded q/K objects, IPC to external q processes, and Python embedded inside q with PyKX under q.
- A PyKX object is a Python wrapper around a q/K object, usually in q memory. Creating wrappers is cheap; conversion out to Python/Pandas can copy or change types.
- Licensed mode unlocks embedded q execution, Pythonic table/query APIs, database
  loading, file I/O, PyKX under q, richer null/type handling, and human-readable
  reprs. Unlicensed mode is mainly Python<->q conversion plus IPC to licensed q
  servers.

## Install and Import

```sh
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install pykx
```

```python
import pykx as kx
```

Use extras only when needed:

```sh
pip install "pykx[pyarrow]"
pip install "pykx[remote]"
pip install "pykx[streaming]"
```

Verify package import:

```sh
python -c "import pykx; print(pykx.__version__)"
```

Verify embedded q when licensed:

```python
import pykx as kx
assert kx.q.til(5).py() == [0, 1, 2, 3, 4]
```

## Configuration Rules

- Set PyKX configuration before `import pykx`.
- Environment variables override `.pykx-config`.
- `.pykx-config` is TOML-like and searched in this order: current directory, `PYKX_CONFIGURATION_LOCATION`, then home directory.

Example:

```python
import os
os.environ["PYKX_QDEBUG"] = "1"
os.environ["PYKX_RELEASE_GIL"] = "1"
import pykx as kx
```

Common configuration names:

| Name | Use |
| --- | --- |
| `PYKX_QDEBUG` | q backtraces on `kx.q` errors |
| `PYKX_UNLICENSED` | force unlicensed mode |
| `PYKX_LICENSED` | fail import if licensed mode cannot initialize |
| `PYKX_THREADING` | run EmbeddedQ on a background thread |
| `PYKX_Q_EXECUTABLE` | q executable for streaming/tick subprocesses |
| `PYKX_4_1_ENABLED` | load q 4.1 libq when licensed |
| `PYKX_PROFILE` | select a `.pykx-config` profile in current source versions |
| `QARGS` | pass q startup flags such as `-s 0` |
| `QHOME`, `QLIC`, `QINIT` | q home, license directory, startup script |

## License Handling

Do not include license file contents or base64 license text in code, prompts, commits, logs, or examples.

Valid PyKX licensed mode needs a kdb Insights license with PyKX/embedq feature
flags. PyKX searches for `kx.lic`, `kc.lic`, and `k4.lic` in the current
directory, then `QLIC`, then `QHOME`. If no file is found, PyKX can use:

- `KDB_LICENSE_B64` for a base64 encoded `kc.lic`.
- `KDB_K4LICENSE_B64` for a base64 encoded `k4.lic`.

Programmatic checks:

```python
import pykx as kx
days = kx.license.expires()
```

Install or update a license from a secure local path:

```python
import pykx as kx
kx.license.install("/secure/path/kc.lic", force=True)
```

## Mode-Aware Coding

- If the task needs `kx.q("...")`, `kx.DB`, Query API with `kx.Column`, table indexing, casting, SQL, local file I/O, or PyKX under q, state that licensed mode is required.
- If the task only needs IPC to an existing q server or Python-to-q conversion, unlicensed mode may be enough.
- For CI without a license, force structural tests and conversion-only smoke tests with `PYKX_UNLICENSED=true`.

## q Executable

Most Python-side PyKX work does not need a standalone `q` executable. Real-Time Capture/tick workflows do. Configure:

```sh
export PYKX_Q_EXECUTABLE=/path/to/q
export QHOME=/path/to/qhome
```

PyKX can install q via `kx.util.install_q()`, but agents should avoid doing this silently in user repos.
