# Spark SPICE — Analog Design MCP for Claude Code

BSIM4 analog circuit design tools on a DGX Spark GB10.  
Design Miller OTAs, LC VCOs, and more — directly from Claude Code.

---

## Install (2 steps)

### Step 1 — Get an API key

```bash
curl -X POST http://100.69.76.67:8089/apply \
  -H "Content-Type: application/json" \
  -d '{"name":"Your Name","email":"you@example.com"}'
```

You'll get back a `spk_...` key immediately.

> **Note:** 100.69.76.67 is a Tailscale IP. You need [Tailscale](https://tailscale.com) running and connected to the same network.

---

### Step 2 — Add the MCP server to Claude Code

```bash
claude mcp add \
  --transport sse \
  --header "X-API-Key: spk_YOUR_KEY_HERE" \
  --scope user \
  spark-spice \
  http://100.69.76.67:8090/sse
```

Restart Claude Code. Done.

---

## Usage

After installing, ask Claude naturally:

| What you say | What runs |
|---|---|
| `characterize NMOS 150nm` | `characterize_device` |
| `gm/Id=12 PMOS noise 是多少` | `query_device_table` |
| `設計 60dB 50MHz Miller OTA` | `explore_design_space` → `size_analog_block` |
| `razavi gm/Id 方法設計 OTA` | `size_analog_block(method="razavi")` |
| `80dB 200MHz 可行嗎` | `explore_design_space` |
| `5GHz LC VCO, phase noise -110dBc` | `size_vco` |
| `之前有設計過類似的嗎` | `recall_designs` |

---

## Available Tools

| Tool | Description | Speed |
|------|-------------|-------|
| `characterize_device` | gm/Id sweep — Id/W, gm/W, ft, noise, Cgg, Rout | fast |
| `query_device_table` | Single operating-point lookup | fast |
| `explore_design_space` | Feasibility check (GPU-accelerated, 2M samples) | ~2s |
| `size_analog_block` | Miller OTA / OTA-5T sizing + BSIM4 simulation | 1–10 min |
| `size_vco` | LC VCO design + phase noise simulation | 1–5 min |
| `recall_designs` | Search previous designs by spec | fast |

---

## Recommended workflow

```
1. characterize_device   → understand the device at your target inversion level
2. explore_design_space  → confirm the spec is reachable (seconds, not minutes)
3. size_analog_block     → get a simulated design with real numbers
```

Always run `explore_design_space` before `size_analog_block` — it catches infeasible specs in seconds instead of wasting a 10-minute simulation.

---

## Example prompts

```
幫我設計一個 60dB 50MHz Miller OTA，150µW power，2pF load，razavi gm/Id 方法
```

```
NMOS 150nm, gm/Id 從 4 到 20，回傳 ft, γ, 1/f corner, intrinsic gain
```

```
80dB 200MHz Miller OTA 可行嗎？binding constraint 是什麼？
```

```
設計 5GHz LC VCO，phase noise -110dBc/Hz at 1MHz offset
```

---

## Requirements

- [Claude Code](https://claude.ai/code) (any version)
- [Tailscale](https://tailscale.com) — to reach the DGX Spark server at 100.69.76.67

---

## Backend

- **Server:** DGX Spark GB10 (NVIDIA Blackwell, CUDA 13)
- **Simulator:** BSIM4 level-54 via ngspice
- **GPU search:** CuPy-accelerated `explore_design_space` — 2M samples in ~1.5s
- **MCP endpoint:** `http://100.69.76.67:8090/sse`
- **API endpoint:** `http://100.69.76.67:8089`
