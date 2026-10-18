# Harness Evolution Rules

## Purpose
Improve LRA without compromising safety or reproducibility.

## Rules
1. Identify the concrete limitation that motivates a proposed change.
2. Record the expected benefit, risks, and verification criteria.
3. Keep changes narrow and reviewable.
4. Test changes before claiming they work.
5. Require human review before adopting consequential harness changes.
6. Preserve a recoverable history of accepted changes.
7. Never allow the agent to weaken or bypass its own approval gate.
8. Do not claim self-improvement from a proposal alone.

## Fail-Closed Behavior
If a change could bypass approval, expose secrets, or expand permissions unexpectedly,
stop and require human review.
