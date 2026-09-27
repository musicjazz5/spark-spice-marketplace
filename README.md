# spark-spice-marketplace

A **Claude Code + spark-spice** marketplace for analog circuit designs. Design OTAs, comparators, gain stages, and other analog blocks using BSIM4 simulation and Razavi gm/Id methodology.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/musicjazz5/spark-spice-marketplace
cd spark-spice-marketplace
```

### 2. Install Claude Code
**macOS:**
```bash
brew install anthropic/anthropic/anthropic-cli
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://apt.anthropic.com/key.gpg | sudo apt-key add -
echo "deb [signed-by=/usr/share/keyrings/anthropic-keyring.gpg] https://apt.anthropic.com stable main" | sudo tee /etc/apt/sources.list.d/anthropic.list
sudo apt update
sudo apt install anthropic
```

### 3. Authenticate
```bash
ant auth login
```

### 4. Design a Circuit
```bash
# Load the project config (auto-loads .claude/settings.json)
ant query "Design a 60 dB, 50 MHz Miller OTA using Razavi gm/Id method with BSIM4 simulation"
```

That's it! Claude will:
1. ✓ Check feasibility (explore_design_space)
2. ✓ Recall any cached prior designs
3. ✓ Run full BSIM4 simulation (size_analog_block)
4. ✓ Generate a formatted design report

## 📁 Repository Structure

```
spark-spice-marketplace/
├── .claude/                    # Claude Code configuration
│   ├── settings.json          # MCP server setup + permissions
│   ├── CLAUDE.md              # Detailed setup & usage guide
│   └── .gitignore            # Security: exclude local overrides
├── .github/
│   └── workflows/
│       └── design-ci.yml      # GitHub Actions CI/CD
├── plugins/                    # Published circuit designs
│   └── miller-ota-60dB/
│       ├── design.json        # Sizing parameters
│       ├── netlist.cir        # SPICE netlist
│       └── report.html        # Generated design report
├── catalog.json               # Design index & metadata
├── spark-spice.json          # MCP server manifest
└── README.md                  # This file
```

## 🛠 Claude Code Configuration

### MCP Server: spark-spice
**Endpoint:** `sse://spark-9fd5.anthropic.com/spark-spice`

**Available Tools:**
- `size_analog_block` — Full BSIM4 simulation + transistor sizing
- `characterize_device` — gm/Id sweep (device selection)
- `explore_design_space` — Fast feasibility check (<3s)
- `recall_designs` — Look up cached prior solutions
- `query_device_table` — Single-point device metrics

**Recommended Models:**
| Task | Model | Cost | Time |
|------|-------|------|------|
| Feasibility check | Haiku 4.5 | $0.01 | <5s |
| Full design (BSIM4) | Opus 5 | $0.50 | 55s |
| Exploration (many specs) | Sonnet 5 | $0.15/run | 60s |

### Load Project Configuration
```bash
# Option 1: Auto-load from .claude/settings.json
ant query "Design ..."

# Option 2: Copy to global settings
cp .claude/settings.json ~/.claude/settings.json
ant query "Design ..."

# Option 3: Verify MCP is connected
ant beta:mcp list
ant status
```

## 📚 Design Examples

### Miller OTA (60 dB, 50 MHz)
```bash
ant query "Design a 60 dB, 50 MHz Miller OTA. \
  Constraints: 150 µW max power, 2 pF load. \
  Use Razavi gm/Id method with BSIM4 simulation. \
  Return: procedure (R1-R8), sizing, headroom analysis."
```

**Output includes:**
- Procedure: 8 hand-design steps (Razavi methodology)
- Simulated DC gain: 67.97 dB ✓
- UGBW: 52.05 MHz ✓
- Phase margin: 84.27° ✓
- Noise: 17.8 nV/√Hz (white)
- Transistor W/L ratios & operating points

### Folded-Cascode OTA
```bash
ant query "Design a folded-cascode OTA for a 10-bit ADC. \
  Specs: 70 dB gain, 100 MHz GBW, 1 pA input-referred noise. \
  Power budget: 500 µW. Use BSIM4 simulation."
```

### Gain Stage Characterization
```bash
ant query "Characterize an NMOS differential pair at L=150nm. \
  Sweep gm/Id from 6–20 V⁻¹. Report: intrinsic gain, fT, noise, Rout. \
  Use spark-spice characterize_device."
```

## 🔧 Development & Contribution

### Add a New Design to the Catalog

1. **Run a design query:**
   ```bash
   ant query "Design [your spec]" > design-output.txt
   ```

2. **Save to plugins:**
   ```bash
   mkdir -p plugins/[design-name]
   cp design-output.txt plugins/[design-name]/report.html
   ```

3. **Extract metadata to design.json:**
   ```json
   {
     "name": "Miller OTA 60dB",
     "spec": {
       "gain_db": 60,
       "gbw_Hz": 50e6,
       "power_W": 150e-6
     },
     "result": {
       "gain_db": 67.97,
       "ugbw_Hz": 52.05e6,
       "pm_deg": 84.27,
       "power_W": 0.000152
     },
     "method": "razavi",
     "bsim4_version": "level-54"
   }
   ```

4. **Update catalog.json:**
   ```bash
   # See catalog.json for format
   ```

5. **Commit and push:**
   ```bash
   git add plugins/ catalog.json
   git commit -m "Add Miller OTA (60 dB, 50 MHz)"
   git push
   ```

## 🔐 Security & Authentication

- **No credentials stored in repo** — use `ant auth login` to set up credentials
- **Local overrides:** Create `.claude/settings.local.json` for machine-specific settings (not tracked)
- **API key** — set `ANTHROPIC_API_KEY` env var or let `ant auth` handle it
- **MCP access** — spark-spice endpoint is public (Anthropic-operated); no auth token needed at MCP layer

## 📊 Pricing & Cost Model

### Claude API Costs (Sonnet 4.6)
- Input: $3/MTok (60% cache hit = $0.90/MTok effective)
- Output: $15/MTok
- Typical full design: ~$0.50 (75K tokens)

### spark-spice Compute
- Feasibility check: free (table lookup)
- BSIM4 simulation: ~$0.05–$0.26 (50–60s runtime)

**Total per design:** ~$0.55–$0.76

Compare to:
- Senior engineer (6 hours @ $100/hr): $600
- EDA tool license (annual): $2,000–$50,000
- **ROI:** 800–1,000× cheaper than traditional CAD

## 🐛 Troubleshooting

### "spark-spice server not connected"
```bash
# Restart Claude Code
ant --reset

# Verify endpoint in .claude/settings.json:
# sse://spark-9fd5.anthropic.com/spark-spice
```

### "BSIM4 simulation failed"
- Spec may be infeasible (extreme gain/GBW on low power)
- Run `explore_design_space` first: `ant query "Is [spec] feasible?"`
- Check the `binding` field in response for limiting constraint

### "Tool not found"
```bash
# List available tools
ant beta:mcp list

# Should show spark-spice tools:
# - size_analog_block
# - characterize_device
# - explore_design_space
# - recall_designs
# - query_device_table
```

## 📖 Full Documentation

See [`.claude/CLAUDE.md`](./.claude/CLAUDE.md) for:
- Detailed tool reference
- Design workflow examples
- Python/SDK integration
- Performance tuning & cost optimization

## 🤝 Contributing

Contributions welcome! Please:
1. Run designs and validate results
2. Add netlists & reports to `plugins/`
3. Update `catalog.json`
4. Submit PR with clear commit messages

## 📄 License

MIT License — see LICENSE file for details.

---

**Questions?** Open an issue or contact the maintainers.  
**Status:** Active development | Last updated: 2026-09-27
