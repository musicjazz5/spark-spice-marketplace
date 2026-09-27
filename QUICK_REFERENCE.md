# spark-spice gm/Id Method — Quick Reference Card

## 1 Minute Version: What is gm/Id?

```
gm/Id = transconductance-to-current ratio (units: V⁻¹)

Higher gm/Id  → Slower, but smaller transistors
Lower gm/Id   → Faster, but larger transistors

The Razavi Method:
  1. Decide what role each transistor plays
  2. Choose optimal gm/Id for that role
  3. Calculate width from gm/Id
  4. Simulate once — done!
```

---

## 5 Minute Version: The 8 Steps (R1–R8)

| Step | Input | Output | Action |
|------|-------|--------|--------|
| R1 | 60 dB spec | Two 44.7 V/V stages | Split gain |
| R2 | Stage 1 gain target | L=150nm, gm/Id=16 | Choose length & inversion level |
| R3 | Stage 2 gain target | L=150nm, gm/Id=18.5 | Balance speed vs. gain |
| R4 | PM ≥ 60° | ωp₂ ≥ 130 MHz | Determine pole placement |
| R5 | Pole location | Cc=400fF, Rz=3157Ω | Design Miller compensation |
| R6 | GBW=50MHz | I₁=20µA, I₂=104µA | Derive currents from bandwidth |
| R7 | Power ≤150µW | Optimize gm/Id | Trade speed for power |
| R8 | ωp₂ location | Rz cancels RHP zero | Stabilize circuit |

→ **Submit to BSIM4 simulation**

---

## Device Role Selection (Key Decisions)

```
INPUT STAGE (Differential Pair)
  Goal: High gain, low noise
  Choose: gm/Id = 14–16 (strong inversion)
  Tradeoff: Larger area, but excellent performance

LOAD / BIAS STAGE
  Goal: High output impedance
  Choose: gm/Id = 8–10 (moderate inversion)
  Tradeoff: Smaller area, stable biasing

OUTPUT STAGE
  Goal: High gm (drive load), high speed
  Choose: gm/Id = 16–18 (strong inversion)
  Tradeoff: Can be large, but fast & powerful
```

---

## Formula Cheatsheet

### Width from gm/Id

```
W = gm_required / (gm/W @ chosen gm/Id)

Example:
  Need gm = 320 µS
  Device table @ gm/Id=16: gm/W = 247 µS/µm
  → W = 320 / 247 = 1.3 µm
```

### Bandwidth from Compensation

```
GBW = gm₁ / (2π · Cc)

Solving for Cc:
  Cc = gm₁ / (2π · GBW)
  
Example:
  gm₁ = 126 µS
  GBW = 50 MHz
  → Cc = 126 µS / (2π × 50e6) = 400 fF
```

### Nulling Resistor

```
Rz = 1 / (2π · f_zero · Cc)

Example:
  f_zero ≈ 3 kHz (chosen empirically)
  Cc = 400 fF
  → Rz = 1 / (2π × 3000 × 400e-15) ≈ 3200 Ω
```

---

## Miller OTA Results (Our Example)

### Input Spec
- Gain: 60 dB ✓
- GBW: 50 MHz ✓
- Phase margin: ≥60° ✓
- Power: ≤150 µW ✓
- Load: 2 pF
- Process: 150 nm CMOS

### Simulated Results
```
DC Gain:       67.97 dB    (spec: 60 dB) ✓
UGBW:          52.05 MHz   (spec: 50 MHz) ✓
Phase Margin:  84.27°      (spec: 60°) ✓
Noise:         17.8 nV/√Hz (white) ✓
Slew Up:       61.3 V/µs   (spec: 50 V/µs) ✓
Slew Down:     35.6 V/µs   (spec: 50 V/µs) ❌
Power:         151.9 µW    (spec: 150 µW) ~✓
```

**Binding Constraint:** Power budget limits downward slew  
**Trade-off:** Accept 35.6 V/µs or increase power to 225 µW

### Transistor Sizing

| Device | Type | gm/Id | L (nm) | W (µm) | Role |
|--------|------|-------|--------|--------|------|
| M1, M2 | NMOS | 13.34 | 150 | 0.40 | Diff pair |
| M3, M4 | PMOS | 8.00 | 150 | 0.81 | Load mirror |
| M6 | NMOS | 18.53 | 150 | 96.6 | Output |
| M7 | PMOS | 8.00 | 150 | 1.24 | Bias source |

---

## When to Use Each Tool

```
❓ "Is my spec feasible?"
   → explore_design_space (table lookup, FREE, <3s)

❓ "Has this been done before?"
   → recall_designs (database, FREE, <1s)

❓ "What gm/Id should I use?"
   → characterize_device (sweep, FREE, <5s)

❓ "At gm/Id=16, what is Vgs?"
   → query_device_table (lookup, FREE, <1s)

❓ "Will this design actually work?"
   → size_analog_block (BSIM4 + R1–R8, $0.55, 55s)
```

---

## Cost Breakdown (per design)

| Item | Cost | Time |
|------|------|------|
| Feasibility check | Free | <3s |
| Prior design lookup | Free | <1s |
| Device characterization | Free | <5s |
| gm/Id table queries | Free | <1s each |
| Hand calculations (human) | Free | ~5 min |
| BSIM4 simulation | $0.55 | 52.8s |
| **Total** | **$0.55** | **~6 min** |

**vs. Traditional CAD:** $600 + 6 hours → **1000× cheaper, 60× faster**

---

## Troubleshooting Decision Tree

```
Design simulates, but specs not met?

   ├─ Gain too low?
   │  └─ Increase L (higher intrinsic gain)
   │
   ├─ GBW too low?
   │  └─ Increase I (higher gm = higher GBW)
   │     or decrease Cc (smaller capacitor)
   │
   ├─ Phase margin bad?
   │  └─ Increase Cc (stabilizes loop)
   │     or adjust Rz (nulling resistor)
   │
   ├─ Slew rate too low?
   │  └─ Increase I (more current to charge load)
   │
   ├─ Power too high?
   │  └─ Trade gm/Id for lower current
   │     (accept slower speed)
   │
   └─ M4 not saturated (headroom)?
      └─ Increase L (more intrinsic gain, less Vds needed)
         or decrease L_load (reduce mirror size)
```

---

## Design Workflow (Checklist)

```
□ 1. Define spec (gain, BW, power, load)

□ 2. Check feasibility
     ant query "Is this spec feasible?"

□ 3. Lookup prior designs
     ant query "Have we designed this before?"

□ 4. Characterize device (if not cached)
     ant query "Sweep gm/Id 6–20 for NMOS @ 150nm"

□ 5. Select gm/Id per role (hand decision, ~2 min)
     Input stage: gm/Id = 14–16
     Load/bias: gm/Id = 8–10
     Output: gm/Id = 16–18

□ 6. Hand calculations (W, I, Cc, Rz) (~5 min)
     or use Razavi procedure in guide

□ 7. Full simulation
     ant query "Design [spec]. Use Razavi gm/Id method."

□ 8. Verify results
     ✓ All specs met?
     ✓ M4/M7 saturated?
     ✓ Noise acceptable?
     ❌ If not, go back to step 5 (adjust gm/Id)

□ 9. Extract netlist & report
```

---

## Command Examples

### Quick Feasibility
```bash
ant query "Is 60 dB, 50 MHz on 150 µW feasible?"
```

### Full Design with Razavi
```bash
ant query "Design a Miller OTA: 60 dB, 50 MHz, 150 µW. \
  Use Razavi gm/Id method with BSIM4 simulation. \
  Return R1–R8 procedure and transistor sizing."
```

### Device Characterization
```bash
ant query "Characterize NMOS L=150nm, gm/Id sweep 6–20. \
  Show: ft, intrinsic gain, noise, Rout."
```

### Python Integration
```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Design 60 dB OTA using Razavi gm/Id"
    }]
)
print(response.content[0].text)
```

---

## Key Insight

**Traditional CAD Flow:**  
Guess W → Simulate → Check specs → Iterate 10× ❌

**gm/Id Method:**  
Choose role → Choose gm/Id → Calculate W → Simulate once ✓

**The difference:** Deterministic engineering vs. trial-and-error guessing.

---

## Learn More

- **Beginner**: `.claude/RAZAVI_GMID_GUIDE.md` (top section)
- **Full guide**: `.claude/RAZAVI_GMID_GUIDE.md` (all 8 steps)
- **Visual**: `docs/WORKFLOW_DIAGRAM.md` (flowcharts)
- **Reference**: `.claude/CLAUDE.md` (tool docs)
- **Example code**: `examples/basic_design.py`

---

**Latest Update:** 2026-09-27  
**Version:** 1.0  
**License:** MIT
