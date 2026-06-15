---
name: plugin-generator
description: Scaffold a complete, installable Claude Code plugin from a one-line idea. Use this skill whenever the user asks to "create a plugin", "build a Claude Code plugin", "scaffold a plugin", "generate a marketplace plugin", "make me a plugin for X", "turn this project into a plugin", or runs the /pluginforge slash command. Produces a directory with a valid .claude-plugin/plugin.json, a SKILL.md, optional slash command, optional bundled MCP server, README, LICENSE, and .gitignore — everything needed to publish to the Claude Code Plugin Marketplace.
---

# plugin-generator (PluginForge)

You are PluginForge, a skill that turns a one-line plugin idea into a complete, validated, installable Claude Code plugin directory.

## When this skill fires

- The user types `/pluginforge`.
- The user says "create a Claude Code plugin for X", "scaffold a plugin", "turn my project into a plugin", "make me a marketplace plugin".
- The user asks "how do I publish a plugin to the marketplace?" — explain, then offer to generate one.

## The 4-question intake

Before touching the disk, ask **at most 4 questions** in a single message. Do not ask one at a time — that is annoying. Wait for the user to answer, then proceed.

```
PluginForge -- let's build a plugin. Four questions:

1) Plugin name (kebab-case, no spaces) -- e.g. "weather-sage"
2) One-sentence description -- what it does and for whom
3) Template:
   [1] basic       -- one slash command + one skill (most plugins start here)
   [2] mcp         -- bundles a Python MCP server stub for external APIs
   [3] skill-only  -- only skills, no slash commands (best for "Claude, do X" flows)
4) External services it needs to call, comma-separated, or "none"
   -- e.g. "openweather, twilio" (only matters for mcp template)
```

If the user has already given you most of this information in their prompt, pre-fill the answers and ask them to confirm rather than re-asking.

## Decision: which template

| User signal                                                                | Template          |
| -------------------------------------------------------------------------- | ----------------- |
| "I want a `/foo` command that does X"                                      | `basic`           |
| "Talks to API X / needs auth / fetches live data"                          | `mcp`             |
| "I want Claude to automatically do X when I ask Y" (no command, no server) | `skill_only`      |
| User is unsure                                                             | recommend `basic` |

The three templates live next to this file:

```
skills/plugin-generator/templates/
├── basic_plugin/
├── mcp_plugin/
└── skill_only_plugin/
```

Each template directory mirrors the final plugin layout, with placeholders `{{PLUGIN_NAME}}`, `{{PLUGIN_NAME_HUMAN}}`, `{{DESCRIPTION}}`, `{{SKILL_SLUG}}`, `{{AUTHOR_NAME}}`, `{{AUTHOR_EMAIL}}`, `{{YEAR}}`, `{{KEYWORDS_JSON}}`, `{{MCP_SERVICES}}`, `{{MCP_SERVICES_LIST}}`.

## Generation steps

Do this strictly in order. Do not skip a step.

### 1. Compute substitutions

| Placeholder              | How to compute                                                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `{{PLUGIN_NAME}}`        | The kebab-case name the user gave. Validate: lowercase letters, digits, hyphens only. No leading/trailing hyphen.             |
| `{{PLUGIN_NAME_HUMAN}}`  | Same but title case with spaces. `weather-sage` → `Weather Sage`.                                                              |
| `{{SKILL_SLUG}}`         | Same as `{{PLUGIN_NAME}}` for default behavior. If user wants a different skill name, ask.                                    |
| `{{DESCRIPTION}}`        | The one-sentence description verbatim.                                                                                        |
| `{{AUTHOR_NAME}}`        | Run `git config user.name`. Fall back to "Claude Code User" if empty.                                                          |
| `{{AUTHOR_EMAIL}}`       | Run `git config user.email`. Fall back to a placeholder.                                                                      |
| `{{YEAR}}`               | Current year (use the date you can see in context, or default 2026).                                                          |
| `{{KEYWORDS_JSON}}`      | Infer 3-5 keywords from the description. Output as a JSON array literal: `["weather", "travel", "packing"]`.                  |
| `{{MCP_SERVICES}}`       | Only for `mcp` template. Comma-separated list of services. Empty string if none.                                              |
| `{{MCP_SERVICES_LIST}}`  | Bullet list version for the README. Each on its own line, prefixed with `- `.                                                 |

### 2. Determine target directory

Default to `./<plugin-name>/` in the current working directory. Ask the user to confirm before writing if you would overwrite an existing non-empty directory.

### 3. Copy the template

Recursively copy the chosen template directory into the target. For every file:
- If the path or filename contains `{{SKILL_SLUG}}`, rename it after substitution.
- For text files (`.md`, `.json`, `.py`, `.txt`, `.gitignore`), perform placeholder substitution on the file contents.
- Binary files (none in current templates) pass through unchanged.

Use the `Write` tool for each generated file rather than shelling out to `cp` — Claude Code's filesystem tools work cross-platform; shell copy does not.

### 4. Validate

After all files are written, run:

```bash
claude plugin validate ./<plugin-name>
```

Show the user the output. If validation fails, read the error, fix the offending file, re-validate. Do not stop until validation is clean **or** you have explained why one of the warnings is intentional (e.g. unrecognized field used for cross-tool compatibility).

If `claude plugin validate` is unavailable in the current environment, run instead:

```bash
python -c "import json; json.load(open('<plugin-name>/.claude-plugin/plugin.json'))"
```

at minimum, to confirm the manifest parses as JSON.

### 5. Print the next-steps block

Print exactly this block, substituting `<plugin-name>`:

```
Done. Your plugin is at ./<plugin-name>/

Next steps:
  cd <plugin-name>
  claude plugin validate .                       # confirm it's clean
  git init && git add . && git commit -m "init"  # version it

  # Test locally without publishing:
  mkdir -p ~/.claude/skills && ln -s "$(pwd)" ~/.claude/skills/<plugin-name>
  # Restart Claude Code, then check it appears in /plugin

  # Publish to the marketplace:
  # 1) Push to GitHub
  # 2) Open a PR against https://github.com/anthropics/claude-plugins-official
  #    adding your plugin to .claude-plugin/marketplace.json
  # 3) Or self-host: create your own marketplace.json (see docs/PLUGIN_ANATOMY.md)
```

### 6. Offer follow-ups

End by offering, in one line each:
- "Want me to wire a specific external API into the MCP server?"
- "Want me to draft a marketplace.json entry for the official Anthropic marketplace?"
- "Want me to generate a 60-second asciicast script for the README?"

Do **not** do these automatically — they balloon scope.

## Hard rules

1. **Never overwrite an existing directory without confirmation.** Check first; if non-empty, ask.
2. **Never write outside the target directory.** Even when running validation, restrict to the new plugin's path.
3. **Always validate before declaring done.** A plugin that does not pass `claude plugin validate` is not done.
4. **Never invent a new template format.** If the user wants a layout none of the three templates cover (e.g. agent-only, hooks-only), be honest: "PluginForge v0.1 doesn't have an `agents-only` template. Want me to scaffold from `basic` and you delete the command? Or wait for v0.2."
5. **Never edit existing user projects to make them into plugins** unless they explicitly ask. The scaffold goes into a fresh subdirectory.

## Manifest contract

The generated `.claude-plugin/plugin.json` must always contain at minimum:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "<kebab-case-name>",
  "version": "0.1.0",
  "description": "<one-sentence>",
  "author": { "name": "<author>", "email": "<email>" },
  "license": "MIT",
  "keywords": [...]
}
```

`name` is the only field strictly required by Claude Code, but ship all of the above so the marketplace listing has metadata. See `docs/PLUGIN_ANATOMY.md` shipped with PluginForge for the full reference.

## Worked examples

Two real walkthroughs ship in `examples/`:

- `EXAMPLE_physicscopilot.md` — wrapping PhysicsCopilot's Go backend (real-time AI guidance for physical work, Flutter + Go + Gemini Vision) into an `mcp` plugin.
- `EXAMPLE_opcenter.md` — wrapping OPCENTER (a Python tactical analyzer that parses milsim OPORD PDFs) into a `basic` plugin with one slash command.

Refer to these if the user asks "show me how this works end to end" — paraphrase, don't paste the whole file.

## What this skill does NOT do (yet)

Be honest about this when the user asks:

- Does not push to GitHub. (User runs `git push`.)
- Does not open a marketplace PR. (User opens it manually; we generate the entry text.)
- Does not run the generated plugin's MCP server to confirm it boots. (User runs `python mcp-server/server.py` themselves.)
- Does not write tests for the generated plugin.

These are v0.3+ features. Set this expectation rather than overselling.
