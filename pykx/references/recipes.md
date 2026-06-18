# Recipes

Source paths: task examples from `docs/user-guide/fundamentals/*`, `docs/user-guide/fundamentals/query/*`, `docs/user-guide/advanced/{database,ipc,streaming,context_interface,serialization}.md`.

## Import with Config

```python
import os

os.environ.setdefault("PYKX_QDEBUG", "1")
import pykx as kx
```

For conversion-only CI without a license:

```python
import os

os.environ["PYKX_UNLICENSED"] = "1"
import pykx as kx
assert kx.toq([1, 2, 3]).py() == [1, 2, 3]
```

## Build a Typed Table

```python
import pykx as kx

trades = kx.Table(data={
    "sym": kx.toq(["AAPL", "MSFT", "AAPL"], ktype=kx.SymbolVector),
    "price": kx.toq([101.5, 250.25, 102.0], ktype=kx.FloatVector),
    "size": kx.toq([100, 200, 50], ktype=kx.LongVector),
})
```

## Keep Free Text as Char Vectors

```python
comments = kx.toq(["ok", "needs review"], strings_as_char=True)
one = kx.CharVector("free-form text")
```

## Handle Nullable Time Data

```python
import numpy as np
import pykx as kx

arr = np.array(["NaT", "2024-01-01T09:30:00"], dtype="datetime64[ns]")
qts = kx.toq(arr, handle_nulls=True)
```

## Execute q Safely

```python
import pykx as kx

res = kx.q("{[x;y] x+y}", 2, 4)
assert res.py() == 6
```

Use q backtraces on one call:

```python
kx.q("{x+1}", "bad", debug=True)
```

## Query API VWAP

```python
import pykx as kx

C = kx.Column
vwap = trades.select(
    columns={
        "vwap": C("size").wavg(C("price")),
        "volume": C("size").sum(),
    },
    by=C("sym"),
)
```

## HDB Query with Partition Predicate First

```python
C = kx.Column
res = db.trade.select(
    where=(C("date") == kx.DateAtom(2024, 1, 2)) & (C("sym") == "AAPL"),
    columns=C("sym") & C("price") & C("size"),
)
```

## SQL with Parameters

```python
kx.q["trades"] = trades
res = kx.q.sql(
    "select * from trades where sym=$1 and price>$2",
    "AAPL",
    100.0,
)
```

Prepared:

```python
prepared = kx.q.sql.prepare("select * from trades where sym=$1")
res = kx.q.sql.execute(prepared, "AAPL")
```

## Create and Extend a DB

```python
db = kx.DB(path="/tmp/db")
db.create(trades, "trade", "date")

today = trades.delete(columns=kx.Column("date"))
db.create(today, "trade", kx.DateAtom("today"))
```

Add a new table:

```python
db.create(quote, "quote", kx.DateAtom("today"))
db.fill_database()
```

## IPC Request/Response

```python
with kx.SyncQConnection("localhost", 5000, no_ctx=True) as q:
    res = q("{[s] select from trade where date=2024.01.02, sym=s}", "AAPL")
```

## IPC Fire-and-Forget Publish

```python
msg = [kx.TimespanAtom("now"), "AAPL", 101.5, 100]
with kx.SyncQConnection("localhost", 5010, wait=False, no_ctx=True) as q:
    q(".u.upd", "trade", msg)
```

## Async IPC

```python
async with kx.AsyncQConnection("localhost", 5000) as q:
    future = q("til 10")
    result = await future
```

## Basic Streaming Prototype

```python
trade_schema = kx.schema.builder({
    "time": kx.TimespanAtom,
    "sym": kx.SymbolAtom,
    "price": kx.FloatAtom,
    "volume": kx.LongAtom,
})

basic = kx.tick.BASIC(
    tables={"trade": trade_schema},
    log_directory="log",
    database="db",
)
basic.start()
```

## Python in q

```q
q)\l pykx.q
q).pykx.pyexec"import numpy as np"
q).pykx.qeval"1+2"
3
q)np:.pykx.import`numpy
q)np[`:arange;5]`
0 1 2 3 4
```

## Remote Python Function on q Server

```python
session = kx.remote.session(host="localhost", port=5050, libraries={"kx": "pykx"})

@kx.remote.function(session)
def add_ten(x):
    return x + 10
```

## Serialize q IPC Bytes

```python
payload = kx.serialize(kx.q.til(5))
data = payload.copy()
roundtrip = kx.deserialize(data)
```

## Subprocess Launch

```python
with kx.PyKXReimport():
    proc = subprocess.Popen(["python", "worker.py"])
```
