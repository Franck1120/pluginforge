# {{PLUGIN_NAME_HUMAN}}

> {{DESCRIPTION}}

Built with [PluginForge](https://github.com/Franck1120/pluginforge).

## Install

```bash
claude plugin install {{AUTHOR_NAME}}/{{PLUGIN_NAME}}
```

Or, for local development:

```bash
git clone <your-repo-url> ~/.claude/skills/{{PLUGIN_NAME}}
# Restart Claude Code
```

## Usage

Type the slash command in Claude Code:

```
/{{PLUGIN_NAME}}
```

Or just ask Claude to do the thing — the bundled skill will trigger automatically when the conversation matches.

## Components

- `commands/{{PLUGIN_NAME}}.md` — the `/{{PLUGIN_NAME}}` slash command.
- `skills/{{SKILL_SLUG}}/SKILL.md` — the skill that fires on relevant prompts.

## Develop

```bash
# Validate the manifest
claude plugin validate .

# Reload after editing
# (in Claude Code) /reload-plugins
```

## License

MIT — see LICENSE.
