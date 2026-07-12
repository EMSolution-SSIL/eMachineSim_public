# Thermal 3by3

Small thermal verification cases for boundary conditions and volume/surface heat
sources.

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/3by3")
result = eMachineSim.run_file(str(case_dir / "input_sample_3D_3by3.json"), str(case_dir))
print(result["success"])
```