# 0. Overview

Source URL: https://code.kx.com/q4m3/0_Overview/

## Agent-Relevant Takeaways

- q is terse, array-oriented, column-oriented, and designed for high-volume time-series data.
- Lists, dictionaries, tables, and functions are best understood as mappings.
- q is interpreted: data and functions live in the workspace, scripts are text, and `parse`/`eval` expose code-as-data workflows.
- kdb+ stores q column lists with persistent backing; q is both query language and stored-procedure language.

## q Syntax/Forms That Matter

- Function application is central: `f x`, `f[x]`, `x g y`, and `g[x;y]`.
- `parse` converts text to q parse trees; `eval` evaluates q data/code.
- Ordered lists and columnar tables are the foundation for time-series operations.

## Common Mistakes/Pitfalls

- Translating object models directly into q. Use dictionaries and tables instead.
- Forgetting q table row order is meaningful, unlike classical SQL set semantics.
- Overusing dynamic `eval`; prefer explicit functions or functional query forms unless code generation is required.

## Small Examples

```q
sq:{x*x}
sq 6

/ A table is a column dictionary with display/query behavior.
t:([] time:09:30 09:31; sym:`AAPL`MSFT; px:187.2 421.5)
select avg px by sym from t
```

## Cross-Links

- [chapter-01-q-shock-and-awe.md](chapter-01-q-shock-and-awe.md)
- [chapter-05-dictionaries.md](chapter-05-dictionaries.md)
- [chapter-08-tables.md](chapter-08-tables.md)
