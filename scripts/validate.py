#!/usr/bin/env python3
"""Lightweight repository checks (standard library only).

Checks: skill front matter, Markdown code fences, relative links,
and obvious secret patterns.
Usage: python scripts/validate.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "session-usage-handoff" / "skill.md"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_RE = re.compile(
    r"(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}"
    r"|AIza[0-9A-Za-z_\-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?i:(password|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{12,}))"
)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
errors = []


def md_files():
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]


def check_front_matter():
    if not SKILL.is_file():
        errors.append(f"missing skill file: {SKILL.relative_to(ROOT)}")
        return
    lines = SKILL.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        errors.append("skill: front matter must start and end with '---'")
        return
    fm = {}
    for line in lines[1 : lines.index("---", 1)]:
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not m:
            errors.append(f"skill: unparseable front matter line: {line[:40]!r}")
            continue
        fm[m.group(1)] = m.group(2).strip()
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"skill: missing or empty '{key}'")
    if fm.get("name") and not NAME_RE.match(fm["name"]):
        errors.append("skill: name must be lowercase, hyphen-separated")
    if fm.get("name") and fm["name"] != SKILL.parent.name:
        errors.append("skill: name must match its directory name")


def check_fences_and_links():
    for p in md_files():
        text = p.read_text(encoding="utf-8")
        if sum(1 for l in text.splitlines() if l.lstrip().startswith("```")) % 2:
            errors.append(f"{p.relative_to(ROOT)}: unbalanced code fence")
        in_fence = False
        for l in text.splitlines():
            if l.lstrip().startswith("```"):
                in_fence = not in_fence
            if in_fence:
                continue
            for target in LINK_RE.findall(l):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                path = target.split("#")[0]
                if path and not (p.parent / path).exists():
                    errors.append(f"{p.relative_to(ROOT)}: broken link {target}")


def check_secrets():
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or not p.is_file() or p.suffix == ".pyc":
            continue
        if p == Path(__file__).resolve():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_RE.search(text):
            errors.append(f"{p.relative_to(ROOT)}: possible secret (value not shown)")


for check in (check_front_matter, check_fences_and_links, check_secrets):
    check()

if errors:
    print("FAILED:")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)
print("All checks passed.")
