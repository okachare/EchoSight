# Geti CSAM Helper MCP

This repository includes a local Model Context Protocol (MCP) server for the **Geti CSAM Helper** agent.

Primary author: **Omkar Kachare, 11943102**

## What it provides

The server exposes:

- `geti-csam://skills/csam-basics`: CSAM fundamentals and image/annotation guidance.
- `geti-csam://skills/geti-setup-helper`: Geti pre-work and readiness guidance.
- `get_setup_links`: approved access and Web Geti links.
- `get_run_readiness_check`: pre-run readiness checklist.
- `diagnose_geti_issue`: first safe diagnostic check for common symptoms.
- `operator_onboarding`: prompt for training a new operator.
- `troubleshooting`: prompt for structured issue diagnosis.

It reads only the two skill files and does not expose raw CSAM images, logs, or model artifacts through MCP.

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
- `mcp_geti_csam_helper.py`
- `requirements-mcp.txt`
- `.vscode/mcp.json`
- `MCP_GETI_CSAM_HELPER.md`

Teammates clone or pull the repository, install the MCP dependency in their local environment, open the repository in VS Code, and start the registered MCP server. They must still have the required Intel access and GitHub Copilot/MCP support enabled.

Do not commit credentials, tokens, private URLs beyond approved project links, or raw CSAM data.
