> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/10-static-anchor-refinement/results.md`.
> Original SHA-256: `8210cfa6e108c229523a34ed41272b057877475d1205b401b5d65d40c1b1b379`. Private media/logs are not included.

# Results and verified closure

**The full-interior background geometry/coverage checkpoint now passes.** Replacing
the original static BA observations with observed map-feature tracks resolves the
late anchor deficit while preserving the qualified cameras. Both predeclared
depth-refinement arms pass every unchanged numeric gate and sampled visual review.
This is not a full-length appearance or dynamic splat result.

| Setting | Median of frame medians | Worst-frame median | Minimum usable anchors | Result |
| --- | ---: | ---: | ---: | --- |
| Previous locked cameras,494 original tracks | 1.498px | 5.281px | 58 | Coverage failed |
| Observed map tracks, unchanged depth, CPU replay | 1.297px | 2.285px | 288 | CPU preflight passes |
| Same observed tracks, scale-only refinement | 0.969px | 1.584px | 288 | Native geometry review passes |
| Same observed tracks, full refinement | 0.764px | 1.060px | 288 | Native geometry review passes |

All new rows use the exact same4,000 observed point identities,305 source RGB/depth
observations and frozen camera package. Table medians use NumPy midpoint medians,
matching native inspection. The CPU preflight separately records Torch lower
medians. The earlier494-track row differs in both observation method and density.

Both native runs leave every camera state tensor exactly unchanged and all camera
parameters frozen. All40 sampled support records pass in each arm. Initialization
camera matrices, calibration, tracks, visibility, depths and world points are
bit-identical between arms. Sampled target-frame schedules match, and losses are
exactly equal before per-observation correction activates. CPU/native sampled
depth differences are at most2.39e-7.

Native stage times, including static reconstruction and inspection, are216.234s
for full refinement and214.292s for scale-only. Disabling per-observation correction
does not materially speed this implementation: most projection work remains.
Those times exclude environment setup/transfer and are not comparable to the
older494-track fit as a hardware benchmark.

An additional fitted-map diagnostic compares depths at324,597 actual selected
observations with their frozen map points. Median absolute relative differences
are6.94% without refinement,2.55% with scale-only and0.54% with full refinement.
Full refinement also has the lowest projection medians in every time bin. It is
the **provisional geometry choice for the next appearance test**. These map points
also define the camera map and candidate tracks; this is supporting consistency
evidence, not independent depth ground truth or full quality promotion.

## What the diagnosis establishes

Of20 rejected final-frame anchors in the previous run,18 have late observations
inconsistent with their dominant static-ray consensus even without Metric3D depth.
All58 accepted final-frame anchors pass that diagnostic. The fixed map alone
therefore could not repair all long-span identity/visibility inconsistencies.
Real static feature observations connect the room without requiring one tracker
identity to survive the entire turn. Some depth refinement remains useful once
the observations are consistent.

An exploratory CPU bank of494 observed-map tracks still retains at least142
usable anchors with2.265px worst-frame median. Smaller background banks could
reduce future BA cost, but no native smaller-bank result is claimed here.

## Artifacts, resources and limits

Execution and closure (historical reference: `docs/execution-results.json`), paired input proof (historical reference: `docs/paired-input-verification.json`),
unchanged-depth control (historical reference: `docs/unchanged-depth-evaluation.json`),
full-depth evaluation (historical reference: `docs/guildhall-anchors-full-depth-geometry-evaluation.json`),
scale-only evaluation (historical reference: `docs/guildhall-anchors-scale-only-geometry-evaluation.json`),
map-depth consistency (historical reference: `docs/map-depth-agreement.json`).

Strict collection verified2,460 stable files with zero pending. The L40S worker was
terminated and independently verified absent; account Pods are zero. No persistent
or network volume was created. Session estimateUS$0.3884; cumulativeUS$4.7246 before
tax, remainingUS$5.2754 of the acceptedUS$10 ceiling. Estimates include setup,
transfer, fitting, retrieval and ephemeral storage; they are not invoices.

No scaffold, photometric warmup, appearance fit, Brush fit, outro or model export
ran under this geometry-only manifest. All98 existing viewer records, including86
archived records, are identical to the pre-run baseline. The12s result is still
the longest published interactive dynamic model. Camera20 remains sealed.

The app presents the settings comparison, source-time error/coverage chart and
actual observed-feature/projection overlays at
http://localhost:4319/#static-anchor-refinement. The card has no model action.
Heavy arrays, native checkpoints, media and worker retrievals remain in ignored
working/preview directories; small protocols and reports are durable here.

See next steps (historical reference: `next-steps.md`) and lessons (historical reference: `lessons.md`).
