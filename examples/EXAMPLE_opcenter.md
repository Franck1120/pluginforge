# Example: Wrap OPCENTER in a Claude Code plugin

**OPCENTER** is a Python **tactical analyzer for milsim / softair operation orders** (a local Hephios Lab project, not yet published as a public repo). It's built for the **Mercenari SOCS** team (CSEN Campania circuit): you feed it the OPORD "book" — the official PDF for an op — and it produces a structured tactical sheet for every objective.

Its pipeline runs in phases (the repo is at Phase 1 MVP, with later phases in roadmap):

1. **Parse** — `pdfplumber` extracts text; robust regex recognizes objective blocks (title, narrative, phases+points, the technical line, `IN / CENTRO / OUT` coordinates and transit waypoints) plus the mandatory-equipment list.
2. **Geo intel** — every UTM coordinate (zone **33T**, WGS84) is converted to lat/lon with `pyproj`, with Google Maps links generated.
3. **Briefing** — patrol composition, axis of movement, phase sequencing and per-objective attack plans.
4. **3D terrain** — CesiumJS terrain export.
5. **Memory** — SQLite store of past ops for similarity lookup.

Phase 1 also raises automatic **WARNINGs** from narrative keywords (smoke → orange smoke grenade required, C4 / demolition → shared C4 budget, mine / minefield → safety distance, hostage / wounded → non-combatant to exfiltrate, stealth / "1 shot" → fire constraint, sniper / DMR → long-range profile, breach → breach team, night → IR / shielded lights), aggregates a **material budget** (estimated need vs declared quantity, status OK/TIGHT/SHORT/UNCERTAIN), and pre-flags **crossing risk** (objective pairs within 200 m → patrols may collide, stagger the infils). Coordinates and numbers always come from the book; missing data is marked `DATO NON NEL BOOK`, never invented.

It runs entirely on the operator's machine — no external API — so this is a **`basic`** plugin: one slash command that drives OPCENTER's CLI, plus a skill that helps you reason about the output at the briefing table.

Time to run end-to-end: **~5 minutes**.

---

## 0. Prerequisites

- Claude Code installed.
- PluginForge installed: `claude plugin install Franck1120/pluginforge`.
- OPCENTER cloned and its deps installed (`pip install -r requirements.txt` in the repo; Python 3.10+). The plugin invokes OPCENTER's own `main.py`.
- An empty parent directory: `cd ~/plugins`.

---

## 1. Invoke PluginForge

```
> /pluginforge
```

Intake:

```
1) Plugin name
   > opcenter-brief

2) Description
   > Parses milsim/softair OPORD PDFs with OPCENTER and produces a
     structured tactical sheet (objectives, WARNINGs, material budget)
     plus a markdown briefing.

3) Template:
   [1] basic     [2] mcp     [3] skill-only
   > 1

4) External services
   > none
```

We pick `basic`: OPCENTER runs locally, there's no API to wrap.

---

## 2. What PluginForge writes

```
opcenter-brief/
├── .claude-plugin/plugin.json
├── .gitignore
├── LICENSE
├── README.md
├── commands/
│   └── opcenter-brief.md
└── skills/
    └── opcenter-brief/
        └── SKILL.md
```

Generated `plugin.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "opcenter-brief",
  "version": "0.1.0",
  "description": "Parses milsim/softair OPORD PDFs with OPCENTER and produces a structured tactical sheet plus a markdown briefing.",
  "author": { "name": "Francesco Rocco", "email": "kekkorocco.fr@gmail.com" },
  "license": "MIT",
  "keywords": ["milsim", "softair", "opord", "tactical", "briefing"]
}
```

---

## 3. Wire OPCENTER (rename the command + point it at the CLI)

OPCENTER already ships a multi-phase CLI (`python main.py parse <book.pdf> -o output/`, plus `geo`, `briefing`, `all`, …). The plugin doesn't need a Python wrapper of its own — the slash command just drives that CLI. Tell Claude where OPCENTER lives via an `OPCENTER_HOME` environment variable.

### 3a. Replace `commands/opcenter-brief.md` body

```markdown
---
description: Parse a milsim/softair OPORD PDF with OPCENTER into a tactical sheet + briefing. Reads WARNINGs, material budget, and crossing risks.
argument-hint: "[parse|briefing|all] [path-to-book.pdf]"
---

# /opcenter-brief

`$ARGUMENTS` is `<subcommand> <path>`, e.g. `parse books/op_steel_tiger.pdf`.
Subcommands map to OPCENTER's CLI: `parse` (Phase 1 sheet + data.json),
`briefing` (Phase 3 markdown briefing from a data.json), `all` (full pipeline).

1. If `$ARGUMENTS` is empty, ask for the subcommand and the book path.
2. Run OPCENTER from its install dir:
   `python "${OPCENTER_HOME}/main.py" $ARGUMENTS -o ./opcenter_out/`
   (for `briefing`, the path argument is a `data.json`, not a PDF).
3. OPCENTER writes:
   - `opcenter_out/scheda_tattica.md` — readable tactical sheet
   - `opcenter_out/data.json` — structured data for later phases
   - (briefing) `opcenter_out/briefing.md`
4. Read `data.json`, then summarize for the operator:
   - Objectives with their IN/CENTRO/OUT coordinates and Google Maps links.
   - All WARNINGs grouped by objective, with the required countermeasure.
   - Material budget status (OK/TIGHT/SHORT/UNCERTAIN) and any SHORT items.
   - Crossing-risk pairs (objectives within 200 m) and a staggering suggestion.
5. Never invent coordinates or quantities. If OPCENTER marked something
   `DATO NON NEL BOOK`, surface it as a gap, do not fill it.
```

### 3b. Tighten `skills/opcenter-brief/SKILL.md`

Set the frontmatter `description` to milsim language so the skill fires on natural requests, not just the slash command:

```
description: Analyze a milsim/softair OPORD book with OPCENTER. Use this skill when the user mentions "OP book", "OPORD", "scheda tattica", "briefing milsim", "softair operation order", a Mercenari SOCS / CSEN op, or invokes /opcenter-brief. Parses the PDF, then helps reason about WARNINGs, material budget, and patrol crossing risk.
```

Replace the body's trigger examples and workflow with concrete ones:

- "Analizza il book di questa OP"
- "Genera la scheda tattica da questo PDF"
- "Quali WARNING ci sono su questo obiettivo?"
- "Il budget materiale regge per tutti gli obiettivi?"
- "Ci sono incroci tra pattuglie da scaglionare?"

The skill's job after OPCENTER runs is the *interesting* part: walk the operator through the WARNINGs (e.g. "OBJ BRAVO needs orange smoke and a breach team"), flag SHORT budget items, and propose an infiltration order that avoids the 200 m crossing pairs.

---

## 4. Validate

```bash
cd opcenter-brief
claude plugin validate .
```

Expected: `✔ Validation passed`.

---

## 5. Install locally and test

```bash
ln -s "$(pwd)" ~/.claude/skills/opcenter-brief
export OPCENTER_HOME=~/code/opcenter   # wherever you cloned it
```

Restart Claude Code. There's a synthetic sample book in the OPCENTER repo (`sample/op_steel_tiger.pdf`):

```
> /opcenter-brief parse ~/code/opcenter/sample/op_steel_tiger.pdf
```

Claude runs `python $OPCENTER_HOME/main.py parse ...`, reads the generated `data.json`, and gives you a briefing-table summary:

```
OP STEEL TIGER — 3 objectives

OBJ ALPHA  (IN 33T 0497500 4520100 → maps link)
  WARNINGS: smoke (orange smoke grenade), night (IR/shielded lights)
OBJ BRAVO  (CENTRO 33T 0498100 4520600 → maps link)
  WARNINGS: C4 (shared budget), breach team
CROSSING RISK: ALPHA ↔ BRAVO ~140 m — stagger the two infils.
MATERIAL BUDGET: C4 TIGHT (need 2, declared 2), smoke OK.
```

Natural language triggers the skill too:

```
> Analizza il book softair in ~/ops/csen_aprile.pdf e dimmi i WARNING
```

---

## 6. Publish

```bash
git init && git add . && git commit -m "opcenter-brief v0.1.0"
gh repo create Franck1120/pluginforge-opcenter-example --public --source=. --push
```

Install path for users:

```bash
claude plugin install Franck1120/pluginforge-opcenter-example
```

Same marketplace options as the PhysicsCopilot example (see `EXAMPLE_physicscopilot.md`, step 6): self-host a `marketplace.json` or submit to the official one.

---

## Why this took 5 minutes instead of 50

PluginForge did the boring work — manifest with the right `$schema`, skill frontmatter with the right fields, slash-command frontmatter with `argument-hint`, README, LICENSE, `.gitignore`.

You did the interesting work — pick `basic` (no API to wrap), write the command body that drives OPCENTER's CLI and reads back `data.json`, and craft the skill that turns raw warnings and budget numbers into an actual briefing the team can act on.
