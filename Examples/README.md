# eMachineSim Examples

This directory contains public sample and verification datasets used by the eMachineSim documentation, SKILLS, and MCP server.

## Layout

- `electrostatic/`: small electrostatic input examples.
- `thermal/`: thermal conduction, BDF, QVOL, thermal-network, motor steady thermal examples, and diagnostic CSV samples.
- `structural/`: structural static, rotor centrifugal-force, modal, and motor NVH examples.

## Before Running Examples

Install the eMachineSim wheel first. See the repository root [`README.md`](../README.md) for the wheel installation, license-file setup, and optional MCP support dependencies.

## Running a Case

Use the public Python API:

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/bdf")
result = eMachineSim.run_file(
    str(case_dir / "input_sample_bdf_min_hexa_qvol.json"),
    str(case_dir),
)
print(result["success"])
```

Generated CSV, VTK, and post files are written to the selected case directory depending on the analysis type and input settings.

## Use with Coding AI and MCP

These examples are intended to be readable by users and AI agents. The eMachineSim SKILLS describe how to reason about the examples, while the `mcp_servers/emachinesim` server can help an AI agent:

- find relevant example directories;
- inspect eMachineSim `input.json` metadata and analysis settings;
- summarize thermal heat-balance CSV files;
- check surface assignment, gap coupling, interface resistance, and cooling path diagnostics;
- create focused JSON variants for known settings such as gap `h`, gap `Nu`, or PM `total_heat`.

The MCP server is designed for the public Python API / pyd workflow. It should not be treated as a general-purpose shell or a replacement for engineering review of mesh quality, material data, boundary conditions, and calibration.
