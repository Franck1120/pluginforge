---
description: {{DESCRIPTION}}
argument-hint: "[query]"
---

# /{{PLUGIN_NAME}}

{{DESCRIPTION}}

This command delegates to the `{{SKILL_SLUG}}` skill, which uses tools exposed by the bundled MCP server (`mcp-server/server.py`).

When invoked:

1. If `$ARGUMENTS` is empty, ask the user once what they want.
2. Decide which MCP tool to call based on the request.
3. Call the tool. Show results.
4. If the tool returns an error, surface it cleanly. Do not retry blindly.

Available external services wired through the MCP server:

{{MCP_SERVICES_LIST}}

Keep responses tight. Default to one paragraph plus a code block if relevant.
