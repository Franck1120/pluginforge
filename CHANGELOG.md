# Changelog

All notable changes to PluginForge are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-06-15

Initial public release.

### Added
- `plugin-generator` skill (PluginForge): 4-question intake that scaffolds a
  complete, installable Claude Code plugin to disk.
- `/pluginforge` slash command.
- Three templates: `basic` (command + skill), `mcp` (bundled Python MCP server
  stub), and `skill-only` (skills, no commands).
- Documentation: `docs/QUICKSTART.md` and `docs/PLUGIN_ANATOMY.md`.
- Worked examples wrapping real projects: `examples/EXAMPLE_physicscopilot.md`
  (an `mcp` plugin over the PhysicsCopilot REST API) and
  `examples/EXAMPLE_opcenter.md` (a `basic` plugin driving the OPCENTER CLI).
- MIT license.

### Fixed
- Removed `displayName` from the plugin manifest and all three templates: older
  Claude Code CLIs (≤ 2.1.131) reject it as an unrecognized key and fail
  `claude plugin validate`. Documented the version constraint in
  `docs/PLUGIN_ANATOMY.md`.
- Replaced the placeholder GitHub username with `Franck1120`
  across the manifest, README, quickstart, templates, and examples.
- Rewrote both worked examples to match the real upstream projects (the prior
  drafts described features that did not exist).

[Unreleased]: https://github.com/Franck1120/pluginforge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Franck1120/pluginforge/releases/tag/v0.1.0
