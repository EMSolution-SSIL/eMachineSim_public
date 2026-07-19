# Public Overview

Use this reference when users ask what eMachineSim is, what analyses it supports,
who it is for, or how it is meant to be used with coding AI.

## Positioning

eMachineSim is a Python API based analysis tool for electric-machine design
support. It focuses on auxiliary analyses around electric machines, not on
replacing the primary electromagnetic field solver.

Target users:

- motor, generator, compressor-motor, and actuator design engineers
- engineers who already have electromagnetic meshes or loss results
- users who want to evaluate thermal paths, rotor stress, and vibration/NVH
  behavior from JSON-controlled workflows
- users who want coding AI to help prepare inputs, run examples, and inspect CSV
  diagnostics

Do not describe eMachineSim as a general-purpose FEM package. Frame it as an
electric-machine design support tool.

## Public Interface

The public user interface is the Python module:

```python
import eMachineSim
```

The typical execution model is JSON-first:

```python
result = eMachineSim.run_file("input.json", r"path\to\run_directory")
```

Use `Session` when a user wants to update conditions and solve repeatedly:

```python
session = eMachineSim.Session()
session.initialize(input_json, run_directory)
result = session.solve()
session.finalize()
```

Avoid presenting the command-line executable as the normal public interface
unless the user explicitly asks about internal or development workflows.

## Supported Analysis Areas

| Area | What to say |
|---|---|
| Steady thermal conduction | FEM heat-conduction analysis in electric-machine regions. |
| Thermal equivalent-circuit coupling | FEM surfaces connect to thermal-network nodes through FEMH ports, then to housing, mount, shaft, bearing, ambient, or end-space paths. |
| BDF/QVOL thermal input | Selected BDF mesh and QVOL cards can be imported for thermal loss aggregation and analysis. |
| JSON-added heat sources | Coil copper loss, PM total heat, arbitrary total heat, and heat density can be added without overwriting BDF QVOL. |
| Gap and surface thermal coupling | Stator/rotor air-gap coupling, Nusselt-number input, area resistance, thin layer, and contact/interface thermal resistance are available for selected surfaces/interfaces. |
| Structural centrifugal-force analysis | Rotor structural stress/deformation workflows for electric-machine rotor evaluation. |
| Modal/NVH workflows | Modal analysis, force mapping, frequency response, circumferential order checks, and simplified acoustic-radiation indicators. |
| Electrostatic samples | Small electrostatic examples are included as a future extension entry point; they are not the main current product focus. |

## SKILLS + Coding AI Message

For public explanations, say that eMachineSim is intended to be used with
documentation, examples, and SKILLS so that a coding AI can help users:

- choose an appropriate example
- create or modify `input.json`
- identify required property IDs and surface groups
- run Python API workflows
- inspect heat balance, load balance, and output CSV files
- explain diagnostic results such as surface overlap, gap heat, interface heat
  flow, and component heat balance

This is important for motor thermal and NVH workflows because users should not
have to memorize every JSON key and CSV file before starting.

## Public Sample Families

Prefer public `Examples/` paths in user-facing answers:

- `Examples/thermal/realistic_motor_steady`
- `Examples/thermal/bdf`
- `Examples/thermal/ring` or quick thermal ring samples if present
- `Examples/structural/rotor`
- `Examples/structural/modal_stator`
- `Examples/electrostatic`

When exact public paths are uncertain, inspect the repository before naming
files.

## Licensing Note

eMachineSim requires license registration. For public answers, direct users to
the license/installation documentation rather than describing internal license
implementation details.

## Current Limits to Mention When Relevant

- No transient thermal analysis.
- No radiation model.
- No CFD or automatic refrigerant/oil flow solver.
- No automatic temperature-dependent phase-resistance iteration.
- BDF support is scoped to selected thermal workflows, not full BDF
  compatibility.
- Motor NVH workflows are support/relative-evaluation workflows, not a fully
  calibrated absolute acoustic solver.

