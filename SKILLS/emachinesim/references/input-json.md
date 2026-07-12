# input.json Structure

Use existing samples as the source of truth. Do not embed full sample JSON files in this skill.

Common sections:

- mesh or BDF import settings
- analysis type and solver settings
- material and property mapping
- boundary conditions and sources
- output controls
- optional thermal network definitions
- optional coupling definitions

Thermal-specific sections may include:

- `bdf_import`
- `auto_surface_groups`
- `thermal_volume_heat_sources`
- `thermal_network`
- `gap_pairing_diagnostics`
- `gap_thermal_couplings`
- `surface_thermal_couplings`

Volume heat source modes:

- `coil_copper_loss`: compute phase copper loss from RMS current and phase resistance.
- `total_heat`: distribute a total heat value to selected property IDs.
- `heat_density`: add a specified volumetric heat density to selected property IDs.

Gap/surface coupling modes:

- `h`
- `k_over_gap`
- `nu`
- `rotating_gap_power_law`
- `area_resistance`
- `thin_layer`

Target selection:

- Prefer property IDs for BDF-derived regions.
- Use existing sample JSON files for exact field names and nesting.

When helping users author input JSON:

1. Ask which analysis type they want.
2. Identify the closest existing sample.
3. Modify only the relevant sections.
4. Point to output CSV files that validate the change.
