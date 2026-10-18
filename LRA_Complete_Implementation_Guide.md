# Living Repository Agent (LRA)
## Complete Implementation Guide — 100% System
### Step-by-Step Professional Build Instructions
**Version 1.0 | Companion to Master File | 18 October 2026**

This document is the full, ordered implementation guide for building the complete Living Repository Agent as defined in the Master Architecture File.  
Follow the phases strictly. Do not skip ahead. Each phase builds on the previous one.

---

## Prerequisites

- GitHub account
- Git installed and configured on your machine
- Basic familiarity with Git, Markdown, and GitHub Actions
- A modern browser
- Optional but recommended: VS Code or similar editor
- No powerful GPU required
- No paid API required for the core system

---

## Phase 0 — Foundation (Day 1)

### Goal
Create the repository skeleton and the constitutional foundation.

### Exact Steps

1. Create a new public GitHub repository named `living-repository-agent` (or your preferred name).
2. Clone the repository to your local machine.
3. Create the exact directory structure:

```
/
├── SOUL.md
├── HARNESS/
│   ├── planner.md
│   ├── research_policy.md
│   ├── synthesis_policy.md
│   ├── tool_registry.md
│   ├── evolution_rules.md
│   └── version.json
├── GRAPH/
│   ├── nodes/
│   ├── edges/
│   └── index.json
├── MISSIONS/
├── SKILLS/
├── WORKFLOWS/
├── APPROVALS/
└── README.md
```

4. Write `SOUL.md` containing:
   - Mission statement
   - Hard constraints (no autonomous real-world side effects, human approval required, free compute only, etc.)
   - Approval rules
   - Model interchangeability policy

5. Create initial empty or placeholder files in `HARNESS/` with clear headers.
6. Initialize `GRAPH/index.json` as an empty object `{}`.
7. Write a clear `README.md` that explains the purpose of the repository and points to the Master File.
8. Commit and push with message: `Phase 0: Foundation structure and SOUL.md`.

### Exit Criteria
- Repository is public
- Directory structure matches the Master File exactly
- `SOUL.md` is complete and committed

---

## Phase 1 — Minimal Viable Loop (Days 2–4)

### Goal
Make one complete mission cycle run with a hard human approval gate.

### Exact Steps

1. Create the first mission folder: `MISSIONS/001-demo/`.
2. Inside it create:
   - `state.json` (start with `"state": "Init"`)
   - `findings/`
   - `proposals/`
   - `artifacts/`
   - `log.md`

3. Define the finite-state machine values that will be used:
   - Init
   - Research
   - Synthesize
   - Propose
   - AwaitApproval
   - Stage
   - Verify
   - Complete
   - Refine

4. Create the first GitHub Actions workflow in `WORKFLOWS/mission-runner.yml` that:
   - Reads `state.json`
   - Can advance the state
   - Stops completely when state is `AwaitApproval`
   - Only continues after a human label or comment is detected

5. Write three core skills in `SKILLS/`:
   - `research.md`
   - `synthesize.md`
   - `propose.md`

6. Implement a simple research step that writes findings into `MISSIONS/001-demo/findings/`.
7. Implement a synthesis step that reads findings and writes a structured proposal into `proposals/`.
8. Make the workflow open or update a GitHub Issue when entering `AwaitApproval`.
9. Test the full cycle manually: trigger workflow → reach AwaitApproval → add approval label → continue to Stage → verify artifacts appear.

### Exit Criteria
- One complete mission can be run from Init to Stage
- The approval gate is real and cannot be bypassed by the agent
- Artifacts only appear after human approval

---

## Phase 2 — Knowledge Graph & Memory (Days 5–7)

### Goal
Replace raw text dumps with a structured, queryable knowledge graph.

### Exact Steps

1. Define node schema (example fields: id, type, content, source, confidence, created, mission_id).
2. Define edge schema (example fields: from, to, relation, confidence, provenance).
3. Update the Research skill so that it only writes verified nodes and edges into `GRAPH/nodes/` and `GRAPH/edges/`.
4. Update `GRAPH/index.json` (or a simple script) so nodes and edges can be listed and queried.
5. Update the Synthesize skill so it reads from the graph instead of only from raw findings.
6. Add provenance tracking (which mission and which source produced each node/edge).
7. Test by running a second mission and confirming the graph grows correctly.

### Exit Criteria
- Research writes structured graph data
- Synthesis can query the graph
- Graph files are committed and inspectable

---

## Phase 3 — Harness Evolution (Days 8–10)

### Goal
Enable the system to propose improvements to its own control logic.

### Exact Steps

1. Write `HARNESS/evolution_rules.md` defining when and how the agent may propose changes.
2. Create an evolution skill that:
   - Reads the mission log and current harness files
   - Proposes concrete, diffable patches to one or more files under `HARNESS/`
   - Opens a pull request with clear rationale
3. Enforce that no harness change is merged automatically — human review is mandatory.
4. Run at least two missions and deliberately generate one harness improvement proposal.
5. Manually review and merge a good proposal, then confirm the new harness is used in the next mission.

### Exit Criteria
- Agent can propose harness patches
- Human merge is required
- Merged changes affect future behavior

---

## Phase 4 — Edge & Browser Substrates (Days 11–14)

### Goal
Add optional free compute substrates beyond GitHub Actions.

### Exact Steps

1. (Optional) Create a simple Cloudflare Worker or equivalent edge Wasm function for parallel research tasks.
2. Make the worker write results back into the repository (via API or by creating a PR).
3. Create a minimal browser-native view (HTML + Pyodide) that can read mission state and display proposals for offline inspection.
4. Document how to trigger edge workers and how to open the browser view.
5. Ensure all new components still respect the same approval gates and repository-as-source-of-truth rule.

### Exit Criteria
- At least one additional compute substrate is usable
- All paths still write to the central repository
- Approval gates remain enforced

---

## Phase 5 — Hardening & Production Readiness (Days 15+)

### Goal
Make the system robust, auditable, and ready for repeated real use.

### Exact Steps

1. Add verification sandboxes (simple test runners inside the workflow or Wasm).
2. Improve logging so every state transition and decision is written to `log.md` and to Git history.
3. Add clear error handling and recovery paths (e.g., what happens if research fails).
4. Write comprehensive operator documentation inside the repository.
5. Create a second and third real mission to prove the system works across different topics.
6. Review and tighten `SOUL.md` constraints based on lessons learned.
7. Tag a release (v1.0) once the system reliably completes full cycles with human approval.

### Exit Criteria
- Multiple missions can be run successfully
- System is auditable through ordinary Git tools
- Documentation is sufficient for a new operator to use it
- All Master File requirements are satisfied

---

## Final Verification Checklist (100% Complete)

- [ ] Repository structure matches Master File exactly
- [ ] SOUL.md contains hard constraints and approval rules
- [ ] Finite-state machine works and cannot skip AwaitApproval
- [ ] Research writes to knowledge graph
- [ ] Synthesis reads from knowledge graph
- [ ] Proposals are generated and staged only after approval
- [ ] Harness evolution can propose patches
- [ ] Human merge is required for harness changes
- [ ] At least one additional compute substrate is optional but functional
- [ ] Multiple missions have been completed successfully
- [ ] Full audit trail exists in Git history
- [ ] README and operator instructions are clear

When every item above is checked, the Living Repository Agent is complete according to the Master Architecture.

---

**End of Complete Implementation Guide**
