---
name: {{SKILL_SLUG}}
description: {{DESCRIPTION}} Use this skill when the user asks for {{PLUGIN_NAME_HUMAN}}-related help, or when they invoke /{{PLUGIN_NAME}}. The skill calls tools exposed by the bundled MCP server.
---

# {{SKILL_SLUG}}

{{DESCRIPTION}}

## When to use this skill

Replace these with concrete trigger phrases tailored to your domain.

- "Help me with X"
- "Look up Y in [external service]"
- "Run Z against the live data"

## Available tools (from the bundled MCP server)

The MCP server in `mcp-server/server.py` exposes these tools. Edit `server.py` to add your real ones.

- `ping` — health check, returns "pong". Use to confirm the server is reachable.
- `echo` — debug helper, returns the input string.

Add a tool per external service:
{{MCP_SERVICES_LIST}}

## Workflow

1. Confirm the request maps to an available tool. If not, say so and stop.
2. Call the tool with validated arguments.
3. Summarize the response. Do not dump raw JSON unless asked.
4. If the tool errors, surface the error verbatim and suggest a fix (often: missing API key, wrong arg type).

## Hard rules

- Never invent tool names. Only call tools the MCP server actually exposes.
- Never store API keys in the conversation. Rely on `userConfig` or environment variables.
- Never silently retry on auth errors. Tell the user the key is missing.

---

Built with [PluginForge](https://github.com/Franck1120/pluginforge).
