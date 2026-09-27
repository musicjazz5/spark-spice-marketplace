# spark-spice Workflow Diagram

## Complete OTA Design Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    60 dB, 50 MHz OTA Design                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │  STEP 1: Check Feasibility (free)   │
        │  tool: explore_design_space         │
        │  time: <3 seconds                   │
        └─────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                Feasible ✓          Infeasible ❌
                    │                   │
                    │            Adjust spec:
                    │            • Lower gain
                    │            • Lower BW
                    │            • Higher power
                    │                   │
                    ▼                   ▼
        ┌─────────────────────────────────────┐
        │  STEP 2: Lookup Prior Designs       │
        │  tool: recall_designs               │
        │  time: <1 second                    │
        └─────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Found ✓              Not found
           (near spec)                  │
                    │                   │
                 Reuse                  ▼
            + fine-tune        ┌─────────────────────────────────────┐
                    │          │  STEP 3: Characterize Device        │
                    │          │  tool: characterize_device          │
                    │          │  sweep: gm/Id 6–22 V⁻¹               │
                    │          │  output: ft, gain, noise, Rout      │
                    │          │  time: <5 seconds                   │
                    │          └─────────────────────────────────────┘
                    │                              │
                    │                              ▼
                    │          ┌─────────────────────────────────────┐
                    │          │  STEP 4: Choose gm/Id per Role      │
                    │          │  (manual decision tree)             │
                    │          │  • Input stage: gm/Id 14–16         │
                    │          │  • Load/bias: gm/Id 8–10            │
                    │          │  • Output: gm/Id 16–18              │
                    │          │  time: ~2 minutes (human)           │
                    │          └─────────────────────────────────────┘
                    │                              │
                    │                              ▼
                    │          ┌─────────────────────────────────────┐
                    │          │  STEP 5: Query Device Table         │
                    │          │  tool: query_device_table           │
                    │          │  for each gm/Id & L combination     │
                    │          │  output: Vgs, Vth, ft, A₀, Rout     │
                    │          │  time: <1 second per device         │
                    │          └─────────────────────────────────────┘
                    │                              │
                    │                              ▼
                    │          ┌─────────────────────────────────────┐
                    │          │  STEP 6: Calculate Widths           │
                    │          │  W = gm_required / (gm/W @ gm/Id)   │
                    │          │  output: W/L for M1, M2, M3, ...    │
                    │          │  time: ~5 minutes (hand calc)       │
                    │          └─────────────────────────────────────┘
                    │                              │
                    │                              ▼
                    │          ┌─────────────────────────────────────┐
                    │          │  STEP 7: Design Compensation        │
                    │          │  Razavi formulas:                   │
                    │          │  Cc = GBW / (2π · gm₆)              │
                    │          │  Rz = 1 / (2π · f₀ · Cc)            │
                    │          │  time: ~3 minutes                   │
                    │          └─────────────────────────────────────┘
                    │                              │
                    │          ┌──────────────────┘
                    │          │
                    └──────────┤
                              ▼
        ┌─────────────────────────────────────┐
        │  STEP 8: Full BSIM4 Simulation      │
        │  tool: size_analog_block            │
        │  method: razavi                     │
        │  output: • Procedure (R1–R8)        │
        │          • Simulated AC: gain, PM   │
        │          • Transient: slew rate     │
        │          • Noise analysis           │
        │          • Operating points        │
        │          • Saturation margins       │
        │  time: 50–60 seconds                │
        │  cost: ~$0.50 (API) + $0.05 (spice)│
        └─────────────────────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
              Specs met ✓         Specs NOT met ❌
                    │                    │
                 Done!             Analysis:
                    │             • Which constraint binds?
                    │             • Can adjust W/L/I?
                    │             • Need higher power?
                    │             • Need faster process?
                    │                    │
                    │              Iterate or
                    │              accept trade-off
                    │                    │
                    ▼                    ▼
        ┌────────────────────────────────────────┐
        │  Report: Design Summary                │
        │  • Netlist (SPICE ready)               │
        │  • Transistor sizing table             │
        │  • Performance vs. spec                │
        │  • Headroom analysis (M4 tightest)     │
        │  • Recommendations for corners/layout  │
        └────────────────────────────────────────┘
```

---

## Razavi gm/Id Methodology: 8 Steps (R1–R8)

```
START (60 dB, 50 MHz, 150 µW)
│
├─ R1: GAIN SPLIT ──────────────────────────┐
│   Input: Specs (60 dB)                    │
│   Output: A₁ = 44.7 V/V, A₂ = 44.7 V/V  │
│   Action: Add 6 dB margin, split gain     │
│
├─ R2: STAGE 1 LENGTH ──────────────────────┐
│   Input: Desired A₁ = 44.7 V/V            │
│   Output: L₁ = 150 nm, gm/Id₁ = 16.0     │
│   Action: Choose L for required gain      │
│
├─ R3: STAGE 2 LENGTH ──────────────────────┐
│   Input: Desired A₂ = 34.8 V/V            │
│   Output: L₆ = 150 nm, gm/Id₆ = 18.5     │
│   Action: Balance speed vs. gain          │
│
├─ R4: PHASE BUDGET ───────────────────────┐
│   Input: Required PM ≥ 60°                │
│   Output: ωp₂ ≥ 130 MHz (2.6 × GBW)      │
│   Action: Determine pole placement        │
│
├─ R5: OUTPUT STAGE ───────────────────────┐
│   Input: ωp₂ requirement                  │
│   Output: Cc = 400 fF, Rz = 3157 Ω       │
│   Action: Design Miller compensation      │
│
├─ R6: CURRENTS ───────────────────────────┐
│   Input: GBW = 50 MHz, Cc = 400 fF       │
│   Output: I₁ = 20 µA, I₂ = 104 µA        │
│   Action: gm₁ = 2π·GBW·Cc (fundamental)  │
│
├─ R7: POWER TRADE ────────────────────────┐
│   Input: P_budget = 150 µW                │
│   Output: Adjust gm/Id to reduce current  │
│   Action: Trade gain/noise for power      │
│
└─ R8: NULLING Rz ─────────────────────────┐
    Input: ωp₂ frequency                    │
    Output: Rz = 3157 Ω                     │
    Action: Cancel RHP zero onto p₂         │
END: Submit to BSIM4 simulation
```

---

## Tool Usage Hierarchy

```
START: Design a 60 dB OTA

Step 1: Feasibility
        │
        └─→ explore_design_space (TABLE LOOKUP)
            Cost: FREE
            Time: <3s
            Output: {reachable_from_table, predicted_specs}

Step 2: Lookup Prior
        │
        └─→ recall_designs (DATABASE)
            Cost: FREE
            Time: <1s
            Output: {prior_designs, distance}

Step 3–7: Hand Calculations
        │
        └─→ characterize_device (TABLE SWEEP)
            Cost: FREE
            Time: <5s
            Output: gm/W, ft, A₀, √Sv, Rout per gm/Id

        └─→ query_device_table (TABLE LOOKUP)
            Cost: FREE
            Time: <1s per query
            Output: Vgs, Vth, overhead, W_for_1uA

Step 8: Full Simulation
        │
        └─→ size_analog_block (BSIM4 + MNA)
            Cost: $0.50 API + $0.05 compute
            Time: 52.8s (3× AC + 1× transient)
            Output: {procedure, simulated, design, headroom}

DONE: Netlist + sizing + report
```

---

## Cost-Benefit Breakdown

```
Traditional EDA CAD Flow
├─ Tool license: $50K/year
├─ Training: 2 weeks
├─ Design iteration: 6 hours
│  (simulation time + manual tweaking)
└─ Total cost: $600+ per design

spark-spice + Claude Flow
├─ Cloud API: $0.50 per design
├─ Compute: $0.05 per design
├─ Claude guidance: Included
├─ No license, no training
└─ Time: 5 min (human) + 1 min (simulation)
    Total cost: $0.60 per design

ROI: 1000× cheaper, 100× faster
```

---

## Decision Tree: When to Use Each Tool

```
                        Start (have a spec)
                              │
                              ▼
                    "Is this spec doable?"
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            YES                       NO
            │                         │
    ┌───────┴─────────┐       Adjust spec
    ▼                 ▼       (higher power,
   explore_       recall_     lower gain, etc.)
   design_space   designs
   (check table)  (DB lookup)
         │             │
         └─────┬───────┘
               ▼
       Found prior design?
        │           │
        NO          YES
        │           └─→ Use as baseline
        │
        ▼
   characterize_device
   (sweep gm/Id)
   │
   ▼
   Hand-select gm/Id per role
   (R2, R3, R5, R6, R7, R8)
   │
   ▼
   size_analog_block
   (BSIM4 full simulation)
   │
   ▼
   Check results:
   • Gain/BW/PM met?
   • Slew rate OK?
   • Headroom OK?
   ├─ YES → Done ✓
   └─ NO → Analyze binding constraint
       └─ Need more power? Try again
       └─ Need different L? Try again
       └─ Spec unreachable? Accept trade-off
```

---

## Example Output from Our Design

```
╔═ R1_GAIN_SPLIT ═════════════════════════════╗
║ A₀ 60 dB + 6 dB margin → 44.7 V/V per stage║
║ • Reason: Two stages needed for 60 dB       ║
║ • Result: Design targets = 44.7² = 2000 V/V║
╚═════════════════════════════════════════════╝

╔═ R2_STAGE1_L ═══════════════════════════════╗
║ L₁ = L₃ = 150 nm gives A₁ = 57.3 V/V       ║
║ gm/Id pair 16.0 (strong inv.)              ║
║ load 8.0 (high Rout for gain)              ║
╚═════════════════════════════════════════════╝

...

╔═ Simulated Results ═════════════════════════╗
║ A₀: 67.97 dB (spec 60 dB) ✓                ║
║ GBW: 52.05 MHz (spec 50 MHz) ✓             ║
║ PM: 84.27° (spec 60°) ✓                    ║
║ Noise: 17.8 nV/√Hz (white) ✓               ║
║ Power: 151.9 µW (spec 150 µW) ~✓           ║
║ Slew: 35.6 V/µs ↓ (spec 50 V/µs) ❌        ║
║ (Power budget limits slew)                 ║
╚═════════════════════════════════════════════╝
```

