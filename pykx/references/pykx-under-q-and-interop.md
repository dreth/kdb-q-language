# PyKX Under q and Interop

Source paths: `docs/pykx-under-q/{intro,api,upgrade}.md`,
`docs/user-guide/advanced/{context_interface,remote-functions,serialization,subprocess}.md`,
`docs/api/{remote,serialize,reimporting}.md`,
`src/pykx/{remote.py,serialize.py,reimporter.py}`.

Public docs: https://code.kx.com/pykx/pykx-under-q/intro.html

## When to Use This Mode

Use PyKX under q when a q process needs to run Python code, call Python libraries,
use q timers/subscriptions/main loop behavior, or migrate embedPy-style workloads.
It requires a licensed q/PyKX setup with PyKX/embedq feature flags.

Install into `QHOME`:

```sh
python -c "import pykx; pykx.install_into_QHOME()"
```

Load in q:

```q
q)\l pykx.q
```

## Execute Python from q

Evaluation vs execution:

```q
q).pykx.qeval"1+2"       / evaluate Python, return q
3

q)a:.pykx.pyeval"1+2"    / evaluate Python, return foreign
q)show a
foreign

q)b:.pykx.eval"1+2"      / wrapped foreign composition
q)b`                     / convert to q
3
q)b`.                    / get Python foreign
foreign

q).pykx.pyexec"import numpy as np"  / side effects
q).pykx.pyexec"x = np.arange(3)"
```

Use `.pykx.eval` for expressions without side effects. Use `.pykx.pyexec` for imports, assignments, function definitions, classes, and file-style setup.

## Foreign and Wrapped Objects

Foreign objects are pointers to Python memory inside the q process. q cannot serialize foreign objects or send them over IPC. Convert to q first when data must cross IPC.

```q
q)x:.pykx.eval"(1, 2, 3)"
q)x`     / q list
1 2 3
q)x`.    / Python foreign
foreign
```

Wrap a raw foreign:

```q
q)f:.pykx.pyeval"lambda x: x + 1"
q)wf:.pykx.wrap f
q)wf[4]`
5
```

## Conversion Defaults and Tags

Default q-to-Python argument conversion for Python callables:

- generic q lists -> Python lists
- q tables/keyed tables -> Pandas DataFrames
- most other q values -> NumPy equivalents

Change default:

```q
q).pykx.util.defaultConv:"py"
q).pykx.util.defaultConv:"np"
q).pykx.util.defaultConv:"pd"
q).pykx.util.defaultConv:"pa"
q).pykx.util.defaultConv:"k"
```

Or use per-argument tags:

```q
q)fn:.pykx.eval"lambda x, y: (type(x).__name__, type(y).__name__)"
q)fn[.pykx.topd ([] a:1 2); .pykx.tok 1 2 3]`
```

Tag choices:

| Tag | Python-side value |
| --- | --- |
| `.pykx.tok` | PyKX/K wrapper |
| `.pykx.topy` | Python native |
| `.pykx.tonp` | NumPy |
| `.pykx.topd` | Pandas |
| `.pykx.topa` | PyArrow |
| `.pykx.toraw` | raw representation |

Text conversion:

```q
q)s:.pykx.eval"'abc'"
q).pykx.toq s
`abc
q).pykx.toq0[s;1b]
"abc"
```

## None and `::`

Python `None` maps to q generic null `::`, but a single `::` argument to a PyKX-wrapped Python callable means "call with no arguments", not "call with one None".

```q
q)pynone:.pykx.eval"None"
q)printer:.pykx.eval"print"
q)printer pynone;
None
```

To preserve q `::` as q data, wrap it:

```q
q)f:.pykx.eval["lambda x: x";<]
q)(::)~f[.pykx.tok[::]]
1b
```

## Calling Python from q

Retrieve or import Python objects:

```q
q)np:.pykx.import`numpy
q)arange:np`:arange
q)arange[5]`
0 1 2 3 4

q).pykx.pyexec"def add(x, y): return x + y"
q)add:.pykx.get[`add;<]  / callable returning q
q)add[2;3]
5
```

Return controls:

```q
q)f:.pykx.eval["lambda x: x + 1";<]  / return q
q)g:.pykx.eval["lambda x: x + 1";>]  / return foreign
```

If passing `<`, `>`, `*`, `` ` ``, or `` `. `` as actual arguments, declare return type up front or wrap those arguments with `.pykx.tok`; otherwise they can be parsed as controls.

Keyword args:

```q
q)p)def func(a=1,b=2,c=3): return a+b+c
q)f:.pykx.get[`func;<]
q)f[1;`c pykw 10]
13
q)f[pykwargs `a`b!10 20]
33
```

Load `p.q` explicitly before defining scripts that use `pykw`, `pyarglist`, or `pykwargs`.

## Context Interface from Python

Use q namespaces as Python attributes:

```python
import pykx as kx

kx.q(".analytics.add:{x+y}")
assert kx.q.analytics.add(2, 3).py() == 5
```

If a namespace is missing, PyKX searches q/k scripts on `kx.q.paths`. For predictable auto-loading, one script should define one public context with a matching filename.

For IPC, the same interface works:

```python
with kx.SyncQConnection(port=5000) as q:
    q(".analytics.add:{x+y}")
    q.analytics.add(2, 3)
```

Use `no_ctx=True` when the context-interface overhead is not worth it.

## Remote Functions

Remote functions define Python locally and execute it on a q server that can load PyKX under q. Install `pykx[remote]` and ensure dependencies exist in the remote q/Python environment.

```python
import pykx as kx

session = kx.remote.session(host="localhost", port=5050, libraries={"kx": "pykx"})

@kx.remote.function(session)
def add_ten(x):
    return x + 10

add_ten(5)
```

Prefer `libraries={...}` or `session.libraries({...})` so imports are checked before functions run remotely.

## Serialization

Use pickle for Python-local persistence of pure PyKX objects, and `kx.serialize`/`kx.deserialize` for q IPC byte format.

```python
payload = kx.serialize(kx.q.til(5))
data = payload.copy()
assert kx.deserialize(data).py() == [0, 1, 2, 3, 4]
```

Do not deserialize untrusted bytes. `pykx.Foreign`, splayed tables, and partitioned tables are not general serializable values.

## Subprocesses

When a child Python process imports PyKX, launch under `PyKXReimport`:

```python
import subprocess
import pykx as kx

with kx.PyKXReimport():
    proc = subprocess.Popen(["python", "worker.py"])
```

Without this guard, inherited PyKX state can crash child processes.
