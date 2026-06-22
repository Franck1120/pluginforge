# Example: Wrap PhysicsCopilot's backend in a Claude Code plugin

[PhysicsCopilot](https://github.com/Franck1120/physicscopilot) is **AI-powered real-time guidance for physical work** — point your phone at a machine and it walks you through the repair. Under the hood it's a Flutter app that streams live camera frames over WebSocket to a Go (Fiber) backend, which calls **Gemini 2.5 Flash Vision** and ranks domain context out of a TF-IDF knowledge base of 12 equipment domains (printers, HVAC, automotive, electronics, …).

The live vision loop belongs to the phone — you can't sensibly stream a camera through an MCP tool. But the backend also exposes a plain REST API for **session lifecycle** and **domain discovery**, and *that* is what makes a useful Claude Code plugin: from a terminal session you can ask "which equipment domains does PhysicsCopilot cover?", open a guided-repair session for a specific device, and track its progress — all without leaving Claude Code.

This walks through using PluginForge to scaffold an `mcp` plugin called `physicscopilot-assist` that wraps PhysicsCopilot's REST endpoints.

Time to run end-to-end: **~6 minutes**, assuming the PhysicsCopilot backend is reachable.

---

## 0. Prerequisites

- Claude Code installed (`claude --version`).
- PluginForge installed: `claude plugin install Franck1120/pluginforge`.
- A reachable PhysicsCopilot backend. Either run it locally (`make run` in the repo, default `http://localhost:8080`) or point at a deployed instance. The endpoints we wrap (`/api/domains`, `/api/sessions`) are public per the OpenAPI spec at `GET /api/docs`.
- An empty parent directory: `cd ~/plugins`.

---

## 1. Invoke PluginForge

In a Claude Code session inside `~/plugins/`:

```
> /pluginforge
```

Answer the 4 intake questions:

```
1) Plugin name (kebab-case)
   > physicscopilot-assist

2) One-sentence description
   > Discover PhysicsCopilot repair domains and open guided-repair
     sessions from Claude Code, via the PhysicsCopilot REST API.

3) Template:
   [1] basic     [2] mcp     [3] skill-only
   > 2

4) External services it needs to call
   > physicscopilot-api
```

We pick `mcp` because the plugin talks to a live HTTP API. (If you already described all of this in your opening prompt — "use PluginForge to scaffold an `mcp` plugin called `physicscopilot-assist` that wraps the PhysicsCopilot REST API" — PluginForge skips the intake and just confirms.)

---

## 2. What PluginForge writes

It generates `./physicscopilot-assist/`:

```
physicscopilot-assist/
├── .claude-plugin/plugin.json
├── .mcp.json
├── .gitignore
├── LICENSE
├── README.md
├── commands/
│   └── physicscopilot-assist.md
├── skills/
│   └── physicscopilot-assist/
│       └── SKILL.md
└── mcp-server/
    ├── server.py
    └── requirements.txt
```

The generated `.claude-plugin/plugin.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "physicscopilot-assist",
  "version": "0.1.0",
  "description": "Discover PhysicsCopilot repair domains and open guided-repair sessions from Claude Code, via the PhysicsCopilot REST API.",
  "author": { "name": "Your Name", "url": "https://github.com/your-handle" },
  "license": "MIT",
  "keywords": ["repair", "maintenance", "gemini", "vision", "mcp"],
  "mcpServers": "./.mcp.json"
}
```

> Note: PluginForge deliberately omits `displayName` — older Claude Code CLIs (2.1.131 and earlier) reject it as an unrecognized key and fail validation. See `docs/PLUGIN_ANATOMY.md`.

The generated `mcp-server/server.py` ships `ping` and `echo` stubs. You replace those with calls to the real backend.

---

## 3. Wire the real backend (one file)

Open `mcp-server/server.py` and replace the stub tools with these three. They map 1:1 onto PhysicsCopilot's documented REST endpoints (`GET /api/domains`, `POST /api/sessions`, `GET /api/sessions/{id}`):

```python
import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("physicscopilot-assist-server")

# Backend base URL. Defaults to a local dev server; override per-deployment.
PHYSICSCOPILOT_API = os.environ.get(
    "PHYSICSCOPILOT_API_URL",
    "http://localhost:8080",
)


@mcp.tool()
def list_domains(detailed: bool = False) -> dict:
    """
    List the equipment domains PhysicsCopilot can guide repairs for
    (printer, hvac, automotive, electronics, ...).
    With detailed=True, also returns the number of knowledge-base
    problems per domain. Wraps GET /api/domains.
    """
    params = {"detailed": "true"} if detailed else None
    resp = httpx.get(f"{PHYSICSCOPILOT_API}/api/domains", params=params, timeout=30.0)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def start_session(device_brand: str, device_model: str) -> dict:
    """
    Open a guided-repair session for a device. Returns the session id,
    status, and step counters. The live camera diagnosis then runs in
    the PhysicsCopilot mobile app against this session.
    Wraps POST /api/sessions.
    """
    resp = httpx.post(
        f"{PHYSICSCOPILOT_API}/api/sessions",
        json={"device_brand": device_brand, "device_model": device_model},
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def get_session(session_id: str) -> dict:
    """
    Fetch the current state of a guided-repair session: status,
    detected problem, and current_step / total_steps progress.
    Wraps GET /api/sessions/{id}.
    """
    resp = httpx.get(f"{PHYSICSCOPILOT_API}/api/sessions/{session_id}", timeout=30.0)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    mcp.run()
```

Make sure `httpx` is in `mcp-server/requirements.txt` (PluginForge already lists `mcp`; add `httpx`).

Then tighten two files PluginForge scaffolded:

- **`skills/physicscopilot-assist/SKILL.md`** — replace the placeholder "Available tools" list with the three real tools, and set the frontmatter `description` to concrete triggers: *"which devices can PhysicsCopilot fix", "what repair domains are supported", "start a repair session for my <brand> <model>", "check my PhysicsCopilot session status".*
- **`commands/physicscopilot-assist.md`** — replace the TODO body with: *"If the user names a device, call `start_session`; if they ask what's supported, call `list_domains`; if they give a session id, call `get_session` and report status + step progress."*

That's the only real work. Everything else PluginForge wrote is correct.

---

## 4. Validate

```bash
cd physicscopilot-assist
claude plugin validate .
```

Expected: `✔ Validation passed`.

---

## 5. Test locally (without publishing)

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)" ~/.claude/skills/physicscopilot-assist
cd mcp-server && pip install -r requirements.txt && cd ..
```

Restart Claude Code, run `/plugin`, and enable `physicscopilot-assist@skills-dir`. With the backend running, try:

```
> /physicscopilot-assist what equipment can you help me fix?
```

The bundled MCP server calls `list_domains` and returns the 12 domains:

```
PhysicsCopilot covers: printer, laptop, kitchen-appliances, hvac,
automotive, industrial-equipment, electronics, home-appliances,
smartphone, furniture, garden, photography.
```

Then:

```
> /physicscopilot-assist start a repair session for my Bosch WAU28T0 washing machine
```

`start_session("Bosch", "WAU28T0")` returns a session id and step counters; you continue the live diagnosis in the PhysicsCopilot app, pointing the phone at the machine.

---

## 6. Publish to the marketplace

```bash
git init && git add . && git commit -m "physicscopilot-assist v0.1.0"
gh repo create Franck1120/pluginforge-physicscopilot-example --public --source=. --push
```

Users can then grab it directly:

```bash
claude plugin install Franck1120/pluginforge-physicscopilot-example
```

To list it in a marketplace, add an entry to a `.claude-plugin/marketplace.json` (see `docs/PLUGIN_ANATOMY.md`):

```json
{
  "name": "physicscopilot-assist",
  "source": { "source": "github", "repo": "Franck1120/pluginforge-physicscopilot-example" },
  "description": "Discover PhysicsCopilot repair domains and open guided-repair sessions from Claude Code.",
  "version": "0.1.0",
  "keywords": ["repair", "maintenance", "vision"]
}
```

---

## What this plugin does — and doesn't

**Does:** domain discovery and session lifecycle over the REST API, from inside Claude Code.

**Doesn't:** the real-time camera vision loop. That's a WebSocket frame stream to Gemini 2.5 Flash and lives in the Flutter mobile client — an MCP tool isn't the right surface for live video. This plugin is the terminal-side companion to the app, not a replacement for it.

---

## Total damage

- Files touched after `pluginforge` ran: **2** (`server.py`, plus one line in `requirements.txt`), and prose edits to `SKILL.md` / the command body.
- Lines of code written by hand: **~50**.
- Time to a working, installed plugin: **~6 minutes**.
