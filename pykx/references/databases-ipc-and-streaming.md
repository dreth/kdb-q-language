# Databases, IPC, and Streaming

Source paths: `docs/user-guide/advanced/database/*`, `docs/user-guide/advanced/ipc.md`, `docs/user-guide/advanced/streaming/*`, `docs/api/{db,ipc,tick,compress}.md`, `src/pykx/{db.py,ipc.py,tick.py,compress_encrypt.py}`.

Public docs: https://code.kx.com/pykx/user-guide/advanced/database/index.html

## kdb+ Databases with `kx.DB`

PyKX `kx.DB` manages persisted kdb+ databases: splayed tables and partitioned tables.

- Splayed: one table split into column files. Good for medium-sized tables and column-subset access.
- Partitioned: one or more tables split by date/month/etc. All tables should follow the same partition structure.
- By default, load one database per Python process. Use `overwrite=True` to replace the loaded DB intentionally.

Create a partitioned DB:

```python
import pykx as kx

trade = kx.Table(data={
    "date": kx.random.random(100000, kx.DateAtom("today") - [1, 2, 3]),
    "time": kx.q.asc(kx.random.random(100000, kx.q("1D"))),
    "sym": kx.random.random(100000, ["AAPL", "MSFT"]),
    "price": kx.random.random(100000, 100.0),
})

db = kx.DB(path="/tmp/db")
db.create(trade, "trade", "date")
```

Create a splayed DB:

```python
db = kx.DB(path="/tmp/splay")
db.create(trade, "trade", format="splayed")
```

Load an existing DB:

```python
db = kx.DB(path="/tmp/db")
# or
db = kx.DB()
db.load("/tmp/db")
```

Replace loaded DB:

```python
db.load("/tmp/otherdb", overwrite=True)
```

## Extending and Managing DBs

Add a new partition:

```python
today_trade = kx.Table(data={
    "time": kx.q.asc(kx.random.random(10000, kx.q("1D"))),
    "sym": kx.random.random(10000, ["AAPL", "MSFT"]),
    "price": kx.random.random(10000, 100.0),
})
db.create(today_trade, "trade", kx.DateAtom("today"))
```

Add a new table to a partitioned DB:

```python
quote = kx.Table(data={
    "time": kx.q.asc(kx.random.random(10000, kx.q("1D"))),
    "sym": kx.random.random(10000, ["AAPL", "MSFT"]),
    "bid": kx.random.random(10000, 100.0),
    "ask": kx.random.random(10000, 100.0),
})
db.create(quote, "quote", kx.DateAtom("today"))
db.fill_database()
```

Call `fill_database()` when a newly added table is not present in older partitions; it creates empty table shells so the table is queryable across the database.

Schema changes mutate persisted data. Back up before changing production DBs:

```python
db.rename_column("trade", "sym", "symbol")
db.set_column_type("trade", "price", kx.RealAtom)
db.add_column("trade", "exchange", kx.SymbolAtom.null)

col_order = db.trade.columns.py()
db.copy_column("trade", "price", "price_copy")
db.apply_function("trade", "price_copy", lambda x: x * 0.5)
db.delete_column("trade", "price")
db.rename_column("trade", "price_copy", "price")
db.reorder_columns("trade", col_order)
```

## Compression and Encryption

Compression algorithms include IPC, gzip, snappy, lz4hc, and zstd.

```python
gzip = kx.Compress(algo=kx.CompressionAlgorithm.gzip, level=4)
db.create(trade, "trade", kx.DateAtom("today"), compress=gzip)
```

Encryption uses Data At Rest Encryption and requires an existing key path plus password. Do not hard-code passwords.

```python
encrypt = kx.Encrypt(path="/secure/path/key.key", password=os.environ["PYKX_DARE_PASSWORD"])
db.create(trade, "trade", kx.DateAtom("today"), encrypt=encrypt)
```

TDE is transparent to queries but adds overhead.

## IPC Connection Choices

| Class | Use |
| --- | --- |
| `kx.SyncQConnection` | normal request/response q IPC |
| `kx.AsyncQConnection` | `asyncio` event-loop integration |
| `kx.SecureQConnection` | TLS q IPC |
| `kx.RawQConnection` | manual receive/polling or Python-as-q-server |

Use context managers:

```python
with kx.SyncQConnection("localhost", 5000) as q:
    assert q("1+1").py() == 2
```

Authentication/TLS:

```python
with kx.SyncQConnection("host", 5000, username="user", password=os.environ["Q_PASSWORD"]) as q:
    q("til 3")

with kx.SyncQConnection("host", 5000, tls=True) as q:
    q("til 3")
```

Do not put real credentials in repo examples.

## IPC Calls

Call q text or q functions with parameters:

```python
with kx.SyncQConnection(port=5000, no_ctx=True) as q:
    q("til 10")
    q("{x+y+z}", 1, 2, 3)
    q("{[s] select from trade where date=2024.01.02, sym=s}", "AAPL")
```

Rules:

- Up to 8 query arguments.
- Python functions cannot be sent over ordinary IPC as data.
- Use `wait=False` for fire-and-forget messages; it returns `pykx.Identity`.
- Use `no_ctx=True` for KX Insights and hot paths where context-interface probes are unwanted.

```python
with kx.SyncQConnection(port=5010, wait=False, no_ctx=True) as q:
    q(".u.upd", "trade", msg)
```

Async:

```python
async with kx.AsyncQConnection("localhost", 5000) as q:
    fut = q("til 10")
    result = await fut
```

For deferred q responses, use `reuse=False` on the async call.

Raw receive loop:

```python
async with kx.RawQConnection(port=5013) as q:
    await q(".u.sub", "", "")
    while True:
        msg = q.poll_recv()
        if msg is None:
            continue
        table = msg[1]
        data = msg[2]
```

## Streaming / Real-Time Capture

PyKX streaming requires a q executable configured with `PYKX_Q_EXECUTABLE`/`QHOME` or available as `q`.

Prototype with `kx.tick.BASIC`:

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

Use explicit topology for controlled deployments:

```python
tick = kx.tick.TICK(port=5010, tables={"trade": trade_schema}, log_directory="log")
tick.start()

hdb = kx.tick.HDB(port=5012)
hdb.start(database="db")

rdb = kx.tick.RTP(port=5011)
rdb.start({"tickerplant": "localhost:5010", "hdb": "localhost:5012", "database": "db"})
```

Publish:

```python
msg = [kx.TimespanAtom("now"), "AAPL", 101.5, 100]
with kx.SyncQConnection(port=5010, wait=False, no_ctx=True) as q:
    q(".u.upd", "trade", msg)
```

Avoid slow subscribers on the primary tickerplant. For slow analytics, use a chained tickerplant:

```python
chained_tp = kx.tick.TICK(port=5013, chained=True)
chained_tp.start({"tickerplant": "localhost:5010"})
```

A chained tickerplant does not keep the authoritative log; keep a logging upstream tickerplant for replay.

RTP processors:

```python
def preprocessor(table, data):
    return data if table == "trade" else None

def postprocessor(table, data):
    agg = kx.q[table].select(
        columns={"max_price": "max price"},
        by={"sym": "sym"},
    )
    with kx.SyncQConnection(port=5010, wait=False, no_ctx=True) as q:
        q(".u.upd", "aggregate", agg._values)
    return None

rtp = kx.tick.RTP(
    port=5014,
    subscriptions=["trade"],
    libraries={"kx": "pykx"},
    pre_processor=preprocessor,
    post_processor=postprocessor,
    vanilla=False,
)
rtp.start({"tickerplant": "localhost:5013"})
```

Lifecycle:

```python
rtp.restart()
rtp.stop()
kx.util.kill_q_process(5010)  # use cautiously
```
