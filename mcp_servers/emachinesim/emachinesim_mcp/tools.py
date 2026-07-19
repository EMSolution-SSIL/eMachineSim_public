from __future__ import annotations

from typing import Any

from . import __version__
from .actions import (
    run_input_json,
    run_input_json_and_summarize_thermal,
    solve_input_json_python_api,
    solve_input_json_python_api_and_summarize_thermal,
    write_gap_coupling_h,
    write_gap_coupling_nu,
    write_total_heat_source,
)
from .summaries import (
    check_surface_assignments,
    find_example,
    inspect_input_json,
    list_examples,
    recommended_csvs,
    summarize_cooling_paths,
    summarize_gap_coupling,
    summarize_interface_resistance,
    summarize_thermal_run,
)


def get_project_info() -> dict[str, Any]:
    return {
        "ok": True,
        "summary": {
            "name": "emachinesim-mcp",
            "version": __version__,
            "mode": "guarded_read_write_run",
            "tool_groups": [
                "input_json_inspection",
                "example_discovery",
                "thermal_heat_balance",
                "surface_assignment",
                "gap_coupling",
                "interface_resistance",
                "cooling_paths",
                "recommended_outputs",
                "input_json_variant_writing",
                "guarded_python_api_solve",
            ],
            "execution_safety": {
                "solve_tools_require_confirm_true": True,
                "preferred_execution": "eMachineSim Python API / pyd",
                "exe_execution": "internal compatibility only",
                "subprocess_shell_for_exe_compatibility": False,
                "allowed_root_recommended": True,
            },
        },
        "warnings": [],
    }


__all__ = [
    "get_project_info",
    "inspect_input_json",
    "list_examples",
    "find_example",
    "summarize_thermal_run",
    "check_surface_assignments",
    "summarize_gap_coupling",
    "summarize_interface_resistance",
    "summarize_cooling_paths",
    "recommended_csvs",
    "write_gap_coupling_h",
    "write_gap_coupling_nu",
    "write_total_heat_source",
    "solve_input_json_python_api",
    "solve_input_json_python_api_and_summarize_thermal",
    "run_input_json",
    "run_input_json_and_summarize_thermal",
]
