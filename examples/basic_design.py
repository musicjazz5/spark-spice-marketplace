#!/usr/bin/env python3
"""
Example: Design a Miller OTA using spark-spice via Claude API.
This script demonstrates how to use the Anthropic SDK to interact with spark-spice.
"""

import os
import json
from anthropic import Anthropic

def design_miller_ota():
    """Design a 60 dB, 50 MHz Miller OTA using Razavi gm/Id method."""

    # Initialize Anthropic client (reads ANTHROPIC_API_KEY from environment)
    client = Anthropic()

    # System prompt that tells Claude about spark-spice capabilities
    system_prompt = """You are an analog circuit designer with access to spark-spice tools.
Use the spark-spice MCP server to design and simulate analog circuits.

Key tools available:
- size_analog_block: Full BSIM4 simulation + transistor sizing
- characterize_device: gm/Id sweep for device selection
- explore_design_space: Fast feasibility check (<3 seconds)
- recall_designs: Find prior solutions near target spec

When designing circuits:
1. First call explore_design_space to check feasibility
2. Use recall_designs to see if this spec was solved before
3. Call size_analog_block with method='razavi' for hand-design + BSIM4 simulation
4. Report transistor sizing, simulated performance, and any margin violations

Always include the Razavi procedure steps (R1-R8) in your response."""

    # Design request
    design_query = """Design a Miller OTA with these specifications:
- DC gain: 60 dB
- GBW: 50 MHz
- Phase margin: ≥ 60°
- Load capacitance: 2 pF
- Power budget: 150 µW

Requirements:
1. Use Razavi gm/Id methodology
2. Use BSIM4 Level-54 simulation
3. Report transistor gm/Id values, W/L ratios, and operating points
4. Provide the R1–R8 hand-design procedure
5. Generate a summary table of results vs. spec

Please proceed."""

    print("=" * 70)
    print("spark-spice Miller OTA Designer")
    print("=" * 70)
    print(f"\nQuery: {design_query}\n")
    print("Sending to Claude with spark-spice MCP server...\n")

    # Call Claude with streaming
    with client.messages.stream(
        model="claude-opus-5",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": design_query
            }
        ]
    ) as stream:
        # Accumulate the full response
        full_response = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n")
    print("=" * 70)
    print("Design Complete!")
    print("=" * 70)

    # Optionally parse and save results
    return full_response


def check_feasibility():
    """Quick feasibility check for a design spec."""

    client = Anthropic()

    query = """Using spark-spice, quickly check if this design is feasible:
- Miller OTA: 60 dB gain, 50 MHz GBW, 150 µW max power
Use explore_design_space (it's a table lookup, not a simulation).
Report: feasible or infeasible, and any binding constraints."""

    print("\n" + "=" * 70)
    print("Feasibility Check (fast, <3 seconds)")
    print("=" * 70 + "\n")

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": query}]
    )

    result = response.content[0].text
    print(result)
    return result


def device_characterization():
    """Characterize an NMOS device across gm/Id range."""

    client = Anthropic()

    query = """Using spark-spice characterize_device, sweep an NMOS transistor:
- Length: 150 nm
- gm/Id range: 6 to 20 V⁻¹
- Report: gm/W, Id/W, ft (fT), intrinsic gain, noise, Rout

Then recommend gm/Id values for:
1. Differential pair (input stage): want high intrinsic gain, medium noise
2. Current source/load: want high Rout, robust biasing
3. Output stage: want high ft (speed), can afford more area

Provide the selection rationale."""

    print("\n" + "=" * 70)
    print("Device Characterization")
    print("=" * 70 + "\n")

    with client.messages.stream(
        model="claude-opus-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": query}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


def main():
    """Run all examples."""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        return

    # Run examples
    print("\n🚀 spark-spice Integration Examples\n")

    # 1. Feasibility check
    check_feasibility()

    # 2. Device characterization
    device_characterization()

    # 3. Full design (longer, so put it last)
    design_miller_ota()

    print("\n✅ All examples completed!\n")


if __name__ == "__main__":
    main()
