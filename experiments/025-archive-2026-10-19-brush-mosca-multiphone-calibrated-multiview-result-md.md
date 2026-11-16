> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/calibrated-multiview/result.md`.
> Original SHA-256: `db91989241066404ef9f0bb29805ce776c14bd39404c142c170f25556924f48a`. Private media/logs are not included.

# First calibrated two-camera refinement: result

17 October 2026. **Two real synchronized recordings now contribute to one
shared Gaussian refinement.** The second training view improves substantially.
The distant, elevated held-out view still breaks up badly, and its person-region
image error is slightly worse. This establishes the integration, not reliable
unseen-view replay or a general multi-phone pipeline. Keep the
locked MoSca quality baseline and hybrid development path (historical reference: `../decision.md`).

## Inspect the result

At http://localhost:4318 choose **Calibrated two-camera trial**. Compare:

- **Calibrated MoSca initializer** — the shared starting geometry.
- **One-view refinement · control** — image optimization from camera 00 only.
- **Two-view refinement · experimental** — shared optimization from cameras
  00 and 24 at the same timestamps.

Use **Recorded viewpoint** to select **Lead camera · 00**, **Second camera · 24**
or **Held-out camera · 02**. Changing viewpoint preserves event time and geometry;
matching view choices carry across model comparisons. Play/pause and scrub,
then pause and orbit. Reset returns to the selected recorded camera.

Start at the second camera: the one-view model has torn/ghosted body surfaces
and a displaced background silhouette. The two-view model retains a much more
complete person there through the arm movement. Hands/head edges still ghost,
and large room regions remain missing. The lead view stays recognizable.

Then select the held-out camera. The true recording shows a recognizable whole
person from above, including feet. Both reconstructions instead show fragmented,
stretched surfaces and large black gaps. This is a clear quality failure, not
just a small cosmetic difference suggested by an aggregate image metric.

The two static **Renderer check** outputs are background-only fixtures. Their
person-seed ghosts are intentional retained evidence from the old Brush model;
they are not new motion reconstructions or recommended scene outputs.

## Which videos contribute

| Camera | Role in this trial |
| --- | --- |
| hd_00_00 | Original lead; photometric/silhouette fitting in both controls |
| hd_00_24 | Additional synchronized recording; stereo calibration for both controls, image fitting only in the two-view model |
| hd_00_02 | Evaluation after both optimizer checkpoints were frozen; no initialization, pose fitting or model updates |

The two training optical axes differ by about 31.5 degrees. The evaluation
camera is about 86.5 degrees from the lead and sees the person from a much more
elevated angle. It is a difficult extrapolation, not evidence that all views
between the training cameras are equally bad. Training views also omit surfaces
and lower-body regions visible in the evaluation recording.

The new camera-24 original was downloaded from the same Panoptic sample and
hash-identified. Twenty actual saved MoSca event states span 0–2.9029 seconds.
All selected training/evaluation presentation timestamps match the lead targets
exactly in these encoded synchronized studio recordings. This does not solve
clock alignment, rolling shutter or camera tracking for casual phone footage.
Source terms remain private noncommercial research with no media/derivative
redistribution. See input provenance (historical reference: `input-report.json`).

## What was actually fitted

This is a new **calibrated refinement of saved MoSca Gaussian states** using
MoSca's pinned native CUDA renderer. It is not an upstream MoSca multi-camera
feature, a newly jointly optimized MoSca scaffold, or a new Brush background.

Both controls start from identical semantic people selected across the static
and dynamic MoSca components. There are 39,028 shared environment Gaussians and
19,678 person Gaussians per state. Camera poses/intrinsics stay fixed. The
two-view objective renders the SAME state into both cameras, averages their
balanced person/background RGB and silhouette losses, and updates shared
geometry/colour/opacity/scale parameters. Views are never interleaved as time.
Fixed identities and a temporal residual-velocity penalty connect the states.

Each control runs 2,000 steps with the same seeded time ordering and explicit
settings. Environment positions are bounded to ±0.20 m; person residuals to
±0.15 m. Scales, colours and opacity have shared regularized residuals. No new
Gaussians are added, no generated views are used, and no 3D body annotations
supervise fitting. The sequence retains real discrete states without learned
continuous-time interpolation. Temporal regularization and shared identities
alone do not prove physically correct 4D geometry.

At the first two-view update, BOTH cameras produce finite, nonzero derivatives
on the same person-position parameter tensor: absolute-gradient sums 0.2497
and 0.3243. The one-view (historical reference: `one-view-report.json`) and
two-view (historical reference: `two-view-report.json`) reports record cameras, losses, hashes and
actual runtime. This is evidence that the second video enters optimization,
not proof that its gradients recover correct unseen surfaces.

## Initialization, failures and calibration limits

The original rear camera 01 differs from the lead by 134 degrees. Camera 24
was selected from supplied calibration, without using evaluation images.
The first new training pair gives only ten valid triangulated SIFT points and
fails the twenty-point gate. A separate training-only check across five fixed
moments yields 59 observations in 52 approximate 5 mm spatial bins, with the
same matching/epipolar thresholds. These bins are not ground-truth point IDs.
See the retained preparation check (historical reference: `stereo-report.json`).

The monocular fit learned focal length ~452 px; the supplied lead calibration
is ~544 px. Source rays are explicitly corrected. A global depth scale alone
fails the loose readiness gate at 16.44 px median second-view reprojection;
direct robust optimization of that scalar also fails. The
scale-only failure (historical reference: `scale-only-report.json`) is retained.

A separate depth-affine calibration uses `z_metric = 5.1529*z_native - 0.7073`,
preserving source rays and transforming Gaussian covariances with its local
Jacobian. It uses 47 training-camera correspondences, with twelve reserved
point observations, reaching 12.37 px training and 14.31 px validation medians
under the unchanged 15 px initialization gate. Observed depths remain positive.
This is a loose, method-selected readiness check, not independent accuracy;
some individual residuals remain large. Both optimization controls share this
two-view-informed initializer. The one-view control is consequently not a
wholly monocular reconstruction from scratch. See
depth calibration (historical reference: `depth-calibration-report.json`) and the investigation (historical reference: `investigation.md`).

## Evaluation after freezing

Both checkpoint hashes were recorded before the held-out frames were decoded
for this trial and before their images were transferred to the worker. The
evaluator verifies hashes before and after measurement. It uses the author's
camera-02 calibration directly, without localization, model updates or threshold
tuning. See freeze receipt (historical reference: `freeze-receipt.json`) and
evaluation summary (historical reference: `evaluation-summary.json`).

Means over twenty states, using black compositing and automatic masks:

| View | One-view person RGB MAE | Two-view person RGB MAE | One-view silhouette IoU | Two-view silhouette IoU |
| --- | ---: | ---: | ---: | ---: |
| Lead camera 00, fitted | 0.0191 | 0.0200 | 0.925 | 0.895 |
| Second camera 24, fitted only in two-view | 0.0781 | 0.0217 | 0.591 | 0.782 |
| Held-out camera 02 | 0.1200 | 0.1291 | 0.357 | 0.363 |

Second-view person error falls about 72%. Held-out person error rises about
7.5%, while silhouette overlap changes little. Whole-image held-out MAE falls
from 0.2680 to 0.2602, primarily a room/background measure; that does not mean
the person improved. Automatic masks are not 3D or manually verified ground
truth. The visible elevated-view failure is decisive here.

Native evidence in ignored private storage:

- Second training camera: recording (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_24/source-000.png`),
  one-view (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_24/mono-000.png`),
  two-view (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_24/two-000.png`),
  two-view final (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_24/two-019.png`).
- Held-out camera: recording (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_02/source-000.png`),
  one-view (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_02/mono-000.png`),
  two-view (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_02/two-000.png`),
  two-view final (historical reference: `../../working/calibrated-multiview/evaluation/hd_00_02/two-019.png`).

## Renderer findings and correction

Brush's Nerfstudio PLY loader and saved validation renders provide a native
reference. One nearly frozen pass preserves positions, scales and opacity.
The DC-only roundtrip changes one trailing blue coefficient; the strict first
attempt fails and is retained. The comparison records that discrepancy rather
than claiming exact parameter identity. The full-SH case has no colour drift.

Shared/native black-backed image MAE is 0.00098 for DC and 0.00097 for SH3.
White backfill increases it to about 0.113: only 2.7% of pixels have accumulated
alpha above 0.99. The model is translucent, so backfill strongly changes its
appearance. This explains a substantial part of earlier white-backed render
differences; it does not prove a new geometry improvement.

Actual Spark/browser black-backed screenshots at native 640×360 have MAE
0.01135 (DC) and 0.01539 (SH3) against Brush native validation. Pixel-perfect
parity is not established; residual renderer/precision differences remain.
The camera/projection conventions are checked separately. Historical harness
background is dark green, not white; its measured errors are 0.01435 and 0.01392.
Black is selected for new runs to state their intended compositing convention,
not because it always minimizes browser error by itself.

The harness now supports explicit `backgroundColor` metadata and named
`inspectionViews`. Legacy outputs keep their prior clear colour. Earlier
white-backed SH diagnostics cannot by themselves establish that retaining SH
is harmful. See native renderer report (historical reference: `renderer-report.json`) and
actual browser pixel comparison (historical reference: `browser-pixel-report.json`).

## Resources and retention

The previous Pod was removed at its scheduled cutoff. This separate A40 session
uses Pod `01t386g2a65qpr`, the same pinned PyTorch image, source archive and Brush
release. Minimal dependencies rebuilt the native CUDA rasterizer; no new depth
or tracking model inference was needed. The standard COCO person-mask weights
are hash-verified and used for training/evaluation masks.

One-view refinement took 72.06 seconds; two-view refinement 103.57 seconds,
including checkpoint/snapshot export. Peak PyTorch-allocated memory was 339.8
and 448.1 MiB respectively; driver/native allocations and segmentation are
outside those numbers. Whole-GPU peak and hardware browser throughput were not
measured. Retrieved artifacts total 227,300,811 compressed bytes, with archive
and 233 file hashes verified; see retrieval record (historical reference: `retrieval.json`).

The new session has a **US$2 allowance** and **20:25:35 Sydney, 17 October 2026**
watchdog deadline, at verified US$0.59/hour. The compatible Pod remains available
within that limit as requested. Its independent watchdog uses
`runpod/working/calibrated-session.json`; the old trial state is preserved.
Status/termination commands must select `--state-name calibrated-session.json`.
No further fitting follows held-out evaluation in this trial. Heavy footage,
models, checkpoints and screenshots remain ignored/private.

## Verification

Verification record (historical reference: `verification.json`) captures five validated outputs, 20
preserved source-clock states per sequence and unchanged frozen checkpoint
hashes after evaluation. Both fits finished before camera02 RGB preparation.
All nine recorded-camera selections passed pose/intrinsic checks, preserved
time/model on switching and supported first-to-last seeking. Play/pause,
rewind, reset and frozen-time orbit passed. An older static run retained its
legacy clear colour and hid the new camera selector.

Harness syntax checks, all 10 server tests and Compose validation passed.
Native images and the actual browser renders were visually inspected; the
held-out breakup is visible in both. Browser interaction checks use Chromium
SwiftShader, so they do not measure hardware rendering performance. Private
browser screenshots are under `working/calibrated-multiview/browser/`.

Recheck published artifacts with `python3 runpod/validate-batch.py --prefix
calibrated- --report working/calibrated-multiview/artifact-validation.json`.
The versioned `runpod/*calibrated*` scripts preserve input preparation,
calibration attempts, refinement, evaluation, retrieval and publishing logic.
Do not rerun fitting against the already inspected held-out camera as an
independent evaluation; reserve a fresh camera for the next experiment.
