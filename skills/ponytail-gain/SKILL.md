---
name: ponytail-gain
description: >
  Displays the published benchmark performance metrics and efficiency gains of the ponytail methodology.
  Use when the user requests "/ponytail-gain", "ponytail gain", "what does ponytail save", "show ponytail impact",
  or "ponytail scoreboard".
  Do NOT use to calculate simulated or dynamic metrics for the current repository.
---

# Ponytail Gain

Displays a standardized benchmark summary card showing empirical efficiency gains achieved by adopting the ponytail methodology across benchmark task suites.

## Scoreboard Output
Render the static benchmark card using plain ASCII bars:

```
  ponytail gain                     benchmark median · 5 tasks · 3 models

  Lines of code   no-skill  ████████████████████  100%
                  ponytail  ██▌·················    6–20%   ▼ 80–94%
  Cost            no-skill  ████████████████████  100%
                  ponytail  █████▌··············   23–53%  ▼ 47–77%
  Speed           ponytail  ▸ 3–6× faster

  This repo:  /ponytail-debt  (shortcuts you deferred)
              /ponytail-audit (what's still cuttable)
```

## Negative Constraints & Honesty Boundary
- ❌ **No Fabricated Local Metrics:** Never estimate or output "lines saved" or "cost saved" for the current unbuilt code in a user repo.
- ❌ **No Persistent State:** Display output only; do not create state files or alter user configuration.

## Verification & Grounding Loop
1. Verify that references to `/ponytail-debt` and `/ponytail-audit` remain accurate with current skill commands.
