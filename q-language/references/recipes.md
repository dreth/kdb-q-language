# Recipes

Use these as compact starting points for common q/kdb+ tasks. Confirm column names and types with `meta`, `cols`, `count`, and small bounded probes before broad queries.

## Load CSV

```q
/ Header row names the columns; schema chars type the data rows.
p:`$":/data/prices.csv"
prices:("SFJ";enlist ",") 0:p
meta prices
```

For nonstandard text, read lines with `read0`, drop or transform headers deliberately, then parse; do not assume ANSI SQL import behavior.

## Create and Use Keyed Tables

```q
quotes:([sym:`IBM`MSFT] bid:100.9 249.8; ask:101.1 250.2)
quotes `IBM

trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
kt:`sym xkey trades
kt ([] sym:`IBM`MSFT)
0!kt
```

Use key-shaped lookup data for multi-row keyed-table access. `key kt` returns key data; `keys kt` returns key column names.

## q-sql Aggregation

```q
trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
select vwap:size wavg px, volume:sum size, hi:max px by sym from trades where size>0
```

q-sql phrase order is `select ... by ... from ... where ...`. `where` predicates are vector expressions and multiple comma-separated predicates are conjunctive.

## Debug Rank and Type Errors

```q
type x
count x
0N!x
meta t
enlist x
```

Check whether a value is an atom, singleton list, table row, or one-row table. Use `enlist` to preserve a single row/list/key; use typed empties like `` `long$()`` in schemas.

## Query Partitioned Tables

```q
\l /data/hdb
meta trade
select[10] from trade where date=2026.06.16,sym=`IBM
select sum size by sym from trade where date within 2026.06.10 2026.06.16,sym in `IBM`MSFT
```

Put the partition constraint first, keep probes bounded, and avoid unqualified `select from bigtable` on HDB data.

## Build Time-Series Joins

```q
quotes:`sym`time xasc quotes
trades:`sym`time xasc trades
aj[`sym`time;trades;quotes]
```

Use `aj` for latest quote at or before each trade. Ensure the temporal column is last in the join column list and both tables are ordered by symbol/time.
