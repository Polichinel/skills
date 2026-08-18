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


def read(path: Path) -> str:
    """Read a file, surfacing rather than hiding a decode failure.

    A validator that silently drops undecodable bytes can report `ok` on content it
    never saw. Decode errors become findings, not silence.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"{path}: not valid UTF-8 ({exc})") from exc


def skill_dirs() -> list[Path]:
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name not in SKIP_DIRS and (d / "SKILL.md").is_file()
    )


def prose_files(skills: list[Path]) -> list[Path]:
    """Every markdown file the prose checks should see: skill docs plus README.md.

    reports/ is excluded, and the reason is structural rather than convenience. A risk
    register that tracks dangling-name concerns necessarily *contains* dangling names --
    C-04's entry lists the three skills that never existed, C-01's quotes the broken
    ~/brain/8_system path, C-15's explains this very exclusion. Section-aware scanning was
    tried: skipping Resolved Concerns still leaves hits in *open* entries, because open
    entries discuss the same history. The check would fail permanently on correct content,
    and a check that fires on correct behaviour gets disabled.

    The cost is real: the stale Source value fixed by hand in this change lived in
    reports/, so a recurrence there goes unseen. Accepted knowingly.
    """
    out = [md for d in skills for md in d.rglob("*.md")]
    out += [p for p in [ROOT / "README.md"] if p.is_file()]
    return sorted(out)


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the leading YAML block.

    Handles the three shapes skills actually use: bare scalars, quoted scalars, and
    folded/indented continuation lines. Quotes are stripped and continuations joined,
    because otherwise `name: "x"` reports a false not-kebab-case and a folded
    `description: >` measures as 0 chars — which would silently exempt exactly the long
    descriptions the 1024 limit exists to catch.
    """
    text = read(path)
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    key: str | None = None
    for line in text[3:end].split("\n"):
        if line.startswith(("#",)) or not line.strip():
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            key, _, v = line.partition(":")
            key = key.strip()
            out[key] = v.strip().lstrip(">|-").strip().strip("\"'")
        elif key:  # folded / indented continuation
            out[key] = (out[key] + " " + line.strip()).strip()
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


REF_RE = re.compile(r"`?((?:[a-z0-9_-]+/)*references/[A-Za-z0-9_.-]+\.md)`?")


def check_references(skills: list[Path]) -> list[str]:
    """A reference resolves relative to its own skill, or as `other-skill/references/x.md`."""
    bad = []
    for d in skills:
        for md in d.rglob("*.md"):
            for ref in set(REF_RE.findall(read(md))):
                if (d / ref).is_file() or (ROOT / ref).is_file():
                    continue
                bad.append(f"{md.relative_to(ROOT)}: unresolved reference `{ref}`")
    return bad


# Hyphenated English, not skill names. Filtering by first segment is cheaper and more
# durable than growing KNOWN_NONSKILLS one word at a time.
ENGLISH_PREFIXES = {"re", "un", "non", "pre", "post", "sub", "inter", "co", "de",
                    "anti", "semi", "multi", "cross", "self", "well", "high", "low"}
SKILLISH = r"[a-z][a-z0-9]+(?:-[a-z0-9]+){1,3}"
BACKTICKED_RE = re.compile(r"`(" + SKILLISH + r")`")
SLASH_RE = re.compile(r"/(" + SKILLISH + r")\b")
DELEGATION_RE = re.compile(
    r"(?:use |see |via |delegate to |hand off to |→ )`?([a-z][a-z0-9]+(?:-[a-z0-9]+){1,3})`?"
)
# Backticked technical terms that are not skills. This list grows; that is the cost of
# a syntactic check, and it is a cheaper cost than a check nobody trusts.
KNOWN_NONSKILLS = {
    "autoresearch-survey", "base-docs", "behavior-neutral", "claude-code", "code-review",
    "credit-war", "cross-repo", "data-readiness", "design-preferences", "end-to-end",
    "expert-review", "fail-loud", "failure-modes", "falsification-audit", "forecast-hub",
    "front-matter", "graphify-out", "half-open", "house-style", "import-linter", "lint-imports",
    "karpathy-autoresearch-explained", "karpathy-pattern", "kebab-case", "metric-validity",
    "multi-expert", "my-project", "no-inference", "no-silent-clamp", "one-liner", "opt-in",
    "output-styles", "path-scoped", "pr-review", "pre-commit", "proxy-divergent",
    "read-only", "reproducibility-critical", "self-descriptive", "setup-uv", "sub-agents",
    "tech-debt", "tech-debt-audit", "test-first", "tight-coupling", "under-explaining",
    "views-frames", "well-specified", "what-to-build", "world-model", "zero-threshold",
}


def check_skill_names(skills: list[Path]) -> list[str]:
    """Catch prose pointing at skills that were never installed (C-04).

    Detects the two forms in which a skill is *referenced* rather than merely mentioned:
    backticked (`clean-architecture-review`) and slash-command (/clean-architecture-review).
    Both are deliberate acts of naming; ordinary hyphenated English never takes either.

    **Known limit, stated rather than papered over:** an unbackticked mention in running
    prose is not detected. Two of C-04's four historical sites were of that kind. Earlier
    versions tried proximity to real skill names, and every attempt false-positived on
    ordinary adjectives -- whole-codebase, version-controlled, large-scale -- each needing
    another filter. That is guard accumulation: the check grows, false positives keep
    coming, and eventually someone disables it. A check that reliably catches the
    load-bearing form beats one that catches everything and gets switched off. The site
    C-04's own trigger names -- the Source table in register-risk/references/schema.md --
    is backticked, and is caught.
    """
    installed = {d.name for d in skills}
    bad = []
    for md in prose_files(skills):
        text = read(md)
        refs = set(BACKTICKED_RE.findall(text)) | set(SLASH_RE.findall(text))
        for cand in sorted(refs - installed - KNOWN_NONSKILLS):
            bad.append(f"{md.relative_to(ROOT)}: refers to '{cand}', not installed")
    return bad


# Paths anywhere inside a code span, not only filling it — `cd /home/simon/...` is how
# most of them actually appear. The permissive tail covers non-ASCII (þingit), which a
# character class silently excluded, making thingit/SKILL.md invisible to this check.
PATH_RE = re.compile(r"(?<![\w/])(~/[^\s`'\"]+|/home/[a-z]+/[^\s`'\"]+)")

ILLUSTRATIVE = ("<", ">", "NN_", "my-project", "example", "claude_learning")


def check_external_paths(skills: list[Path]) -> list[str]:
    """Catch dependencies on paths that no longer exist (C-01)."""
    bad = []
    for md in prose_files(skills):
        for raw in set(PATH_RE.findall(read(md))):
            p = Path(raw.replace("~", str(Path.home()), 1))
            # Ignore paths that are clearly illustrative rather than depended on.
            if "..." in raw:          # truncated example, not a dependency
                continue
            raw = raw.rstrip(".,;:)]`'\"")
            if any(s in raw for s in ILLUSTRATIVE):
                continue
            if not p.exists():
                bad.append(f"{md.relative_to(ROOT)}: missing external path `{raw}`")
    return bad


def check_readme(skills: list[Path]) -> list[str]:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return ["README.md: missing"]
    text = read(readme)
    listed = set(re.findall(r"^\|\s*\*\*([a-z0-9-]+)\*\*\s*\|", text, re.M))
    installed = {d.name for d in skills}
    bad = [f"README.md: lists '{n}' which is not installed" for n in sorted(listed - installed)]
    bad += [f"README.md: does not list installed skill '{n}'" for n in sorted(installed - listed)]
    return bad


def check_allowlist(skills: list[Path]) -> list[str]:
    """Check the allow-list itself, not just the repo's conformance to it.

    KNOWN_NONSKILLS exempts tokens from check 3. Nothing verified the list: an entry that
    is also an installed skill would silently exempt that skill from the dangling-name
    check, and the suite would stay green. That is an assertion about conformance standing
    in for an assertion about the property -- the shape views-datafactory named as C-351.
    """
    # Stale entries are deliberately not flagged: an entry matching nothing exempts a
    # token nobody writes, which costs nothing, while flagging them churns the list every
    # time a term leaves the prose. Only the case that hides a real bug is checked.
    installed = {d.name for d in skills}
    bad = [f"KNOWN_NONSKILLS exempts '{n}', which IS an installed skill -- "
           f"it would be silently unchecked" for n in sorted(installed & KNOWN_NONSKILLS)]
    return bad


CHECKS = [
    ("frontmatter", check_frontmatter),
    ("references", check_references),
    ("skill-names", check_skill_names),
    ("external-paths", check_external_paths),
    ("readme", check_readme),
    ("allowlist", check_allowlist),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    ap.add_argument("--skip", action="append", default=[], metavar="CHECK",
                    help="skip a check by name; repeatable. Used by CI for "
                         "external-paths, which depends on this machine's home dir.")
    args = ap.parse_args()

    skills = skill_dirs()
    if not skills:
        print(f"FAIL  no skills found under {ROOT}")
        return 1

    failed = 0
    for label, fn in CHECKS:
        if label in args.skip:
            if not args.quiet:
                print(f"skip  {label}")
            continue
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
