# Standard library imports.
from os import environ
from pathlib import Path

# Third party imports.
from agentmesh.governance import govern
from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider
from starlette.requests import Request
from starlette.responses import JSONResponse

# Local imports.
from tools import TOOLS

# Constants.
BASE_DIRECTORY = Path(__file__).parent
POLICY_PATH = BASE_DIRECTORY / "policy.yml"


def main() -> None:
    """Start the MCP server."""

    # Get the FASTMCP_PORT environment variable.
    if "FASTMCP_PORT" not in environ:
        raise RuntimeError("FASTMCP_PORT environment variable is not set.")

    fastmcp_port = int(environ["FASTMCP_PORT"])

    # Init an MCP server.
    mcp = FastMCP(name="{{ cookiecutter.project_slug }}")

    # Govern and register tools with the MCP server.
    for tool in TOOLS:
        governed_tool = govern(
            tool,
            policy=str(POLICY_PATH),
            agent_id="{{ cookiecutter.project_slug }}",
        )
        mcp.add_tool(governed_tool)

    # Register skills with the MCP server.
    mcp.add_provider(
        SkillsDirectoryProvider(
            roots=BASE_DIRECTORY / "skills",
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
        port=fastmcp_port,
    )


if __name__ == "__main__":
    main()
