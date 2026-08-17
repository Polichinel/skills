#!/usr/bin/env python3
"""Validate the skills collection against the five invariants C-03 names.

Checks, in order of how often they have actually broken here:

  1. frontmatter      every SKILL.md has name + description, description <= 1024 chars,
                      name is kebab-case and matches its directory
  2. references       every `references/*.md` path named in a skill resolves
  3. skill-names      every skill name mentioned in prose is an installed skill
  4. external-paths   every `~/...` or `/home/...` path a skill depends on exists
  5. readme           every skill in README's tables exists, and vice versa

Exit 0 if clean, 1 if any FAIL. Run from anywhere:

    python3 scripts/validate_skills.py
    python3 scripts/validate_skills.py --quiet     # only failures

Why this exists: C-01 (a renumbered vault path) and C-04 (three references to skills
that were never installed) both survived nine commits undetected and were found by
hand. Checks 2 and 4 catch C-01; check 3 catches C-04.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", "docs", "reports", "scripts", "__pycache__"}
DESC_LIMIT = 1024
NAME_RE = re.compile(r"^[a-z0-9-]+$")


def skill_dirs() -> list[Path]:
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name not in SKIP_DIRS and (d / "SKILL.md").is_file()
    )


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the leading YAML block. Flat key: value only, which is all skills use."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].split("\n"):
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def check_frontmatter(skills: list[Path]) -> list[str]:
    bad = []
    for d in skills:
        fm = frontmatter(d / "SKILL.md")
        if not fm:
            bad.append(f"{d.name}/SKILL.md: no parseable YAML frontmatter")
            continue
        name, desc = fm.get("name"), fm.get("description")
        if not name:
            bad.append(f"{d.name}/SKILL.md: missing `name`")
        else:
            if not NAME_RE.match(name):
                bad.append(f"{d.name}/SKILL.md: name '{name}' is not kebab-case")
            if name != d.name:
                bad.append(f"{d.name}/SKILL.md: name '{name}' != directory '{d.name}'")
        if not desc:
            bad.append(f"{d.name}/SKILL.md: missing `description`")
        elif len(desc) > DESC_LIMIT:
            bad.append(f"{d.name}/SKILL.md: description {len(desc)} chars > {DESC_LIMIT}")
    return bad


REF_RE = re.compile(r"`?((?:[a-z0-9-]+/)?references/[A-Za-z0-9_.-]+\.md)`?")


def check_references(skills: list[Path]) -> list[str]:
    """A reference resolves relative to its own skill, or as `other-skill/references/x.md`."""
    bad = []
    for d in skills:
        for md in d.rglob("*.md"):
            for ref in set(REF_RE.findall(md.read_text(encoding="utf-8", errors="ignore"))):
                if (d / ref).is_file() or (ROOT / ref).is_file():
                    continue
                bad.append(f"{md.relative_to(ROOT)}: unresolved reference `{ref}`")
    return bad


TOKEN_RE = re.compile(r"[a-z][a-z0-9]+(?:-[a-z0-9]+){1,3}")
DELEGATION_RE = re.compile(
    r"(?:use |see |via |delegate to |hand off to |→ )`?([a-z][a-z0-9]+(?:-[a-z0-9]+){1,3})`?"
)
KNOWN_NONSKILLS = {
    "base-docs", "claude-code", "pre-commit", "import-linter", "tech-debt",
    "code-review", "sub-agents", "output-styles", "path-scoped", "well-specified",
    "design-preferences", "read-only", "self-descriptive", "cross-repo", "multi-expert",
    "kebab-case", "front-matter", "one-liner", "opt-in", "fail-loud", "end-to-end",
}


def check_skill_names(skills: list[Path]) -> list[str]:
    """Catch prose pointing at skills that were never installed (C-04).

    Two detection paths, because C-04 appeared in both forms:
      a) explicit delegation  -- "use clean-architecture-review"
      b) comma list           -- "(expert-code-review, test-review, clean-architecture-review)"
         Detected by: a token sitting in a list where >= 2 siblings ARE installed skills.
         Path (b) is what the first version of this check missed.
    """
    installed = {d.name for d in skills}
    bad = []
    for d in skills:
        for md in d.rglob("*.md"):
            text = md.read_text(encoding="utf-8", errors="ignore")
            flagged: set[str] = set()

            for cand in set(DELEGATION_RE.findall(text)):
                if cand not in installed and cand not in KNOWN_NONSKILLS:
                    if re.search(rf"\(use {re.escape(cand)}\)|{re.escape(cand)} skill", text):
                        flagged.add(cand)

            # Comma lists: split on separators, count how many members are real skills.
            for run in re.findall(r"[(\[][^()\[\]]{20,400}[)\]]", text):
                members = [m.strip(" `*_") for m in re.split(r",|\bor\b|\band\b", run)]
                toks = [m for m in members if TOKEN_RE.fullmatch(m)]
                real = [t for t in toks if t in installed]
                if len(real) >= 2:
                    for t in toks:
                        if t not in installed and t not in KNOWN_NONSKILLS:
                            flagged.add(t)

            for cand in sorted(flagged):
                bad.append(f"{md.relative_to(ROOT)}: refers to '{cand}', not installed")
    return bad


PATH_RE = re.compile(r"`(~/[A-Za-z0-9_./-]+|/home/[a-z]+/[A-Za-z0-9_./-]+)`")


def check_external_paths(skills: list[Path]) -> list[str]:
    """Catch dependencies on paths that no longer exist (C-01)."""
    bad = []
    for d in skills:
        for md in d.rglob("*.md"):
            for raw in set(PATH_RE.findall(md.read_text(encoding="utf-8", errors="ignore"))):
                p = Path(raw.replace("~", str(Path.home()), 1))
                # Ignore paths that are clearly illustrative rather than depended on.
                if any(seg in raw for seg in ("<", ">", "NN_", "my-project", "example")):
                    continue
                if not p.exists():
                    bad.append(f"{md.relative_to(ROOT)}: missing external path `{raw}`")
    return bad


def check_readme(skills: list[Path]) -> list[str]:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return ["README.md: missing"]
    text = readme.read_text(encoding="utf-8", errors="ignore")
    listed = set(re.findall(r"^\|\s*\*\*([a-z0-9-]+)\*\*\s*\|", text, re.M))
    installed = {d.name for d in skills}
    bad = [f"README.md: lists '{n}' which is not installed" for n in sorted(listed - installed)]
    bad += [f"README.md: does not list installed skill '{n}'" for n in sorted(installed - listed)]
    return bad


CHECKS = [
    ("frontmatter", check_frontmatter),
    ("references", check_references),
    ("skill-names", check_skill_names),
    ("external-paths", check_external_paths),
    ("readme", check_readme),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    args = ap.parse_args()

    skills = skill_dirs()
    if not skills:
        print(f"FAIL  no skills found under {ROOT}")
        return 1

    failed = 0
    for label, fn in CHECKS:
        problems = fn(skills)
        if problems:
            failed += 1
            print(f"FAIL  {label} ({len(problems)})")
            for p in problems:
                print(f"        {p}")
        elif not args.quiet:
            print(f"ok    {label}")

    if not args.quiet:
        print(f"\n{len(skills)} skills checked")
    if failed:
        print(f"\n{failed} of {len(CHECKS)} checks failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
