# Structural Box

Small structural verification case.

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/structural/box")
result = eMachineSim.run_file(str(case_dir / "input_sample_3D_3by3.json"), str(case_dir))
print(result["success"])
```