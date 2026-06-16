# 14. Introduction to Kdb+

Source URL: https://code.kx.com/q4m3/14_Introduction_to_Kdb%2B/

## Agent-Relevant Takeaways

- kdb+ persists q tables as serialized, splayed, partitioned, or segmented data on disk.
- Splayed tables store each column as a separate file in a table directory.
- Partitioned tables add a partition directory, most often by date, so queries can prune data.
- Symbol columns in persisted databases require a symbol domain file, commonly `sym`.
- Query performance depends heavily on partition filters, column selection, attributes, and avoiding unnecessary materialization.

## q Syntax/Forms That Matter

- Serialize table: `` `:/db/t set t ``
- Splay: `` `:/db/trades/ set .Q.en[`:db] trades `` (adapt to actual database root/domain)
- Load database: `\l /path/to/db`
- Partitioned query pattern: `select ... from trades where date within d0 d1, sym in syms`
- Inspect: `tables[]`, `meta trades`, `count trades`
- Utility family: `.Q.*` helpers for enumeration, splay, and database operations.

## Common Mistakes/Pitfalls

- Querying partitioned tables without a partition constraint.
- Persisting symbol columns without managing the symbol file/domain.
- Treating splayed tables like ordinary in-memory tables for all updates.
- Appending data with mismatched schema or attributes.
- Forgetting `QHOME`/working-directory assumptions in scripts.

## Small Examples

```q
/ Shape a daily partition query to prune first, then aggregate.
select vwap:size wavg px by sym from trades
  where date=2026.06.16, sym in `IBM`MSFT
```

## Cross-Links

- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
- [chapter-11-io.md](chapter-11-io.md)
