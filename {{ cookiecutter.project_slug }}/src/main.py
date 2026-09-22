# Standard library imports.
from functools import wraps
from os import environ

# Third party imports.
from agentmesh.governance import govern
from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider
from starlette.requests import Request
from starlette.responses import JSONResponse

# Local imports.
from tools import TOOLS

SECURITY_POLICY_FILE_PATH = "policy.yaml"
SKILLS_DIRECTORY = "skills"


def get_security_policy(file_path: str = SECURITY_POLICY_FILE_PATH) -> str:
    """Read the security policy from the provided file path.

    Returns:
        The security policy as a string.
    """
    with open(file=file_path, encoding="UTF-8", mode="r") as policy_file:
        return policy_file.read()


def defang(fn: callable, policy: str, agent_id: str) -> callable:
    """Wrap a function with governance checks.

    Args:
        fn: The function to wrap.
        policy: The security policy to enforce.
        agent_id: The ID of the agent to enforce the policy for.

    Returns:
        A wrapped function that enforces the security policy.

    """
    governor = govern(fn=fn, policy=policy, agent_id=agent_id)

    @wraps(fn)
    def defanged_tool(*args, **kwargs):
        return governor(*args, **kwargs)

    return defanged_tool


def main() -> None:
    """Start the MCP server."""

    # Check if the FASTMCP_PORT environment variable is set.
    if "FASTMCP_PORT" not in environ:
        raise RuntimeError("The FASTMCP_PORT environment variable is not set.")

    # Get the FASTMCP_PORT environment variable.
    fastmcp_port = int(environ["FASTMCP_PORT"])

    # Init an MCP server.
    mcp = FastMCP(name="{{ cookiecutter.project_slug }}")

    # Read the policy file.
    policy = get_security_policy()

    # Register tools with the MCP server.
    for tool in TOOLS:
        safe_tool = defang(
            fn=tool,
            policy=policy,
            agent_id="{{ cookiecutter.project_slug }}",
        )
        mcp.add_tool(safe_tool)

    # Register skills with the MCP server.
    mcp.add_provider(
        SkillsDirectoryProvider(
            roots=SKILLS_DIRECTORY,
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
