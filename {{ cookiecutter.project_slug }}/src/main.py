# Standard library imports.
from os import environ
from pathlib import Path

# Third party imports.
from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider
from starlette.requests import Request
from starlette.responses import JSONResponse

# Local imports.
from shinobi.tools import TOOLS


def main():
    """Start the MCP server."""

    # Get the FASTMCP_PORT environment variable.
    if "FASTMCP_PORT" not in environ:
        raise RuntimeError("FASTMCP_PORT environment variable is not set.")
    FASTMCP_PORT = int(environ["FASTMCP_PORT"])

    # Init a MCP server.
    mcp = FastMCP(name="shinobi")

    # Register tools with the MCP server.
    for tool in TOOLS:
        mcp.add_tool(tool)

    # Register skills with the MCP server.
    mcp.add_provider(
        SkillsDirectoryProvider(
            roots=Path(__file__).parent / "skills",
        )
    )

    @mcp.custom_route("/api/v1/health", methods=["GET"])
    async def health(request: Request) -> JSONResponse:
        """Respond to health checks.

        Returns:
            A JSON-based response that indicates the service is running.
        """
        return JSONResponse(content={"status": "ok"})

    # Start the MCP server.
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=FASTMCP_PORT,
    )


if __name__ == "__main__":
    main()
