# 11. I/O

Source URL: https://code.kx.com/q4m3/11_IO/

## Agent-Relevant Takeaways

- q uses handles for files, processes, sockets, HTTP, and WebSockets.
- Symbols beginning with `:` represent file handles; `hsym` helps safely form handles from paths.
- q values can be serialized/deserialized as binary; tables can be saved, loaded, or splayed.
- Text I/O requires explicit parsing and type conversion.
- IPC supports synchronous and asynchronous remote execution. Treat remote input as code execution risk.

## q Syntax/Forms That Matter

- File handle: `` `:/path/file ``, `hsym `$"/path with spaces/file.csv"`
- Binary set/get: `handle set value`, `get handle`
- Text lines: `read0 handle`, `handle 0: lines`
- CSV-like load: `("SFI"; enlist ",") 0: handle`
- Open/close: `hopen`, `hclose`
- IPC: `h:hopen `:host:port`, sync `h "2+2"`, async `neg[h] "expr"`

## Common Mistakes/Pitfalls

- Building file handles by string concatenation instead of `hsym`.
- Loading text without specifying types and delimiters.
- Forgetting to close handles in long-running processes.
- Sending unsanitized strings for remote execution.
- Confusing serialized single-file tables with splayed directories.

## Small Examples

```q
path:hsym `$"/tmp/prices.csv"
rows:("SFI"; enlist ",") 0: path

h:hopen `:localhost:5010
@[hclose;h;{()}]
```

## Cross-Links

- [chapter-07-transforming-data.md](chapter-07-transforming-data.md)
- [chapter-10-execution-control.md](chapter-10-execution-control.md)
- [chapter-14-introduction-to-kdb.md](chapter-14-introduction-to-kdb.md)
