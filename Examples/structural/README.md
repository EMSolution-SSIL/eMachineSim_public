# Structural Examples

Public structural examples for static structural analysis, modal analysis, and
motor NVH workflows.

Run cases from Python with `eMachineSim.run_file()` and inspect displacement,
modal, and NVH CSV/post outputs in the case directory.

Notable examples:

- `rotor/`: 90-degree rotor structural sample with centrifugal-force checks.
- `rotor_45deg/`: 45-degree rotor sector sample with automatic cyclic sector
  constraints and inner-radius radial support.
- `modal_stator/`: stator modal, force mapping, frequency response, and
  simplified acoustic radiation workflow.
