> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/incremental-scene-fusion/result.md`.
> Original SHA-256: `97e0989dc13d062a3d23b39719f5f109259e4d4a3faa80b93ca88f66c9c64448`. Private media/logs are not included.

# First late-upload enrichment result — 19 October 2026

**Incremental insertion and refinement work mechanically and improve seen-view
appearance, but visual geometry quality remains insufficient.** Adding 1,500
splats to an existing scene reduces person-region RGB error 28.7% in the new
upload and24.4%/29.7% in the old views. Partial lower-body coverage appears in B;
both shoes remain absent from the previously seen stress view. Do not promote
this as a complete person, a faithful new-view reconstruction or dynamic fusion.

Previous work was committed and pushed first as `18d6535`. This separate package
implements the user's revised arrival workflow. The old shared-person experiments
and overall full-MoSca quality baseline remain intact.

## What was actually tested

At event state000, A is the saved assembled Brush room and MoSca foreground
built from cameras00/24. It already contains two recordings; this is a convenient
existing-scene control, not a claim that A was freshly built from one upload.
Camera21 simulates a later B upload. Upload arrival is separate from event time.
Source calibration and known synchronization control alignment in this study.

All 21,096 old Gaussians remain fixed, including 1,418 Brush room Gaussians.
Three frozen candidates were inspected:

- **A:** saved scene, converted into author-world meters with full covariance.
- **Union:** A plus 1,500 B proposals, voxel-deduplicated among proposals and kept
  at least1cm from old foreground centers. Initial opacity0.5, scale8mm.
- **Refined:** the union after 128 joint-view optimization steps on additions
  only. Old00/24 and new21 images all supply finite nonzero position gradients.
  Opacity pruning below 0.03 was enabled; no addition crossed that threshold, so
  all1,500 remain. This does not demonstrate effective duplicate consolidation.

B proposals use one cached MASt3R21/24 forward, registered with 16,828 saved
calibrated correspondence anchors. The robust fit retains 15,102 with1.05cm
median and2.13cm90th-percentile residual. This measures agreement in overlap,
not unseen-foot depth accuracy. Calibrated B rays carry the aligned inferred
depths; their near-zero reprojection error is by construction.

**B was not independently reconstructed as a complete MoSca video.** This is a
one-image depth-proposal backend for a first frozen-instant growth test. New
geometry is model-inferred; sampled B colors are observed. No new model download,
independent upload registration, motion-scaffold update or temporal fusion ran.

## Matched measurements

Person mean absolute RGB error on0–1 RGB, same640x360 renderer and conservative
source masks for every candidate. Lower is better.

| Recorded view | A | Union | Refined | Refined vs A |
| --- | ---: | ---: | ---: | ---: |
| Original00 |0.09480 |0.09492 |0.07164 |24.4% lower |
| Original24 |0.08770 |0.08511 |0.06165 |29.7% lower |
| Late upload21 |0.12640 |0.11917 |0.09012 |28.7% lower |
| Previously seen stress02 |0.17443 |0.17562 |0.16071 |7.9% lower |

B foreground mask coverage grows 86.4% →90.6% →94.1%. Within the pre-existing
conservative B shoe interiors, left coverage grows 0% →23.9% →71.6%; right grows
0% →0% →6.9%. These are alpha-coverage diagnostics, not correctly reconstructed
shoe-surface percentages. Both stress02 shoe interiors remain at0% coverage.

The predeclared numerical development signal passes: B improves at least5%, A
person appearance does not regress by more than5%, and one shoe interior gains
at least 0.05 coverage. **The visual quality gate fails.** Appearance gains and
larger alpha coverage cannot establish reliable3D geometry. Old-view background
RGB error increases slightly (00:0.01244 →0.01309;24:0.01921 →0.01961) despite
unchanged Brush parameters: foreground additions can still spill/occlude there.

## Actual inspection

The raw union makes small visual changes. Refinement adds substantial visible
lower legs and a dark partial foot in B, and darkens/fills shirt regions. The
person becomes grainier; new lower-body shapes are fragmented/blocky and do not
form two credible shoes. The±10degree virtual views show additional volume,
with holes, silhouette artifacts and inaccurate-looking surfaces remaining.
Stress02 remains badly fragmented, with no recovered feet. This is partial
seen-view enrichment, not a reliable free-navigation result.

Private inspection panels:
source B and all candidates (historical reference: `../working/incremental-scene-fusion/trial/hd_00_21-comparison.jpg`),
original00 (historical reference: `../working/incremental-scene-fusion/trial/hd_00_00-comparison.jpg`),
stress02 (historical reference: `../working/incremental-scene-fusion/trial/hd_00_02-comparison.jpg`),
magnified feet (historical reference: `../working/incremental-scene-fusion/trial/foot-comparison.jpg`),
nearby orbit (historical reference: `../working/incremental-scene-fusion/trial/nearby-orbit.jpg`).
The full source24 comparison was also inspected. Camera02 was read only after
these three candidates froze for this study; it was already seen historically,
so it is never called fresh. Reserved camera 20 RGB remains sealed.

## Verification and resource use

Five focused tests pass: similarity/covariance, depth-sorted occlusion,
projection/gradients, insertion without old-parameter mutation and PLY roundtrip.
Frozen native-reference agreement passes with 0.00604 whole-image and0.00672
person MAE; maximum pixel error0.373 shows that this is not exact pixel parity.
The local renderer uses Gaussian covariance projection and alpha compositing,
not the native CUDA training renderer. Training was160x90 while evaluation is
640x360; this resolution/low-pass difference may contribute to graininess and
needs a single-variable control before attributing all artifacts to fusion.

Actual exported refined PLY replay reproduces B person MAE within3.85e-7.
All source/planned-code/model hashes, finite positive scales, proper rotations,
bounded updates and frozen assets verify. Old training arrays and the refined
PLY's old prefix are bitwise unchanged. The union export's type promotion causes
up to9.54e-7 rounding in logged scales/appearance/opacity; its old positions and
rotations are bitwise unchanged. No old asset was overwritten to hide this.
See verification (historical reference: `docs/verification.json`), report (historical reference: `docs/report.json`),
registration (historical reference: `docs/pointmap-alignment.json`), fit (historical reference: `docs/fit.json`),
bounds (historical reference: `docs/bounds.json`) and the separate visual receipt (historical reference: `docs/visual-review.json`).

Whole guarded execution96.19s; worker93.75s, fit44.92s and inference8.28s.
Worker peak3,303.77MiB; sampled peak3,045.64MiB, below5GiB/1800s. Two CPU threads,
no training GPU/cloud or paid compute. Cached inputs/environment were reused;
no dependencies or checkpoints were installed/downloaded. Private artifacts
remain under working/incremental-scene-fusion/. Temporary fitting processes ended.
The local viewer service was started for inspection; other Docker apps were
left alone. Browser screenshots use software rendering, not a hardware benchmark. All
three models, calibrated view switching, orbit/reset and zero invalid manifests
pass browser checks; ten harness tests, syntax and Compose validation pass.
Pixel comparison confirms orbit changes the image and reset restores it exactly.
See browser check (historical reference: `docs/browser-check.json`) and publication (historical reference: `docs/publication.json`).

Two validation/setup corrections required no model rerun: an inspector filename
shadowed Python's stdlib inspect and was renamed; an overly strict union-prefix
byte check exposed the documented floating-point export rounding. The first
browser attempt found the local viewer stopped; only its existing service was
started before retrying. Frozen candidates and fit/inference were not repeated.

## Decision

Continue the incremental architecture as a candidate, with A preserved and B
allowed to add incomplete evidence. Do not return to requiring a complete shared
initializer before every useful update. Do not replace the overall quality
baseline: missing stress-view feet and grainy surfaces remain material failures.

First compare the same cached proposals/refinement at a higher training
resolution, without changing insertion or depth settings, to isolate that
confound. Then isolate **visibility-aware consolidation of overlapping additions**, with
old observations retained and Brush fixed. This test froze the old person and
could only add a new layer; earlier inferred geometry must eventually be corrected
or replaced when a later upload contradicts it. Define that controlled comparison
before fitting again. A further seen upload13 can then constrain B's foot-depth
hypotheses. Extend through time only after insertion/consolidation is coherent;
new splats currently have no motion attachment beyond this instant.
