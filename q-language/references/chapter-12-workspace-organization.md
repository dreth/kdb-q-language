# 12. Workspace Organization

Source URL: https://code.kx.com/q4m3/12_Workspace_Organization/

## Agent-Relevant Takeaways

- q organizes names in contexts, which work like namespaces and dictionaries.
- The default context is `.`. Application code commonly uses named contexts such as `.app`.
- Contexts can be created, inspected, saved, loaded, and expunged.
- Namespacing is important for reusable libraries and for avoiding global-name collisions in long-running processes.

## q Syntax/Forms That Matter

- Qualified name: `.ns.name`
- Change context: `\d .ns`; return default: `\d .`
- Get/set by symbol: `get `.ns.name`, `set[`.ns.name;value]`
- Context dictionary: `` `.ns ``
- Delete name: `delete name from `.ns` or expunge via system command patterns

## Common Mistakes/Pitfalls

- Loading scripts that define globals in `.` unexpectedly.
- Forgetting the active context after `\d`.
- Confusing OS paths with q contexts because both use dotted or separated naming conventions.
- Deleting or overwriting names in shared contexts.

## Small Examples

```q
.risk.limit:1000000
.risk.check:{[notional] notional<.risk.limit}
.risk.check 500000
```

## Cross-Links

- [chapter-10-execution-control.md](chapter-10-execution-control.md)
- [chapter-13-commands-and-system-variables.md](chapter-13-commands-and-system-variables.md)
