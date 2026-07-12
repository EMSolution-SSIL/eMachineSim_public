# eMachineSim Examples

This directory contains public sample and verification datasets used by the
eMachineSim documentation and Codex skill files.

## Layout

- `electrostatic/`: small electrostatic input examples.
- `thermal/`: thermal conduction, BDF, QVOL, and motor steady thermal examples.
- `structural/`: structural static, modal, and motor NVH examples.

## Running a Case

Use the public Python API:

```python
from pathlib import Path
import eMachineSim

case_dir = Path("Examples/thermal/3by3")
result = eMachineSim.run_file(str(case_dir / "input_sample_3D_3by3.json"), str(case_dir))
print(result["success"])
```

Generated CSV and post files are written to the selected case directory.