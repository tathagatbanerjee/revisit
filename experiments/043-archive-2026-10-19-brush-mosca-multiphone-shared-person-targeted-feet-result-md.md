> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/targeted-feet-result.md`.
> Original SHA-256: `64e118c9f5ccdf46079274c650cb0210aa9466674ef758f6bb5c32818163396d`. Private media/logs are not included.

# Native detail audit and targeted shoe check — 19 October 2026

**Full-person readiness still fails.** The native images do not give us reliable
manual point identities on both shoes or either hand. One additional cached
MASt3R21/02 pair supplies three calibrated pair matches but no unambiguous
three-view tracks. Neither shoe acquires validated interior support. No initializer
or Gaussian model was exported, and no acceptance tolerance changed.

## Source-only audit

Inspecting unmarked1920x1080 shoe and hand crops before projecting saved points
confirms visibility, but not reliable point correspondence. Black shoe uppers
have little resolvable texture; visible sole extrema change with viewpoint.
Overlapping fingers and the small watch do not provide a confidently identical
resolved detail in every relevant image. Camera02 occludes the watch-side hand;
camera24 crops both feet. This is an identifiability limitation in this audit,
not proof that no useful feature exists anywhere in the originals.

The audit receipt (historical reference: `landmark-audit.json`) records zero reliable manual tracks,
empty point observations and no numerical manual point score. Coordinates or
uncertainty values were not invented. Existing coarse semantic centers cannot be
used as ground truth. The investigation (historical reference: `landmark-investigation.md`) predates
inspection; native crops and source hashes are retained privately.

## Fixed targeted pair

The separate investigation (historical reference: `targeted-feet-investigation.md`) and
plan (historical reference: `targeted-feet-plan.json`) fixed exactly one21/02 pair before launch.
Conservative polygons were independently inspected inside the uppers of each
shoe in21/13/02, excluding floor, sole-contact boundaries, ankles and trousers.
They label anatomy membership only; they are not homologous point observations.
The source-review receipt (historical reference: `targeted-feet-source-review.json`) predates inference.

| Fixed stage | Matches |
| --- | ---: |
| Raw reciprocal21/02 pairs |1,371 |
| Network border check |1,193 |
| Both foreground masks; finite confidence |65 |
| Descriptor dot>=0.8 |9 |
| Calibrated epipolar/depth/reprojection/ray-angle checks |3 |
| Unambiguous join with saved21/13 |0 |
| Validated interior support, each shoe |0 |

No descriptor-confidence cutoff was imposed. The failure is not the original
>=1.5 cutoff alone. Of the three geometric matches, two fall near a shoe and
within0.75px640 of old eligible anchors; their similarly near alternatives fail
the predeclared unambiguous join rule. The third nearest distance is1.91px.
Do not turn zero joined tracks into a claim that every pair match is false, or
relax the ratio/radius after observing this result. Three sparse pair matches
also cannot establish complete shoes. See stage diagnostic (historical reference: `targeted-feet-stage-diagnostic.json`).

Full-source and magnified shoe-interior panels were inspected. They correctly
show no accepted three-view points, with both actual source shoes retained.
The shoe consistency signal and full-person visual gate fail. Camera20 remains
sealed; all images in this check are already-seen training data. Manual13 and
automatic conservative masks in other views remain different, as before.

## Verification and resources

Thirteen focused geometry/membership tests pass. Exact coordinate replay
reproduces pair geometry, joins, third-camera checks and shoe membership without
new neural inference. Crop tensor parity, source/model/input/calibration hashes,
old293-bin candidate, previous three-view artifacts and fixed room/person controls
verify unchanged. See report (historical reference: `targeted-feet-report.json`),
verification (historical reference: `targeted-feet-verification.json`) and visual review (historical reference: `targeted-feet-visual-review.json`).

One local two-thread CPU run took147.34s; forward8.03s. Worker peak3,187.59MiB,
parent-sampled peak2,831.28MiB, below5GiB/900s. Initial available RAM8.83GiB.
No GPU, cloud resource, installation, download or paid compute. Results and
private crop images remain in ignored working storage; no worker is left running.

## Decision and next step

Stop unchanged full-person MASt3R pairs against02:13/02 and21/02 now both fail
useful foot-track support. Preserve their raw data and the promising21/13/24
upper-body tracks. Joint observed-person initialization and fitting remain gated;
this does not advance to coherent motion or the structural-prior comparison.

The next bounded investigation should test a **foot-specific native crop**
strategy with the cached model and fixed cameras. First inspect the exact source
and model crop mapping, retaining both shoes and sufficient context, and state
which native detail the whole-person resize loses. Upsampling cannot create
missing source texture. Fix one crop rule and a small pair/track test before any
inference; retain the same anatomical and three-view checks. Do not simply try
another unchanged pair or sweep thresholds. If the native evidence cannot
support this route, record that limitation and present a change of initialization
strategy, including the explicit distinction between observed and inferred body
surfaces, before attempting a fit. No further model run follows this result.
