# 10. Execution Control

Source URL: https://code.kx.com/q4m3/10_Execution_Control/

## Agent-Relevant Takeaways

- q has conditional forms, loops, early return, signal, protected evaluation, debugging, and script loading.
- Prefer vector conditionals and q-sql/vector operations over `while` and `do` for data work.
- `$[...]` is an expression and returns a value; `if` is for side-effect statements and has no else result.
- Protected evaluation is essential around file, IPC, parse, and dynamic execution boundaries.

## q Syntax/Forms That Matter

- Conditional expression: `$[cond;trueExpr;falseExpr]`
- Vector conditional: `?[mask;trueValues;falseValues]`
- Statement conditional: `if[cond; expr1; expr2]`
- Loop: `do[n; expr]`, `while[cond; expr]`
- Return: `:value`; signal error: `'msg`
- Protected eval: `@[f;x;handler]`, `.[f;args;handler]`
- Load script: `\l file.q`

## Common Mistakes/Pitfalls

- Using `$[v;...]` to test null; test `null v` explicitly.
- Expecting `if` to return a useful else value.
- Writing loops for columnar data that should be vectorized.
- Swallowing errors in protected evaluation without surfacing context.

## Small Examples

```q
classify:{[px] $[px>100;`rich;`cheap]}
classify each 99 101 102

safeValue:{[txt] @[value;txt;{`parseFailed,x}]}
safeValue "1+2"
```

## Cross-Links

- [chapter-06-functions.md](chapter-06-functions.md)
- [chapter-11-io.md](chapter-11-io.md)
- [appendix-b-error-messages.md](appendix-b-error-messages.md)
