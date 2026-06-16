# 8. Tables

Source URL: https://code.kx.com/q4m3/8_Tables/

## Agent-Relevant Takeaways

- A q table is a flipped column dictionary; columns are equal-length lists.
- Table definition syntax `([] c1:...; c2:...)` is preferred for clarity.
- Use `meta`, `cols`, `count`, `key`, and `value` to inspect tables and keyed tables.
- Keyed tables are dictionaries from key table to value table.
- Foreign keys and virtual columns let one table reference another.
- Attributes can improve search/sort/group performance but must match data properties.

## q Syntax/Forms That Matter

- Table: `([] sym:`IBM`MSFT; px:101.2 250.5)`
- Empty schema: `([] sym:`symbol$(); px:`float$())`
- Keyed table: `([sym:`IBM`MSFT] px:101.2 250.5)`
- Unkey: `0!kt`; key columns: `key kt`
- Metadata: `meta t`; column access: `t.sym`, `t[`sym]`
- Attribute apply: `` `s#xs ``, `` `p#xs ``, `` `g#xs ``

## Common Mistakes/Pitfalls

- Creating scalar columns without matching row count or `enlist`.
- Forgetting keyed tables are not the same shape as ordinary tables.
- Updating key columns as if they were normal value columns.
- Adding attributes to data that is not actually sorted/parted/grouped/unique.

## Small Examples

```q
trades:([] time:09:30 09:31 09:32; sym:`IBM`IBM`MSFT; px:101 102 250f; size:100 50 200)
meta trades
select last px by sym from trades

quotes:([sym:`IBM`MSFT] bid:100.9 249.8; ask:101.1 250.2)
quotes `IBM
```

## Cross-Links

- [chapter-05-dictionaries.md](chapter-05-dictionaries.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
