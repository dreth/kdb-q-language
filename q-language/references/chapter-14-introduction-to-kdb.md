# 14. Introduction to Kdb+

Source URL: https://code.kx.com/q4m3/14_Introduction_to_Kdb%2B/

## Agent-Relevant Takeaways

- kdb+ persists q tables as serialized, splayed, partitioned, or segmented data on disk.
- Splayed tables store each column as a separate file in a table directory.
- Partitioned tables add a partition directory, most often by date, so queries can prune data.
- Symbol columns in persisted databases require a symbol domain file, commonly `sym`.
- Query performance depends heavily on partition filters, column selection, attributes, and avoiding unnecessary materialization.
- Mapped splayed/partitioned tables are not ordinary in-memory tables for every operation.
- Partitioned tables expose the partition as a virtual column, commonly `date`; `i` is row number within each partition.

## q Syntax/Forms That Matter

- Serialize table: `` `:/db/t set t ``
- Splay: `` `:/db/trades/ set .Q.en[`:db] trades `` (adapt to actual database root/domain)
- Load database: `\l /path/to/db`
- Partitioned query pattern: `select ... from trades where date within d0 d1, sym in syms`
- Daily partition write pattern: `` `:/db/2026.06.16/trades/ set .Q.en[`:db] delete date from dayTrades ``
- Inspect: `tables[]`, `meta trades`, `count trades`
- Utility family: `.Q.*` helpers for enumeration, splay, and database operations.

## Common Mistakes/Pitfalls

- Querying partitioned tables without a partition constraint.
- Persisting symbol columns without managing the symbol file/domain.
- Treating splayed tables like ordinary in-memory tables for all updates.
- Appending data with mismatched schema or attributes.
- Forgetting `QHOME`/working-directory assumptions in scripts.
- Using `exec from partitionedTable` directly where a `select` wrapper is needed.
- Filtering on virtual `i` without a partition constraint, returning rows from each partition.
- Persisting the virtual partition column inside each partition instead of removing it before write.

## Small Examples

```q
/ Shape a daily partition query to prune first, then aggregate.
select vwap:size wavg px by sym from trades
  where date=2026.06.16, sym in `IBM`MSFT

/ Write one date partition with enumerated symbols.
root:`:/db
`:/db/2026.06.16/trades/ set .Q.en[root] delete date from dayTrades
\l /db

/ Pull columns through select first, then exec from the smaller result.
exec px from select px from trades where date=2026.06.16, sym=`IBM
```

## Cross-Links

- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
- [chapter-11-io.md](chapter-11-io.md)
