# Appendix A. Built-in Functions

Source URL: https://code.kx.com/q4m3/A_Built-in_Functions/

## Agent-Relevant Takeaways

- Appendix A is a lookup catalog for q built-ins. Read it when choosing a primitive instead of hand-writing logic.
- Many built-ins have unary and binary forms; verify which valence you need.
- Prefer built-ins for aggregation, searching, grouping, sorting, text processing, math, time-series deltas, moving windows, and list reshaping.

## q Syntax/Forms That Matter

- Aggregates: `sum`, `avg`, `min`, `max`, `prd`, `dev`, `var`, `med`, `wavg`, `wsum`
- Running/moving: `sums`, `avgs`, `deltas`, `ratios`, `mavg`, `msum`, `prev`, `next`, `xprev`
- Selection/search: `where`, `find`/`?`, `in`, `within`, `bin`, `binr`, `like`, `ss`, `ssr`
- Shape/list: `count`, `til`, `take`/`#`, `drop`/`_`, `cut`, `raze`, `enlist`, `flip`, `ungroup`
- Sort/group: `asc`, `desc`, `iasc`, `idesc`, `group`, `distinct`, `rank`, `xrank`
- Evaluation/system: `parse`, `eval`, `value`, `system`, `getenv`, `setenv`

## Common Mistakes/Pitfalls

- Reimplementing built-ins with loops.
- Forgetting aggregate behavior on nulls differs by function and type.
- Confusing keyword names with operator glyphs, especially `?`, `#`, `_`, `,`, `^`.
- Using parallel `peach` where side effects or ordering assumptions make it unsafe.

## Small Examples

```q
px:100 101 103 102f
deltas px
3 mavg px

t:([] sym:`A`A`B; px:10 11 20f)
select last px, max px by sym from t
```

## Cross-Links

- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-06-functions.md](chapter-06-functions.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
