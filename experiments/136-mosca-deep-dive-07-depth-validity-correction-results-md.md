> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/07-depth-validity-correction/results.md`.
> Original SHA-256: `362588727542544dcd7fabe68e9382169d40fbc71b42bf70e07c3f6c9945aa01`. Private media/logs are not included.

# Depth-validity correction results

Worker terminated and independently verified absent. Conservative cumulative estimateUS$3.6006 before tax; US$6.3994 remains of the acceptedUS$10 ceiling. All98 previous viewer records, including86 archived records, are unchanged.

| Case | Outcome | Source-fit median |
| --- | --- | ---: |
| guildhall-25s-large | FAILED_GEOMETRY_REVIEW | — |
| guildhall-outro | NOT_RUN | — |

Native render scores are fitted-source development evidence. Quality and GPU speed are not independently validated. Interior and outro remain separate shots; edited transition is source-only.

Stage outcomes, reviews, cost and closure (historical reference: `docs/execution-results.json`). Frozen inputs (historical reference: `docs/input-manifest.json`).

The correction reduced the median of frame-median background reprojection errors
from **68.54 px to 1.75 px** on the same cached priors. This is an observed-track
alignment diagnostic, not a photorealism or novel-view score.

| Diagnostic | Corrected result | Frozen gate |
| --- | ---: | ---: |
| Overall median | 1.75 px | ≤5 px |
| Five successive time-bin medians | 1.71 / 1.43 / 1.37 / 9.40 / 51.88 px | Each ≤8 px |
| Worst frame median | 175.82 px | ≤20 px |
| Shared source8–11s | 1.40 px | ≤5 px |
| Turn region source14–18s | 3.84 px | ≤8 px |

The final two bins and worst frame failed. Six source/track overlays include
0,12.67,15,16,17 and25.33s; the final view has substantial projection mismatch.
Manual review therefore rejected geometry. Appearance training, export and the
separate outro were not started. The app shows both failed full-interior trials
as diagnostic cards without a model action; its98 existing models are unchanged.

All40 recorded support checks passed. Retained sampled comparisons rose from
97.71% to99.97%; positive input-depth support remained100%. Thus improvement was
not achieved by discarding most comparisons. The final logged depth loss was
0.00788, but low aggregate loss did not establish correct late geometry.

Six CPU correction regressions and the native CUDA forward/backward check passed.
All2,682 retrieved stable files passed strict collection, with zero pending files.
Session estimate US$0.4683; cumulative US$3.6006 before tax; US$6.3994 remains.
The worker was terminated and an independent query found zero account Pods.

Numeric and support evaluation (historical reference: `docs/guildhall-25s-large-geometry-evaluation.json`),
manual rejection (historical reference: `docs/review-decisions.json`), lessons (historical reference: `lessons.md`),
next steps (historical reference: `next-steps.md`).
