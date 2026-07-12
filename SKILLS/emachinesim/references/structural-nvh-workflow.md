# Structural, Modal, and Motor NVH Workflow

Use this reference for structural stress, centrifugal-force analysis, contact examples, modal analysis, and motor NVH workflows.

Important sample locations:

- `Examples/structural/rotor/`
- `Examples/structural/modal_stator/`
- `Examples/structural/modal_2d_square/`
- `examples/intermediate/structural-ring/`
- `motor_nvh_plan/`

Typical structural workflow:

1. Select or create a structural input JSON.
2. Define mesh, material, constraints, and loads.
3. Solve displacement/stress.
4. Inspect displacement and load-balance outputs.
5. For contact, inspect contact state and penalty assembly diagnostics.

Typical modal/NVH workflow:

1. Run modal extraction.
2. Map electromagnetic or external tooth forces to structural nodes.
3. Compute modal participation or frequency response.
4. Inspect circumferential order and acoustic radiation summaries where available.

Representative output files:

- `displacement.neu`
- `displacement.atl`
- `post_geom.neu`
- `post_geom.atl`
- `modal_frequencies.csv`
- `modal_modes.csv`
- `modal_modes_full.neu`
- `structural_load_balance.csv`
- `contact_state.csv`
- `contact_penalty_assembly.csv`
- `motor_nvh_*summary.csv`
- `motor_nvh_*orders.csv`
- `motor_nvh_*response*.csv`

Known limitations:

- Confirm exact supported element and boundary types from the current samples.
- Treat motor NVH examples as workflow samples unless calibrated material, damping, and force data are supplied.
