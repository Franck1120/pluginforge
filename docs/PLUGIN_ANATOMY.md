# Plugin Anatomy

What's actually inside a Claude Code plugin, file by file. PluginForge generates this layout; this document explains *why*.

Reference: [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference).

---

## The minimum viable plugin

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

That's it. Three files. The manifest is technically optional (Claude Code auto-discovers from the folder name), but you want one for marketplace metadata.

---

## `.claude-plugin/plugin.json` — the manifest

### Why it lives in `.claude-plugin/` and not at the root

Everything else (`commands/`, `skills/`, `agents/`, `hooks/`, `.mcp.json`) lives at the plugin root. The manifest is the only file that goes in `.claude-plugin/`. This namespacing was introduced in late 2025 so that a plugin can also be a valid VS Code extension or npm package without field collisions.

### The schema

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "my-plugin",
  "displayName": "My Plugin",
  "version": "0.1.0",
  "description": "What it does, in one sentence.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/you"
  },
  "homepage": "https://docs.example.com/my-plugin",
  "repository": "https://github.com/you/my-plugin",
  "license": "MIT",
  "keywords": ["a", "b", "c"]
}
```

### Field reference (the ones that matter)

| Field         | Required | Notes                                                                                                                                              |
| ------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | yes      | kebab-case, no spaces. Used for component namespacing (e.g. `my-plugin:my-skill`).                                                                  |
| `displayName` | no       | Shown in `/plugin` picker. Can contain spaces. Requires Claude Code v2.1.143+. ⚠️ Older CLIs (e.g. 2.1.131) **reject it as an error** (`Unrecognized key: "displayName"`). Omit it unless every target install is on 2.1.143+. PluginForge's templates leave it out for this reason. |
| `version`     | no       | Semver. If omitted, Claude Code uses the git commit SHA — every commit is treated as a new version. Set this once you're shipping.                  |
| `description` | no       | Shown in marketplace listings. One sentence. Make it count.                                                                                        |
| `author`      | no       | Object with `name`, `email`, optional `url`.                                                                                                       |
| `license`     | no       | SPDX identifier (`MIT`, `Apache-2.0`, etc).                                                                                                        |
| `keywords`    | no       | Array of strings, used for marketplace search.                                                                                                     |

### Component-path fields (use only when you deviate from defaults)

| Field          | Default        | Why override                                                |
| -------------- | -------------- | ----------------------------------------------------------- |
| `skills`       | `skills/`      | You want skills in a non-default path.                      |
| `commands`     | `commands/`    | Same.                                                       |
| `agents`       | `agents/`      | Same.                                                       |
| `hooks`        | `hooks/hooks.json` | Inline or alternate path for hook config.               |
| `mcpServers`   | `.mcp.json`    | Inline `mcpServers` object, or alternate config path.       |
| `lspServers`   | `.lsp.json`    | Same.                                                       |

### Default enablement

```json
{ "defaultEnabled": false }
```

Set to `false` if your plugin costs the user money (e.g. calls a paid API). Users must explicitly enable it. Requires Claude Code v2.1.154+.

---

## `skills/<name>/SKILL.md` — the brain

A skill is a markdown file with YAML frontmatter:

```markdown
---
name: my-skill
description: Detailed explanation of when Claude should fire this skill. THIS IS THE TRIGGER SURFACE — write it as if Claude reads only this and the user's prompt.
---

# my-skill

Body content. Treated as system context when the skill fires.
```

### The frontmatter `description` is the entire game

Claude Code decides whether to fire a skill almost entirely from this string. Concrete trigger phrases beat abstract descriptions every time.

Bad:

```yaml
description: A helpful weather assistant.
```

Good:

```yaml
description: Generate travel packing advice from a 5-day OpenWeather forecast for any city. Use this skill when the user asks "what should I pack for [city]", "is it cold in [city] next week", "packing list for [city]", or invokes /weather-sage.
```

### Optional supporting files

```
skills/my-skill/
├── SKILL.md
├── reference.md        # extra context, only loaded when the skill fires
└── scripts/
    └── helper.py       # callable via Bash tool from the skill
```

---

## `commands/<name>.md` — slash commands

A "command" in Claude Code is just a skill with a flat-file structure instead of a directory. The file becomes a `/name` slash command.

```markdown
---
description: One-line summary shown in the slash-command picker.
argument-hint: "[your-arg-name]"
---

# /my-command

Prompt body. When the user types `/my-command something`, Claude receives this body with `$ARGUMENTS` replaced by `something`.
```

`argument-hint` is shown in the picker placeholder. Keep it short.

---

## `.mcp.json` — bundled MCP servers

If your plugin ships an MCP server (e.g. Python wrapper around an API), declare it here. Path-substitution variables like `${CLAUDE_PLUGIN_ROOT}` resolve to the installed plugin's directory.

```json
{
  "mcpServers": {
    "my-plugin-server": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-server/server.py"],
      "env": {
        "PLUGIN_ROOT": "${CLAUDE_PLUGIN_ROOT}"
      }
    }
  }
}
```

Variables available: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.*}`, any `${ENV_VAR}`.

---

## Marketplace.json — distribution

This file does NOT live in your plugin. It lives in a separate repo (or the same repo if you self-host a single-plugin marketplace) at `.claude-plugin/marketplace.json`.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "my-marketplace",
  "version": "1.0.0",
  "description": "Curated Claude Code plugins by me",
  "owner": { "name": "Your Name", "email": "you@example.com" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": { "source": "github", "repo": "you/my-plugin" },
      "description": "What it does",
      "version": "0.1.0",
      "keywords": ["a", "b"]
    }
  ]
}
```

`source` is an **object** whose inner `source` key names the kind — `github`,
`git`, `local`, or `npm` — alongside its locator (`repo` for GitHub, as
`owner/repo`). GitHub is the easiest path for open source. ⚠️ Note: the form
`"source": { "type": "github", ... }` shown in some older docs is **rejected**
by `claude plugin validate` (`plugins.0.source: Invalid input`) — the inner key
is `source`, not `type`.

---

## Validation

```bash
claude plugin validate <plugin-dir>           # warnings allowed
claude plugin validate <plugin-dir> --strict  # warnings fail
```

Validation strictness has changed across CLI versions. On current builds the validator **rejects unrecognized top-level keys as errors** (a `plugin.json` carrying a `displayName` on CLI 2.1.131 fails outright). Keep the manifest to the documented fields above, and run `claude plugin validate .` against the oldest CLI you intend to support before publishing. Use `--strict` in CI to also fail on warnings.

---

## Scope: where plugins install

| Scope     | Settings file                  | Use case                                  |
| --------- | ------------------------------ | ----------------------------------------- |
| `user`    | `~/.claude/settings.json`      | Personal plugins, all projects (default)  |
| `project` | `.claude/settings.json`        | Team plugins shared via git               |
| `local`   | `.claude/settings.local.json`  | Per-project, gitignored                   |
| `managed` | enterprise managed settings    | IT-pushed, read-only                      |

---

## Skills-directory plugins (the dev mode)

For local development, drop your plugin folder at `~/.claude/skills/<name>/` (with its `.claude-plugin/plugin.json`). On the next Claude Code session it loads as `<name>@skills-dir` — no install step, no marketplace needed. Edit `SKILL.md` and changes apply live; other components need `/reload-plugins`.

That's exactly what `git clone ... ~/.claude/skills/...` does in the quickstart.

---

## What PluginForge doesn't generate (yet)

| Component       | Why not (yet)                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| `agents/`       | Subagent files. v0.2 will add an `agents-pack` template.                                                       |
| `hooks/`        | Event handlers (`PostToolUse`, `SubagentStop`, etc). v0.2 will add a `hooks-only` template.                    |
| `output-styles/`| Output style overrides. Niche; add manually if you need them.                                                  |
| `themes/`       | Color themes. Add manually; it's just one JSON file.                                                           |
| LSP server config | LSP integration. Highly language-specific; you'd want to hand-write `.lsp.json`.                             |

If you need any of these, scaffold from the closest template and edit. PluginForge is opinionated about staying minimal until v0.2.
