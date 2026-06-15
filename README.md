# PluginForge

> **The plugin that builds plugins.** Scaffold a publishable Claude Code plugin from a one-line idea in under 60 seconds.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-d97757)](https://code.claude.com)
[![Status: MVP](https://img.shields.io/badge/Status-MVP-orange)]()

---

## Why this exists

Claude Code shipped its **Plugin Marketplace** in May 2026. 250k developers/month browse it. 15% rev share on paid plugins. The whole stack is sitting there, waiting.

But getting your first plugin published is a paper cut:

- `claude plugin init` gives you a skeleton — no opinionated structure, no templates, no walkthrough.
- The manifest schema lives in three different docs pages.
- Nobody explains how to wire a Python MCP server into a plugin in less than an afternoon.
- "How do I actually publish this to the marketplace?" — buried in a sub-page.

**PluginForge is the on-ramp.** You say what you want. Claude Code, guided by the `plugin-generator` skill, asks you 4 questions and writes the entire plugin to disk — manifest, skill, commands, MCP server stub, README, license, the works.

---

## 30-second demo

```text
$ claude
> /pluginforge

PluginForge -- let's build a plugin.

1) What's your plugin called? (kebab-case)
   > physicscopilot-tutor

2) One sentence: what does it do?
   > Turns a textbook problem photo into a worked solution

3) Pick a template:
   [1] basic      -- one command + one skill   (most plugins)
   [2] mcp        -- bundles a Python MCP server
   [3] skill-only -- pure skills, no slash commands
   > 2

4) Any external services it needs to talk to? (comma-separated, blank for none)
   > openai, wolfram-alpha

Generating physicscopilot-tutor/ ...
  + .claude-plugin/plugin.json
  + skills/physicscopilot-tutor/SKILL.md
  + commands/physicscopilot-tutor.md
  + mcp-server/server.py
  + mcp-server/requirements.txt
  + .mcp.json
  + README.md
  + LICENSE
  + .gitignore

Validating ... ok (0 errors, 0 warnings)

Next:
  cd physicscopilot-tutor
  claude plugin validate .
  git init && git add . && git commit -m "initial scaffold"
  See: docs/PUBLISHING.md to push to the marketplace.
```

> Asciicast placeholder: `docs/assets/demo.cast` — record with `asciinema rec` once the slash command is wired.

---

## Install

```bash
# From the official marketplace (once published)
claude plugin install pluginforge@anthropic-official

# Or directly from this repo
claude plugin install Franck1120/pluginforge
```

To try it before it's marketplace-ready, clone and add it as a skills-directory plugin:

```bash
git clone https://github.com/Franck1120/pluginforge ~/.claude/skills/pluginforge
# Restart Claude Code
```

---

## Quick example

```text
> Build me a Claude Code plugin called "weather-sage" that queries the OpenWeather API
  and gives travel packing advice. Use PluginForge.

Claude (PluginForge skill activates):
  I'll scaffold this for you. A few questions:
  - Plugin name: weather-sage (kebab-case OK)
  - Description: "Travel packing advice driven by OpenWeather forecasts."
  - Template: I'd recommend `mcp` since you need a live API. Confirm?
  - External services: openweather. Anything else?
  ...

[generates 9 files in ./weather-sage/]
```

That's it. The directory is a valid, installable Claude Code plugin.

---

## What's in this repo

```
pluginforge/
├── .claude-plugin/plugin.json   # The PluginForge plugin manifest
├── skills/plugin-generator/     # The brain: SKILL.md + templates
├── commands/pluginforge.md      # /pluginforge slash command
├── examples/                    # Real walkthroughs (PhysicsCopilot, OPCENTER)
├── docs/                        # QUICKSTART + PLUGIN_ANATOMY
├── scripts/validate.py          # Structure + JSON lint (run by CI)
├── .github/                     # Issue templates + test workflow
├── CHANGELOG.md                 # Versioned change log
├── CONTRIBUTING.md              # How to contribute
├── LICENSE                      # MIT
└── README.md
```

---

## Roadmap

**v0.1 (now)** — Three templates (basic, mcp, skill-only). Manual `git init` after.

**v0.2 (week 1)** — Auto-validate with `claude plugin validate --strict`. More templates (hooks-only, agents-pack, output-style).

**v0.3 (week 2)** — `--auto-publish` flag: creates GitHub repo, pushes, opens marketplace PR.

**v0.4 (month 1)** — Skill linter: critiques your trigger description with eval queries before you ship.

**v0.5+** — Telemetry on plugins generated, leaderboard of most-installed forged plugins, Pro tier ($19/mo) with private templates.

---

## Author

**Hephios Lab** — [Francesco "Kekko" Rocco](mailto:kekkorocco.fr@gmail.com)
Cloud / System Engineer. Builder of [PhysicsCopilot](https://github.com/Franck1120/physicscopilot), OPCENTER, and Sapori.

If PluginForge saves you an afternoon, ping me on X (`@kekko`) or open an issue with what you built.

---

## License

MIT. Use it, fork it, sell what you build with it.
