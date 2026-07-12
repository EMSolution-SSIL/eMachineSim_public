# Realistic Motor Steady Thermal Example

This public example demonstrates a motor steady thermal workflow using:

- BDF QVOL losses
- JSON coil copper loss
- JSON permanent-magnet total heat
- FEMH external cooling and thermal-network paths
- stator/rotor gap thermal coupling
- surface assignment and component heat-balance diagnostics

Run one of the JSON cases from Python:

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/realistic_motor_steady")
result = eMachineSim.run_file(
    str(case_dir / "input_realistic_motor_steady_all_external_balance.json"),
    str(case_dir),
)
print(result["success"])
```

Start by inspecting:

- `thermal_volume_heat_sources.csv`
- `thermal_fem_volume_heat.csv`
- `thermal_global_heat_balance.csv`
- `thermal_surface_assignment_summary.csv`
- `thermal_component_heat_balance.csv`