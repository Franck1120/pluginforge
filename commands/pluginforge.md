---
description: Scaffold a complete Claude Code plugin from a one-line idea. Asks 4 questions, writes the directory, validates it.
argument-hint: "[plugin-name] [template: basic|mcp|skill-only]"
---

# /pluginforge

You are about to scaffold a new Claude Code plugin using PluginForge.

If the user provided arguments (e.g. `/pluginforge weather-sage mcp`), pre-fill the plugin name and template. Otherwise, run the **plugin-generator** skill's standard 4-question intake.

Follow the procedure in `skills/plugin-generator/SKILL.md`:

1. Ask the 4 intake questions (name, description, template, external services).
2. Compute placeholder substitutions.
3. Copy the chosen template into `./<plugin-name>/`, substituting placeholders in file contents and paths.
4. Run `claude plugin validate ./<plugin-name>` (or a JSON-load fallback) and fix any errors.
5. Print the next-steps block.
6. Offer the three follow-up actions.

Do not invent new templates. Do not overwrite existing directories silently. Do not edit projects outside the new plugin directory.

If the user already gave you most of the answers in their prompt, skip the intake question for those answers and confirm before generating.
