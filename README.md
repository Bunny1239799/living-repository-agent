# Living Repository Agent (LRA)

The Living Repository Agent (LRA) is a repository-centered mission workflow.
It uses version-controlled files, GitHub Actions, research and synthesis
outputs, and a human approval gate to control when a mission may be staged.

## Current 50% demonstration

The current implementation includes:

- A constitutional rules file in `SOUL.md`.
- Harness policies and a version file in `HARNESS/`.
- A small, inspectable JSON knowledge graph in `GRAPH/`.
- Research, synthesis, and proposal instructions in `SKILLS/`.
- A first demonstration mission in `MISSIONS/001-first-demo/`.
- A research-engine mission in `MISSIONS/002-research-engine/`.
- GitHub Actions workflows under `.github/workflows/`.
- A research script and tests under `tools/` and `tests/`.

Mission 001 is recorded in state `Stage` and has a stage record.
Mission 002 has produced research, synthesis, and a proposal and is currently
in `AwaitApproval`. Mission 002 must remain there until an authorized human
approval is accepted by the workflow.

## Run the Mission 002 demonstration

1. Open the repository's **Actions** tab on GitHub.
2. Select **LRA Research Mission Runner**.
3. Use **Run workflow** if the workflow offers that action.
4. Open the completed run and inspect the research, synthesis, proposal,
   and Mission 002 state file.
5. Open the issue linked to the mission proposal and review the evidence
   before deciding whether to approve.
6. Only if you independently approve the proposal, use the repository's
   configured approval mechanism: apply the `approved` label or post the
   exact comment `APPROVED`.
7. Inspect the resulting Actions run and repository history. Confirm that
   staging occurred only after the approval-verification job accepted the
   approval.

Do not approve a mission merely to make the demonstration pass. If you do not
approve it, leaving it at `AwaitApproval` is the correct safe outcome.

Repository:
https://github.com/Bunny1239799/living-repository-agent

## Safety and operating boundaries

- Staging requires an accepted human approval.
- Research and synthesis outputs require human review; source retrieval alone
  does not prove that every claim is true.
- The research-engine output is a bounded, extractive pipeline, not an
  independent fact-checking system.
- Do not treat a successful workflow run as proof that every acceptance
  criterion has passed. Inspect the state, artifacts, logs, and approval path.

## Known gaps — 50% is not 100%

- The knowledge graph is minimal and is not yet a mature queryable memory
  system.
- Full harness-evolution proposals and their human-reviewed merge cycle have
  not been demonstrated here.
- Optional edge/WebAssembly and browser-native substrates are not implemented
  as completed capabilities.
- Repeated multi-mission reliability and production recovery still require
  verification.
- The full under-five-minute demonstration and all ten sprint acceptance
  criteria must be checked against actual runs.

## Governing documentation

The authoritative Master Architecture File and the two governing documents
must be available and linked from this repository before documentation
acceptance is considered complete:

- `LRA_24Hour_50Percent_Sprint_Plan.md`
- `LRA_Complete_Implementation_Guide.md`

These files are not currently present at the repository root in the inspected
checkout. Do not substitute this README for those source documents.

## Repository layout

- `SOUL.md` — core mission and hard constraints.
- `HARNESS/` — planner, policies, tool registry, evolution rules, and version.
- `GRAPH/` — graph nodes, edges, and index.
- `MISSIONS/` — mission states, findings, proposals, logs, and artifacts.
- `SKILLS/` — research, synthesis, and proposal instructions.
- `.github/workflows/` — executable GitHub Actions workflows.
- `tools/` and `tests/` — research implementation and automated tests.

The executable GitHub Actions workflows live in `.github/workflows/`, where
GitHub discovers them. The planned `WORKFLOWS/` directory is currently empty;
do not mistake that empty directory for a runnable workflow.

