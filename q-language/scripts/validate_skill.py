#!/usr/bin/env python3
"""Structural checks for the q-language skill."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REFERENCES = ROOT / "references"

REQUIRED_REFERENCE_FILES = [
    "index.md",
    "preface.md",
    "chapter-00-overview.md",
    "chapter-01-q-shock-and-awe.md",
    "chapter-02-basic-data-types-atoms.md",
    "chapter-03-lists.md",
    "chapter-04-operators.md",
    "chapter-05-dictionaries.md",
    "chapter-06-functions.md",
    "chapter-07-transforming-data.md",
    "chapter-08-tables.md",
    "chapter-09-queries-q-sql.md",
    "chapter-10-execution-control.md",
    "chapter-11-io.md",
    "chapter-12-workspace-organization.md",
    "chapter-13-commands-and-system-variables.md",
    "chapter-14-introduction-to-kdb.md",
    "appendix-a-built-in-functions.md",
    "appendix-b-error-messages.md",
    "colophon.md",
]

REQUIRED_HEADINGS = [
    "Source URL:",
    "## Agent-Relevant Takeaways",
    "## q Syntax/Forms That Matter",
    "## Common Mistakes/Pitfalls",
    "## Small Examples",
    "## Cross-Links",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def check_skill_frontmatter() -> None:
    text = (ROOT / "SKILL.md").read_text()
    if not text.startswith("---\n"):
        fail("SKILL.md missing YAML frontmatter")
    try:
        _, fm, _ = text.split("---\n", 2)
    except ValueError:
        fail("SKILL.md frontmatter is not closed")
    keys = [line.split(":", 1)[0] for line in fm.splitlines() if line.strip()]
    if keys != ["name", "description"]:
        fail(f"SKILL.md frontmatter keys must be only name and description, got {keys}")
    if "name: q-language" not in fm:
        fail("SKILL.md name must be q-language")


def check_openai_yaml() -> None:
    text = (ROOT / "agents" / "openai.yaml").read_text()
    required = [
        'display_name: "q Language"',
        "short_description:",
        "default_prompt:",
        "allow_implicit_invocation: true",
    ]
    for item in required:
        if item not in text:
            fail(f"openai.yaml missing {item}")
    if "$q-language" not in text:
        fail("openai.yaml default_prompt must mention $q-language")


def check_references() -> None:
    for name in REQUIRED_REFERENCE_FILES:
        path = REFERENCES / name
        if not path.exists():
            fail(f"missing reference {name}")
        text = path.read_text()
        if name != "index.md":
            for heading in REQUIRED_HEADINGS:
                if heading not in text:
                    fail(f"{name} missing {heading}")
            if "https://code.kx.com/q4m3/" not in text:
                fail(f"{name} missing q4m3 source URL")


def check_local_links() -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)")
    for path in [ROOT / "SKILL.md", REPO / "README.md", *REFERENCES.glob("*.md")]:
        text = path.read_text()
        base = path.parent
        for link in link_re.findall(text):
            target = (base / link).resolve()
            if not target.exists():
                fail(f"{path.relative_to(REPO)} has broken link to {link}")


def check_q_runtime(q_path: str) -> None:
    program = """1+1
trades:([] sym:`IBM`MSFT`IBM; px:101 250 102f; size:100 200 50)
select vwap:size wavg px, volume:sum size by sym from trades
\\
"""
    result = subprocess.run(
        [q_path, "-q"],
        input=program,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )
    if result.returncode != 0:
        fail(f"q semantic smoke test failed: {result.stderr.strip() or result.stdout.strip()}")
    if "2" not in result.stdout or "IBM" not in result.stdout or "MSFT" not in result.stdout:
        fail("q semantic smoke test produced unexpected output")


def main() -> None:
    check_skill_frontmatter()
    check_openai_yaml()
    check_references()
    check_local_links()
    q_path = shutil.which("q")
    print("structural validation: ok")
    if q_path:
        check_q_runtime(q_path)
        print(f"q runtime detected: {q_path}; semantic smoke test: ok")
    else:
        print("q runtime detected: no; validation is structural only")


if __name__ == "__main__":
    main()
