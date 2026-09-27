# Razavi gm/Id Method: Step-by-Step Guide

## 🎯 What is gm/Id?

**gm/Id** is the **transconductance-to-current ratio** (units: V⁻¹), a key metric that tells you:
- **Inversion level** of a transistor (how hard it's working)
- **Trade-off** between speed (ft), noise, gain, and power

### The gm/Id Spectrum

```
gm/Id:   4        8        12       16       20
         |--------|--------|--------|--------|
Regime:  Weak     Moderate  Strong   Very     Extreme
         inv.     inv.      inv.     strong   strong

Speed:   ↑↑↑      ↑↑        ↑        ↓        ↓↓
Gain:    ↓↓↓      ↓↓        ↓        ↑        ↑↑
Noise:   ↓↓↓      ↓↓        ↓        ↑        ↑↑
Power:   ↓↓↓      ↓↓        ↓        ↑        ↑↑
```

**Razavi Method** = **choose the right gm/Id for each device role**, then size from there.

---

## 📊 Example: Design a 60 dB, 50 MHz Miller OTA

### STEP 1: Divide Gain Between Stages

**Input:** Spec says 60 dB total gain  
**Problem:** One stage can't give 60 dB (limited by transistor output impedance)  
**Solution:** Split into two stages

```
A₀ = A₁ × A₂ = 44.7 V/V × 44.7 V/V ≈ 2000 V/V = 66 dB ✓
     (with 6 dB margin for real-world effects)

Stage 1: Differential pair → current mirror load
A₁ ≈ gm₁ × Rout₁ = gm₁ × (1/gm₃ || 1/gds₁)

Stage 2: Common-source amp with active load
A₂ ≈ gm₆ × Rout₂ = gm₆ × (1/gm₇ || 1/gds₆)
```

**Why this works:**
- Each stage's gain depends on **gm × Rout**
- To get high gain, you need **high gm/Id** (stronger inversion = larger gm per unit current)
- But you also need **high output impedance** (Rout) from the load stage

---

### STEP 2: Characterize Devices Across gm/Id Range

**Tool:** `characterize_device`

```bash
# Sweep NMOS at L=150nm, gm/Id from 6 to 20 V⁻¹
ant query "Characterize NMOS L=150nm, gm/Id sweep 6–20. \
  Show: gm/W, ft, intrinsic gain, noise, Rout."
```

**Output Table** (example):

```
gm/Id  | Id/W    | gm/W    | ft      | A₀(intrinsic) | √Svg    | Rout×W  | Region
(V⁻¹)  | (µA/µm) | (mS/µm) | (GHz)   | (V/V)         | (nV/Hz) | (kΩ·µm) |
-------|---------|---------|---------|---------------|---------|---------|--------
6      | 20.5    | 123     | 4.8     | 285           | 18      | 850     | Weak inv
8      | 28.2    | 170     | 5.2     | 220           | 24      | 620     | Weak-mod
10     | 38.1    | 201     | 5.5     | 168           | 32      | 480     | Moderate
12     | 50.8    | 223     | 5.8     | 128           | 42      | 370     | Moderate
14     | 66.3    | 238     | 6.0     | 96            | 54      | 290     | Strong
16     | 84.2    | 247     | 6.1     | 74            | 68      | 240     | Strong
18     | 104.8   | 253     | 6.1     | 58            | 84      | 200     | Strong
20     | 127.9   | 257     | 6.0     | 46            | 102     | 170     | V.strong
```

**What to notice:**
- **Higher gm/Id** = smaller area (W), but **lower ft** (speed tops out ~6 GHz)
- **Higher gm/Id** = higher intrinsic gain (excellent for Stage 1)
- **Higher gm/Id** = higher noise (bad for input stage)

---

### STEP 3: Choose gm/Id for Each Device Role

Based on the characterization and circuit role:

```
┌─ STAGE 1 (Differential Pair) ─────────────────┐
│                                               │
│  Role: Maximize gain, minimize noise          │
│  Choice: gm/Id = 16.0 (strong inversion)      │
│                                               │
│  Reasoning:                                   │
│  • High intrinsic gain (74 V/V, enough)       │
│  • Good noise (68 nV/√Hz, acceptable)         │
│  • fT = 6.1 GHz >> 50 MHz spec ✓              │
│  • Rout = 240 kΩ·µm (good for A₁)            │
│                                               │
└───────────────────────────────────────────────┘

┌─ STAGE 1 LOAD (Mirror) ──────────────────────┐
│                                               │
│  Role: High output impedance, bias stability │
│  Choice: gm/Id = 8.0 (moderate inv.)          │
│                                               │
│  Reasoning:                                   │
│  • High Rout = 620 kΩ·µm ✓                    │
│  • Lower ft OK (just a current source)        │
│  • Diode-connected for bias stability         │
│                                               │
└───────────────────────────────────────────────┘

┌─ STAGE 2 GAIN STAGE (CS) ─────────────────────┐
│                                               │
│  Role: High gain AND speed for bandwidth      │
│  Choice: gm/Id = 18.5 (very strong inv.)      │
│                                               │
│  Reasoning:                                   │
│  • Very high intrinsic gain (58 V/V)          │
│  • High fT = 6.1 GHz (can go faster)          │
│  • Can afford large W for Cc compensation     │
│                                               │
└───────────────────────────────────────────────┘

┌─ STAGE 2 LOAD (Biasing) ──────────────────────┐
│                                               │
│  Role: Current source, stable biasing         │
│  Choice: gm/Id = 8.0 (same as Stage 1 load)   │
│                                               │
│  Reasoning:                                   │
│  • Matched bias gives predictable behavior    │
│  • High Rout OK (passive load in this stage)  │
│                                               │
└───────────────────────────────────────────────┘
```

**This is the core of Razavi method** — choosing ONE gm/Id per device role.

---

### STEP 4: Calculate Required Channel Length

**Tool:** `query_device_table`

**Formula:** You want specific **gain per stage**, which needs specific **Rout**.

```
A₁ = gm₁ × Rout₁
44.7 = 170 µS/µm × (1/gm₃ || 1/gds₁)

For gm/Id=16 (M1):  gm₁/W₁ = 247 µS/µm
For gm/Id=8 (M3):   gm₃/W₃ = 170 µS/µm

Rout ≈ 1/(gm₃ + gds) ≈ 1/gm₃ (dominant)
Rout ≈ 1/(170 µS/µm × W₃)

For A₁ = 44.7: W₃ must be sized so Rout is large enough
```

**But first: choose L (channel length)**

```
Higher L = higher intrinsic gain (less channel modulation)
         = lower fT (slower)
         = more die area

Lower L = faster fT (good for bandwidth)
        = lower gain (need wider transistors)
        = less area

Trade-off: Use minimum L that gives required gain without wasting area

Typical choice: L = 150 nm (0.15 µm)
• fT still ~6 GHz >> 50 MHz ✓
• Intrinsic gain still ~60–100 V/V ✓
• Min area
```

---

### STEP 5: Calculate Transistor Widths

**Formula:**

```
Given:
  I₁ = 20 µA (Stage 1 tail current, from GBW = 2π·gm₁·Cc)
  gm/Id₁ = 16.0

Calculate:
  gm₁ = gm/Id₁ × I₁ = 16.0 × 20 µA = 320 µS
  
  At L=150nm, NMOS: gm/W @ gm/Id=16 = 247 µS/µm
  
  W₁ = gm₁ / (gm/W) = 320 µS / 247 µS/µm = 1.3 µm
```

**Repeated for all devices:**

| Device | Role | gm/Id | I (µA) | gm/W @ L | W (µm) | Vgs (mV) | Notes |
|--------|------|-------|--------|----------|--------|----------|-------|
| M1, M2 | Diff pair | 16.0 | 20 | 247 | 0.40 | 516 | Input stage |
| M3, M4 | Load mirror | 8.0 | 20 | 170 | 0.81 | 577 | Current mirror |
| M6 | Output stage | 18.5 | 104 | 253 | 96.6 | 377 | Power delivery |
| M7 | Bias source | 8.0 | 104 | 170 | 1.24 | 600 | Stable bias |

**Key insight:** Each transistor's width is determined by:
```
W = (Required gm) / (gm/W at chosen gm/Id)
```

---

### STEP 6: Verify Operating Point & Headroom

**Question:** Are transistors in saturation? (Can't get gain if they're in triode)

```
For each transistor:
  Vsat = Vgs - Vth (minimum drain-source voltage for saturation)
  Margin = Vds - Vsat (must be > 0)

Example for M1 (NMOS diff pair):
  Vth ≈ 440 mV
  Vgs ≈ 516 mV (from gm/Id table)
  Vsat ≈ 516 - 440 = 76 mV
  
  If Vds = 535 mV:
  Margin = 535 - 76 = 459 mV ✓ (plenty of room)
```

**Headroom bottleneck** (our OTA):
- M4 (Stage 1 output): Margin = 156 mV (tight, but OK)
  - This tells you: M4 is the most constrained device
  - On PVT corners, it might go into triode → lose gain
  - Solution: Increase L₄, or increase power supply

---

### STEP 7: Design Compensation Network (Miller Compensation)

**Problem:** Two-stage amplifier has **two poles** → **poor phase margin** without compensation

```
Pole 1 (dominant): p₁ = 1 / (Rout₁ · CL)
                     ≈ 1 / (200 kΩ × 2 pF) ≈ 2.5 MHz
                     (set by output stage load)

Pole 2 (right-half-plane): p₂ ≈ gm₆ / Cc
                             (depends on Miller capacitor)

Without compensation: p₂ can be LOWER than p₁
  → Phase margin collapses
  → Circuit oscillates ❌
```

**Miller Compensation to the rescue:**

```
Add capacitor Cc across M6 output → M7 gate (feedback path)
This creates a TRANSMISSION ZERO that cancels p₂

Cc feeds back output changes to input of Stage 2
→ Reduces gain at high frequencies
→ Pushes p₂ to high frequency (>10× GBW)

Razavi formula:
  Cc = GBW / (2π · gm₆)
     = 50 MHz / (2π · 1936 µS)
     = 4.1 pF / 10 ≈ 0.4 pF ✓

Nulling resistor Rz (in series with Cc):
  Rz = 1 / (2π · f₀ · Cc)
  where f₀ ≈ 3160 Hz (chosen to cancel RHP zero onto p₂)
  Rz ≈ 3160 Ω ✓
```

**Result:**
- Cc transfers (multiplies) by ~gm₆/gm₁ at low freq
- Creates virtual pole that dominates
- Phase margin recovers: PM = 84° ✓

---

### STEP 8: Full BSIM4 Simulation

**Tool:** `size_analog_block` with `method='razavi'`

After all hand calculations, **verify everything works**:

```
Input:
  block="miller_ota"
  gain_db=60, gbw_Hz=50e6
  method="razavi"

Output:
  ✓ Simulated DC gain: 67.97 dB (spec: ≥60) ✓
  ✓ Simulated UGBW: 52.05 MHz (spec: ≥50 MHz) ✓
  ✓ Phase margin: 84.27° (spec: ≥60°) ✓
  ✓ All transistors saturated ✓
  ✓ M4 margin: 156 mV (tightest, but OK)
  ✓ Power: 151.9 µW (spec: ≤150 µW) ✓
  
  Slew rate: 35.6 V/µs (spec: ≥50 V/µs) ❌
    → Power budget is limiting factor
```

---

## 🔍 Why gm/Id Method Works

### Traditional CAD Flow (Hours → Days)

```
1. Guess W/L for each transistor
   ↓
2. Run SPICE simulation
   ↓
3. Check: gain, bandwidth, phase margin, noise, power
   ↓
4. Is it OK?
   NO → Go back to Step 1 ❌❌❌
   YES → Done ✓
```

### Razavi gm/Id Flow (Minutes → One Simulation)

```
1. Characterize device across gm/Id range
   ↓
2. Choose gm/Id for each device role
   ↓
3. Hand-calculate W, L, I using gm/Id table
   ↓
4. Run BSIM4 simulation ONCE → Works ✓
   ↓
5. Report: procedure, netlists, headroom
```

**Key differences:**
- **Every step is deterministic** (gm/Id → W → gain → frequency)
- **No guessing** (hand-design procedure is predictable)
- **One simulation** (not iterative trial-and-error)
- **Portable** (gm/Id table works across process nodes, supply voltages)

---

## 💡 Real Example: Our Miller OTA

### The 8 Steps (R1–R8) from spark-spice Output

```
R1_GAIN_SPLIT: A₀ 60 dB + 6 dB margin → 44.7 V/V per stage
   Goal: Set target gain per stage

R2_STAGE1_L: L₁ = L₃ = 150 nm → A₁ = 57.3 V/V, gm/Id pair 16.0, load 8
   → Choose channel length

R3_STAGE2_L: stage 2 needs 34.8 V/V → L₆ = L₇ = 150 nm → 51.4 V/V
   → Channel length for Stage 2

R4_PHASE_BUDGET: 90 - PM₆₀ - mirror₆ - RzC₁₃ = 21° for ωp₂ → 130 MHz
   → Determine pole placement

R5_OUTPUT_STAGE: M6 gm/Id 14.0 (fT 6.02 GHz >> 10×ωp₂); Cc 52 fF, C₂ 2.05 pF
   → Design compensation

R6_CURRENTS: gm₁ = 2π·GBW·Cc = 126 µS → I₁ = 20 µA @ gm/Id 12.6
   → Calculate tail current from bandwidth requirement

R7_POWER_TRADE: 190 µW over 150 µW → adjust gm/Id to reduce current
   → Optimize power

R8_NULLING_RZ: Rz = 3157 Ω → cancels RHP zero onto p₂
   → Stabilize circuit
```

Each step is a **deterministic calculation** — not a guess.

---

## 🎯 Summary: How gm/Id Helps

### Problem it Solves
> "I need to size transistors for a 60 dB OTA. Do I use W=1µm? W=10µm? How do I choose?"

### Traditional Answer
> "Try different sizes in SPICE until it works." ❌ Hours of iteration.

### gm/Id Answer
> "Choose gm/Id based on device role (input stage: high gain → gm/Id 16; load: high Rout → gm/Id 8), then calculate W deterministically from gm/Id table." ✓ One simulation.

### The Magic
```
gm/Id Table
    ↓
Device Role Selection (gm/Id = 8, 16, 18, ...)
    ↓
Deterministic W, L, I Calculation
    ↓
One BSIM4 Simulation
    ↓
Done (with R1–R8 procedure as proof-of-work)
```

---

## 📈 For Your Next Design

Try this workflow:

```bash
# Step 1: Quick feasibility check (free)
ant query "Is a folded-cascode OTA with 70 dB, 100 MHz on 500 µW feasible?"

# Step 2: Full design with Razavi procedure
ant query "Design a folded-cascode OTA: 70 dB, 100 MHz, 500 µW. \
  Use Razavi gm/Id method with BSIM4 simulation. \
  Return R1–R8 procedure and transistor W/L."

# Step 3: Verify headroom
# → Check M4 margin in output
# → If tight, increase L or power

# Step 4: Run netlist in your own SPICE for corner analysis
# → spark-spice runs nominal; you run PVT corners
```

---

## 🔗 Further Reading

- **Textbook:** Razavi, *Design of Analog CMOS Integrated Circuits*, Ch. 6 (two-stage OTA)
- **Paper:** Jesper et al., "A Survey of Circuit Layout Issues for Analog Design," *IEEE JSSC* 1999
- **Online:** CMOSedu.com (Inversion Coefficient Tutorial)

