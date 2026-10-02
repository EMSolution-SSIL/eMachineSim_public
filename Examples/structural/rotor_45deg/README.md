# 45-Degree Structural Rotor Sector

This example is a 45-degree rotor sector model for centrifugal-force structural
checks and modal checks. It demonstrates automatic sector-boundary extraction
and simplified inner-radius shaft support when the shaft itself is not meshed.

## Files

- `rotor.msh`: original Gmsh 4.1 ASCII mesh.
- `rotor_structural.bdf`: Nastran BDF converted from the Gmsh mesh.
- `input_rotor_45deg_1500rpm_cyclic.json`: static centrifugal-force case.
- `input_rotor_45deg_modal_cyclic.json`: structural modal case.
- `structural_cyclic_sector_constraints.csv`: detected sector-boundary constraints.
- `structural_radial_support_constraints.csv`: detected inner-radius support constraints.
- `structural_displacement.vtk`: displacement and von Mises stress result.
- `modal_modes_cyclic_full.vtk`: modal shapes expanded to a full 360-degree view.

## Mesh Conversion

The BDF file can be regenerated from the Gmsh mesh with:

```bat
python scripts\convert_gmsh41_to_nastran.py ^
  Examples\structural\rotor_45deg\rotor.msh ^
  Examples\structural\rotor_45deg\rotor_structural.bdf ^
  --include-physical 20,30,50000,50001
```

## Boundary Conditions

`STRUCTURAL_CYCLIC_SECTOR_BC` extracts the minimum-angle and maximum-angle
periodic boundaries. `STRUCTURAL_RADIAL_SUPPORT_BC` then excludes those periodic
boundary nodes and constrains the minimum-radius node row in the radial
direction, approximating support from a non-meshed shaft.
