# 5. Dictionaries

Source URL: https://code.kx.com/q4m3/5_Dictionaries/

## Agent-Relevant Takeaways

- A dictionary maps keys to values and is built with `!`.
- Lookup uses function/index notation: `d key` or `d[key]`.
- Dictionaries generalize lists: lists map integer positions to items; dictionaries use explicit keys.
- A table starts as a column dictionary whose values are same-length column lists, then `flip` gives table behavior.

## q Syntax/Forms That Matter

- Dictionary: `` `a`b`c!10 20 30 ``
- Key/value extraction: `key d`, `value d`, `count d`
- Lookup: `d `a`, `d[`a`c]`
- Reverse lookup/find: `d?20`
- Remove keys: `key _ d`
- Column dictionary to table: `flip `c1`c2!(1 2;`a`b)`

## Common Mistakes/Pitfalls

- Assuming dictionary keys must be unique; non-unique keys are possible but usually troublesome.
- Forgetting a singleton dictionary needs enlisted key/value shape.
- Expecting lookup of a missing key to behave like every other language map; q returns a null appropriate to the value type in many cases.
- Joining dictionaries with overlapping keys without checking which value wins.

## Small Examples

```q
d:`bid`ask!101.2 101.4
d `ask

cols:`sym`px`size!(`IBM`MSFT;101.2 250.5;100 200)
t:flip cols
```

## Cross-Links

- [chapter-03-lists.md](chapter-03-lists.md)
- [chapter-08-tables.md](chapter-08-tables.md)
- [chapter-09-queries-q-sql.md](chapter-09-queries-q-sql.md)
