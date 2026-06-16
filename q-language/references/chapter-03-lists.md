# 3. Lists

Source URL: https://code.kx.com/q4m3/3_Lists/

## Agent-Relevant Takeaways

- Lists are ordered and zero-indexed. Simple lists are homogeneous and contiguous; general lists can hold mixed or nested values.
- `count`, `first`, `last`, `til`, `where`, `take`, `drop`, `cut`, `raze`, and indexing patterns are core q building blocks.
- A list can act as a map from indices to values.
- Indexing can be repeated (`m[1][2]`) or done at depth (`m[1;2]`).

## q Syntax/Forms That Matter

- Simple list: `10 20 30`
- General list: `(10;`a;"bc")`
- Empty general list: `()`; typed empty list: `` `long$()``
- Singleton list: `enlist 42`
- Join: `,`; fill/coalesce: `^`
- Indexing: `xs 0`, `xs[0 2]`, `xs[where xs>10]`

## Common Mistakes/Pitfalls

- Forgetting `enlist` when constructing singleton lists, rows, or nested values.
- Creating a general list accidentally by mixing types when a simple typed list is needed.
- Confusing omitted index, empty index, and null item behavior.
- Assuming out-of-range indexing always errors; lists can return typed nulls in some contexts.

## Small Examples

```q
xs:10 20 30 40
xs 1 3
xs where xs>25

nested:(1 2 3;10 20 30)
nested[1;2]
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-06-functions.md](chapter-06-functions.md)
