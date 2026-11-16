> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/assembled-hybrid/result.md`.
> Original SHA-256: `3a03f421c7e752d3828cc8e0da0bbd2792404fd87629f6bc016525af3c81dab4`. Private media/logs are not included.

# Assembled multi-view hybrid: result

17 October 2026. **Recovered image-only cameras now drive a real masked Brush
background fit, combined with saved complete-person MoSca motion and a shared
two-camera refinement.** The room/background is more complete and the two
training views are useful. A fresh third view still shows fragmented hands/head
and missing lower legs/feet; its person-region error is worse than the matched
MoSca reference. Keep this integrated candidate alongside the existing quality
baseline, without promoting it as reliable unseen-view replay.

## What our best compatible capability means

The pieces have to share a recording and a valid coordinate bridge. The earlier
three-phone Medium map does not contain the phone used for its saved motion fit.
We therefore use the coherent indoor Panoptic cameras 00/24: their recovered
camera poses passed the 1080p calibration check, and their complete-person,
two-view-refined motion is available. We did not mix disjoint phone-map worlds.
This establishes a two-fixed-camera studio integration, not moving-phone
trajectory recovery feeding a freshly trained dynamic scaffold.

| Piece | Actually used here |
| --- | --- |
| Camera recovery | Image-only SfM from original 1080p training frames; supplied lens intrinsics, estimated extrinsics |
| Brush environment | Fresh masked multi-view fit from 10 recovered views and 1,044 observed static seed points |
| People | Saved two-view-refined MoSca complete observed-person layer: 19,678 Gaussians, including selected source-static people |
| Shared optimization | One 2000-step fit from both videos at each sampled event time, fixed identities and temporal residual regularization |
| Playback/inspection | Twenty real saved event states, 0–2.9029s; independent frozen-time orbit and fixed-view playback |

The seed uses masked background triangulation; no MoSca person seeds are copied. Brush degree0 matches the
shared DC renderer; no point subsampling is used. Ten image/mask names are
flattened with camera prefixes, giving unambiguous pinned Brush v0.3.0 sibling
mask lookup. COCO masks remove people from the static image objective; shadows
and segmentation errors can remain. Camera recovery uses 1080p; fitting uses
640×360 with explicit COLMAP/OpenCV pixel-centre conversion.

## Coordinate and asset-reuse bridge

Brush fits in the recovered SfM world. The saved refined person Gaussians begin
in the previous author-calibrated motion world. One training-camera-correspondence
similarity places them into the recovered world, using the old training
calibration as a bridge. Scale is 7.9101 arbitrary SfM units per source unit;
maximum camera orientation mismatch 0.1904° and centre mismatch 1.294% of baseline.
This passes the predeclared 5°/3% bridge gate.

This is **not a purely image-only motion alignment**. The saved motion asset
retains its earlier calibration dependence, which is recorded in every output.
Internally, residual optimization uses source units for its displacement bounds;
rendering/export uses the recovered SfM world. A common change of world coordinates
does not create new surface observations or establish metric accuracy.

For the two physically fixed cameras, the five recovered poses per camera are
averaged to one fixed inspection/refinement pose. Brush sees the ten individual
recovered training poses. The matched reference also uses these recovered mean
poses, so its source-view metrics differ slightly from the old author-camera
viewer output. All three new comparisons share cameras, clocks and compositing.

## The three candidates

1. **MoSca two-view · matched reference**: the previous refined scene, transformed
   into the recovered world; 39,028 background plus 19,678 person Gaussians.
2. **Assembled hybrid · before refinement**: fresh Brush background with the same
   saved people; 1,418 background plus 19,678 person Gaussians. Background fills more
   room, but person translucency makes simply swapping backgrounds insufficient.
3. **Assembled hybrid · two-view refined**: the assembled scene after shared
   refinement, same 21,096 identities. Bounded source-unit position residuals
   (background±0.20, people±0.15), shared DC/opacity/scale changes, fixed rotations
   and temporal regularization. No new MoSca scaffold/depth/tracking inference.

Both camera losses have finite nonzero gradients on shared person positions:
absolute gradient sums 0.20715 and 0.25837. This is actual two-view fitting.
All original models are retained; no fitting follows the new-view evaluation.

## Fresh-view evaluation

Before fitting, choose unused camera 21 by calibration alone: it minimizes the
maximum optical-axis angle to the two training cameras among unused candidates.
Angles are 32.22°/30.72°. It looks downward and sees lower-body surfaces absent
from both training crops. It is a new camera, not necessarily an interpolation
between them. Camera02 remains a previously seen, much harder stress diagnostic.

All three candidates freeze and their hashes are recorded before camera 21 RGB
is downloaded/decoded. Freeze receipt epoch 1792227808.086; fresh preparation
starts 1792227813.423. No candidate update follows evaluation. The 9,050,462-byte
original has recorded URL/SHA256 in evaluation provenance (historical reference: `evaluation-summary.json`).
Twenty rectified frames match the source clocks exactly in this authored
synchronized capture. This does not establish synchronization for casual phones.
The fresh source record (historical reference: `fresh-source.json`) retains usage terms and transformations.
Fresh COCO mask overlays were reviewed across all 20 states; they broadly cover
the person, including feet. They are not independently annotated ground truth.

Mean absolute RGB errors, black compositing, native CUDA renderer:

| View | Model | Whole image | Background | Person |
| --- | --- | ---: | ---: | ---: |
| Training00 | Matched MoSca | 0.01457 | 0.01112 | 0.03058 |
| Training00 | Assembled | 0.02388 | 0.01440 | 0.08403 |
| Training00 | Refined hybrid | 0.01456 | 0.01249 | 0.02002 |
| Training24 | Matched MoSca | 0.14365 | 0.15770 | 0.02978 |
| Training24 | Assembled | 0.02613 | 0.01971 | 0.07691 |
| Training24 | Refined hybrid | 0.01837 | 0.01661 | 0.02103 |
| Fresh21 | Matched MoSca | 0.18128 | 0.19449 | 0.07205 |
| Fresh21 | Assembled | 0.08929 | 0.08630 | 0.11930 |
| Fresh21 | Refined hybrid | 0.08561 | 0.08306 | 0.10666 |
| Seen stress02 | Matched MoSca | 0.26020 | 0.26749 | 0.12907 |
| Seen stress02 | Assembled | 0.11204 | 0.11127 | 0.14920 |
| Seen stress02 | Refined hybrid | 0.13462 | 0.13294 | 0.18262 |

Fresh-view whole-image error falls 52.8%, background error 57.3%, but person error
rises 48.0% versus the matched reference. Silhouette IoU changes 0.596→0.625 and
mask coverage 0.808→0.824; those small gains do not repair person appearance.
Source24 background error falls 89.5%, with better person error after refinement.
The extreme seen view's person/room quality regresses under refinement compared
with assembly alone. We do not equate lower whole-image error with better people.

## What the actual images show

Training views show a recognizable person moving through the arm sequence, with
more room/floor context. Hands and head edges still ghost. The fresh view has
large background rays/blur and a floating person ending around the lower legs;
feet visible in the recording are absent from the reconstruction. Arm/head
surfaces fragment as motion increases. Camera02 remains badly broken. This is a
clear person-geometry coverage failure, not a subtle metric-only regression.

A more complete but blurry background covers black holes from the old scene;
that can strongly lower aggregate RGB error while the person gets worse. The
fixed inherited topology and front-derived observations do not supply unseen
feet/back surfaces. Current evidence supports a useful fitted-view hybrid
prototype, not faithful free navigation around the person.

Native private evidence:

- Source00 refined (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_00/refined-000.png`).
- Source24 refined final (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_24/refined-019.png`).
- Fresh recording (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_21/source-000.png`),
  matched reference (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_21/baseline-000.png`),
  refined hybrid (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_21/refined-000.png`).
- Fresh all-state comparisons: states0–9 (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_21/contact-0.jpg`),
  states10–19 (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_21/contact-1.jpg`).
- Seen stress view (historical reference: `../../working/assembled-hybrid/retrieved/assembled/evaluation/hd_00_02/refined-000.png`).

## Inspect in the harness

At http://localhost:4318 select **Assembled multi-view hybrid**. Start with
**Assembled hybrid · two-view refined**, compare **MoSca two-view · matched
reference**, and use **Recorded viewpoint** for Lead00, Second24, Fresh21 and
Seen stress02. Changing recorded viewpoint preserves event time. The view choice carries across
model comparisons, while changing models resets the timeline to zero; scrub to
the same event time when comparing. Pause and
orbit, scrub to the end, then play from a chosen view. All outputs are sampled
snapshots with the original 20-state clock; loading may slow browser playback.

## Verification and resources

Brush 3000 steps take 21s. Shared refinement takes 105.83s, with 373.3MiB peak
PyTorch-allocated memory; driver/native allocations and evaluation segmentation
are outside that number. Whole-GPU peak and hardware browser throughput are not
measured. Native evaluation takes 34.73s. All jobs ran on the already-compatible
A40 at US$0.59/hr, within the existing US$2 allowance and 20:25:35 Sydney watchdog.
No new worker or extension. The successful Pod remains retained until that cutoff.

Retrieval (historical reference: `retrieval.json`) verifies the 197,290,420-byte archive and all 492 files.
Artifact checks (historical reference: `artifact-validation.json`) verify finite fields, unit quaternions,
frame hashes, constant background prefixes and changing person geometry for all
three outputs. Rescaled seed observations lie inside the coarse masks in 5952/5955
checks, with three boundary exceptions; semantic purity is not guaranteed. The
median rescaled sparse reprojection error is 0.222px. Browser verification and final freeze/clock checks are recorded
in verification (historical reference: `verification.json`). Native first/final views, all fresh frames
and fresh masks were visually inspected. Source media/models remain private and
ignored. The first local preparation hit a NumPy-bool JSON serialization error;
its dataset was preserved and the serialization repaired before GPU fitting.
Brush emitted XDG runtime warnings but exited 0 and exported its model.

The next experiment should add observed person surfaces and multi-view geometry
initialization while retaining this integrated regression case. Keep the locked
quality baseline and report all three candidates rather than selecting by room
RGB alone.
