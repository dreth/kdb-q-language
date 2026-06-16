# 9. Queries: q-sql

Source URL: https://code.kx.com/q4m3/9_Queries_q-sql/

## Agent-Relevant Takeaways

- q-sql templates are q expressions for table work, not ANSI SQL.
- Main templates: `select`, `update`, `delete`, `insert`, and `upsert`.
- Phrase order matters: q-sql template order is `select ... by ... from ... where ...`, not ANSI SQL order.
- `where` filters are vector boolean expressions; multiple where subphrases are conjunctive.
- `by` groups and can also key results.
- Joins, parameterized queries, views, and functional forms support dynamic applications.
- `exec` returns column values or dictionaries rather than a table; use it for extraction, not row-preserving results.
- Functional forms mirror templates: `?` for select/exec and `!` for update/delete.
- Join choice depends on key shape, duplicate handling, temporal ordering, and whether unmatched left rows must survive.

## q Syntax/Forms That Matter

- Select: `select cols by group from t where pred`
- Exec: `exec px by sym from trades`
- Aggregate: `select avg px, sum size by sym from trades`
- Group-relative filter: `select from trades where px=max px fby sym`
- Update: `update notional:px*size from trades`
- Delete rows/cols: `delete from t where pred`, `delete col from t`
- Insert/upsert: `insert[`t;row]`, `upsert[`t;rows]`
- Functional select/exec: `?[t;constraints;by;select]`
- Functional update/delete: `![t;constraints;by;updates]`
- Functional dictionaries: `select`/`updates` are `` `newcol``, expressions; `by` is `0b` or a grouping dictionary.
- Common joins: `lj`, `ij`, `ej`, `pj`, `aj`, `wj`, `uj`, `,`
- Join operand rules: `lj`/`ij` commonly take an unkeyed left table and keyed right table; `ej` takes join columns plus two tables; `aj`/`wj` require ordered temporal columns.

## Common Mistakes/Pitfalls

- Mixing SQL phrase order into q and producing invalid templates.
- Forgetting `insert` mutates a named table while many queries return new tables.
- Not enlisting singleton rows.
- Using dynamic q-sql strings when functional forms would be safer.
- Ignoring keyed-table semantics for upsert.
- Building functional `where` with a bare predicate instead of a list of constraints.
- Forgetting to enlist literal symbols in functional expressions, e.g. `` (=;`sym;enlist `IBM) ``.
- Using `uj` for conforming tables when `,` or `raze` is cheaper.
- Running `aj` on unsorted temporal data or with the time column in the wrong join-column position.

## Small Examples

```q
trades:([] time:2026.06.16D09:30 2026.06.16D09:31 2026.06.16D09:32; sym:`IBM`IBM`MSFT; px:101 102 250f; size:100 50 200)
select vwap:size wavg px, volume:sum size by sym from trades where size>50

update side:$[px>200;`high;`low] from trades

/ Dynamic column selection with functional form pieces.
?[trades;enlist (>;`size;50);0b;`sym`px!`sym`px]

/ Dynamic aggregate by symbol.
?[trades;();enlist[`sym]!enlist `sym;enlist[`vwap]!enlist (wavg;`size;`px)]

/ Functional update/delete by table name.
![`trades;enlist (=;`sym;enlist `IBM);0b;(enlist `notional)!enlist (*;`px;`size)]
![`trades;enlist (<;`size;100);0b;()]

/ Join operand shapes.
inst:([] sym:`IBM`MSFT; sector:`tech`tech)
trades lj `sym xkey inst
ej[`sym;trades;inst]

/ As-of join: quote current at each trade time.
quotes:([] time:2026.06.16D09:29 2026.06.16D09:31; sym:`IBM`IBM; bid:100 101f; ask:101 102f)
aj[`sym`time;trades;quotes]

w:-0D00:00:02.000000000 0D00:00:01.000000000+\:trades`time
wj[w;`sym`time;trades;(quotes;(max;`ask);(min;`bid))]
```

## Cross-Links

- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-06-functions.md](chapter-06-functions.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
