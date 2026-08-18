#!/usr/bin/env python
"""Convert a small ASCII Gmsh 4.1 surface mesh to a free-field Nastran BDF.

This utility is intentionally narrow: it supports the Gmsh entities/nodes/
elements layout used by the eMachineSim structural sector examples and writes
GRID, CTRIA3, and CQUAD4 cards that the built-in NASTRANMeshReader can read.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _section(lines: list[str], name: str) -> list[str]:
    start = f"${name}"
    end = f"$End{name}"
    try:
        i0 = lines.index(start)
        i1 = lines.index(end)
    except ValueError as exc:
        raise SystemExit(f"Missing Gmsh section {name}") from exc
    return lines[i0 + 1 : i1]


def _read_entities(lines: list[str]) -> dict[tuple[int, int], int]:
    sec = _section(lines, "Entities")
    counts = [int(x) for x in sec[0].split()]
    if len(counts) != 4:
        raise SystemExit("Unsupported $Entities header")
    idx = 1
    entity_to_physical: dict[tuple[int, int], int] = {}
    for dim, count in enumerate(counts):
        for _ in range(count):
            parts = sec[idx].split()
            idx += 1
            tag = int(parts[0])
            phys_count_index = 4 if dim == 0 else 7
            physical = tag
            if len(parts) > phys_count_index:
                nphys = int(parts[phys_count_index])
                if nphys > 0 and len(parts) > phys_count_index + 1:
                    physical = int(parts[phys_count_index + 1])
            entity_to_physical[(dim, tag)] = physical
    return entity_to_physical


def _take_tokens(lines: list[str], start: int, count: int) -> tuple[list[str], int]:
    out: list[str] = []
    idx = start
    while len(out) < count and idx < len(lines):
        out.extend(lines[idx].split())
        idx += 1
    if len(out) < count:
        raise SystemExit("Unexpected end of Gmsh token block")
    return out[:count], idx


def _read_nodes(lines: list[str]) -> dict[int, tuple[float, float, float]]:
    sec = _section(lines, "Nodes")
    header = [int(x) for x in sec[0].split()]
    nblocks, nnodes = header[0], header[1]
    idx = 1
    nodes: dict[int, tuple[float, float, float]] = {}
    for _ in range(nblocks):
        entity_dim, _entity_tag, parametric, nblock = [int(x) for x in sec[idx].split()]
        idx += 1
        tags_raw, idx = _take_tokens(sec, idx, nblock)
        coord_width = 3 + (entity_dim if parametric else 0)
        coords_raw, idx = _take_tokens(sec, idx, nblock * coord_width)
        for i, tag_text in enumerate(tags_raw):
            tag = int(tag_text)
            base = i * coord_width
            nodes[tag] = (
                float(coords_raw[base]),
                float(coords_raw[base + 1]),
                float(coords_raw[base + 2]),
            )
    if len(nodes) != nnodes:
        raise SystemExit(f"Node count mismatch: header={nnodes}, parsed={len(nodes)}")
    return nodes


def _read_elements(
    lines: list[str],
    entity_to_physical: dict[tuple[int, int], int],
    include_physical: set[int] | None,
) -> list[tuple[str, int, int, list[int]]]:
    sec = _section(lines, "Elements")
    header = [int(x) for x in sec[0].split()]
    nblocks = header[0]
    idx = 1
    out: list[tuple[str, int, int, list[int]]] = []
    type_map = {
        2: ("CTRIA3", 3),
        3: ("CQUAD4", 4),
    }
    for _ in range(nblocks):
        entity_dim, entity_tag, element_type, nblock = [int(x) for x in sec[idx].split()]
        idx += 1
        card = type_map.get(element_type)
        if card is None:
            idx += nblock
            continue
        card_name, nnodes = card
        physical = entity_to_physical.get((entity_dim, entity_tag), entity_tag)
        for _elem in range(nblock):
            parts = [int(x) for x in sec[idx].split()]
            idx += 1
            if include_physical is not None and physical not in include_physical:
                continue
            eid = parts[0]
            node_ids = parts[1 : 1 + nnodes]
            out.append((card_name, eid, physical, node_ids))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--include-physical",
        default="",
        help="Comma-separated physical IDs to export, for example 20,30,50000,50001.",
    )
    args = parser.parse_args()

    include = None
    if args.include_physical.strip():
        include = {int(x.strip()) for x in args.include_physical.split(",") if x.strip()}

    lines = [line.strip() for line in args.input.read_text(encoding="utf-8").splitlines()]
    entity_to_physical = _read_entities(lines)
    nodes = _read_nodes(lines)
    elements = _read_elements(lines, entity_to_physical, include)

    used_node_ids = sorted({nid for _card, _eid, _pid, nids in elements for nid in nids})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="ascii", newline="\n") as fp:
        fp.write("BEGIN BULK\n")
        for nid in used_node_ids:
            x, y, z = nodes[nid]
            fp.write(f"GRID {nid} 0 {x:.16e} {y:.16e} {z:.16e}\n")
        for card, eid, pid, nids in elements:
            fp.write(f"{card} {eid} {pid} " + " ".join(str(nid) for nid in nids) + "\n")
        fp.write("ENDDATA\n")

    print(
        f"converted {args.input} -> {args.output}: "
        f"nodes={len(used_node_ids)}, elements={len(elements)}"
    )


if __name__ == "__main__":
    main()
