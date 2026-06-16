# 4. Operators

Source URL: https://code.kx.com/q4m3/4_Operators/

## Agent-Relevant Takeaways

- Operators and keywords are functions. Unary and binary forms can differ.
- q has no traditional operator precedence. Evaluation is "left of right": a function applies to the expression on its right.
- Many primitive functions are atomic: they automatically extend item-wise over lists.
- Match `~` tests structural equivalence; `=` tests item-wise equality.
- Amend `:` is the core update mechanism for lists, dictionaries, and tables.

## q Syntax/Forms That Matter

- Unary application: `f x`; binary application: `x f y`
- Equality/disequality: `=`, `<>`; match: `~`
- Arithmetic: `+`, `-`, `*`, `%`; integer division/modulus: `div`, `mod`
- Greater/lesser: `|`, `&`
- Amend: `@[target;index;fn]`, `.[target;path;fn]`
- Alias/view: `::`

## Common Mistakes/Pitfalls

- Writing arithmetic as if `*` binds tighter than `+`.
- Using `=` when a whole-result equality check needs `~`.
- Missing parentheses around the right argument of a binary operator.
- Confusing amend in-place effects with expressions that return modified copies.

## Small Examples

```q
/ Be explicit for generated code.
(2*3)+4
2*(3+4)

1 2 3 = 1 0 3
1 2 3 ~ 1 2 3

@[10 20 30;1;+;5]
```

## Cross-Links

- [chapter-01-q-shock-and-awe.md](chapter-01-q-shock-and-awe.md)
- [chapter-03-lists.md](chapter-03-lists.md)
- [chapter-06-functions.md](chapter-06-functions.md)
