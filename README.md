# cookiecutter-mcp-server

[![CI Pipeline](https://github.com/deathlabs/cookiecutter-mcp-server/actions/workflows/ci.yaml/badge.svg)](https://github.com/deathlabs/cookiecutter-mcp-server/actions/workflows/ci.yaml)

A Cookiecutter template for creating Python MCP servers with Microsoft's [Agent Governance Toolkit (AGT)](https://github.com/microsoft/agent-governance-toolkit) built in. The template includes skills, tools, and an AGT policy so you can see how the pieces work together and adapt them for your own MCP server. The template also includes two optional Codex configuration files. `.codex/config.toml` connects Codex to the MCP server, and `.codex/agents/knowledge-manager.toml` defines a sample agent that uses its tools. You should replace AGT policy, skills, and tools with ones suited to your project.

## Quickstart

There are two ways to start using this template. Use Option 1 to create an MCP server for your own project. Use Option 2 to explore the template by cloning the repository and running its Makefile to create, start, and test an example MCP server. Both options end with trying out the MCP server using the provided Codex subagent.

The instructions below assume you are using VS Code and OpenAI's Codex agent. They also assume you have or will get the following software installed: [Make](https://www.gnu.org/software/make/), [Docker](https://docs.docker.com/get-started/get-docker/), [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [Semgrep](https://semgrep.dev/), [TruffleHog](https://github.com/trufflesecurity/trufflehog), [Hadolint](https://github.com/hadolint/hadolint), [Syft](https://github.com/anchore/syft#installation), [Grype](https://github.com/anchore/grype#installation), [yq](https://github.com/mikefarah/yq), [cookiecutter](https://github.com/cookiecutter/cookiecutter), [VS Code](https://code.visualstudio.com/), and the [VS Code Extension for Codex](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt). Ruff, Semgrep, TruffleHog, Hadolint, Syft, and Grype are used in our development workflow to help identify and reduce security risks introduced by this cookiecutter template.

### Option 1

**Step 1.** Run Cookiecutter against the GitHub repository.

```bash
cookiecutter https://github.com/deathlabs/cookiecutter-mcp-server.git
```

When prompted, either accept the default values or provide your own.

```
  [1/11] project_name (Megatron):
  [2/11] project_slug (megatron):
  [3/11] project_description (Megatron is an MCP server that exposes tools and skills that agents can use to stop the Autobots.):
  [4/11] author (Victor Fernandez III):
  [5/11] year (2026):
  [6/11] github_organization (deathlabs):
  [7/11] github_repository (deathlabs/megatron):
  [8/11] port (8002):
  [9/11] custom_agent_name (knowledge-manager):
  [10/11] custom_agent_description (Manages observation records through the megatron MCP server.):
  [11/11] custom_agent_developer_instructions (You are responsible for managing the observation records stored by the megatron MCP server. Use megatron MCP tools to list records and read individual
records. Use its delete tool when the parent agent explicitly delegates a deletion. Do not use shell commands, filesystem tools, or other connectors to access or change these records. Before deleting a
record, list the available records and read the specific record to confirm its ID and contents. Never infer a record ID from its position in a list. If a megatron tool is unavailable or denies an
operation, report that result to the parent agent. Do not work around a denial through another tool. Stay within the scope delegated by the parent agent. Report which records you inspected, which
records you deleted, and any operations you could not complete.):
```

**Step 2.** Open the MCP server you created in VS Code. Replace `<project-name>` with the project name you entered or accepted in the previous step (e.g., `megatron`).

```bash
code <project-name>
```

**Step 3.** Use the Makefile to create, start, and test your MCP server.

```bash
make
```

**Step 4.** [Try the demo](#demo).

### Option 2

**Step 1.** Clone the repository.

```bash
git clone https://github.com/deathlabs/cookiecutter-mcp-server.git
```

**Step 2.** Change to the repository directory.

```bash
cd cookiecutter-mcp-server
```

**Step 3.** Use the Makefile to create, start, and test an example MCP server. The Makefile places the created MCP server in the `build` folder, in a subfolder named after the server.

```bash
make
```

**Step 4.** Open the created MCP server in VS Code. Replace `megatron` with the name of the server you created.

```bash
code build/megatron
```

**Step 5.** [Try the demo](#demo).

### Demo

**Step 1.** Tell Docker you want to watch the logs for your MCP server. Replace `<project-name>` with the name of your actual MCP server container (e.g., `megatron_mcp`).

```bash
docker logs <project-name> -f
```

**Step 2.** Enter this prompt into the Codex extension of your VS Code instance to try out your MCP server.

> Have @knowledge-manager list and read all observations. Then tell it to delete the ones whose names end in an odd number.

Eventually, your Codex agent should report something similar to the following. 

```
@knowledge-manager listed all 10 observations and read 9.

- Deleted: observation-001, 005, 007, 009.
- Retained: observation-002, 003, 004, 006, 008, 010.

Automatic approval review blocked reading observation-003 under rule `deny-deletion-of-observation-003`, stating “Deleting observation 003 is not allowed.” Its deletion was not attempted.
```

In the logs, you should also see an entry that looks like below. 

```
[09/23/26 11:42:02] Error calling tool 'delete_record'
                    ╭─────────── Traceback (most recent call last) ────────────╮
                    │ /home/megatron/.venv/lib/python3.14/site-packages/ │
                    │ fastmcp/server/server.py:1517 in call_tool               │
                    │                                                          │
                    │ /home/megatron/.venv/lib/python3.14/site-packages/ │
                    │ fastmcp/tools/base.py:440 in _run                        │
                    │                                                          │
                    │                 ... 9 frames hidden ...                  │
                    │                                                          │
                    │ /home/megatron/main.py:47 in protected_function    │
                    │                                                          │
                    │    44 │   # Restore the function's signature so it can b │
                    │    45 │   @wraps(fn)                                     │
                    │    46 │   def protected_function(*args, **kwargs):       │
                    │ ❱  47 │   │   return governor(*args, **kwargs)           │
                    │    48 │                                                  │
                    │    49 │   return protected_function                      │
                    │    50                                                    │
                    │                                                          │
                    │ /home/megatron/.venv/lib/python3.14/site-packages/ │
                    │ agentmesh/governance/govern.py:281 in __call__           │
                    │                                                          │
                    │   278 │   │   if not decision.allowed:                   │
                    │   279 │   │   │   if self._config.on_deny:               │
                    │   280 │   │   │   │   return self._config.on_deny(decisi │
                    │ ❱ 281 │   │   │   raise GovernanceDenied(decision)       │
                    │   282 │   │                                              │
                    │   283 │   │   # Advisory layer — runs ONLY after determi │
                    │   284 │   │   if self._config.advisory and decision.allo │
                    ╰──────────────────────────────────────────────────────────╯
                    GovernanceDenied: Action denied by policy rule
                    'deny-deletion-of-observation-003': Deleting observation 003
                    is not allowed.
```

## Cleaning Up

To stop your MCP server and delete its container image, enter the commands below.

```bash
make stop-container
make remove-container
make remove-container-image
```
