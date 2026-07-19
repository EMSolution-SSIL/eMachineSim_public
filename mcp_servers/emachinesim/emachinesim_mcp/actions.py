from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .readers import read_json, require_file, resolve_path
from .summaries import inspect_input_json, summarize_thermal_run


def _ok(summary: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    return {"ok": True, "summary": summary, "warnings": warnings or []}


def _fail(message: str, warnings: list[str] | None = None) -> dict[str, Any]:
    return {"ok": False, "summary": {"error": message}, "warnings": warnings or []}


def _ensure_within_allowed_root(path: Path, allowed_root: str | None) -> list[str]:
    if not allowed_root:
        return ["allowed_root was not provided; caller is responsible for path safety."]
    root = resolve_path(allowed_root)
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path is outside allowed_root: {path} not under {root}") from exc
    return []


def _write_json_with_backup(data: dict[str, Any], output_path: Path, create_backup: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if create_backup and output_path.exists():
        backup = output_path.with_suffix(output_path.suffix + ".bak")
        shutil.copy2(output_path, backup)
    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _thermal_network(data: dict[str, Any]) -> dict[str, Any]:
    thermal_network = data.setdefault("thermal_network", {})
    if not isinstance(thermal_network, dict):
        raise ValueError("thermal_network must be a JSON object.")
    return thermal_network


def _find_named_item(items: Any, name: str, section_name: str) -> dict[str, Any]:
    if not isinstance(items, list):
        raise ValueError(f"{section_name} must be a JSON array.")
    for item in items:
        if isinstance(item, dict) and item.get("name") == name:
            return item
    raise ValueError(f"Could not find {section_name} item named '{name}'.")


def write_gap_coupling_h(
    input_json_path: str,
    output_json_path: str,
    coupling_name: str,
    h: float,
    allowed_root: str | None = None,
    create_backup: bool = True,
) -> dict[str, Any]:
    """Write a variant input JSON with a named gap coupling set to mode='h'."""
    if h <= 0.0:
        return _fail("h must be positive.")
    input_path = require_file(input_json_path)
    output_path = resolve_path(output_json_path)
    try:
        warnings = _ensure_within_allowed_root(output_path, allowed_root)
        data = read_json(input_path)
        network = _thermal_network(data)
        couplings = network.get("gap_thermal_couplings") or data.get("gap_thermal_couplings")
        coupling = _find_named_item(couplings, coupling_name, "gap_thermal_couplings")
        coupling["mode"] = "h"
        coupling["h"] = float(h)
        for key in ("nu", "nusselt_number", "air_thermal_conductivity", "k_air", "gap_thickness"):
            coupling.pop(key, None)
        _write_json_with_backup(data, output_path, create_backup)
    except Exception as exc:
        return _fail(str(exc))
    return _ok({
        "input_json": str(input_path),
        "output_json": str(output_path),
        "coupling_name": coupling_name,
        "mode": "h",
        "h": float(h),
    }, warnings)


def write_gap_coupling_nu(
    input_json_path: str,
    output_json_path: str,
    coupling_name: str,
    nu: float,
    air_thermal_conductivity: float,
    gap_thickness: float,
    allowed_root: str | None = None,
    create_backup: bool = True,
) -> dict[str, Any]:
    """Write a variant input JSON with a named gap coupling set to mode='nu'."""
    if nu <= 0.0:
        return _fail("nu must be positive.")
    if air_thermal_conductivity <= 0.0:
        return _fail("air_thermal_conductivity must be positive.")
    if gap_thickness <= 0.0:
        return _fail("gap_thickness must be positive.")
    input_path = require_file(input_json_path)
    output_path = resolve_path(output_json_path)
    h_equiv = float(nu) * float(air_thermal_conductivity) / float(gap_thickness)
    try:
        warnings = _ensure_within_allowed_root(output_path, allowed_root)
        data = read_json(input_path)
        network = _thermal_network(data)
        couplings = network.get("gap_thermal_couplings") or data.get("gap_thermal_couplings")
        coupling = _find_named_item(couplings, coupling_name, "gap_thermal_couplings")
        coupling["mode"] = "nu"
        coupling["nu"] = float(nu)
        coupling["air_thermal_conductivity"] = float(air_thermal_conductivity)
        coupling["gap_thickness"] = float(gap_thickness)
        coupling.pop("h", None)
        _write_json_with_backup(data, output_path, create_backup)
    except Exception as exc:
        return _fail(str(exc))
    return _ok({
        "input_json": str(input_path),
        "output_json": str(output_path),
        "coupling_name": coupling_name,
        "mode": "nu",
        "nu": float(nu),
        "air_thermal_conductivity": float(air_thermal_conductivity),
        "gap_thickness": float(gap_thickness),
        "h_equiv": h_equiv,
    }, warnings)


def write_total_heat_source(
    input_json_path: str,
    output_json_path: str,
    source_name: str,
    property_ids: list[int],
    total_heat: float,
    modeled_fraction: float = 1.0,
    distribution: str = "uniform_by_target_volume",
    allowed_root: str | None = None,
    create_backup: bool = True,
) -> dict[str, Any]:
    """Add or update a thermal_volume_heat_sources mode='total_heat' item."""
    if not source_name:
        return _fail("source_name must not be empty.")
    if not property_ids:
        return _fail("property_ids must not be empty.")
    if total_heat < 0.0:
        return _fail("total_heat must be non-negative.")
    if modeled_fraction < 0.0:
        return _fail("modeled_fraction must be non-negative.")
    if distribution != "uniform_by_target_volume":
        return _fail("Only distribution='uniform_by_target_volume' is supported.")

    input_path = require_file(input_json_path)
    output_path = resolve_path(output_json_path)
    assigned_heat = float(total_heat) * float(modeled_fraction)
    try:
        warnings = _ensure_within_allowed_root(output_path, allowed_root)
        data = read_json(input_path)
        sources = data.setdefault("thermal_volume_heat_sources", [])
        if not isinstance(sources, list):
            raise ValueError("thermal_volume_heat_sources must be a JSON array.")
        source = None
        for item in sources:
            if isinstance(item, dict) and item.get("name") == source_name:
                source = item
                break
        if source is None:
            source = {"name": source_name}
            sources.append(source)
        source.clear()
        source.update({
            "name": source_name,
            "mode": "total_heat",
            "target": {"property_ids": [int(pid) for pid in property_ids]},
            "total_heat": float(total_heat),
            "modeled_fraction": float(modeled_fraction),
            "distribution": distribution,
        })
        _write_json_with_backup(data, output_path, create_backup)
    except Exception as exc:
        return _fail(str(exc))
    return _ok({
        "input_json": str(input_path),
        "output_json": str(output_path),
        "source_name": source_name,
        "mode": "total_heat",
        "property_ids": [int(pid) for pid in property_ids],
        "total_heat": float(total_heat),
        "modeled_fraction": float(modeled_fraction),
        "assigned_heat": assigned_heat,
    }, warnings)


def run_input_json(
    executable_path: str,
    input_json_path: str,
    working_directory: str | None = None,
    timeout_seconds: int = 600,
    confirm: bool = False,
    allowed_root: str | None = None,
) -> dict[str, Any]:
    """Run eMachineSim for one input JSON file with explicit confirmation."""
    if not confirm:
        return _fail("Execution requires confirm=True.")
    if timeout_seconds <= 0:
        return _fail("timeout_seconds must be positive.")

    exe = require_file(executable_path)
    input_json = require_file(input_json_path)
    work_dir = resolve_path(working_directory) if working_directory else input_json.parent
    if not work_dir.is_dir():
        return _fail(f"Working directory not found: {work_dir}")

    try:
        warnings = _ensure_within_allowed_root(input_json, allowed_root)
        warnings.extend(_ensure_within_allowed_root(work_dir, allowed_root))
        start = time.perf_counter()
        completed = subprocess.run(
            [str(exe), str(input_json)],
            cwd=str(work_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            shell=False,
        )
        elapsed = time.perf_counter() - start
    except subprocess.TimeoutExpired as exc:
        return _fail(f"Execution timed out after {timeout_seconds} seconds.", [str(exc)])
    except Exception as exc:
        return _fail(str(exc))

    stdout_tail = completed.stdout[-4000:] if completed.stdout else ""
    stderr_tail = completed.stderr[-4000:] if completed.stderr else ""
    return _ok({
        "executable": str(exe),
        "input_json": str(input_json),
        "working_directory": str(work_dir),
        "return_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "stdout_tail": stdout_tail,
        "stderr_tail": stderr_tail,
    }, warnings if completed.returncode == 0 else warnings + ["Execution returned a nonzero exit code."])


def run_input_json_and_summarize_thermal(
    executable_path: str,
    input_json_path: str,
    working_directory: str | None = None,
    timeout_seconds: int = 600,
    confirm: bool = False,
    allowed_root: str | None = None,
) -> dict[str, Any]:
    """Run one input JSON and then summarize thermal result CSVs in the work directory."""
    run_result = run_input_json(
        executable_path=executable_path,
        input_json_path=input_json_path,
        working_directory=working_directory,
        timeout_seconds=timeout_seconds,
        confirm=confirm,
        allowed_root=allowed_root,
    )
    work_dir = working_directory or str(require_file(input_json_path).parent)
    thermal_summary = summarize_thermal_run(work_dir)
    warnings = run_result.get("warnings", []) + thermal_summary.get("warnings", [])
    return _ok({
        "run": run_result.get("summary", {}),
        "thermal_summary": thermal_summary.get("summary", {}),
        "input_summary": inspect_input_json(input_json_path).get("summary", {}),
    }, warnings)


def _import_emachinesim_module(module_name: str, module_search_path: str | None):
    if module_search_path:
        search_path = str(resolve_path(module_search_path))
        if search_path not in sys.path:
            sys.path.insert(0, search_path)
    return __import__(module_name)


def _result_to_summary(result: Any) -> dict[str, Any]:
    if result is None:
        return {"return_value": None}
    if isinstance(result, dict):
        return result
    summary: dict[str, Any] = {
        "return_type": type(result).__name__,
        "repr": repr(result)[:1000],
    }
    for name in ("ok", "success", "status", "return_code", "message", "output_directory"):
        if hasattr(result, name):
            try:
                value = getattr(result, name)
                if isinstance(value, (str, int, float, bool)) or value is None:
                    summary[name] = value
                else:
                    summary[name] = repr(value)[:1000]
            except Exception:
                pass
    return summary


def solve_input_json_python_api(
    input_json_path: str,
    run_directory: str | None = None,
    module_name: str = "eMachineSim",
    module_search_path: str | None = None,
    use_session: bool = False,
    confirm: bool = False,
    allowed_root: str | None = None,
) -> dict[str, Any]:
    """Solve one input JSON through the eMachineSim Python API / pyd."""
    if not confirm:
        return _fail("Python API solve requires confirm=True.")

    input_json = require_file(input_json_path)
    run_dir = resolve_path(run_directory) if run_directory else input_json.parent
    if not run_dir.is_dir():
        return _fail(f"Run directory not found: {run_dir}")

    try:
        warnings = _ensure_within_allowed_root(input_json, allowed_root)
        warnings.extend(_ensure_within_allowed_root(run_dir, allowed_root))
        emachinesim = _import_emachinesim_module(module_name, module_search_path)
    except Exception as exc:
        return _fail(
            f"Could not import Python module '{module_name}': {exc}",
            ["Install the eMachineSim wheel or pass module_search_path to the directory containing the pyd."],
        )

    start = time.perf_counter()
    old_cwd = Path.cwd()
    try:
        os.chdir(run_dir)
        if use_session:
            if not hasattr(emachinesim, "Session"):
                return _fail(f"Module '{module_name}' does not provide Session.")
            session = emachinesim.Session()
            try:
                session.initialize(str(input_json), str(run_dir))
                result = session.solve()
            finally:
                if hasattr(session, "finalize"):
                    session.finalize()
            method = "Session.initialize/solve/finalize"
        else:
            if not hasattr(emachinesim, "run_file"):
                return _fail(f"Module '{module_name}' does not provide run_file.")
            result = emachinesim.run_file(str(input_json), str(run_dir))
            method = "run_file"
    except Exception as exc:
        return _fail(f"Python API solve failed: {exc}")
    finally:
        os.chdir(old_cwd)
    elapsed = time.perf_counter() - start

    return _ok({
        "module_name": module_name,
        "module_file": getattr(emachinesim, "__file__", None),
        "method": method,
        "input_json": str(input_json),
        "run_directory": str(run_dir),
        "elapsed_seconds": elapsed,
        "result": _result_to_summary(result),
    }, warnings)


def solve_input_json_python_api_and_summarize_thermal(
    input_json_path: str,
    run_directory: str | None = None,
    module_name: str = "eMachineSim",
    module_search_path: str | None = None,
    use_session: bool = False,
    confirm: bool = False,
    allowed_root: str | None = None,
) -> dict[str, Any]:
    """Solve one input JSON through Python API / pyd and summarize thermal CSVs."""
    solve_result = solve_input_json_python_api(
        input_json_path=input_json_path,
        run_directory=run_directory,
        module_name=module_name,
        module_search_path=module_search_path,
        use_session=use_session,
        confirm=confirm,
        allowed_root=allowed_root,
    )
    run_dir = run_directory or str(require_file(input_json_path).parent)
    thermal_summary = summarize_thermal_run(run_dir)
    warnings = solve_result.get("warnings", []) + thermal_summary.get("warnings", [])
    return _ok({
        "solve": solve_result.get("summary", {}),
        "thermal_summary": thermal_summary.get("summary", {}),
        "input_summary": inspect_input_json(input_json_path).get("summary", {}),
    }, warnings)
