# Python API

Use the public Python module:

```python
import eMachineSim
```

Typical user-facing workflow:

```python
import eMachineSim

session = eMachineSim.Session()
session.load_json("path/to/input.json")
result = session.solve()
print(result.success)
```

Useful API concepts:

- `run_file(path)`: execute one input JSON file.
- `run_json(text_or_dict)`: execute one input JSON payload.
- `Session`: keep a simulation session object for repeated use.
- `Session.solve()`: solve the current session.
- result getters expose generated output paths or parsed summaries where available.
- `run_self_test(name)` is useful for validation, but it is not the main user workflow.

Naming guidance:

- Use `eMachineSim` in user documentation and examples.
- Do not use legacy `eMachineSim` names.
- Avoid presenting the executable as the public interface unless the user asks for internal debugging.

Wheel distribution:

- Users are expected to install a wheel such as `emachinesim-...whl`.
- Python dependencies should be installed from the project-provided requirements file when needed.
- Native dependencies should be bundled into the wheel where possible.
