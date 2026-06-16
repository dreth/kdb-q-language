# Appendix B. Error Messages

Source URL: https://code.kx.com/q4m3/B_Error_Messages/

## Agent-Relevant Takeaways

- q errors are terse. Diagnose by mapping the symbol to category: runtime, parse, system, or license.
- Start with the expression shape: valence, type, rank, length, name resolution, and parse structure.
- Use smaller expressions, `type`, `count`, `meta`, and protected evaluation to isolate the failing part.

## q Syntax/Forms That Matter

- Protected unary evaluation: `@[f;x;{x}]`
- Protected multi-arg evaluation: `.[f;args;{x}]`
- Debug prompt appears after unhandled errors in interactive sessions; inspect variables before exiting.
- Common signals: `'type`, `'length`, `'rank`, `'domain`, `'parse`, `'value`

## Common Mistakes/Pitfalls

- Treating the error text as a complete diagnosis. It is usually only the first clue.
- Fixing symptoms without checking atom/list rank.
- Ignoring parse errors caused by missing whitespace around names or invalid q-sql phrase order.
- Missing license/system errors that are unrelated to code logic.

## Small Examples

```q
safe:{[f;x] @[f;x;{`error`detail!(x;y)}]}
safe[{x+1};"abc"]

type each (1;1 2;"ab";`ab)
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-10-execution-control.md](chapter-10-execution-control.md)
