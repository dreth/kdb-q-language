# 6. Functions

Source URL: https://code.kx.com/q4m3/6_Functions/

## Agent-Relevant Takeaways

- q functions are data and can be assigned, passed, projected, and applied dynamically.
- Explicit parameters use `{[x;y] ...}`; implicit parameters `x`, `y`, `z` are available for short lambdas.
- q uses call-by-name evaluation for function arguments, which matters for side effects and repeated evaluation.
- Projection fixes some arguments and returns a new function.
- Iterators (`each`, `over`, `scan`, etc.) are essential for idiomatic q.

## q Syntax/Forms That Matter

- Function definition: `f:{[x;y] x+y}`
- Anonymous function call: `{x*x} 5`
- Nullary function: `{[] .z.P}`
- Early return/signal: `:value`, `'error`
- Projection: `add10:+[10;]`, `within5_9:within[;5 9]`
- Identity: `::`

## Common Mistakes/Pitfalls

- Overusing explicit loops instead of atomic functions or iterators.
- Using globals accidentally from inside functions.
- Forgetting semicolons separate expressions inside function bodies.
- Creating projections with omitted arguments in the wrong position.
- Assuming every function is atomic; user functions need `each` or explicit atomic construction when list behavior differs.

## Small Examples

```q
vwap:{[px;sz] sz wavg px}
vwap[101 102 103;100 200 100]

scale:{[m;x] m*x}
double:scale[2;]
double 10 20 30
```

## Cross-Links

- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-10-execution-control.md](chapter-10-execution-control.md)
- [appendix-a-built-in-functions.md](appendix-a-built-in-functions.md)
