# Standard library imports.
from asyncio import run, sleep
from os import getenv

# Third party imports.
from fastmcp import Client
from fastmcp.utilities.skills import list_skills

# Constants.
SERVER = "{{ cookiecutter.project_name }} MCP Server"
URL = getenv("MCP_URL", "http://localhost:{{ cookiecutter.port }}/mcp")
HEALTH_ATTEMPTS = 5
HEALTH_RETRY_DELAY = 1
GREEN = "\033[32m"
RESET = "\033[0m"


async def main() -> None:

    # Wait for the MCP server to become available.
    for attempt in range(1, HEALTH_ATTEMPTS + 1):
        try:
            async with Client(URL) as client:
                await list_skills(client)
            break
        except Exception as error:
            if attempt == HEALTH_ATTEMPTS:
                raise RuntimeError(f"The {SERVER} is not up.") from error
            await sleep(HEALTH_RETRY_DELAY)

    async with Client(URL) as client:
        # Test 1: the server must expose at least one skill.
        skill_list = await list_skills(client)
        skill_exposure_error = f"The {SERVER} is not exposing any skills."
        assert len(skill_list) > 0, skill_exposure_error
        skills = ", ".join([skill.name for skill in skill_list])
        print(f" {GREEN}✔{RESET} The {SERVER} is exposing: {skills}")

        for skill in skill_list:
            mcp_resource = f"skill://{skill.name}/SKILL.md"
            mcp_resource_contents = await client.read_resource(mcp_resource)

            # Test 2: the skill must be readable.
            skill_read_error = f"The '{skill.name}' skill cannot be read."
            assert mcp_resource_contents, skill_read_error
            print(f" {GREEN}✔{RESET} The {skill.name} skill can be read")

            # Test 3: the skill cannot be empty.
            empty_skill_error = f"The {skill.name} skill is empty."
            assert mcp_resource_contents[0].text, empty_skill_error
            print(f" {GREEN}✔{RESET} The {skill.name} skill is not empty")

    print(f"[+] The {SERVER} is up-up")


if __name__ == "__main__":
    run(main())
