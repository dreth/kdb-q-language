# 1. Q Shock and Awe

Source URL: https://code.kx.com/q4m3/1_Q_Shock_and_Awe/

## Agent-Relevant Takeaways

- This chapter is the fastest orientation to q syntax: assignment, comments, evaluation order, atoms, lists, functions, dictionaries, tables, q-sql, I/O, IPC, and WebSockets.
- Assignment uses `:`. Equality uses `=`.
- q reads left to right but evaluates function application right to left; there is no conventional arithmetic precedence.
- q examples often rely on the console. Script code should be explicit about names, semicolons, and side effects.

## q Syntax/Forms That Matter

- Assignment: `name:value`
- Line comment: `/ text`; multi-line comment blocks are script-oriented.
- Function: `{[x;y] x+y}`; implicit arguments: `x`, `y`, `z`.
- List: `1 2 3`; general list: `(1;`a;"bc")`
- Dictionary: `` `a`b!10 20 ``
- Table: `([] c1:1 2; c2:`a`b)`
- q-sql: `select cols by group from t where pred`

## Common Mistakes/Pitfalls

- Writing `a=42` for assignment.
- Assuming `2*3+4` means `(2*3)+4`; in q, add parentheses when precedence matters.
- Missing `enlist` for singleton rows or singleton keyed-table records.
- Treating strings and symbols interchangeably.

## Small Examples

```q
price:101.5 102.0 100.75
qty:200 150 300
notional:price*qty

trades:([] sym:`IBM`IBM`MSFT; px:101.5 102.0 300.2; size:200 150 50)
select vwap:size wavg px by sym from trades
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-03-lists.md](chapter-03-lists.md)
- [chapter-06-functions.md](chapter-06-functions.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
