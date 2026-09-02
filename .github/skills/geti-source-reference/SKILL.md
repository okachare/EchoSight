---
name: geti-source-reference
description: "Use the official open-edge-platform/geti GitHub repository for Geti literature, source-code understanding, version-aware debugging, getitune training behavior, application behavior, and upstream issue investigation."
---

# Geti Source Reference

Use the official upstream repository as a technical reference when local project notes or UI evidence do not explain Geti behavior.

## Canonical sources

- Repository: https://github.com/open-edge-platform/geti
- Active development branch: `develop`
- Releases: https://github.com/open-edge-platform/geti/releases
- User documentation: https://docs.geti.intel.com/
- Geti library documentation: https://docs.geti.intel.com/docs/user-guide/library/get-started/intro
- Upstream issues: https://github.com/open-edge-platform/geti/issues
- Upstream discussions: https://github.com/open-edge-platform/geti/discussions

The repository is Apache-2.0 licensed. Do not copy large source sections into project documentation. Link to the upstream file, release, issue, or documentation page and summarize only the relevant behavior.

## Source map

| Question | Upstream area |
|---|---|
| How is the end-to-end product assembled? | `application/` and the root `README.md` |
| How does Python training, testing, export, or optimization work? | `library/` and `library/src/getitune/` |
| Which recipes/models exist for a task? | `library/src/getitune/recipe/` |
| How are backend jobs, projects, datasets, or APIs implemented? | `application/backend/` |
| How does the Web UI expose a workflow? | `application/ui/` |
| What does Geti recommend operators do? | `skills/`, `.agents/skills/`, and `application/docs/` |
| Is behavior release-specific? | Git tags/releases and file history for the affected path |

## Literature and evidence workflow

1. Start with the upstream README and official documentation for the concept.
2. Follow the source map to the implementation or first-party skill that explains it.
3. Record the URL, branch or release, commit if available, and access date in project notes.
4. Separate upstream design or documented behavior from this project's observed Geti Web/Windows evidence.
5. Prefer a short summary and a link over reproducing upstream code.

Do not treat the moving `develop` branch as proof of behavior in an installed release. Prefer the matching release tag when diagnosing a deployed version.

## Source-first debugging workflow

1. Capture the exact error, task, model/recipe, Geti version, platform, dataset format, split, and job timestamp.
2. Identify whether the symptom belongs to the application, `getitune`, a recipe, Datumaro/data handling, OpenVINO export, or the host environment.
3. Search the matching upstream release and affected path for the exact exception or component name.
4. Compare the installed version with the upstream fix or issue timeline before recommending an upgrade, downgrade, or rerun.
5. Reproduce with the smallest safe dataset or a documented upstream example when practical.
6. Preserve the local log and record the upstream URL, version, and conclusion in `Debug/`.

For the known `ValueError: Boxes batch must have 4 coordinates` symptom, retain the local finding that empty annotations affected the legacy path. Use upstream source and issue history to determine whether the installed version has changed; never claim that a current Web release has the same defect without matching evidence.

## Getitune API orientation

The upstream README currently demonstrates `create_engine`, `list_models`, `engine.train`, `engine.test`, `engine.export`, `engine.optimize`, and `engine.predict`. Treat README snippets as orientation, then confirm signatures and supported recipes in the matching installed package and documentation before giving executable advice.

## Response requirements

- Cite the upstream URL or repository path for claims based on Geti source.
- State the branch or release used, especially when reading `develop`.
- Label conclusions as documented, source-confirmed, locally observed, reproduced, or hypothesized.
- Keep Intel/private access links and project data separate from public upstream references.
- Do not upload CSAM images, private logs, credentials, or proprietary annotations to upstream issues or public discussions.
