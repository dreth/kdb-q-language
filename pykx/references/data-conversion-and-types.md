# Data Conversion and Types

Source paths: `docs/learn/objects.md`,
`docs/user-guide/fundamentals/{creating,evaluating,indexing,conversion_considerations,text,nulls_and_infinities,temporal}.md`,
`docs/api/pykx-q-data/{toq,wrappers,type_conversions}.md`,
`src/pykx/toq.pyx`, `src/pykx/wrappers.py`.

Public docs: https://code.kx.com/pykx/user-guide/fundamentals/creating.html

## Defaults

- PyKX objects are `pykx.K` wrappers over q memory. Keep them as K/PyKX while using q analytics.
- Convert into PyKX with `kx.toq`. Convert out with `.py()`, `.np()`, `.pd()`, `.pa()`, or `.pt()` beta.
- Python data passed to q functions, IPC calls, and indexes is converted through `kx.toq`.
- Python-to-q conversion copies data. q-to-NumPy/Pandas conversion often avoids copies; `.py()` generally copies.

```python
import pykx as kx
import pandas as pd

qv = kx.toq([1, 2, 3])
qt = kx.toq(pd.DataFrame({"sym": ["AAPL", "MSFT"], "px": [101.5, 250.25]}))

assert qv.py() == [1, 2, 3]
df = qt.pd()
```

## Creating Objects

Prefer `kx.toq` for ordinary conversion and explicit constructors for schemas or q-specific values.

```python
import pykx as kx

v = kx.toq([1, 2, 3], ktype=kx.FloatVector)
t = kx.Table(data={
    "sym": kx.toq(["AAPL", "MSFT"]),
    "price": kx.toq([101.5, 250.25], ktype=kx.FloatVector),
    "size": kx.toq([100, 200], ktype=kx.LongVector),
})
```

For tabular column type control:

```python
qt = kx.toq(df, ktype={"price": kx.FloatVector, "size": kx.LongVector})
```

Dictionary-based `ktype` for tables is licensed-mode functionality.

## Assigning to q Memory

Prefer item assignment:

```python
kx.q["trades"] = t
assert kx.q["trades"].py() is not None
```

Avoid `kx.q.trades = t`; attribute assignment can place data under a dotted name such as `.trades`.

## Text: Symbol vs Char

Python `str` defaults to q symbol:

```python
kx.toq("abc")                         # SymbolAtom: `abc
kx.toq("abc", ktype=kx.CharVector)    # CharVector: "abc"
kx.toq("abc", strings_as_char=True)   # CharVector: "abc"
```

Use symbols for low-cardinality repeated values such as tickers, table names, and
enum-like categories. Use char vectors for free text, mutable text, logs, IDs
with unbounded cardinality, or text where per-character access matters. Symbols
are interned and are not deallocated in the q process.

`bytes` maps to char data:

```python
kx.toq(b"a")      # CharAtom
kx.toq(b"abc")    # CharVector
```

## Nulls and Infinities

Use typed values instead of raw sentinels:

```python
kx.LongAtom.null
kx.TimespanAtom.null
kx.IntAtom.inf
kx.IntAtom.inf_neg
kx.SymbolAtom.null
```

Check values with q or wrapper properties:

```python
x = kx.q("0N 1 2")
assert x.has_nulls
assert kx.q("0n").is_null
assert kx.q("0w").is_inf
```

Pitfalls:

- q char null is a space; a char vector containing spaces can report `has_nulls`.
- q symbol null is the empty symbol.
- Integral nulls in Python/NumPy/Pandas/PyArrow may become nullable arrays, masked arrays, or raw sentinel values depending on conversion mode.
- If you need nullable integral columns in Python, prefer `.pd()` or `.pa()` over plain `.np()` when the mask matters.

## Temporals

q timestamp epoch starts at 2000; Python/NumPy epoch starts at 1970. Safe direct nanosecond timestamp range is roughly:

- Minimum: `1707-09-22T00:12:43.145224194`
- Maximum: `2262-04-11T23:47:16.854775807`

Use `handle_nulls=True` when converting `NaT` values into q:

```python
import numpy as np

arr = np.array(["NaT", "2024-01-01T12:00:00"], dtype="datetime64[ns]")
qts = kx.toq(arr, handle_nulls=True)
```

Use `raw=True` only when you want underlying numeric values and will handle epoch/null/infinity semantics yourself:

```python
raw_ns = kx.q("0N -0W 0Wp").np(raw=True)
```

Python native datetime only stores microseconds, so round-tripping q nanosecond timestamps through `.py()` loses precision.

## Indexing and Mutation

PyKX indexing follows Python syntax but q semantics are underneath. Index arguments are converted with `kx.toq`.

```python
v = kx.q.til(10)
assert v[2].py() == 2
assert v[-1].py() == 9
assert v[2:5].py() == [2, 3, 4]

v[1] = 100
```

Table slicing returns table-like objects:

```python
head = trades[:5]
row = trades[0]
```

Nested list element assignment is not generally supported as an in-place deep mutation.

## Nested Lists

`pykx.List.np()` defaults to object arrays for mixed or ragged lists. For regular numeric N-dimensional lists, use reshape:

```python
arr = kx.random.random([2, 2, 2], 5.0).np(reshape=True)
fast = big_regular_list.np(reshape=[10000, 100, 10])
```

Pass explicit shape when known; it avoids expensive shape discovery.

## Performance Conversion Rules

- Filter or select in q first; convert only the subset required by Python.
- Convert table columns, not whole tables, when the Python consumer needs only a few columns.
- Use `.np()`/`.pd()` over `.py()` where practical.
- Avoid nested columns when converting q tables to Pandas; they can force copying.
- Use `raw=True` only for controlled fast paths where adjusted temporal/GUID/text semantics are not needed.
