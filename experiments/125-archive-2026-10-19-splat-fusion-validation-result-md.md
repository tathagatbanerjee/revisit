> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/result.md`.
> Original SHA-256: `684a63b48e7de260c4e4d63d52cd080eff4387fe57848abcd5e11374402defa7`. Private media/logs are not included.

# Sequential fusion validation results — 19 October 2026

All eight numbered stages were executed in order, plus one separately scoped
local geometry trial within05. **The end-to-end pipeline is not validated.**
Known-answer controls work, but consolidation/refinement gains are too small,
and independent moving-person geometry remains incompatible.

| Stage | Executed result | Scope |
| --- | --- | --- |
| 01 Export/transforms (historical reference: `01-export-transforms/result.md`) | Pass: rotation error3.0e-7deg, relative scale error3.7e-9, max render difference1.45e-5 | Two fragments of one saved splat; intrinsic matching, not point-ID fitting |
| 02 Independent registration (historical reference: `02-independent-registration/result.md`) | Room gate passes:59.84→8.10px,0.0737m-equivalent on six reserved identities | Two actual independent fits; reused seen calibration-assisted landmarks |
| 03 Persistence/change (historical reference: `03-persistence-and-change/result.md`) | Injected control passes:97.8% macro precision,99.94% macro recall, zero occluded patches falsely removed | Synthetic changes; real changed-room recapture remains unvalidated |
| 04 Consolidation (historical reference: `04-overlap-consolidation/result.md`) | Exact-duplicate control passes; real gate fails:641 B duplicates removed,0.21% reserved MAE gain | Source-image checkerboard development split;2% gain required |
| 05 Refinement (historical reference: `05-fusion-refinement/result.md`) | Both fail: colour correction worsens reserved MAE0.65%; local XYZ improves0.36%, below2% gate | Separate fixed colour and512-Gaussian geometry trials; A remains fixed |
| 06 Time alignment (historical reference: `06-time-alignment/result.md`) | Exact and cross-view tests pass after clock conversion correction: correct six-frame shift, effectively zero offset error,12.89% ambiguity margin | One short seen event; actual local PTS, no audio/drift validation |
| 07 Dynamic fusion (historical reference: `07-dynamic-fusion/result.md`) | Fails: person reprojection24.69→219.82px; two people in three rendered motion states | Known source clocks isolate geometry failure; no successful actor fusion |
| 08 Incremental uploads (historical reference: `08-incremental-uploads/result.md`) | Bookkeeping control passes:100% known coverage, zero duplicate identities, A byte-identical after save/reload and C | Three fragments of one model; genuine third independent upload unvalidated |

## What the tests establish

01/08 verify that transforms, Gaussian covariance, duplicate bookkeeping and
serialization can work without damaging the original anchor. They use exactly
shared intrinsic descriptors, an easier case than independently trained splats.
08's old-view regression sample has only one opaque pixel and is insufficient
for any general appearance-stability claim.

02 verifies a limited room registration gate; it does not establish consistent
person geometry.03 explicitly tests additions, movement, removals and occlusion
with known injected truth. It lacks a real changed-room pair and does not solve
semantic association under changed lighting or independent reconstruction noise.

04 compares A, B, raw union and consolidation with the same source cameras and
frozen sample grid. Raw union improves A-source background MAE0.05643→0.03989,
but slightly worsens B-source MAE0.02609→0.02651. Consolidation barely changes
that trade-off. Masked static layers deliberately have large foreground holes;
black excluded regions are not a claim of complete-room reconstruction.

05's separate geometry trial matches the independent CPU renderer at initialization
within1.6e-9 RGB, performs30 bounded Adam updates, and scores the exported model
with recomputed support and depth sorting. Fitting errors improve more than
reserved errors. There is no colour/geometry sweep, checkpoint selection,
densification or actor optimization. Neither05 candidate is promoted.

06's initial run correctly finds motion shift6 but miscalculates seconds by
0.1001s because decoded sample intervals alternate about0.066733/0.100100s.
The preserved failure is in its initial result. One implementation correction
uses actual local timestamps of matched frames; matching, thresholds and gates
are unchanged. No claim of arbitrary phone synchronization follows this result.

07 uses the same20 previously seen person observations, excluded from the new
room optimizer but used in an earlier separate development diagnostic. Its three
actual rendered states visibly contain two people. Correct clocks cannot repair
that internal shape/depth discrepancy.

## Inputs, execution and preservation

Existing native Panoptic00/24 full MoSca exports, their saved cameras and seen
source images are used locally. Camera20 RGB remains sealed. No fresh evaluation
images, new captures, model downloads, full Gaussian training or paid resources.
No viewer source/catalog changes were needed; the existing viewer remains active.

All models and previews are under ignored
`working/splat-fusion-validation/`. Eight stage runtimes total129.34s; the
additional geometry trial takes24.82s, excluding implementation and inspection.
The eight main processes record384.08MiB peak RSS each; the additional torch
geometry trial's peak memory was not captured. These are CPU measurements, not
GPU/browser performance claims.

Independent artifact verification passes on15 saved PLYs and91 immutable inputs:
finite values, normalized rotations, documented B-only deletions, A unchanged,
colour-only/geometry-only update boundaries, full dynamic point retention, and
incremental covariance/provenance preservation. Numerical correctness and failed
quality gates are separate conclusions. All inspected previews and numerical
records are retained. See artifact checks (historical reference: `docs/artifact-check.json`),
source freeze (historical reference: `docs/source-freeze.json`) and per-stage JSON records.

## Next priority

Do not proceed as if component controls validate production fusion. Preserve the
independent-per-upload architecture, but make actual room/person geometry
compatible before overlap consolidation: a controlled camera-intrinsics/depth
comparison is a useful next candidate. A meaningful real change-detection test
requires a recaptured changed scene, and a real incremental test requires a
third compatible independent reconstruction and substantial old-view coverage.
These follow-ups remain unrun; no additional paid fit is launched here.
