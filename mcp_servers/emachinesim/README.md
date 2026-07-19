# eMachineSim MCP Server

This MCP server provides structured access to eMachineSim input and result
diagnostics. It also includes guarded tools for writing selected input JSON
variants and solving a single eMachineSim input file through the Python API /
pyd module.

The server is intended for coding AI agents that need to inspect `input.json`,
thermal diagnostic CSV files, public examples, and heat-balance outputs without
requiring users to manually inspect every file.

## Install for Development

```bat
cd mcp_servers\emachinesim
python -m pip install -e .
```

The MCP runtime dependency is the Python `mcp` package. The pure reader and
summary modules can be imported without starting the MCP server.

## Run

```bat
python -m emachinesim_mcp.server
```

## MCP Client Configuration

Register this server in an MCP-capable AI client using the Python environment
where the `mcp` package is installed.

Generic stdio-style configuration:

```json
{
  "mcpServers": {
    "emachinesim": {
      "command": "python",
      "args": [
        "-m",
        "emachinesim_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\eMachineSim_public\\mcp_servers\\emachinesim"
      }
    }
  }
}
```

If `emachinesim-mcp` is installed with `python -m pip install -e .`, the
`PYTHONPATH` entry may not be necessary.

## Phase 1: Read-Only Tools

- `get_project_info`
- `inspect_input_json`
- `list_examples`
- `find_example`
- `summarize_thermal_run`
- `check_surface_assignments`
- `summarize_gap_coupling`
- `summarize_interface_resistance`
- `summarize_cooling_paths`
- `get_recommended_csvs`

All tools return JSON-serializable dictionaries.

## Phase 3: Guarded Write and Python API Solve Tools

These tools are intentionally narrow. They do not provide arbitrary file editing
or arbitrary shell execution.

- `write_gap_coupling_h`
- `write_gap_coupling_nu`
- `write_total_heat_source`
- `solve_input_json_python_api`
- `solve_input_json_python_api_and_summarize_thermal`

Solve tools require `confirm=True` and import the `eMachineSim` Python module
by default. This module is expected to be provided by the installed eMachineSim
wheel or by a development `.pyd` directory passed as `module_search_path`.

Use `allowed_root` when possible so the tool can reject paths outside the
intended project or example directory.

Example guarded solve:

```python
solve_input_json_python_api_and_summarize_thermal(
    input_json_path=r"C:\path\to\input.json",
    run_directory=r"C:\path\to\case-directory",
    module_name="eMachineSim",
    module_search_path=None,
    confirm=True,
    allowed_root=r"C:\path\to\case-directory",
)
```

If the eMachineSim wheel is installed in the same Python environment, keep
`module_search_path=None`. If you are testing a development `.pyd`, pass the
directory containing the `.pyd` as `module_search_path`.

For session-based workflows, set `use_session=True`. The server then uses:

```python
session = eMachineSim.Session()
session.initialize(input_json, run_directory)
session.solve()
session.finalize()
```

## Safety Policy

- No unrestricted shell command execution.
- No automatic license handling.
- No long regression scripts by default.
- JSON write tools create focused variants for known eMachineSim settings.
- Result summaries are read from existing CSV outputs after execution.
- Public user workflows should use the Python API / pyd, not the internal debug
  executable.
