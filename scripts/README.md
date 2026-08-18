# Public Helper Scripts

This directory contains small helper scripts that are useful when preparing
public eMachineSim examples.

## Gmsh 4.1 to Nastran BDF

`convert_gmsh41_to_nastran.py` converts a simple Gmsh 4.1 ASCII 2D mesh to a
free-field Nastran BDF file containing `GRID`, `CTRIA3`, and `CQUAD4` cards.

Example:

```bat
python scripts\convert_gmsh41_to_nastran.py ^
  Examples\structural\rotor_45deg\rotor.msh ^
  Examples\structural\rotor_45deg\rotor_structural.bdf ^
  --include-physical 20,30,50000,50001
```

The `--include-physical` option can be used to keep only structural physical
groups and exclude air or hole regions from the exported BDF.
