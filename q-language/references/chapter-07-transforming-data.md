# 7. Transforming Data

Source URL: https://code.kx.com/q4m3/7_Transforming_Data/

## Agent-Relevant Takeaways

- `type` is the first diagnostic for atom/list/table/dictionary behavior.
- Cast with type symbols or type chars; some casts widen safely, while narrowing can overflow or lose precision.
- `string`, `$`, `value`, and parsing forms bridge text and q values.
- Typed empty lists are required for robust schemas.
- Enumerations normalize repeated symbols and underpin foreign keys and persisted symbol domains.
- `sv` and `vs` join/split text or symbols and are safer building blocks than ad hoc concatenation.
- Parse text with expected types; use `value` only for controlled q expressions.

## q Syntax/Forms That Matter

- Type check: `type x`
- Cast: `` `int$42.0 ``, `"I"$"42"`
- Text conversion: `string x`, `value "1 2 3"`
- Split/join: `"," vs "a,b,c"`, `"," sv ("a";"b";"c")`
- Typed empty: `` `symbol$()``, `` `float$()``
- Enumeration: `city:`london`paris`, then `` `city$`london`paris`london ``; resolve with `value e`
- Fill/coalesce after cast: `^[0N;42]`

## Common Mistakes/Pitfalls

- Parsing untrusted text with `value` without controlling the input.
- Forgetting cast is atomic and applies across lists.
- Narrowing numeric data without checking range/null behavior.
- Misusing enumerations before the domain exists or failing to persist/load symbol domains with databases.
- Extending enum domains accidentally during ingest instead of validating against an expected set.
- Converting user text to symbols in a long-lived process without a bounded domain.
- Treating `"J"$txt` parsing failures as data-quality successes.

## Small Examples

```q
schema:([] sym:`symbol$(); ts:`timestamp$(); px:`float$(); size:`long$())
type each schema

`int$10.9 20.1
"J"$("100";"200";"300")

parts:"," vs "IBM,101.5,200"
(`symbol$first parts;"F"$parts 1;"J"$parts 2)

city:`london`paris
e:`city$`london`paris`london
value e
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
