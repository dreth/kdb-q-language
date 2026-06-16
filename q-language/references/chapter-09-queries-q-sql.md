# 9. Queries: q-sql

Source URL: https://code.kx.com/q4m3/9_Queries_q-sql/

## Agent-Relevant Takeaways

- q-sql templates are q expressions for table work, not ANSI SQL.
- Main templates: `select`, `update`, `delete`, `insert`, and `upsert`.
- Phrase order matters: q-sql template order is `select ... by ... from ... where ...`, not ANSI SQL order.
- `where` filters are vector boolean expressions; multiple where subphrases are conjunctive.
- `by` groups and can also key results.
- Joins, parameterized queries, views, and functional forms support dynamic applications.

## q Syntax/Forms That Matter

- Select: `select cols by group from t where pred`
- Aggregate: `select avg px, sum size by sym from trades`
- Update: `update notional:px*size from trades`
- Delete rows/cols: `delete from t where pred`, `delete col from t`
- Insert/upsert: `insert[`t;row]`, `upsert[`t;rows]`
- Functional select: `?[t;where;by;select]`
- Common joins: `ij`, `lj`, `aj`, `wj`, `uj`

## Common Mistakes/Pitfalls

- Mixing SQL phrase order into q and producing invalid templates.
- Forgetting `insert` mutates a named table while many queries return new tables.
- Not enlisting singleton rows.
- Using dynamic q-sql strings when functional forms would be safer.
- Ignoring keyed-table semantics for upsert.

## Small Examples

```q
trades:([] sym:`IBM`IBM`MSFT; px:101 102 250f; size:100 50 200)
select vwap:size wavg px, volume:sum size by sym from trades where size>50

update side:$[px>200;`high;`low] from trades

/ Dynamic column selection with functional form pieces.
?[trades;enlist (>;`size;50);0b;`sym`px!`sym`px]
```

## Cross-Links

- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-06-functions.md](chapter-06-functions.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
