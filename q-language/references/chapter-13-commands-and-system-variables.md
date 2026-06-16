# 13. Commands and System Variables

Source URL: https://code.kx.com/q4m3/13_Commands_and_System_Variables/

## Agent-Relevant Takeaways

- Backslash commands manage the q session: load files, set ports, inspect workspace, list tables/functions/variables, time expressions, and configure display/runtime options.
- `system` executes many command equivalents from q code.
- `.z.*` variables expose runtime hooks, environment information, callbacks, and system state.
- Use commands for diagnostics and scripts; be cautious in generated application logic.

## q Syntax/Forms That Matter

- List tables/vars/functions: `\a`, `\v`, `\f`
- Load: `\l path/to/file.q`
- Context: `\d .ns`
- Port: `\p 5010`; from code: `system "p 5010"`
- Timing: `\t expr`, `\ts expr`
- Workspace: `\w`
- Display precision: `\P 12`
- Common system variables: `.z.P`, `.z.D`, `.z.T`, `.z.K`, `.z.pw`, `.z.ts`

## Common Mistakes/Pitfalls

- Using command syntax inside functions where `system` is required.
- Accidentally opening a port or changing global process settings in library code.
- Depending on display precision instead of actual numeric value.
- Forgetting timer callbacks can affect process behavior globally.

## Small Examples

```q
system "P 12"
.z.P

/ In the console:
\\ts select avg px by sym from trades
```

## Cross-Links

- [chapter-10-execution-control.md](chapter-10-execution-control.md)
- [chapter-12-workspace-organization.md](chapter-12-workspace-organization.md)
- [chapter-11-io.md](chapter-11-io.md)
