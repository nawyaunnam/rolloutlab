# Engineering notes: RolloutLab — deterministic feature rollouts

## Problem and flow

Versioned flag configuration → validated rules → explicit deny/allow overrides → attribute checks → SHA-256 bucket → decision with reason and version. Stable hashing avoids randomized Python hash values and preserves cohort membership as rollout percentages grow.

## Current boundaries

Library and CLI demo, not a hosted feature-flag platform. No user tracking, remote configuration delivery, or statistical causal inference. Store pseudonymous subject IDs in a real integration and design experiment analysis separately.

## Interview walkthrough

1. Run the demo and explain each output in terms of the code.
2. Show a test that exercises a failure rather than only a successful call.
3. Trace one input through the core implementation and its stored state.
4. Explain the tradeoff made by the current storage or algorithm choice.
5. Describe what would change with 100× the data or concurrent users.
6. Make a small extension and add a regression test before using this in a resume.

## Validation

See `test_engine.py` for executable assertions and `docs/demo-output.txt` for
captured results. CI is configured but remote CI results are not assumed.
