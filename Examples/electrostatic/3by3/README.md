# Electrostatic 3by3

Minimal 3D electrostatic verification case.

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/electrostatic/3by3")
result = eMachineSim.run_file(str(case_dir / "input_sample_3D_3by3.json"), str(case_dir))
print(result["success"])
```