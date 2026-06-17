#!/usr/bin/env python3
"""Structural checks for the q-language skill."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
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

AUX_REFERENCE_FILES = [
    "anti-patterns.md",
    "executable-examples.md",
    "recipes.md",
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
    for name in [*REQUIRED_REFERENCE_FILES, *AUX_REFERENCE_FILES]:
        path = REFERENCES / name
        if not path.exists():
            fail(f"missing reference {name}")
        if name in REQUIRED_REFERENCE_FILES and name != "index.md":
            text = path.read_text()
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


def find_q() -> str | None:
    return shutil.which("q") or (
        str(Path("/opt/data/home/.kx/bin/q"))
        if Path("/opt/data/home/.kx/bin/q").exists()
        else None
    )


def run_q(q_path: str, program: str) -> str:
    result = subprocess.run(
        [q_path, "-q"],
        input=f"{program.rstrip()}\n\\\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )
    if result.returncode != 0:
        fail(f"q semantic test failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def assert_contains(output: str, expected: list[str], label: str) -> None:
    missing = [item for item in expected if item not in output]
    if missing:
        fail(f"q semantic test {label} missing {missing!r}; output was:\n{output}")


def check_q_runtime(q_path: str) -> None:
    semantic_cases = [
        (
            "lists",
            """
show "CASE lists"
xs:10 20 30 40
show xs where xs>20
show count enlist 42
""",
            ["CASE lists", "30 40", "1"],
        ),
        (
            "dictionaries",
            """
show "CASE dictionaries"
d:`IBM`MSFT!101 250f
show d`IBM
show key d
""",
            ["CASE dictionaries", "101f", "`IBM`MSFT"],
        ),
        (
            "qsql aggregation",
            """
show "CASE qsql"
trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
show select vwap:size wavg px, volume:sum size by sym from trades
""",
            ["CASE qsql", "IBM", "101.6667", "150", "MSFT", "250", "200"],
        ),
        (
            "joins",
            """
show "CASE joins"
trades:([] sym:`IBM`MSFT`IBM; px:101 250 103f; size:100 200 50)
inst:([] sym:`IBM`MSFT; sector:`tech`software)
show trades lj `sym xkey inst
show (`sym xkey inst)`IBM
""",
            ["CASE joins", "sector", "software", "sector| tech"],
        ),
        (
            "asof join",
            """
show "CASE aj"
quotes:([] time:09:30:00.000 09:30:01.000 09:30:02.000; sym:`IBM`IBM`IBM; bid:100 101 102f; ask:101 102 103f)
trades:([] time:09:30:01.500 09:30:02.500; sym:`IBM`IBM; px:101.2 102.4)
show aj[`sym`time;trades;quotes]
""",
            ["CASE aj", "09:30:01.500", "101.2", "101", "102.4", "103"],
        ),
    ]

    for label, program, expected in semantic_cases:
        assert_contains(run_q(q_path, program), expected, label)

    with tempfile.TemporaryDirectory(prefix="q-skill-") as tmp:
        csv_path = Path(tmp) / "prices.csv"
        output = run_q(
            q_path,
            f"""
show "CASE csv"
p:`$":{csv_path}"
p 0:("sym,px";"IBM,101.5";"MSFT,250.25");
t:("SF";enlist ",") 0:p
show t
show meta t
""",
        )
        assert_contains(output, ["CASE csv", "IBM", "101.5", "MSFT", "250.25", "sym| s", "px | f"], "csv")


def main() -> None:
    check_skill_frontmatter()
    check_openai_yaml()
    check_references()
    check_local_links()
    q_path = find_q()
    print("structural validation: ok")
    if q_path:
        check_q_runtime(q_path)
        print(f"q runtime detected: {q_path}; semantic snippet suite: ok")
    else:
        print("q runtime detected: no; validation is structural only")


if __name__ == "__main__":
    main()
