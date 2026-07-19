# Thermal Coupled Analysis Reference

Use this reference for detailed thermal conduction plus thermal equivalent
circuit workflows, especially realistic motor steady thermal cases.

## Core Mental Model

Thermal heat flow is assembled from:

```text
BDF QVOL heat
+ JSON-added volume heat
+ FEM conduction
+ FEMH surface ports
+ thermal-network elements
+ gap/interface internal exchange
```

Global heat balance should close. Gap coupling and interface resistance are
internal heat exchange paths; they should appear in component balances but should
not be double-counted as external outflow.

## Input JSON Sections to Look For

Common sections:

- `metaData`: must include `type = "eMachineSimInput"` and version.
- `bdf_import`: BDF mesh, QVOL, material-source options, property exclusions.
- `thermal_volume_heat_sources`: BDF-independent JSON heat additions.
- surface group definitions: external, gap, end-face, or interface selections.
- FEMH boundary/port settings: selected surface to thermal-network node.
- `thermal_network`: thermal-network nodes and RTH/GTH paths.
- `gap_thermal_couplings` or `surface_thermal_couplings`: gap/contact/thin-layer
  coupling.
- shared-node interface resistance settings when coil/core or PM/core
  interfaces need thermal resistance without user-created duplicate nodes.

## BDF/QVOL and Material Handling

Supported BDF thermal diagnostics include:

- multi `BEGIN BULK`
- `CHEXA`, `CPENTA`, `CTETRA`
- `QVOL`
- `PSOLID`, `MAT1`, `MAT4`, `MAT5` diagnostics

Default material source is JSON:

```json
"bdf_import": {
  "material_source": "json"
}
```

Use BDF `MAT4.k` only when explicitly requested:

```json
"bdf_import": {
  "material_source": "bdf_mat4_isotropic",
  "bdf_material_fallback": "error"
}
```

For electromagnetic motor meshes, outer air properties may be excluded from the
thermal FEM model. In the realistic motor family, property `50` is treated as an
outer electromagnetic air region and the stator outer surface becomes the FEMH
boundary to housing/ambient paths.

## Volume Heat Sources

Heat is additive:

```text
total FEM volume heat = BDF QVOL heat + JSON volume heat
```

Supported JSON modes:

- `coil_copper_loss`: `current_rms^2 * phase_resistance`, distributed by target
  coil-region volume. `coil_fill_factor` is diagnostic only and does not rescale
  the assigned heat.
- `total_heat`: assigned heat equals `total_heat * modeled_fraction`.
- `heat_density`: assigned heat equals `qvol * target_volume`.

Representative realistic motor losses:

```text
BDF QVOL heat     = 1.091336675596593 W
coil copper loss  = 23.004 W
PM magnet loss    = 1.25 W
total heat        = 25.345336675596593 W
```

Useful CSVs:

- `thermal_volume_heat_sources.csv`
- `thermal_fem_volume_heat.csv`
- `thermal_global_heat_balance.csv`

## FEMH and Thermal Network

FEMH connects selected FEM surfaces to thermal-network nodes. Explain it as a
surface heat-transfer port:

```text
FEM surface --FEMH--> network node --RTH/GTH--> other network nodes
```

Typical motor nodes:

- `housing`
- `mount`
- `shaft`
- `bearing`
- `end_space_air`
- `ambient`

Typical paths:

- stator radial outer surface to `housing`
- `housing` to `mount` to `ambient`
- rotor radial non-gap surface to `shaft`
- `shaft` to `bearing` to `ambient` or `mount`
- stator/rotor end faces to `end_space_air`

Useful CSVs:

- `thermal_femh_ports.csv`
- `thermal_network_nodes.csv`
- `thermal_network_element_flows.csv`
- `thermal_network_balance.csv`
- `thermal_cooling_path_summary.csv`

Remember that thermal-network heat flow is signed by the declared path
direction. A negative value means actual heat flows opposite the declared
direction.

## Surface Assignment Safety

Always verify that the same face is not accidentally used by two external paths.
For physical gap cases:

```text
femh_and_gap_overlap area = 0
```

Useful CSVs:

- `thermal_surface_groups.csv`
- `thermal_surface_assignment.csv`
- `thermal_surface_assignment_summary.csv`
- `thermal_surface_temperature_summary.csv`

If gap faces are intentionally removed from external FEMH, they may be listed as
unassigned external area in no-gap cases. In gap-coupled cases they should be
classified as gap-coupling surfaces.

## Gap Coupling

Gap coupling uses paired stator/rotor surface groups and `node_pair_lumped`
assembly.

Supported modes:

- `h`
- `k_over_gap`
- `nu`
- `rotating_gap_power_law`
- `area_resistance`
- `thin_layer`

For `mode = "nu"`:

```text
h_equiv = Nu * air_thermal_conductivity / gap_thickness
```

For `Nu = 1`, `k = 0.026 W/m/K`, `gap = 0.001 m`:

```text
h_equiv = 26 W/m2/K
```

Useful CSVs:

- `thermal_gap_pair_summary.csv`
- `thermal_gap_coupling_summary.csv`
- `thermal_gap_coupling_flow_summary.csv`
- `thermal_gap_h_model_summary.csv`

## Shared-Node Interface Thermal Resistance

Use shared-node interface resistance when users ask whether coil/core or PM/core
interfaces can have thermal resistance even though the electromagnetic mesh
shares nodes.

Workflow:

1. Select adjacent property groups.
2. Automatically find the shared material interface.
3. Internally split interface nodes for thermal analysis.
4. Stamp conductance/resistance between duplicate node pairs.
5. Output node split and heat-flow diagnostics.

Typical realistic motor pairs:

- coil properties `10000` to `10005` against stator core `10`
- PM property `50000` against rotor core `20`

Useful CSVs:

- `thermal_interface_resistance_summary.csv`
- `thermal_interface_resistance_node_splits.csv`
- `thermal_interface_resistance_node_pairs.csv`
- `thermal_interface_resistance_flows.csv`
- `thermal_interface_resistance_flow_summary.csv`
- `thermal_component_heat_balance.csv`

In VTK temperature plots, a temperature discontinuity across the split interface
is expected when interface resistance is active.

## Axial End-Space Cooling

The realistic motor sample is an axially extruded 2D-like model. It lacks real
3D end-space, end bracket, oil/refrigerant, and coil-end geometry. Equivalent
end-face cooling paths compensate for missing top/bottom heat flow.

Current model:

- stator/rotor end faces selected by axial-normal filters
- end faces connected by FEMH to `end_space_air`
- `end_space_air` connected to housing and ambient-side paths by thermal
  resistances

This is an equivalent path, not automatic coil-end geometry or automatic
coil-end loss modeling.

Representative axial-end cooling result:

```text
stator radial cooling avg. temperature = 67.55 degC
stator end faces avg. temperature      = 72.67 degC
rotor radial cooling avg. temperature  = 44.38 degC
rotor end faces avg. temperature       = 44.71 degC
stator gap avg. temperature            = 67.92 degC
rotor gap avg. temperature             = 52.15 degC
gap heat                               = 0.824813796 W
global relative residual               = 3.782002356724577e-11
```

## Diagnostic Order for AI Agents

When reviewing a thermal result, inspect in this order:

1. `thermal_volume_heat_sources.csv`: confirm loss inputs.
2. `thermal_fem_volume_heat.csv`: confirm BDF heat + JSON heat.
3. `thermal_global_heat_balance.csv`: confirm residual is small.
4. `thermal_surface_assignment_summary.csv`: confirm no unintended overlap.
5. `thermal_femh_ports.csv`: confirm major FEMH outflows.
6. `thermal_cooling_path_summary.csv`: confirm path conductance and heat flow.
7. `thermal_component_heat_balance.csv`: confirm stator/rotor/component balance.
8. Gap/interface CSVs only after global balance is plausible.

## Common User Questions

**Can coil-core thermal resistance be modeled?** Yes. Use shared-node interface
thermal resistance between coil properties and stator core property.

**Can PM-rotor thermal resistance be modeled?** Yes. Use shared-node interface
thermal resistance between PM property and rotor core property.

**Can users change the thermal equivalent circuit?** Yes. They can edit
thermal-network nodes/elements and FEMH surface-to-node connections in JSON.

**Can outer electromagnetic air be ignored?** Yes. Exclude the outer air
property from thermal FEM and apply FEMH to the motor outer surface.

**How is hollow-shaft cooling represented?** Use a shaft-side FEMH or thermal
network path to a coolant/ambient node. Current examples use equivalent paths;
there is no CFD coolant solver.

