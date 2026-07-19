from __future__ import annotations

from pathlib import Path
from typing import Any

from .readers import (
    find_row,
    first_row,
    numeric_row,
    read_csv_if_exists,
    read_json,
    require_dir,
    resolve_path,
    rows_to_dict,
    to_float,
    to_int,
)


def ok_response(summary: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    return {"ok": True, "summary": summary, "warnings": warnings or []}


def inspect_input_json(path: str) -> dict[str, Any]:
    data = read_json(path)
    meta = data.get("metaData") if isinstance(data.get("metaData"), dict) else {}
    bdf_import = data.get("bdf_import") if isinstance(data.get("bdf_import"), dict) else {}
    thermal_network = data.get("thermal_network") if isinstance(data.get("thermal_network"), dict) else {}
    heat_sources = data.get("thermal_volume_heat_sources")
    gap_couplings = thermal_network.get("gap_thermal_couplings") or data.get("gap_thermal_couplings")
    surface_couplings = thermal_network.get("surface_thermal_couplings") or data.get("surface_thermal_couplings")
    interface = thermal_network.get("interface_thermal_resistances") or data.get("interface_thermal_resistances")

    warnings: list[str] = []
    if meta.get("type") != "eMachineSimInput":
        warnings.append("metaData.type is missing or is not eMachineSimInput.")
    if not meta.get("eMachineSimVersion"):
        warnings.append("metaData.eMachineSimVersion is missing.")

    likely = "unknown"
    if bdf_import or heat_sources or gap_couplings or thermal_network:
        likely = "thermal"
    elif "structural" in str(data).lower():
        likely = "structural"
    elif "modal" in str(data).lower() or "nvh" in str(data).lower():
        likely = "modal_or_nvh"
    elif "electrostatic" in str(data).lower():
        likely = "electrostatic"

    summary = {
        "path": str(resolve_path(path)),
        "metadata_type": meta.get("type"),
        "emachinesim_version": meta.get("eMachineSimVersion"),
        "comments": meta.get("comments"),
        "likely_analysis_type": likely,
        "has_bdf_import": bool(bdf_import),
        "bdf_mesh_file": bdf_import.get("bdf_file") or bdf_import.get("mesh_file") or bdf_import.get("file"),
        "bdf_material_source": bdf_import.get("material_source"),
        "num_thermal_volume_heat_sources": len(heat_sources) if isinstance(heat_sources, list) else 0,
        "thermal_volume_heat_source_modes": sorted({str(x.get("mode", "")) for x in heat_sources if isinstance(x, dict)}) if isinstance(heat_sources, list) else [],
        "has_thermal_network": bool(thermal_network),
        "num_gap_couplings": len(gap_couplings) if isinstance(gap_couplings, list) else 0,
        "num_surface_couplings": len(surface_couplings) if isinstance(surface_couplings, list) else 0,
        "num_interface_resistances": len(interface) if isinstance(interface, list) else 0,
    }
    return ok_response(summary, warnings)


def summarize_thermal_run(run_directory: str) -> dict[str, Any]:
    run_dir = require_dir(run_directory)
    warnings: list[str] = []
    global_rows = read_csv_if_exists(run_dir, "thermal_global_heat_balance.csv")
    volume_rows = read_csv_if_exists(run_dir, "thermal_fem_volume_heat.csv")
    source_rows = read_csv_if_exists(run_dir, "thermal_volume_heat_sources.csv")

    if not global_rows:
        warnings.append("thermal_global_heat_balance.csv not found.")
    if not volume_rows:
        warnings.append("thermal_fem_volume_heat.csv not found.")

    global_row = first_row(global_rows)
    total_volume_row = find_row(volume_rows, "group_type", "total") or first_row(volume_rows)

    source_totals: dict[str, float] = {}
    for row in source_rows:
        mode = row.get("mode", "")
        assigned = to_float(row.get("assigned_heat"))
        if assigned is not None:
            source_totals[mode] = source_totals.get(mode, 0.0) + assigned

    summary = {
        "run_directory": str(run_dir),
        "fem_qvol_heat": to_float(global_row.get("fem_qvol_heat")),
        "fem_bdf_qvol_heat": to_float(global_row.get("fem_bdf_qvol_heat")),
        "fem_json_volume_heat": to_float(global_row.get("fem_json_volume_heat")),
        "fem_rhs_heat": to_float(global_row.get("fem_rhs_heat")),
        "femh_outflow_heat": to_float(global_row.get("femh_outflow_heat")),
        "network_fixed_temperature_outflow_heat": to_float(global_row.get("network_fixed_temperature_outflow_heat")),
        "global_balance_residual": to_float(global_row.get("global_balance_residual")),
        "global_balance_relative_error": to_float(global_row.get("global_balance_relative_error")),
        "volume_total_elements": to_int(total_volume_row.get("num_elements")),
        "volume_total_volume": to_float(total_volume_row.get("total_volume")),
        "volume_bdf_qvol_heat": to_float(total_volume_row.get("bdf_qvol_heat")),
        "volume_json_heat": to_float(total_volume_row.get("json_volume_heat")),
        "volume_total_qvol_heat": to_float(total_volume_row.get("total_qvol_heat")),
        "json_heat_by_mode": source_totals,
    }
    return ok_response(summary, warnings)


def check_surface_assignments(run_directory: str) -> dict[str, Any]:
    run_dir = require_dir(run_directory)
    rows = read_csv_if_exists(run_dir, "thermal_surface_assignment_summary.csv")
    warnings: list[str] = []
    if not rows:
        warnings.append("thermal_surface_assignment_summary.csv not found.")

    by_category = rows_to_dict(rows, "category")
    categories = {}
    for category, row in by_category.items():
        categories[category] = {
            "face_count": to_int(row.get("face_count")),
            "total_area": to_float(row.get("total_area")),
        }

    overlap_area = categories.get("femh_and_gap_overlap", {}).get("total_area")
    if overlap_area and abs(overlap_area) > 0.0:
        warnings.append("FEMH/gap overlap area is nonzero.")

    summary = {
        "run_directory": str(run_dir),
        "categories": categories,
        "femh_and_gap_overlap_area": overlap_area,
        "unassigned_external_area": categories.get("unassigned_external", {}).get("total_area"),
        "gap_coupling_only_area": categories.get("gap_coupling_only", {}).get("total_area"),
        "femh_only_area": categories.get("femh_only", {}).get("total_area"),
    }
    return ok_response(summary, warnings)


def summarize_gap_coupling(run_directory: str) -> dict[str, Any]:
    run_dir = require_dir(run_directory)
    summary_rows = read_csv_if_exists(run_dir, "thermal_gap_coupling_summary.csv")
    flow_rows = read_csv_if_exists(run_dir, "thermal_gap_coupling_flow_summary.csv")
    h_rows = read_csv_if_exists(run_dir, "thermal_gap_h_model_summary.csv")
    warnings: list[str] = []
    if not summary_rows:
        warnings.append("thermal_gap_coupling_summary.csv not found.")

    flows = rows_to_dict(flow_rows, "coupling_name")
    hmodels = rows_to_dict(h_rows, "coupling_name")
    couplings = []
    for row in summary_rows:
        name = row.get("coupling_name", "")
        flow = flows.get(name, {})
        hmodel = hmodels.get(name, {})
        couplings.append({
            "coupling_name": name,
            "pairing_name": row.get("pairing_name"),
            "mode": row.get("mode"),
            "assembly": row.get("assembly"),
            "accepted_face_pair_count": to_int(row.get("accepted_face_pair_count")),
            "assembled_node_pair_count": to_int(row.get("assembled_node_pair_count")),
            "effective_area_sum": to_float(row.get("effective_area_sum")),
            "total_conductance": to_float(row.get("total_node_pair_conductance") or row.get("total_pair_conductance")),
            "equivalent_resistance": to_float(row.get("equivalent_resistance")),
            "h_equiv": to_float(row.get("h_equiv") or hmodel.get("h_equiv")),
            "Nu": to_float(row.get("Nu") or hmodel.get("Nu")),
            "gap_thickness": to_float(row.get("gap_thickness") or hmodel.get("gap_thickness")),
            "heat_flow_source_to_target": to_float(flow.get("total_heat_source_to_target")),
        })

    return ok_response({"run_directory": str(run_dir), "couplings": couplings}, warnings)


def summarize_interface_resistance(run_directory: str) -> dict[str, Any]:
    run_dir = require_dir(run_directory)
    summary_rows = read_csv_if_exists(run_dir, "thermal_interface_resistance_summary.csv")
    flow_rows = read_csv_if_exists(run_dir, "thermal_interface_resistance_flow_summary.csv")
    warnings: list[str] = []
    if not summary_rows:
        warnings.append("thermal_interface_resistance_summary.csv not found.")

    flows = rows_to_dict(flow_rows, "coupling_name")
    couplings = []
    for row in summary_rows:
        name = row.get("coupling_name", "")
        flow = flows.get(name, {})
        couplings.append({
            "coupling_name": name,
            "mode": row.get("mode"),
            "split_side": row.get("split_side"),
            "assembly": row.get("assembly"),
            "side_a_property_ids": row.get("side_a_property_ids"),
            "side_b_property_ids": row.get("side_b_property_ids"),
            "interface_face_count": to_int(row.get("interface_face_count")),
            "duplicated_node_count": to_int(row.get("duplicated_node_count")),
            "assembled_node_pair_count": to_int(row.get("assembled_node_pair_count")),
            "interface_area": to_float(row.get("interface_area")),
            "h_equiv": to_float(row.get("h_equiv")),
            "total_conductance": to_float(row.get("total_conductance")),
            "equivalent_resistance": to_float(row.get("equivalent_resistance")),
            "heat_side_a_to_side_b": to_float(flow.get("total_heat_side_a_to_side_b")),
        })

    return ok_response({"run_directory": str(run_dir), "couplings": couplings}, warnings)


def summarize_cooling_paths(run_directory: str, limit: int = 50) -> dict[str, Any]:
    run_dir = require_dir(run_directory)
    rows = read_csv_if_exists(run_dir, "thermal_cooling_path_summary.csv")
    warnings: list[str] = []
    if not rows:
        warnings.append("thermal_cooling_path_summary.csv not found.")

    paths = []
    by_type: dict[str, float] = {}
    for row in rows[:max(0, limit)]:
        heat = to_float(row.get("heat_flow"))
        path_type = row.get("path_type", "")
        if heat is not None:
            by_type[path_type] = by_type.get(path_type, 0.0) + heat
        paths.append({
            "path_type": path_type,
            "path_name": row.get("path_name"),
            "source_surface": row.get("source_surface"),
            "target_name": row.get("target_name"),
            "area": to_float(row.get("area")),
            "h_equiv": to_float(row.get("h_equiv")),
            "total_conductance": to_float(row.get("total_conductance")),
            "equivalent_resistance": to_float(row.get("equivalent_resistance")),
            "source_average_temperature": to_float(row.get("source_average_temperature")),
            "target_average_temperature": to_float(row.get("target_average_temperature")),
            "temperature_difference": to_float(row.get("temperature_difference")),
            "heat_flow": heat,
        })

    return ok_response({
        "run_directory": str(run_dir),
        "num_paths_reported": len(paths),
        "heat_flow_sum_by_type": by_type,
        "paths": paths,
    }, warnings)


def list_examples(root: str, max_depth: int = 3) -> dict[str, Any]:
    root_path = require_dir(root)
    entries: list[str] = []
    for path in sorted(root_path.rglob("*")):
        if not path.is_dir():
            continue
        rel = path.relative_to(root_path)
        if len(rel.parts) <= max_depth:
            entries.append(rel.as_posix())
    return ok_response({"root": str(root_path), "directories": entries})


def find_example(root: str, query: str, max_results: int = 20) -> dict[str, Any]:
    root_path = require_dir(root)
    terms = [term.lower() for term in query.split() if term.strip()]
    matches: list[str] = []
    for path in sorted(root_path.rglob("*")):
        rel = path.relative_to(root_path).as_posix()
        hay = rel.lower()
        if all(term in hay for term in terms):
            matches.append(rel)
            if len(matches) >= max_results:
                break
    return ok_response({"root": str(root_path), "query": query, "matches": matches})


def recommended_csvs(analysis_type: str) -> dict[str, Any]:
    key = analysis_type.strip().lower()
    mapping = {
        "thermal": [
            "thermal_volume_heat_sources.csv",
            "thermal_fem_volume_heat.csv",
            "thermal_global_heat_balance.csv",
            "thermal_surface_assignment_summary.csv",
            "thermal_femh_ports.csv",
            "thermal_cooling_path_summary.csv",
            "thermal_component_heat_balance.csv",
            "thermal_gap_coupling_summary.csv",
            "thermal_interface_resistance_summary.csv",
        ],
        "structural": [
            "structural_load_balance.csv",
            "contact_state.csv",
            "contact_penalty_assembly.csv",
        ],
        "modal": [
            "modal_frequencies.csv",
            "modal_modes.csv",
            "motor_nvh_frequency_response_summary.csv",
            "motor_nvh_modal_participation.csv",
        ],
        "nvh": [
            "modal_frequencies.csv",
            "motor_nvh_force_circumferential_order_summary.csv",
            "motor_nvh_frequency_response_summary.csv",
            "motor_nvh_acoustic_radiation_summary.csv",
        ],
        "electrostatic": [
            "post files such as potential/field outputs",
            "available CSV diagnostics depend on the sample",
        ],
    }
    if key not in mapping:
        return ok_response({"analysis_type": analysis_type, "recommended_csvs": []}, [f"Unknown analysis type: {analysis_type}"])
    return ok_response({"analysis_type": key, "recommended_csvs": mapping[key]})

