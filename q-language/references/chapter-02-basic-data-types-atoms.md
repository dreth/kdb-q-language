# 2. Basic Data Types: Atoms

Source URL: https://code.kx.com/q4m3/2_Basic_Data_Types_Atoms/

## Agent-Relevant Takeaways

- Atoms are scalar values. Each q atom has a type code; lists have positive type codes and atoms have negative type codes.
- Numeric types include short, int, long, real, float; default integer literals are long and default decimal literals are float.
- Text is split into chars (`"a"`) and symbols (`` `abc ``). Symbols are interned and should not be generated unboundedly from arbitrary text.
- Temporal atoms have specific literal forms for date, month, time, minute, second, datetime, timestamp, and timespan.
- Nulls are typed; use `null` to test them.
- Boolean, byte, GUID, and char use proxy nulls because all bit patterns are otherwise valid.
- Integer arithmetic can overflow into integral null/infinity bit patterns; division returns floats and uses float infinity/null.

## q Syntax/Forms That Matter

- Boolean: `1b`, byte: `0x2a`, short/int/long suffixes: `42h`, `42i`, `42j`
- Float/real: `4.2`, `4.2e`
- Symbol: `` `abc ``; char list string: `"abc"`
- Date/time: `2026.06.16`, `12:34:56.789`, `2026.06.16D12:34:56.789000000`
- Temporal arithmetic: `date+int`, `timestamp+timespan`, `timestamp-date`
- Null/infinity examples: `0N`, `0Nj`, `0n`, `0W`, `0w`, `0Nd`, `0Np`, `` ` ``

## Common Mistakes/Pitfalls

- Comparing nulls with `=` instead of `null`.
- Using symbols for high-cardinality unbounded strings in services.
- Mixing temporal types without checking units and precision.
- Forgetting that a single char is an atom but a string is a char list.
- Assuming q nulls behave like SQL `NULL`; q nulls are ordinary typed values in vectors.
- Relying on `0N` for all missing data; use typed schemas and `null`.

## Small Examples

```q
type each (42;42i;4.2;`abc;"abc";2026.06.16)
null (0N;0n;`;2026.06.16)

show `timestamp$"2026.06.16D09:30:00.000000000"

d:2026.06.16
ts:2026.06.16D09:30:00.000000000
(d+1; ts+0D00:00:01.000000000)
null (0Nd;0Np;0Nn;0Nt;`)
```

## Cross-Links

- [chapter-07-transforming-data.md](chapter-07-transforming-data.md)
- [chapter-03-lists.md](chapter-03-lists.md)
- [appendix-b-error-messages.md](appendix-b-error-messages.md)
