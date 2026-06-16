# Appendix B. Error Messages

Source URL: https://code.kx.com/q4m3/B_Error_Messages/

## Agent-Relevant Takeaways

- q errors are terse. Diagnose by mapping the symbol to category: runtime, parse, system, or license.
- Start with the expression shape: valence, type, rank, length, name resolution, and parse structure.
- Use smaller expressions, `type`, `count`, `meta`, and protected evaluation to isolate the failing part.
- For q-sql errors, inspect the parsed phrase order, table kind, column names, and atom-vs-list rank of every predicate.

## q Syntax/Forms That Matter

- Protected unary evaluation: `@[f;x;{x}]`
- Protected multi-arg evaluation: `.[f;args;{x}]`
- Debug prompt appears after unhandled errors in interactive sessions; inspect variables before exiting.
- Common signals: `'type`, `'length`, `'rank`, `'domain`, `'parse`, `'value`
- Common query causes: wrong column name (`'column`/`'value`), mismatched column lengths (`'length`), scalar where predicate (`'type`/`'rank`)
- Error map: `'type` wrong type/cast, `'length` non-conforming lists/columns, `'rank` arity/depth mismatch, `'domain` invalid value, `'splay` invalid persisted table shape.

## Common Mistakes/Pitfalls

- Treating the error text as a complete diagnosis. It is usually only the first clue.
- Fixing symptoms without checking atom/list rank.
- Ignoring parse errors caused by missing whitespace around names or invalid q-sql phrase order.
- Missing license/system errors that are unrelated to code logic.
- Fixing a join by changing data types without checking key shape and duplicate rows.
- Debugging a persisted query as if the table were fully materialized in memory.
- Missing that `'length` during table construction usually means column counts disagree.

## Small Examples

```q
safe:{[f;x] @[f;x;{`error`detail!(x;y)}]}
safe[{x+1};"abc"]

type each (1;1 2;"ab";`ab)
meta ([] sym:`IBM`MSFT; px:101 250f)
```

## Cross-Links

- [chapter-02-basic-data-types-atoms.md](chapter-02-basic-data-types-atoms.md)
- [chapter-04-operators.md](chapter-04-operators.md)
- [chapter-10-execution-control.md](chapter-10-execution-control.md)
