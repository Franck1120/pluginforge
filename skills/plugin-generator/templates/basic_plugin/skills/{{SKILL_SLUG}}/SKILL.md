---
name: {{SKILL_SLUG}}
description: {{DESCRIPTION}} Use this skill when the user asks for {{PLUGIN_NAME_HUMAN}}-related help, or when they invoke /{{PLUGIN_NAME}}.
---

# {{SKILL_SLUG}}

{{DESCRIPTION}}

## When to use this skill

Replace this list with concrete trigger phrases. Examples:

- "Help me with X"
- "Do Y for me"
- "Analyze this Z"

The more specific you make the trigger phrases in the frontmatter `description`, the more reliably Claude Code will fire this skill at the right time.

## Workflow

Replace this with the steps Claude should follow when the skill fires:

1. Gather context (ask 1-2 questions if needed; do not pepper the user).
2. Do the core work.
3. Present results clearly.

## Hard rules

- Never modify files outside the user's working directory.
- Never call external APIs without explicit user consent (or wire that consent into `userConfig` in `plugin.json`).
- If a step fails, say so plainly. Do not pretend it worked.

## What this skill does NOT do

Be honest about scope. List things users might expect but you don't handle.

---

Built with [PluginForge](https://github.com/Franck1120/pluginforge).
