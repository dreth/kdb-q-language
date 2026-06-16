# 3. Lists

Source URL: https://code.kx.com/q4m3/3_Lists/

## Agent-Relevant Takeaways

- Lists are ordered and zero-indexed. Simple lists are homogeneous and contiguous; general lists can hold mixed or nested values.
- `count`, `first`, `last`, `til`, `where`, `take`, `drop`, `cut`, `raze`, and indexing patterns are core q building blocks.
- A list can act as a map from indices to values.
- Indexing can be repeated (`m[1][2]`) or done at depth (`m[1;2]`).
- List indexing accepts atoms, index lists, boolean masks via `where`, and nested paths.
- `#` and `_` are overloaded: take/reshape and drop/cut. Negative counts operate from the end.

## q Syntax/Forms That Matter

- Simple list: `10 20 30`
- General list: `(10;`a;"bc")`
- Empty general list: `()`; typed empty list: `` `long$()``
- Singleton list: `enlist 42`
- Join: `,`; fill/coalesce: `^`
- Indexing: `xs 0`, `xs[0 2]`, `xs[where xs>10]`
- Index at depth: `m[1;2]`, amend at depth: `.[m;1 2;+;10]`
- Shape: `n#xs`, `-n#xs`, `n_xs`, `-n_xs`, `raze nested`
- Indexed assignment: `xs[1]:99`, `xs[where xs>20]:0`
- Search/group: `xs?20`, `where mask`, `distinct xs`, `group xs`

## Common Mistakes/Pitfalls

- Forgetting `enlist` when constructing singleton lists, rows, or nested values.
- Creating a general list accidentally by mixing types when a simple typed list is needed.
- Confusing omitted index, empty index, and null item behavior.
- Assuming out-of-range indexing always errors; lists can return typed nulls in some contexts.
- Using `where` as a filter result instead of indices; apply it back to the list/table.
- Forgetting that `x 1 2` selects two items, while `x[1;2]` descends two levels.

## Small Examples

```q
xs:10 20 30 40
xs 1 3
xs where xs>25

nested:(1 2 3;10 20 30)
nested[1;2]

/ Boolean selection is two steps: make indices, then index.
idx:where xs within 20 40
xs idx

/ Matrix-style selection.
m:(1 2 3;10 20 30)
m[;1]
m[0 1;2]

/ Preserve nested rows with enlist.
(enlist `IBM`MSFT),enlist `AAPL
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-06-functions.md](chapter-06-functions.md)
