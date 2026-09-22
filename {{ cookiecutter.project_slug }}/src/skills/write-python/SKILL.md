---
name: python-writing-style
description: Write, revise, or review Python code in Vic's preferred style. Use this skill whenever creating or modifying Python files, examples, tests, command-line tools, APIs, MCP servers, or code snippets.
---

# Python Writing Style

Apply this style to new and revised Python code. Preserve the project's established behavior, architecture, public interfaces, and tooling.

## Project Conventions

Inspect the surrounding Python files and project configuration before writing code. Follow an explicit project rule when it conflicts with this skill. Otherwise, use the rules below consistently.

## Imports

Organize imports into these groups, separated by one blank line. Add the matching comment above every group that is present:

```python
# Standard library imports.

# Third party imports.

# Local imports.
```

Within each group, prefer direct imports of the symbols used. Keep imports readable and remove unused imports.

## Constants

Place module-level constants after the imports under this heading:

```python
# Constants.
```

Use uppercase names for constants. Prefer configuration read once at module load when that matches the application's existing behavior.

## Python

- Add parameter and return types to functions and methods.
- Prefer built-in generic types such as `list[str]` and unions such as `str | None`.
- Use descriptive names instead of abbreviations.
- Keep functions focused and control flow easy to follow.
- Prefer guard clauses when they reduce nesting.
- Use f-strings for interpolation.
- Use `pathlib.Path` for filesystem paths unless an API requires strings.
- Define a specific exception when callers need to distinguish a domain failure.
- Preserve asynchronous behavior when working in asynchronous code.

## Comments and Messages

- Write comments as complete sentences ending with periods.
- Explain intent or a non-obvious constraint, not what the next line plainly does.
- Use docstrings for public modules, classes, functions, and methods when their purpose is not already obvious from the name and signature.
- Make assertion and exception messages identify what failed and, when useful, include the relevant value.

## Design

Favor simple, explicit constructs over clever abstractions. Do not add classes, helper layers, dependencies, compatibility shims, or configuration options unless the task requires them. Do not rewrite unrelated code solely to enforce this style.

## Formatting and Validation

Match the repository's formatter and linter. When none is configured, produce PEP 8-compatible code with four-space indentation, double-quoted strings, trailing commas in multiline collections and calls, and readable line lengths.

Before finishing, check that imports are grouped and labeled, constants are separated, types are present, comments follow the style, and the edited code passes the project's relevant formatter, linter, type checker, and tests when available.
