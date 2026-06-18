# Query and q Execution

Source paths: `docs/user-guide/fundamentals/evaluating.md`,
`docs/user-guide/fundamentals/query/{index,pyquery,sql,qquery,perf}.md`,
`docs/api/{query,columns}.md`, `docs/api/pykx-execution/q.md`,
`src/pykx/{embedded_q.py,query.py}`.

Public docs: https://code.kx.com/pykx/user-guide/fundamentals/query/index.html

## Choose the Query Surface

- Use the Pythonic Query API when composing structured filters, projections, updates, and groupings against PyKX table objects.
- Use SQL when the user supplies SQL or when prepared SQL improves repeated query execution.
- Use raw q/qSQL when the logic is q-specific, needs exact q syntax, or is already q code.
- Over IPC, prefer remote q functions and parameters over string interpolation.

## Local q Execution

Local embedded q execution requires licensed mode.

```python
import pykx as kx

kx.q("til 10")
kx.q("{x+y}", 2, 4)
kx.q("{[t;s] select from t where sym=s}", trades, "AAPL")
```

Rules:

- Python arguments are converted with `kx.toq`.
- q function calls take at most 8 arguments.
- Use `debug=True` for one call or `PYKX_QDEBUG=true` before import for q backtraces.

```python
kx.q("{x+1}", "bad", debug=True)
```

q keyword wrappers are available as attributes:

```python
v = kx.q.til(10)
ma = kx.q.mavg(3, v)
mx = kx.q.max([1, 4, 2])
```

Some q names conflict with Python syntax. Use `getattr(kx.q, "not")` or `kx.q("not")`.

## Query API

Create a table:

```python
trades = kx.Table(data={
    "sym": ["AAPL", "MSFT", "AAPL"],
    "date": [kx.DateAtom(2024, 1, 2)] * 3,
    "price": [101.5, 250.25, 102.0],
    "size": [100, 200, 50],
})
```

Filter, project, aggregate:

```python
from pykx import Column as C

aapl = trades.select(where=C("sym") == "AAPL")
vwap = trades.select(
    columns={"vwap": C("size").wavg(C("price")), "volume": C("size").sum()},
    by=C("sym"),
)
px = trades.exec(columns=C("price"))
```

Update and delete:

```python
with_notional = trades.update(columns=(C("price") * C("size")).name("notional"))
no_msft = trades.delete(where=C("sym") == "MSFT")
```

Important support limits:

| Operation | In-memory table | Splayed | Partitioned |
| --- | --- | --- | --- |
| `select` | yes | yes | yes |
| `exec` | yes | yes | no |
| `update`/`delete` | returns updated table | returns table, does not modify disk | no |

`kx.Column` expression support is licensed-mode functionality. In unlicensed mode, use string query expressions where the API permits them.

## SQL

Use `kx.q.sql` or table `.sql()`:

```python
kx.q["trades"] = trades
kx.q.sql("select * from trades where sym = 'AAPL'")
kx.q.sql("select * from $1 where price > $2", trades, 100.0)
trades.sql("select * from $1 where price > 100")
```

For repeated SQL, prepare once and execute repeatedly:

```python
prepared = kx.q.sql.prepare("select * from trades where sym=$1")
res = kx.q.sql.execute(prepared, "AAPL")
```

Keep prepared argument types consistent with the prepared prototype. Avoid injecting large client-side tables into remote IPC SQL with `$1`; use server-side table names or create the table on the server first.

If SQL fails to load, set `PYKX_DEBUG_INSIGHTS_LIBRARIES=true` before import to get a better error.

## Raw q/qSQL

Use qSQL directly when needed:

```python
kx.q["trades"] = trades
kx.q("select from trades where sym=`AAPL")
kx.q("{[t;s;minpx] select from t where sym=s, price>minpx}", trades, "AAPL", 100.0)
```

Use raw q for q-only functions such as `aj`, keyed-table manipulation, attributes, functional qSQL, complex lambdas, or when porting existing q.

## HDB Query Performance

For partitioned databases, put the partition predicate first:

```python
trade.select(where=(C("date") == kx.DateAtom(2024, 1, 2)) & (C("sym") == "IBM"))
```

Avoid:

```python
trade.select(where=(C("sym") == "IBM") & (C("date") == kx.DateAtom(2024, 1, 2)))
```

For in-memory repeated symbol filters on large tables, apply attributes when the data shape supports them:

```python
quotes = quotes.grouped("sym")
quotes.select(where=C("sym") == "IBM")
```

Attribute reminders:

- `sorted` helps ordered searches.
- `unique` asserts no duplicates.
- `grouped` builds lookup metadata and survives inserts.
- `parted` can be faster than grouped but requires equal values to be contiguous.
- Setting attributes costs resources; use them where query speed matters on large data.

## IPC Query Notes

Over IPC:

```python
with kx.SyncQConnection("localhost", 5000, no_ctx=True) as q:
    q("{[s] select from trade where date=2024.01.02, sym=s}", "AAPL")
```

If using the context interface:

```python
with kx.SyncQConnection("localhost", 5000) as q:
    q(".analytics.vwap:{[s] select vwap:size wavg price by sym from trade where sym=s}")
    q.analytics.vwap("AAPL")
```

The context interface sends extra probes. Disable it with `no_ctx=True` on performance-sensitive paths or KX Insights connections.
