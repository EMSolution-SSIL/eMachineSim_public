# Outputs and Diagnostics

Use this reference to help users find the right output file to inspect.

Thermal/BDF:

- `thermal_bdf_import_summary.csv`: BDF import counts, sections, QVOL summary.
- `thermal_bdf_property_material_summary.csv`: PSOLID/MAT diagnostic mapping.
- `thermal_bdf_element_type_summary.csv`: element type/property heat summary.
- `thermal_volume_heat_sources.csv`: JSON-added volume heat source summary.
- `thermal_fem_volume_heat.csv`: BDF heat, JSON heat, total heat.
- `thermal_global_heat_balance.csv`: global heat balance residual.
- `thermal_component_heat_balance.csv`: component-level heat balance.
- `thermal_surface_assignment_summary.csv`: FEMH/gap/unused external face assignment.
- `thermal_surface_temperature_summary.csv`: surface temperatures.
- `thermal_cooling_path_summary.csv`: FEMH and coupling path conductance/flow summary.
- `thermal_gap_*`: gap pairing, conductance, heat-flow, and h-model diagnostics.

Structural:

- `displacement.neu` or `displacement.atl`: displacement post files.
- `post_geom.neu` or `post_geom.atl`: post geometry.
- `structural_load_balance.csv`: structural load balance.
- `contact_state.csv`: contact state.
- `contact_penalty_assembly.csv`: contact penalty assembly details.

Modal/NVH:

- `modal_frequencies.csv`: extracted modal frequencies.
- `modal_modes.csv`: modal vectors or summaries.
- `modal_modes_full.neu`: post file with full modal shapes.
- `motor_nvh_*summary.csv`: high-level NVH summaries.
- `motor_nvh_*orders.csv`: circumferential/order decomposition.
- `motor_nvh_*response*.csv`: response and participation data.

Matrix/debug outputs:

- Matrix Market `.mm` files and `.dat` debug files may appear when optional matrix/debug output controls are enabled.
- User-facing documentation should focus on stable CSV and post files unless debugging is requested.

Diagnostic strategy:

1. Check the heat/load balance first.
2. Check region/property selection summaries.
3. Check boundary or surface assignment.
4. Check detailed path/flow files only after the global balance is plausible.
