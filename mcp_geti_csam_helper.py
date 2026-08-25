"""Local MCP server for the shareable Geti CSAM Helper agent."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP


ROOT = Path(__file__).resolve().parent
SKILLS = {
    "csam-basics": ROOT / ".github" / "skills" / "csam-basics" / "SKILL.md",
    "geti-setup-helper": ROOT / ".github" / "skills" / "geti-setup-helper" / "SKILL.md",
}

mcp = FastMCP("Geti CSAM Helper")


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


@mcp.tool()
def get_setup_links() -> dict[str, str]:
    """Return the approved Geti access and application links."""
    return {
        "access_request": "http://goto/getiapply",
        "web_application": "http://goto/cdgeti",
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
    return """Act as the Geti CSAM Helper and train a new operator through a complete Web Geti setup. Use the CSAM Basics and Geti Setup Helper resources. Provide numbered steps, expected results, the RTC/readiness check, and the evidence that must be saved. Do not start a long training run or alter data without explicit operator confirmation."""


@mcp.prompt()
def troubleshooting() -> str:
    """Prompt for a structured Geti CSAM troubleshooting response."""
    return """Act as the Geti CSAM Helper. Diagnose the operator's issue using this format: Assessment, Evidence, Next check, Fix, Verification, and Risk or limitation. Start with the smallest safe check, distinguish verified facts from hypotheses, and do not invent metrics or model results."""


if __name__ == "__main__":
    mcp.run(transport="stdio")
