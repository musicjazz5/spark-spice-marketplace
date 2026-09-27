# Claude Code Configuration for spark-spice-marketplace

## Overview
This repository integrates **spark-spice**, an MCP server for analog circuit design using BSIM4 Level-54 silicon models and Razavi gm/Id methodology.

## MCP Server: spark-spice

### Endpoint
```
sse://spark-9fd5.anthropic.com/spark-spice
```

### Available Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| `size_analog_block` | Full BSIM4 simulation + sizing | Generate netlists, W/L ratios, operating points |
| `characterize_device` | gm/Id sweep (6–22 V⁻¹ range) | Device selection for each stage |
| `explore_design_space` | Table-based feasibility check | Fast spec validation (≤3 seconds) |
| `recall_designs` | Cached design database | Find prior solutions near target spec |
| `query_device_table` | Single gm/Id operating point | Fine-grained device metrics |

### Example: Miller OTA Design (60 dB, 50 MHz)

```python
# 1. Check feasibility (free, <3s)
explore_design_space(
    block="miller_ota",
    gain_db=60, gbw_Hz=50e6,
    method="razavi"
)

# 2. Full design with BSIM4 (52.8s)
size_analog_block(
    block="miller_ota",
    gain_db=60, gbw_Hz=50e6,
    method="razavi",
    c_load_F=2e-12,
    power_W=0.00015
)
```

Response includes:
- **Procedure**: R1–R8 hand-design steps (Razavi method)
- **Simulated**: AC gain, UGBW, phase margin, noise, slew rate
- **Design**: transistor gm/Id, L, W, I₁, I₂, Cc, Rz
- **Headroom**: per-device saturation margins

## Setup & Usage

### Prerequisites
1. Claude Code CLI: `brew install anthropic/anthropic/anthropic-cli` (macOS) or `apt install anthropic` (Linux)
2. Authentication: `ant auth login`
3. Git: `git clone https://github.com/musicjazz5/spark-spice-marketplace`

### Load this Project's Config

```bash
# Clone and enter repo
git clone https://github.com/musicjazz5/spark-spice-marketplace
cd spark-spice-marketplace

# Option A: Use project-level settings
# Claude Code automatically loads .claude/settings.json
ant query "help me design a 60 dB OTA"

# Option B: Copy to home config (global)
cp .claude/settings.json ~/.claude/settings.json
```

### Verify MCP Connection

```bash
# Check MCP server status
ant status

# List all available tools
ant beta:mcp list

# Test spark-spice connection
ant query "List the tools available in spark-spice"
```

## Common Workflows

### 1. Quick Spec Feasibility Check
**Cost**: negligible  
**Time**: <3 seconds

```bash
ant query "Can I design a 60 dB, 50 MHz Miller OTA on 150 µW?"
# Uses explore_design_space (table lookup only)
```

### 2. Full Design with BSIM4 Simulation
**Cost**: ~$0.50 (Sonnet) / ~$0.05–$0.26 (spark-spice compute)  
**Time**: 50–60 seconds

```bash
ant query "Design a 60 dB, 50 MHz Miller OTA using Razavi gm/Id method. Include BSIM4 simulation."
# Uses size_analog_block (3× AC + 1× transient simulation)
```

### 3. Device Characterization (for component selection)
**Cost**: negligible  
**Time**: <5 seconds

```bash
ant query "Characterize an NMOS device at L=150nm, sweeping gm/Id from 6 to 20 V⁻¹. Show ft, noise, Rout."
# Uses characterize_device
```

## Model & Performance Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Model | `claude-opus-5` | Fast, cost-effective; use `claude-fable-5` for complex specs |
| Thinking | adaptive | No `budget_tokens` on Opus 5; effort tuning is the lever |
| Effort | `high` | Circuit design is complex; use `xhigh` for mission-critical designs |
| Streaming | enabled | Long spark-spice runs benefit from progress visibility |
| Cache | enabled | System prompt caches; ~60% hit rate on repeated queries |

### Cost Optimization Tiers

| Task | Model | Cost | Time |
|------|-------|------|------|
| Feasibility + table lookup | Haiku 4.5 | $0.01 | <5s |
| Full design (BSIM4) | Opus 5 | $0.60 | 55s |
| Multi-design exploration | Sonnet 5 | $0.15/run | 60s |

## Troubleshooting

### "spark-spice server not connected"
- Check internet connectivity
- Verify `settings.json` has the correct URL: `sse://spark-9fd5.anthropic.com/spark-spice`
- Restart Claude Code: `ant --reset`

### "BSIM4 simulation failed"
- Spec may be infeasible (e.g., extreme gain/GBW on low power)
- Run `explore_design_space` first to validate
- Check `binding` field in response for the limiting constraint

### "Tool not found in spark-spice"
- Confirm MCP is connected: `ant beta:mcp list`
- spark-spice tool set is static; new tools require server update

## Integration Examples

### Python + Anthropic SDK
```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    system="You have access to spark-spice tools for analog circuit design.",
    messages=[
        {"role": "user", "content": "Design a 60 dB OTA using Razavi method"}
    ]
)
print(response.content[0].text)
```

### Claude Code CLI
```bash
ant query "What is the phase margin of a 50 MHz Miller OTA?"
ant query --file design-spec.txt "Turn this into a netlist"
```

## Resources

- **spark-spice Documentation**: In-MCP help via `ant query "Describe size_analog_block parameters"`
- **Razavi Method**: Reference in [tool procedure output](./examples/miller-ota-razavi.md)
- **BSIM4 Model**: Level-54 (Verilog-A), default 150 nm CMOS
- **Examples**: See `./plugins/` for integration samples

## Contributing

1. Run a design: `ant query "Design [spec]"`
2. Capture the output artifact and result
3. Save to `./plugins/[design-name]/` with:
   - `netlist.cir` (SPICE netlist)
   - `design.json` (sizing parameters)
   - `report.html` (Claude-generated report)
4. Update `catalog.json` and push:
   ```bash
   git add .
   git commit -m "Add [design] to catalog"
   git push
   ```

## Security & Privacy

- `.claude/settings.local.json` is not tracked (add sensitive local overrides here)
- No credentials stored in this repo; use `ant auth login` for authentication
- spark-spice runs on Anthropic's infrastructure; no data is logged beyond MCP transaction records

## License

This repository and all designs are provided under the MIT License. See LICENSE for details.
