# Anti-Patterns

Common generated-code mistakes and the q idiom to use instead.

## SQL Literalism

Do not write ANSI SQL order or string SQL unless you are intentionally sending text to another system.

```q
/ q-sql
select avg px by sym from trades where date=2026.06.16
```

## Symbol and Backtick Confusion

Symbols are backtick values, not quoted strings. They are interned for the process lifetime.

```q
sym:`IBM
select from trades where sym=`IBM
```

Avoid converting unbounded user text to symbols in long-running processes; keep arbitrary identifiers as strings or enumerate against a controlled domain.

## Atom vs Singleton List

An atom is not a one-item list. Use `enlist` when shape matters.

```q
enlist `IBM
([] sym:enlist `IBM; px:enlist 101f)
```

This matters for table rows, functional q-sql constraints, and keyed-table lookup data.

## Keyed Tables Are Dictionaries

Do not treat keys as ordinary mutable columns. Unkey, change, and rekey when needed.

```q
kt:`sym xkey trades
kt ([] sym:`IBM`MSFT)
trades2:0!kt
```

Use `keys kt` for key column names and `key kt` for the key table.

## Row-Loop Thinking

Prefer vector expressions, q-sql, and joins over per-row loops.

```q
update notional:px*size from trades
select vwap:size wavg px by sym from trades
trades lj `sym xkey inst
```

Loops are usually a sign the table operation has not been expressed in q yet.

## Dynamic Query Strings

Prefer functional forms when names or filters are dynamic.

```q
c:enlist (=;`sym;enlist `IBM)
a:`sym`px!`sym`px
?[trades;c;0b;a]
```

Build constraints as a list, and enlist literal symbols inside parse-tree expressions.
