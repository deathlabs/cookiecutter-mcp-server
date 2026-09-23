# cookiecutter-mcp-server
[![CI Pipeline](https://github.com/deathlabs/cookiecutter-mcp-server/actions/workflows/ci.yaml/badge.svg)](https://github.com/deathlabs/cookiecutter-mcp-server/actions/workflows/ci.yaml) 

A Cookiecutter template for creating Python MCP servers with Microsoft's [Agent Governance Toolkit (AGT)](https://github.com/microsoft/agent-governance-toolkit) built in. The template includes skills, tools, and an AGT policy so you can see how the pieces work together and adapt them for your own MCP server. The template also includes two optional Codex configuration files. `.codex/config.toml` connects Codex to the MCP server, and `.codex/agents/knowledge-manager.toml` defines a sample agent that uses its tools. You should replace AGT policy, skills, and tools with ones suited to your project.

## Quickstart

There are two ways to start using this template. Use Option 1 to create an MCP server for your own project. Use Option 2 to explore the template by cloning the repository and running its Makefile to create, start, and test an example MCP server. Both options end with trying out the MCP server using the provided Codex subagent.

The instructions below assume you are using VS Code and OpenAI's Codex agent. They also assume you have or will get the following software installed: [Make](https://www.gnu.org/software/make/), [Docker](https://docs.docker.com/get-started/get-docker/), [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [Semgrep](https://semgrep.dev/), [TruffleHog](https://github.com/trufflesecurity/trufflehog), [Hadolint](https://github.com/hadolint/hadolint), [Syft](https://github.com/anchore/syft#installation), [Grype](https://github.com/anchore/grype#installation), [yq](https://github.com/mikefarah/yq), [VS Code](https://code.visualstudio.com/), and the [VS Code Extension for Codex](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt). Ruff, Semgrep, TruffleHog, Hadolint, Syft, and Grype are used in our development workflow to help identify and reduce security risks introduced by this cookiecutter template.

### Option 1

**Step 1.** Run Cookiecutter against the GitHub repository.

```bash
cookiecutter https://github.com/deathlabs/cookiecutter-mcp-server.git
```

**Step 2.** Open the MCP server you created in VS Code. Replace `<project-name>` with its directory name.

```bash
code <project-name>
```

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

### Demo

Enter this prompt to try out your MCP server.

> Have @knowledge-manager list and read all observations. Then tell it to delete the ones whose names end in an odd number.
