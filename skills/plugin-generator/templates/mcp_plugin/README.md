# {{PLUGIN_NAME_HUMAN}}

> {{DESCRIPTION}}

Built with [PluginForge](https://github.com/Franck1120/pluginforge). Bundles a Python MCP server.

## External services this plugin talks to

{{MCP_SERVICES_LIST}}

Set the corresponding API keys via the plugin's `userConfig` (prompted at enable time) or as environment variables — see `mcp-server/server.py` for the exact names.

## Install

```bash
claude plugin install {{AUTHOR_NAME}}/{{PLUGIN_NAME}}
```

The MCP server requires Python 3.10+ and starts automatically when the plugin is enabled. Install its dependencies first:

```bash
cd ~/.claude/plugins/{{PLUGIN_NAME}}/mcp-server
pip install -r requirements.txt
```

## Usage

```
/{{PLUGIN_NAME}} [your query]
```

The slash command invokes the MCP tools exposed by the bundled server.

## Components

- `commands/{{PLUGIN_NAME}}.md` — the `/{{PLUGIN_NAME}}` slash command.
- `skills/{{SKILL_SLUG}}/SKILL.md` — the skill that fires on relevant prompts.
- `mcp-server/server.py` — the Python MCP server, exposing tools that wrap your external services.
- `.mcp.json` — wires the server into Claude Code.

## Develop the MCP server

```bash
cd mcp-server
pip install -r requirements.txt
python server.py   # boots on stdio; Claude Code will start it for you in normal use
```

## Validate

```bash
claude plugin validate .
```

## License

MIT — see LICENSE.
