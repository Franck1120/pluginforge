# {{PLUGIN_NAME_HUMAN}}

> {{DESCRIPTION}}

Built with [PluginForge](https://github.com/Franck1120/pluginforge). Pure skills — no slash commands, no MCP server. The cleanest possible plugin.

## Install

```bash
claude plugin install {{AUTHOR_NAME}}/{{PLUGIN_NAME}}
```

## How to use

There is no slash command. Just talk to Claude:

- "Help me with X"
- "Do Y for me"
- "Analyze this Z"

The bundled skill triggers automatically when the conversation matches its description.

## Components

- `skills/{{SKILL_SLUG}}/SKILL.md` — the skill.

## Develop

Edit the skill, then run `/reload-plugins` in Claude Code (no restart needed for SKILL.md edits).

```bash
claude plugin validate .
```

## License

MIT — see LICENSE.
