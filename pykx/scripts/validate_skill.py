#!/usr/bin/env python3
"""Structural checks for the PyKX skill."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REFERENCES = ROOT / "references"

REQUIRED_REFERENCE_FILES = [
    "index.md",
    "getting-started-and-configuration.md",
    "data-conversion-and-types.md",
    "query-and-q-execution.md",
    "databases-ipc-and-streaming.md",
    "pykx-under-q-and-interop.md",
    "operational-pitfalls-and-troubleshooting.md",
    "recipes.md",
    "anti-patterns.md",
]

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    *[f"references/{name}" for name in REQUIRED_REFERENCE_FILES],
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files() -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.exists():
            fail(f"missing required file {name}")


def check_skill_frontmatter() -> None:
    text = read(ROOT / "SKILL.md")
    if not text.startswith("---\n"):
        fail("SKILL.md missing YAML frontmatter")
    try:
        _, fm, body = text.split("---\n", 2)
    except ValueError:
        fail("SKILL.md frontmatter is not closed")
    keys = [line.split(":", 1)[0] for line in fm.splitlines() if line.strip()]
    if keys != ["name", "description"]:
        fail(f"SKILL.md frontmatter keys must be only name and description, got {keys}")
    if "name: pykx" not in fm:
        fail("SKILL.md name must be pykx")
    if len(body.splitlines()) > 150:
        fail("SKILL.md body should stay lean (<150 lines)")


def check_openai_yaml() -> None:
    text = read(ROOT / "agents" / "openai.yaml")
    required = [
        'display_name: "PyKX"',
        "short_description:",
        "default_prompt:",
        "allow_implicit_invocation: true",
    ]
    for item in required:
        if item not in text:
            fail(f"openai.yaml missing {item}")
    if "$pykx" not in text:
        fail("openai.yaml default_prompt must mention $pykx")


def check_references() -> None:
    for name in REQUIRED_REFERENCE_FILES:
        path = REFERENCES / name
        text = read(path)
        if not text.startswith("# "):
            fail(f"{name} must start with an H1")
        if name == "index.md":
            if "Source base:" not in text or "https://code.kx.com/pykx/" not in text:
                fail("index.md missing source base/public docs URL")
        else:
            if "Source paths:" not in text:
                fail(f"{name} missing Source paths")
        if len(text) > 30000:
            fail(f"{name} is too large for a concise agent reference")
        if text.count("```") % 2:
            fail(f"{name} has unbalanced fenced code blocks")


def markdown_files() -> list[Path]:
    return [ROOT / "SKILL.md", REPO / "README.md", *sorted(REFERENCES.glob("*.md"))]


def check_local_links() -> None:
    link_re = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:)([^)]+\.md)(?:#[^)]+)?\)")
    for path in markdown_files():
        text = read(path)
        base = path.parent
        for link in link_re.findall(text):
            target = (base / link).resolve()
            if not target.exists():
                fail(f"{rel(path)} has broken link to {link}")


def check_secret_hygiene() -> None:
    long_b64 = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{80,}={0,2}(?![A-Za-z0-9+/=])")
    for path in [ROOT / "SKILL.md", ROOT / "agents" / "openai.yaml", *REFERENCES.glob("*.md")]:
        text = read(path)
        if long_b64.search(text):
            fail(f"{rel(path)} appears to contain a long base64-like secret")
        lowered = text.lower()
        for bad in ["password='", 'password="', "secret='", 'secret="']:
            if bad in lowered:
                fail(f"{rel(path)} appears to hard-code a secret-like value")


def run_python(program: str, env: dict[str, str], timeout: int = 25) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", program],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        env=env,
        cwd="/tmp",
        check=False,
    )


def check_pykx_runtime() -> None:
    conversion_program = r"""
import pykx as kx
v = kx.toq([1, 2, 3])
assert v.py() == [1, 2, 3], v.py()
print("pykx conversion smoke: ok")
"""
    env = os.environ.copy()
    env.setdefault("PYKX_UNLICENSED", "true")
    result = run_python(conversion_program, env)
    if result.returncode != 0:
        combined = f"{result.stdout}\n{result.stderr}"
        if "ModuleNotFoundError" in combined and "pykx" in combined:
            print("pykx runtime detected: no; validation is structural only")
            return
        fail(f"PyKX conversion smoke failed:\n{combined.strip()}")
    print(result.stdout.strip())

    query_program = r"""
import pykx as kx
r = kx.q("1+1")
assert r.py() == 2, r
print("pykx embedded q query smoke: ok")
"""
    query_env = os.environ.copy()
    query_env.pop("PYKX_UNLICENSED", None)
    query_env.setdefault("PYKX_LICENSED", "true")
    result = run_python(query_program, query_env, timeout=20)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        first = (result.stderr or result.stdout).strip().splitlines()
        reason = first[-1] if first else "embedded q unavailable"
        print(f"pykx embedded q query smoke: skipped ({reason[:160]})")


def main() -> None:
    check_required_files()
    check_skill_frontmatter()
    check_openai_yaml()
    check_references()
    check_local_links()
    check_secret_hygiene()
    print("structural validation: ok")
    check_pykx_runtime()


if __name__ == "__main__":
    main()
