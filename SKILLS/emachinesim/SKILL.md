---
name: emachinesim
description: Use when helping users work with eMachineSim as a Python-facing finite-element simulation tool, including Python API usage, input JSON authoring, thermal motor/BDF workflows, structural/modal/NVH workflows, electrostatic examples, output CSV/post-file interpretation, and user-facing documentation. Prefer existing sample files under Examples/electrostatic, Examples/thermal, and Examples/structural instead of embedding sample JSON inside the skill.
---

# eMachineSim

Use this skill for user-facing eMachineSim work. Treat `eMachineSim` as the public Python module and avoid presenting the command-line executable as the normal user interface unless the user explicitly asks about internal/debug workflows.

## Core Rules

- Prefer Python API usage with `import eMachineSim`.
- Do not duplicate full sample input JSON files inside this skill. Point to samples under `Examples/electrostatic`, `Examples/thermal`, or `Examples/structural`.
- Explain workflows in terms of analysis intent, input JSON sections, expected outputs, and diagnostic checks.
- Keep development-only details out of user-facing answers unless the user asks for implementation or validation work.
- When sample locations are uncertain, inspect the repository before giving exact paths.

## Workflow Selection

- For Python API usage, read `references/python-api.md`.
- For input JSON structure, read `references/input-json.md`.
- For thermal motor, BDF/QVOL, FEMH, volume heat sources, gap coupling, or cooling paths, read `references/thermal-motor-workflow.md`.
- For structural, modal, motor NVH, force mapping, or acoustic-radiation workflows, read `references/structural-nvh-workflow.md`.
- For electrostatic examples, read `references/electrostatic-workflow.md`.
- For output files, CSV diagnostics, and post files, read `references/outputs-and-diagnostics.md`.

## Response Style

When answering users:

1. Start with the intended workflow.
2. Name the relevant sample directory or JSON files.
3. Show the smallest useful Python snippet or JSON fragment.
4. List the output files to inspect.
5. State current limitations when they affect interpretation.
