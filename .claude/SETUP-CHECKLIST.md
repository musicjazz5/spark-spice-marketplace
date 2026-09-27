# Claude Code + spark-spice Setup Checklist

## ✅ Installation Steps

### Step 1: Install Claude Code CLI
- [ ] **macOS**: `brew install anthropic/anthropic/anthropic-cli`
- [ ] **Linux**: Follow apt/dnf instructions in main README
- [ ] Verify: `ant --version`

### Step 2: Authenticate
- [ ] Run: `ant auth login`
- [ ] Confirm active credential: `ant auth status`
- [ ] Check env: `echo $ANTHROPIC_API_KEY` (should show `sk-ant-...` or empty if using OAuth)

### Step 3: Clone Repository
```bash
git clone https://github.com/musicjazz5/spark-spice-marketplace
cd spark-spice-marketplace
```

### Step 4: Verify MCP Server Connection
```bash
# List configured MCP servers
ant beta:mcp list

# Should show spark-spice tools:
# ✓ size_analog_block
# ✓ characterize_device  
# ✓ explore_design_space
# ✓ recall_designs
# ✓ query_device_table
```

### Step 5: Test spark-spice
```bash
# Quick test (table lookup, ~2 seconds)
ant query "Using spark-spice explore_design_space, \
  check if a 60 dB, 50 MHz Miller OTA is feasible on 150 µW"

# Should get: reachable_from_table: true
```

---

## 🎯 Configuration Files

### `.claude/settings.json`
**What it does:** Configures Claude Code to use spark-spice MCP server  
**Location:** Automatically loaded by Claude Code  
**Contains:**
- MCP server endpoint: `sse://spark-9fd5.anthropic.com/spark-spice`
- Default model: `claude-opus-5` (fast, cost-effective)
- Permissions: bash, read, edit, write, web_fetch, web_search

### `.claude/CLAUDE.md`
**What it does:** Detailed reference guide  
**Contains:**
- Tool reference (all 5 spark-spice tools)
- Cost models & pricing
- Workflow examples (quick spec check, full design, characterization)
- Troubleshooting guide

### `.claude/.gitignore`
**What it does:** Prevents accidental credential commits  
**Contains:** Exclusions for `settings.local.json`, `auth.json`, cache files

---

## 🚀 Quick Commands

### Design a Circuit
```bash
cd ~/spark-spice-marketplace
ant query "Design a 60 dB, 50 MHz Miller OTA using Razavi gm/Id with BSIM4"
```

### Check Feasibility (fast, free)
```bash
ant query "Is a 60 dB, 50 MHz OTA feasible on 150 µW?"
```

### Characterize Device
```bash
ant query "Sweep an NMOS at L=150nm, gm/Id 6–20 V⁻¹. \
  Show ft, intrinsic gain, noise, Rout."
```

### Run Python Example
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY='sk-ant-...'
python3 examples/basic_design.py
```

---

## 💰 Cost Expectations

| Task | Model | Input | Output | Total |
|------|-------|-------|--------|-------|
| Feasibility | Haiku 4.5 | $0.00 | $0.01 | $0.01 |
| Full design | Opus 5 | $0.24 | $0.19 | $0.43 |
| spark-spice compute | — | — | — | $0.05–$0.26 |
| **Design total** | — | — | — | **~$0.60** |

---

## 🔒 Security Checklist

- [ ] Never commit `ANTHROPIC_API_KEY` to git
- [ ] Use `ant auth login` for persistent credentials
- [ ] If using API key: set via `export ANTHROPIC_API_KEY=...` (shell only)
- [ ] No spark-spice credentials needed (Anthropic-operated, public endpoint)
- [ ] Local overrides go in `.claude/settings.local.json` (in .gitignore)

---

## 🐛 Troubleshooting

### "Command not found: ant"
→ Install Claude Code CLI (Step 1 above)

### "MCP server not connected"
```bash
# Restart Claude Code
ant --reset

# Verify endpoint in .claude/settings.json:
# "url": "sse://spark-9fd5.anthropic.com/spark-spice"
```

### "BSIM4 simulation failed"
→ Run `explore_design_space` first (feasibility check)  
→ Check binding constraints in response

### "Rate limit (429)"
→ Reduce query frequency or use cheaper model (Haiku instead of Opus)  
→ Cache hit rate should be ~60%, so repeated queries are cheaper

---

## 📚 Next Steps

1. **Run an example:** `python3 examples/basic_design.py`
2. **Read CLAUDE.md:** Full tool reference
3. **Try a design:** `ant query "Design [your spec]"`
4. **Contribute:** Add your designs to `plugins/` and update catalog.json

---

## 📞 Support

- **GitHub Issues**: Open an issue on the repository
- **Anthropic Docs**: https://docs.anthropic.com
- **spark-spice Help**: `ant query "Describe size_analog_block parameters"`

---

**Last Updated:** 2026-09-27  
**Status:** ✅ All systems ready
