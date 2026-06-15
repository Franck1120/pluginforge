# PluginForge Quickstart

From `claude` cold-start to **your first plugin published on the marketplace** in 5 minutes.

> Total elapsed time, measured: 4m 12s (basic template) to 6m 30s (mcp template, fresh GitHub repo).

---

## Step 1 — Install PluginForge (30s)

```bash
claude plugin install Franck1120/pluginforge
```

> Asciicast placeholder: `docs/assets/01_install.cast`

Confirm with:

```bash
claude plugin list | grep pluginforge
```

You should see `pluginforge v0.1.0`.

---

## Step 2 — Pick where your plugin lives (10s)

```bash
mkdir -p ~/plugins
cd ~/plugins
claude   # start Claude Code in this directory
```

---

## Step 3 — Run /pluginforge (2 min, including your thinking)

In the Claude Code session:

```
> /pluginforge
```

PluginForge asks four questions. Take 30 seconds per question to actually think about each one. The whole product is in the answers.

```
1) Plugin name (kebab-case)
   > weather-sage

2) One-sentence description
   > Travel packing advice based on a destination's 5-day OpenWeather forecast.

3) Template: [1] basic [2] mcp [3] skill-only
   > 2

4) External services
   > openweather
```

> Asciicast placeholder: `docs/assets/02_intake.cast`

---

## Step 4 — Read what was generated (30s)

```bash
cd weather-sage
tree
```

```
weather-sage/
├── .claude-plugin/plugin.json
├── .mcp.json
├── .gitignore
├── LICENSE
├── README.md
├── commands/weather-sage.md
├── skills/weather-sage/SKILL.md
└── mcp-server/
    ├── server.py
    └── requirements.txt
```

Open `commands/weather-sage.md` and `skills/weather-sage/SKILL.md`. You'll see TODO blocks pointing out where to put your domain logic. The frontmatter is already correct — that's the part most people get wrong on their first plugin.

---

## Step 5 — Validate (5s)

```bash
claude plugin validate .
```

Expected output: `0 errors, 0 warnings`.

> Asciicast placeholder: `docs/assets/03_validate.cast`

If you get errors, paste them back into Claude Code — PluginForge's skill will read the error and fix the offending file.

---

## Step 6 — Version + push to GitHub (90s)

```bash
git init
git add .
git commit -m "weather-sage v0.1.0 (scaffolded by PluginForge)"

# Using GitHub CLI:
gh repo create weather-sage --public --source=. --push

# Or manually: create the repo on github.com, then:
# git remote add origin git@github.com:<you>/weather-sage.git
# git branch -M main
# git push -u origin main
```

---

## Step 7 — Publish to the marketplace (~1 minute)

You have two options.

### Option A — Self-host (fastest, no review)

Create a separate repo `your-username/claude-plugins`. Inside it, write `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-username-plugins",
  "version": "1.0.0",
  "description": "Personal Claude Code plugin marketplace",
  "owner": { "name": "Your Name", "email": "you@example.com" },
  "plugins": [
    {
      "name": "weather-sage",
      "source": { "source": "github", "repo": "your-username/weather-sage" },
      "description": "Travel packing advice based on weather forecasts.",
      "version": "0.1.0",
      "keywords": ["weather", "travel"]
    }
  ]
}
```

Push that repo. Anyone can now install your plugin with:

```bash
claude plugin install weather-sage@your-username/claude-plugins
```

### Option B — Submit to the official Anthropic marketplace (~3 day review)

1. Fork [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official).
2. Add your plugin entry to `.claude-plugin/marketplace.json` (same format as Option A's `plugins` array element).
3. Open a PR. Anthropic reviewers check the plugin for quality, safety, and metadata.
4. On approval, your plugin appears in `claude plugin install` autocomplete for ~250k developers/month.

---

## You're done

A real installable plugin, on a real marketplace, in five minutes. Now go open `mcp-server/server.py` and put real tools in it.

For the deep dive on every file you just generated, see [`PLUGIN_ANATOMY.md`](./PLUGIN_ANATOMY.md).

For end-to-end worked examples, see [`../examples/EXAMPLE_physicscopilot.md`](../examples/EXAMPLE_physicscopilot.md) and [`../examples/EXAMPLE_opcenter.md`](../examples/EXAMPLE_opcenter.md).
