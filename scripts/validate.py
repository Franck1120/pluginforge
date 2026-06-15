#!/usr/bin/env python3
"""Structure + JSON lint for PluginForge.

Runs in CI and locally (`python scripts/validate.py`). No third-party deps.

Checks:
  1. The plugin manifest parses as JSON.
  2. Each template, after placeholder substitution, produces JSON that parses
     (plugin.json and any .mcp.json) — this is what a generated plugin ships.
  3. Every SKILL.md has YAML frontmatter with `name:` and `description:`.
  4. The MCP template's server.py byte-compiles.

Exit code is non-zero if any check fails.
"""
from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "skills" / "plugin-generator" / "templates"

# Dummy values used to render templates so the result is valid JSON.
SUBS = {
    "{{PLUGIN_NAME}}": "demo-plugin",
    "{{PLUGIN_NAME_HUMAN}}": "Demo Plugin",
    "{{DESCRIPTION}}": "A demo plugin used only for CI validation.",
    "{{SKILL_SLUG}}": "demo-plugin",
    "{{AUTHOR_NAME}}": "CI Bot",
    "{{AUTHOR_EMAIL}}": "ci@example.com",
    "{{YEAR}}": "2026",
    "{{KEYWORDS_JSON}}": '["demo", "ci", "test"]',
    "{{MCP_SERVICES}}": "example-api",
    "{{MCP_SERVICES_LIST}}": "- example-api",
}

errors: list[str] = []
checks = 0


def render(text: str) -> str:
    for key, value in SUBS.items():
        text = text.replace(key, value)
    return text


def check_json(path: Path, *, rendered: bool) -> None:
    global checks
    checks += 1
    try:
        raw = path.read_text(encoding="utf-8")
        json.loads(render(raw) if rendered else raw)
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"JSON parse failed: {path} -> {exc}")


def check_skill_frontmatter(path: Path) -> None:
    global checks
    checks += 1
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        errors.append(f"SKILL.md missing YAML frontmatter: {path}")
        return
    front = match.group(1)
    if "name:" not in front:
        errors.append(f"SKILL.md frontmatter missing 'name': {path}")
    if "description:" not in front:
        errors.append(f"SKILL.md frontmatter missing 'description': {path}")


def main() -> int:
    global checks
    # 1. Plugin manifest.
    check_json(ROOT / ".claude-plugin" / "plugin.json", rendered=False)

    # 2. Templates (rendered).
    for manifest in TEMPLATES.rglob(".claude-plugin/plugin.json"):
        check_json(manifest, rendered=True)
    for mcp in TEMPLATES.rglob(".mcp.json"):
        check_json(mcp, rendered=True)

    # 3. All SKILL.md files (own skill + templates).
    for skill in ROOT.rglob("SKILL.md"):
        check_skill_frontmatter(skill)

    # 4. MCP server stub compiles.
    server = TEMPLATES / "mcp_plugin" / "mcp-server" / "server.py"
    if server.exists():
        checks += 1
        try:
            py_compile.compile(str(server), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"server.py does not compile: {exc}")
    else:
        errors.append(f"missing MCP server stub: {server}")

    if errors:
        print(f"FAILED - {len(errors)} problem(s) across {checks} checks:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK - {checks} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
