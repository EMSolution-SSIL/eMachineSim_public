# Thermal Motor and BDF Workflow

Use this reference for BDF/QVOL thermal analysis, motor steady thermal samples, FEMH thermal-network coupling, and gap/surface thermal couplings.

Important sample locations:

- `Examples/thermal/realistic_motor_steady/QVOL_loss_mix.bdf`
- `Examples/thermal/realistic_motor_steady/`
- `Examples/thermal/bdf/`

Typical workflow:

1. Import BDF mesh and QVOL losses.
2. Add JSON volume heat sources if needed.
3. Generate or select surface groups.
4. Apply FEMH external cooling and thermal network paths.
5. Add gap or surface-to-surface coupling when needed.
6. Check global and component heat balances.
7. Inspect surface assignment overlap.

Loss sources:

- BDF `QVOL`: electromagnetic or imported volumetric losses.
- `coil_copper_loss`: phase copper loss from current and resistance.
- `total_heat`: measured or externally computed total loss, such as PM magnet loss.
- `heat_density`: externally computed W/m3 source.

Common diagnostics:

- total heat equals BDF QVOL heat plus JSON volume heat.
- FEM RHS heat equals total volume heat.
- FEMH and network outflow close the global balance.
- `femh_and_gap_overlap` area is zero for physical gap-coupled cases.
- gap heat is internal exchange and should not be double-counted as external outflow.

Representative output files:

- `thermal_bdf_import_summary.csv`
- `thermal_bdf_element_type_summary.csv`
- `thermal_volume_heat_sources.csv`
- `thermal_fem_volume_heat.csv`
- `thermal_global_heat_balance.csv`
- `thermal_component_heat_balance.csv`
- `thermal_surface_assignment_summary.csv`
- `thermal_cooling_path_summary.csv`
- `thermal_gap_coupling_summary.csv`
- `thermal_gap_coupling_flow_summary.csv`
- `thermal_gap_h_model_summary.csv`

Known limitations:

- No transient thermal analysis.
- No radiation model.
- No temperature-dependent material or current-resistance iteration.
- No mortar/projection for nonmatching surface meshes.
- BDF support is intentionally limited to the thermal workflow needs.
