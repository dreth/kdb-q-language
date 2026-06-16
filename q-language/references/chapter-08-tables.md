# 8. Tables

Source URL: https://code.kx.com/q4m3/8_Tables/

## Agent-Relevant Takeaways

- A q table is a flipped column dictionary; columns are equal-length lists.
- Table definition syntax `([] c1:...; c2:...)` is preferred for clarity.
- Use `meta`, `cols`, `count`, `key`, and `value` to inspect tables and keyed tables.
- Keyed tables are dictionaries from key table to value table.
- Foreign keys and virtual columns let one table reference another.
- Attributes can improve search/sort/group performance but must match data properties.
- Use `xkey` or keyed-table definition syntax to key by one or more columns; use `0!kt` to unkey.
- A table row is a dictionary; selecting multiple keyed rows requires key-shaped data, often via `([] keycol:...)`.
- `key kt` returns the key table; `keys kt` returns key column names.

## q Syntax/Forms That Matter

- Table: `([] sym:`IBM`MSFT; px:101.2 250.5)`
- Empty schema: `([] sym:`symbol$(); px:`float$())`
- Keyed table: `([sym:`IBM`MSFT] px:101.2 250.5)`
- Key/unkey: `` `sym xkey t ``, `0!kt`; key data: `key kt`; key names: `keys kt`
- Metadata: `meta t`; column access: `t.sym`, `t[`sym]`
- Records: `first t`, `t 0`, `t[0;`px]`, `enlist rowdict`
- Attribute apply: `` `s#xs ``, `` `p#xs ``, `` `g#xs ``

## Common Mistakes/Pitfalls

- Creating scalar columns without matching row count or `enlist`.
- Forgetting keyed tables are not the same shape as ordinary tables.
- Updating key columns as if they were normal value columns.
- Adding attributes to data that is not actually sorted/parted/grouped/unique.
- Looking up a keyed table with a bare symbol when the key shape is a row/table.
- Assuming `key kt` returns just column names; it returns the key table.
- Assuming key values are always unique; duplicate keys can make lookup/update results surprising.

## Small Examples

```q
trades:([] time:09:30 09:31 09:32; sym:`IBM`IBM`MSFT; px:101 102 250f; size:100 50 200)
meta trades
select last px by sym from trades

quotes:([sym:`IBM`MSFT] bid:100.9 249.8; ask:101.1 250.2)
quotes `IBM

kt:`sym xkey trades
keys kt
key kt
kt ([] sym:`IBM`MSFT)

kt2:`sym`time xkey trades
kt2 ([] sym:`IBM`IBM; time:09:30 09:31)
0!kt
```

## Cross-Links

- [chapter-05-dictionaries.md](chapter-05-dictionaries.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
