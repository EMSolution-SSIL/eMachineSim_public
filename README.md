# eMachineSim Public Materials

This repository contains public support materials for **eMachineSim**, a Python API based analysis toolset for electric-machine design support.

eMachineSim focuses on support analyses for electric-machine development:

- steady thermal conduction analysis;
- thermal equivalent-circuit coupling;
- BDF/QVOL loss import workflows;
- coil copper loss and permanent magnet loss inputs;
- stator/rotor gap thermal coupling diagnostics;
- centrifugal-force structural analysis;
- modal and vibration/NVH support workflows;
- small electrostatic sample workflows.

Documentation site:

- https://emsolution-ssil.github.io/eMachineSimDocs/

## Repository Contents

- `Examples/`: public sample datasets referenced by the documentation, SKILLS, and MCP server.
- `skills/`: coding-AI reference files for eMachineSim workflows.
- `mcp_servers/emachinesim/`: MCP server for AI-agent access to examples, input JSON inspection, diagnostic CSV summaries, guarded JSON variant writing, and Python API based single-case solves.
- `requirements.txt`: optional Python dependencies for the public MCP/AI-agent support tools.
- `LICENSE*.md`, `NOTICE.md`, `TRADEMARKS.md`: license and notice drafts for public review.

The eMachineSim C/C++ source code and internal debug executable are not part of this public repository. Normal user workflows should use the installed Python wheel and the `eMachineSim` Python module.

## Install eMachineSim from a Wheel

Download the wheel file from the private GitHub Release used for your evaluation or licensed version.

Example Windows setup:

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install path\to\emachinesim-0.1.0-cp311-cp311-win_amd64.whl
```

If you also want to use the MCP server or other AI-agent support tools in this repository, install the public support dependencies:

```bat
python -m pip install -r requirements.txt
```

For the MCP server package itself:

```bat
python -m pip install -e mcp_servers\emachinesim
```

Wheels are Python-version specific. Use a `cp311-cp311-win_amd64` wheel for Python 3.11 and a `cp313-cp313-win_amd64` wheel for Python 3.13. A wheel built for one CPython minor version cannot be installed into another CPython minor version.

## License File

eMachineSim requires license registration. Place the issued license file according to the installation guide in the documentation site before running analyses.

Temporary contact page:

- https://www.ssil.co.jp/product/EMSolution/contact/

## Quick Python API Check

After installing the wheel, run a small public example from this repository:

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/bdf")
input_json = case_dir / "input_sample_bdf_min_hexa_qvol.json"

result = eMachineSim.run_file(str(input_json), str(case_dir))
print(result["success"])
print(result.get("analysis_type"))
print(result.get("output_files"))
```

Generated CSV and post-processing files are written to the selected case directory. For thermal cases, typical files to inspect include:

- `thermal_fem_volume_heat.csv`
- `thermal_global_heat_balance.csv`
- `thermal_bdf_import_summary.csv`

## Session API Check

For repeated scripted runs, use `Session.solve()`:

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/bdf")
input_json = case_dir / "input_sample_bdf_min_hexa_qvol.json"

session = eMachineSim.Session()
session.initialize(str(input_json), str(case_dir))
result = session.solve()
session.finalize()

print(result["success"])
```

The current Session workflow still uses the JSON-first solver path internally, but it is convenient for parameter sweeps and AI-assisted generation of input variants.

## Use with Coding AI and MCP

This repository is designed so users and coding AI agents can inspect the same public materials:

- **Docs** explain what eMachineSim can do and how workflows are intended to be used.
- **Examples** provide public input files and result files.
- **SKILLS** provide workflow guidance for coding AI.
- **MCP server** provides structured tools for AI agents to inspect examples, read `input.json`, summarize thermal CSV diagnostics, and create focused JSON variants.

For MCP setup and tool-level details, see [`mcp_servers/emachinesim/README.md`](./mcp_servers/emachinesim/README.md).

## Packaging Notes for Release Maintainers

The wheel is built from an already-built `eMachineSim.pyd` using the development repository script:

```bat
python scripts\build_emachinesim_wheel.py --pyd x64\Release\eMachineSim.pyd
```

For public Releases, prefer a Release-configuration `.pyd`. A Debug-configuration `.pyd` can be packaged for internal testing, but the Release note should make that clear.

## License

This public repository is **not** distributed under an open-source license. It is made available for eMachineSim documentation, evaluation, learning, and user-support purposes.

- Documentation content and SKILLS-related text are governed by [`LICENSE-DOCUMENTATION.md`](./LICENSE-DOCUMENTATION.md).
- Sample scripts, sample `input.json` files, and public example materials are governed by [`LICENSE-SAMPLE-CODE.md`](./LICENSE-SAMPLE-CODE.md).
- Logos, product names, screenshots, icons, diagrams, and other brand assets are governed by [`TRADEMARKS.md`](./TRADEMARKS.md) and are not licensed for reuse.
- Competitive use, redistribution, modified public distribution, and incorporation into competing products, competing services, or competing AI assistance features are prohibited unless Science Solutions International Laboratory, Inc. grants prior written permission.

These license files are draft materials prepared for legal review before formal public release.

## Contact

For eMachineSim inquiries, please contact Science Solutions International Laboratory, Inc. through the official EMSolution product contact page:

https://www.ssil.co.jp/product/EMSolution/contact/

