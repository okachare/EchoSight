# Geti CSAM Helper MCP

This repository includes a local Model Context Protocol (MCP) server for the **Geti CSAM Helper** agent.

Primary author: **Omkar Kachare, 11943102**

## What it provides

The server exposes:

- `geti-csam://skills/csam-basics`: CSAM fundamentals and image/annotation guidance.
- `geti-csam://skills/geti-setup-helper`: Geti pre-work and readiness guidance.
- `geti-csam://skills/geti-trainer`: Detailed click-by-click Web Geti operator training.
- `geti-csam://skills/geti-source-reference`: Official upstream Geti literature, source navigation, and version-aware debugging guidance.
- `get_setup_links`: approved access and Web Geti links.
- `get_geti_source_links`: official Geti GitHub, documentation, release, issue, and discussion links.
- `get_run_readiness_check`: pre-run readiness checklist.
- `diagnose_geti_issue`: first safe diagnostic check for common symptoms.
- `operator_onboarding`: prompt for training a new operator.
- `troubleshooting`: prompt for structured issue diagnosis.

It reads only the four skill files and does not expose raw CSAM images, logs, or model artifacts through MCP.

The helper uses `https://github.com/open-edge-platform/geti` as its public upstream reference for Geti architecture, `getitune`, recipes, source-level debugging, and release history. Upstream `develop` is treated as a moving development reference; installed-release behavior must be checked against the matching tag or local evidence.

## VS Code use

The server is registered in `.vscode/mcp.json`. Open the repository in VS Code with GitHub Copilot and MCP support enabled. Start or trust the `geti-csam-helper` server from the MCP controls, then select the **Geti CSAM Helper** agent.

## Install and run locally

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-mcp.txt
python .\mcp_geti_csam_helper.py
```

The server uses stdio, so it is normally launched by an MCP host rather than opened as a standalone terminal application.

For development inspection with the MCP CLI:

```powershell
mcp dev .\mcp_geti_csam_helper.py
```

## Sharing with the team

Commit and push these files with the agent package:

- `.github/agents/geti-csam-helper.agent.md`
- `.github/skills/csam-basics/SKILL.md`
- `.github/skills/geti-setup-helper/SKILL.md`
- `.github/skills/geti-trainer/SKILL.md`
- `.github/skills/geti-source-reference/SKILL.md`
- `mcp_geti_csam_helper.py`
- `requirements-mcp.txt`
- `.vscode/mcp.json`
- `MCP_GETI_CSAM_HELPER.md`

Teammates clone or pull the repository, install the MCP dependency in their local environment, open the repository in VS Code, and start the registered MCP server. They must still have the required Intel access and GitHub Copilot/MCP support enabled.

Do not commit credentials, tokens, private URLs beyond approved project links, or raw CSAM data.
