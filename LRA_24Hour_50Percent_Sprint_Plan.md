# Living Repository Agent (LRA)
## 24-Hour / 50% Sprint Plan
### Minimum Viable Demonstration — Exact Ordered Steps
**Version 1.0 | 18 October 2026**

This document is the only plan you need for the next 24 hours.  
Goal: Deliver a working 50% core of the Living Repository Agent that can be demonstrated live.

Do not add extra features. Follow the order. Check off each step.

---

## Definition of 50% (What Success Looks Like)

By the end of this sprint you will have:

- A public GitHub repository with the correct structure
- A working finite-state machine
- A hard human approval gate that actually blocks progress
- One complete cycle: Research → Synthesize → Propose → AwaitApproval → Stage
- Real, inspectable files that appear only after approval
- A clean README that honestly states what is included and what is still missing

This is enough to stand in front of people and prove the architecture is real.

---

## Exact Time Allocation (Recommended)

- Hours 0–2:   Repository + structure + SOUL.md
- Hours 2–6:   State machine + first workflow + approval gate
- Hours 6–12:  Research + Synthesize + Propose skills
- Hours 12–16: Make one full cycle run end-to-end
- Hours 16–20: Clean up, write README, test demonstration sequence
- Hours 20–22: Final verification and push
- Hours 22–24: Buffer / rest / prepare how you will present it

---

## Step-by-Step Instructions (Do in Exact Order)

### Step 1 — Create the Repository (0–30 min)

1. Go to GitHub → New repository
2. Name it: `living-repository-agent` (or similar)
3. Make it **Public**
4. Add a README
5. Clone it to your laptop
6. Open the folder in your editor

### Step 2 — Create the Full Directory Structure (30–60 min)

Create these folders and files exactly:

```
SOUL.md
HARNESS/
  planner.md
  research_policy.md
  synthesis_policy.md
  tool_registry.md
  evolution_rules.md
  version.json
GRAPH/
  nodes/
  edges/
  index.json
MISSIONS/
SKILLS/
WORKFLOWS/
APPROVALS/
README.md
```

Commit: `Phase 0: Create directory structure`

### Step 3 — Write SOUL.md (60–90 min)

Write a clear SOUL.md that contains:

- Short mission statement
- Hard rules:
  - No real-world side effects without human approval
  - Free compute only
  - Model is interchangeable
  - Approval is mandatory at Propose → Stage transition
- Simple approval rule: “Workflow must stop at AwaitApproval until a human adds the label `approved` or posts the comment `APPROVED`”

Commit: `Add SOUL.md with hard constraints`

### Step 4 — Create First Mission Folder (90–120 min)

Create:

```
MISSIONS/001-first-demo/
  state.json
  findings/
  proposals/
  artifacts/
  log.md
```

Put this inside `state.json`:

```json
{
  "mission_id": "001-first-demo",
  "state": "Init",
  "created": "2026-10-18",
  "title": "First demonstration mission"
}
```

Commit: `Create first mission folder and state.json`

### Step 5 — Create the Core Workflow (2–4 hours)

Create file: `WORKFLOWS/mission-runner.yml`

The workflow must:

1. Read the current state from `MISSIONS/001-first-demo/state.json`
2. If state is `Init` → move to `Research`
3. If state is `Research` → run research skill (or placeholder) and move to `Synthesize`
4. If state is `Synthesize` → create a simple proposal and move to `Propose`
5. If state is `Propose` → move to `AwaitApproval` and open/update a GitHub Issue
6. If state is `AwaitApproval` → **STOP**. Do nothing else until a human adds label `approved` or comments `APPROVED`
7. Only after approval → move to `Stage` and create files inside `artifacts/`

Keep the workflow simple. It is better to have a working gate than a fancy but broken workflow.

Commit early and often while building this.

### Step 6 — Write the Three Core Skills (4–7 hours)

Create these three files in `SKILLS/`:

**research.md**  
Instructions for gathering information and writing findings into `MISSIONS/001-first-demo/findings/`.

**synthesize.md**  
Instructions for reading findings and producing a structured summary.

**propose.md**  
Instructions for turning the synthesis into a clear proposal file inside `proposals/`.

Even if the research is partially manual or uses simple free tools at this stage, the files and the flow must exist.

### Step 7 — Make One Full Cycle Work (7–12 hours)

This is the most important part.

1. Set state to `Init`
2. Trigger the workflow
3. Confirm it moves through Research → Synthesize → Propose → AwaitApproval
4. Confirm it stops and opens an issue
5. Manually add the label `approved` (or the comment)
6. Re-trigger or let the workflow continue
7. Confirm it moves to `Stage` and creates files in `artifacts/`

Do not stop until this complete loop works at least once.

### Step 8 — Add Minimal Knowledge Graph Support (12–15 hours)

Even a simple version is enough for 50%:

1. When research runs, also write 2–3 simple node files into `GRAPH/nodes/`
2. Write 1–2 simple edge files into `GRAPH/edges/`
3. Update `GRAPH/index.json` with a basic list

This proves the graph concept without requiring a full database.

### Step 9 — Clean README and Final Polish (15–18 hours)

Update `README.md` so it clearly says:

- What this repository is
- What the 50% demo currently does
- What is still missing (full harness evolution, edge Wasm, etc.)
- How to run the demonstration (exact steps a stranger can follow)
- Link to the Master File

### Step 10 — Final Verification (18–22 hours)

Run this checklist:

- [ ] Repository is public
- [ ] Directory structure is correct
- [ ] SOUL.md exists and contains hard rules
- [ ] state.json can move through the states
- [ ] Workflow stops at AwaitApproval
- [ ] Adding approval label allows it to continue
- [ ] Artifacts only appear after approval
- [ ] At least some graph files exist
- [ ] README is honest and clear
- [ ] You can demonstrate the full loop in under 5 minutes

If any item fails, fix it before stopping.

---

## First Mission Topic (Recommended)

**Title:** Compare free WebAssembly and edge runtimes suitable for AI agents (2026)

This topic is narrow, technical, and produces a useful proposal. It also matches the architecture you are building.

---

## What to Say When You Demonstrate

“This is a live 50% implementation of the Living Repository Agent.  
The repository is the mind.  
The workflow is the nervous system.  
The approval gate is real — the system stops until a human approves.  
After approval it stages the artifacts.  
The remaining 50% (full knowledge graph maturity, automatic harness evolution, edge workers) is already designed and will be completed next.”

---

## Rules for the Sprint

- Do not add new features that are not in this list
- Commit after every meaningful change
- If something is taking too long, simplify it rather than perfect it
- The approval gate must work. Everything else can be simplified
- Keep the Master File and this Sprint Plan in the repository

---

**End of 24-Hour / 50% Sprint Plan**

You now have everything required to execute.  
Start with Step 1.
