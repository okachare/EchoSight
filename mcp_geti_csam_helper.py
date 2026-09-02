"""Local MCP server for the shareable Geti CSAM Helper agent."""

from pathlib import Path

from mcp.server.mcpserver import MCPServer


ROOT = Path(__file__).resolve().parent
SKILLS = {
    "csam-basics": ROOT / ".github" / "skills" / "csam-basics" / "SKILL.md",
    "geti-setup-helper": ROOT / ".github" / "skills" / "geti-setup-helper" / "SKILL.md",
    "geti-trainer": ROOT / ".github" / "skills" / "geti-trainer" / "SKILL.md",
    "geti-source-reference": ROOT / ".github" / "skills" / "geti-source-reference" / "SKILL.md",
}

mcp = MCPServer("Geti CSAM Helper")


def read_skill(name: str) -> str:
    path = SKILLS[name]
    if not path.is_file():
        raise FileNotFoundError(f"Skill file not found: {path}")
    return path.read_text(encoding="utf-8")


@mcp.resource("geti-csam://skills/csam-basics")
def csam_basics() -> str:
    """CSAM fundamentals, image data, defects, and task selection."""
    return read_skill("csam-basics")


@mcp.resource("geti-csam://skills/geti-setup-helper")
def geti_setup_helper() -> str:
    """Geti access, image conversion, dataset preparation, and readiness checks."""
    return read_skill("geti-setup-helper")


@mcp.resource("geti-csam://skills/geti-trainer")
def geti_trainer() -> str:
    """Detailed Web Geti operator training and UI workflow guidance."""
    return read_skill("geti-trainer")


@mcp.resource("geti-csam://skills/geti-source-reference")
def geti_source_reference() -> str:
    """Official upstream Geti source navigation and version-aware debugging guidance."""
    return read_skill("geti-source-reference")


@mcp.tool()
def get_setup_links() -> dict[str, str]:
    """Return the approved Geti access and application links."""
    return {
        "access_request": "http://goto/getiapply",
        "web_application": "http://goto/cdgeti",
    }


@mcp.tool()
def get_geti_source_links() -> dict[str, str]:
    """Return official upstream Geti sources for literature and debugging."""
    return {
        "repository": "https://github.com/open-edge-platform/geti",
        "development_branch": "https://github.com/open-edge-platform/geti/tree/develop",
        "releases": "https://github.com/open-edge-platform/geti/releases",
        "documentation": "https://docs.geti.intel.com/",
        "getitune_documentation": "https://docs.geti.intel.com/docs/user-guide/library/get-started/intro",
        "issues": "https://github.com/open-edge-platform/geti/issues",
        "discussions": "https://github.com/open-edge-platform/geti/discussions",
    }


@mcp.tool()
def get_run_readiness_check() -> list[str]:
    """Return the pre-run readiness checks for a Geti CSAM training run."""
    return [
        "Access confirmed",
        "Source TIFF preserved",
        "TIFF frames converted and output count verified",
        "Image quality and dimensions reviewed",
        "Dataset manifest created",
        "Labels approved",
        "Task type selected",
        "Annotations submitted and reviewed",
        "Split verified",
        "Project and model settings captured",
        "Storage and evidence folder selected",
        "Training impact understood and operator approval obtained",
    ]


@mcp.tool()
def diagnose_geti_issue(symptom: str) -> dict[str, str]:
    """Map a common Geti CSAM symptom to its first safe diagnostic check."""
    text = symptom.lower()
    if "boxes batch" in text or "no object" in text or "empty annotation" in text:
        return {
            "likely_cause": "An empty annotation reached validation or testing, especially on the legacy getitune path.",
            "first_check": "Inspect annotations and split membership for clean or unsubmitted images.",
            "known_workaround": "Use submitted defect annotations for the legacy path; verify Web behavior before formal clean-image scoring.",
        }
    if "missing" in text or "frame" in text or "tiff" in text:
        return {
            "likely_cause": "The multi-frame TIFF conversion or output selection may be incomplete.",
            "first_check": "Compare source frame count with generated files and open representative outputs.",
            "known_workaround": "Use TiffSplitter and prefer PNG for lossless training inputs.",
        }
    if "mask" in text or "prediction" in text or "inference" in text:
        return {
            "likely_cause": "Model/version, confidence threshold, input image, or generalization may be involved.",
            "first_check": "Confirm project, model version, export precision, input image, and confidence threshold.",
            "known_workaround": "Capture a representative prediction and compare it with the reviewed ground truth.",
        }
    return {
        "likely_cause": "The symptom needs more context before a reliable diagnosis.",
        "first_check": "Collect the exact error, project, task, model version, image count, split, and timestamp.",
        "known_workaround": "Review the CSAM Basics and Geti Setup Helper resources before rerunning a job.",
    }


@mcp.prompt()
def operator_onboarding() -> str:
    """Prompt for training a new operator on a complete Geti CSAM setup."""
    return """Act as the Geti CSAM Helper and train a new operator through a complete Web Geti setup. Use the CSAM Basics, Geti Setup Helper, Geti Trainer, and Geti Source Reference resources. Provide detailed numbered steps, visible button names, expected results, checkpoints, the RTC/readiness check, and required evidence. Ask for a screenshot when the UI or button name is uncertain. Do not start a long training run or alter data without explicit operator confirmation."""


@mcp.prompt()
def web_geti_training() -> str:
    """Prompt for detailed click-by-click Web Geti operator training."""
    return """Act as the Geti Trainer. Teach the operator the requested Web Geti workflow one safe step at a time. For every step provide Action, Expected result, and Checkpoint. Use exact visible button names only when known, ask for a screenshot when uncertain, and pause for confirmation before consequential actions such as submitting annotations, starting training, changing a split, exporting, or deleting data."""


@mcp.prompt()
def troubleshooting() -> str:
    """Prompt for a structured Geti CSAM troubleshooting response."""
    return """Act as the Geti CSAM Helper. Diagnose the operator's issue using this format: Assessment, Evidence, Next check, Fix, Verification, and Risk or limitation. Start with the smallest safe check, distinguish verified facts from hypotheses, and when local evidence is insufficient consult the official open-edge-platform/geti repository or matching release. State the upstream URL/version used and do not invent metrics or model results."""


if __name__ == "__main__":
    mcp.run(transport="stdio")
