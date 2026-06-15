# Contributing to PluginForge

Thanks for wanting to help. PluginForge is small on purpose — keep contributions
focused and the bar is easy to clear.

## Ways to contribute

- **Report a bug** — open an issue with the bug-report template. Include your
  `claude --version`, the template you used, and the exact `claude plugin validate`
  output.
- **Request a feature** — open an issue with the feature-request template. New
  templates (hooks-only, agents-pack, output-style) are explicitly on the roadmap.
- **Send a PR** — see below.

## Development setup

PluginForge is a Claude Code plugin, not a compiled project. To work on it:

```bash
git clone https://github.com/Franck1120/pluginforge
cd pluginforge

# Load it as a skills-directory plugin for live testing
ln -s "$(pwd)" ~/.claude/skills/pluginforge
# Restart Claude Code, then run /pluginforge
```

Python 3.10+ is needed only to run the validation script.

## Before you open a PR

Run the structure check that CI runs:

```bash
python scripts/validate.py
```

It must report all checks passing. The check:
- parses `.claude-plugin/plugin.json`,
- renders each template with dummy values and validates the result parses as JSON,
- confirms every `SKILL.md` has YAML frontmatter with `name` and `description`,
- byte-compiles the MCP template's `server.py`.

If you have the Claude Code CLI, also run `claude plugin validate .` on the repo
and on a freshly generated plugin.

## Conventions

- **Manifests stay minimal.** Ship only documented fields. In particular, do not
  re-add `displayName` to templates — older CLIs reject unknown keys (see
  `docs/PLUGIN_ANATOMY.md`).
- **Examples must be real.** If you add a worked example, it has to describe a
  project that actually exists and behaves as written. No invented features.
- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, …) and are atomic.

## Code of conduct

Be decent. Assume good faith. That's the whole policy.
