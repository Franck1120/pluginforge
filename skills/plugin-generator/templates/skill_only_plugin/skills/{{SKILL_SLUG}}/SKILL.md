---
name: {{SKILL_SLUG}}
description: {{DESCRIPTION}} Use this skill when the user explicitly asks about {{PLUGIN_NAME_HUMAN}} topics. The description in this frontmatter is the entire trigger surface — write it carefully.
---

# {{SKILL_SLUG}}

{{DESCRIPTION}}

## When to use this skill

Skills with no slash command rely 100% on the frontmatter `description` above to decide when to fire. The crisper the trigger phrases there, the more reliably Claude Code will pick this skill at the right moment.

Concrete trigger phrases (rewrite these for your domain):

- "Help me with X"
- "I have a Y problem"
- "Can you Z this?"

## Workflow

1. Confirm you understood the user's intent. One sentence.
2. Do the work.
3. Present the answer concisely.

## Hard rules

- Stay in scope. If the user asks something this skill is not designed for, hand back to Claude's default behavior.
- Never write to disk without being asked.
- Never run shell commands without being asked.

## What this skill does NOT do

List explicitly what users might expect but you don't deliver. Honesty here saves bug reports later.

---

Built with [PluginForge](https://github.com/Franck1120/pluginforge).
