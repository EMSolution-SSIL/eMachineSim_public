from __future__ import annotations

from . import tools


def create_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "The Python 'mcp' package is required to run the eMachineSim MCP server. "
            "Install this package with `python -m pip install -e mcp_servers/emachinesim`."
        ) from exc

    mcp = FastMCP("emachinesim")

    mcp.tool()(tools.get_project_info)
    mcp.tool()(tools.inspect_input_json)
    mcp.tool()(tools.list_examples)
    mcp.tool()(tools.find_example)
    mcp.tool()(tools.summarize_thermal_run)
    mcp.tool()(tools.check_surface_assignments)
    mcp.tool()(tools.summarize_gap_coupling)
    mcp.tool()(tools.summarize_interface_resistance)
    mcp.tool()(tools.summarize_cooling_paths)
    mcp.tool(name="get_recommended_csvs")(tools.recommended_csvs)
    mcp.tool()(tools.write_gap_coupling_h)
    mcp.tool()(tools.write_gap_coupling_nu)
    mcp.tool()(tools.write_total_heat_source)
    mcp.tool()(tools.solve_input_json_python_api)
    mcp.tool()(tools.solve_input_json_python_api_and_summarize_thermal)

    return mcp


def main() -> None:
    create_server().run()


if __name__ == "__main__":
    main()
