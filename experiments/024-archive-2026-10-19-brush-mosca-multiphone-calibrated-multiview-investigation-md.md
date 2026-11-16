> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/calibrated-multiview/investigation.md`.
> Original SHA-256: `c1c6e90b353afadefe747894728f284a8ca8c98b7edfed5f34a66f2816864f18`. Private media/logs are not included.

# Calibrated multi-view feasibility trial

17 October 2026. The user approved the renderer comparison and a small genuine
two-camera fitting test with a third camera held out. The previous A40 was
terminated by its watchdog at 14:28 Sydney; API independently shows no Pods
at 18:16. Retain those results and the locked MoSca quality baseline.

## Input and calibration gate

Use Panoptic 171204_pose1_sample, roughly three seconds, the same twenty actual
native states already exported from the monocular fit. Source terms remain
research-only, noncommercial and no redistribution. Existing cameras 00 and 01
have a 134-degree optical-axis difference, which explains poor static matching.
Select camera **hd_00_24** (31.5 degrees from lead **hd_00_00**) using calibration
only, download its original recording from the same documented source, and
reserve **hd_00_02** exclusively for evaluation. Do not inspect evaluation images
to choose fitting settings. Preserve source frame presentation timestamps and
rectify with the supplied camera models. Report synchronization residuals.

Find mutual SIFT correspondences in the two first training frames, filter with
the supplied epipolar geometry, triangulate in author world units converted to
meters, and check positive depth/reprojection residuals. Require at least twenty
usable two-view points before paid fitting. This does not establish dense or
correct dynamic geometry.

Input readiness outcome before launch: the first pair supplies only ten valid
points and is retained as `input/report.json`, gate failed. A separate
training-only preparation check uses five fixed samples [0,4,8,12,16] from the
same twenty states, without changing SIFT ratio or geometric thresholds. It
supplies 59 valid observations in 52 approximate 5 mm spatial bins. Use these
time-indexed observations for depth-scale initialization; repeated points are
not independent accuracy evidence. No evaluation image was opened. This expands
the initial correspondence sampling, not the footage, fitting split or gate.

The monocular model learned focal length 452 px, versus supplied ~544 px.
Before using calibrated cameras, explicitly correct its reference-camera ray
coordinates with K_author^-1 K_fitted. Transform full Gaussian covariances,
not just centers. Estimate positive depth scale from training-only triangulated
points and the native renderer's depth; do not use held-out camera pixels or
author 3D body annotations. Report depth-scale dispersion and second-camera
reprojection error. Fail the alignment gate if fewer than twenty valid depth
samples or median second-view residual exceeds 15 px. This is a loose
initialization gate, not independent accuracy.

Calibration readiness update: scale-only initialization fails at 16.44 px.
Direct robust optimization of that same scalar does not improve it (16.45 px;
21.72 px on a reserved fifth of training-camera points). Retain that failure.
A separate, explicit depth-affine calibration `z_metric = a*z_native + b`
preserves source rays and adds one offset parameter. Fit positive a and b with
soft-L1 reprojection, f_scale=3, on 47 training-camera points; reserve twelve
points for a loose readiness check. It reaches 12.37 px training and 14.31 px
validation median, under the unchanged 15 px gate, with all observed depths
positive. Camera 02 RGB remains unseen. These point-validation results have
informed method selection and are not independent accuracy evidence. Transform
Gaussian covariances with the local Jacobian of this ray-preserving depth warp;
both single-view and two-view controls receive the exact same initialization.

Renderer outcome before refinement: black-backfill shared/native Brush MAE is
~0.001 for both DC and degree-3 SH, versus ~0.113 with white backfill. Geometry,
opacity and scales survive the frozen pass unchanged; DC-only round-trip changes
one final blue coefficient, retained as a warning, while full SH has no colour
drift. Native Torch comparisons will use black for the new trial. Existing
harness clear colour is dark green; make that explicit in the pixel comparison
rather than silently equating screenshots with white-backfill diagnostics.

## Renderer prerequisite

Reuse pinned Brush v0.3.0. Its Nerfstudio loader supports an initial PLY and
separate validation transforms; the COLMAP loader instead initializes from
points3D. Use the PLY route for one near-frozen update with negligible/zero
learning rates and no noise/refinement, then compare its own saved evaluation
render with the exported model at the identical K, pose, resolution and SH
setting in the shared renderer/harness. Check export parameter drift. Compare
background/alpha conventions explicitly; report uncovered regions separately.
Do not attribute adapter differences to fitted geometry. Preserve DC and full
SH cases. No claim of parity follows without actual pixels.

## Small motion integration

If input/alignment gates pass, use the saved MoSca people (static and moving)
and environment as initialization for a bounded **calibrated multi-view
Gaussian refinement**, using MoSca's pinned native CUDA renderer. One shared
Gaussian state at each timestamp is rendered into both training cameras;
never interleave simultaneous views as consecutive time. Camera poses stay
fixed. Gaussian identities and temporal residual regularization connect states.
This is an experimental refinement stage, not an upstream MoSca feature or
complete jointly trained MoSca scaffold.

Keep a one-training-view optimization control from the same initialization and
settings; disclose that initialization scale uses two-view observations. Compare
adding camera 24 to the objective, rather than claiming a wholly monocular
initialization. Use <=2,000 steps each, existing Gaussian membership, DC colours,
bounded position/scale residuals and temporal regularization. Balance person and
background image losses so the room does not hide people failures. No generated
views or 3D annotation supervision. Record losses from each training camera and
that each produces nonzero finite gradients on shared geometry.

Freeze/hash checkpoints before opening held-out images. Evaluate camera 02
without refitting poses, selecting thresholds or changing models. Compare
source/second/held-out images, mask coverage, image error, actual body completeness,
fixed-camera time changes and frozen-time nearby views. Retain regressions and
failures. A two-view loss does not guarantee better third-view geometry.

## Compute, cost and stop conditions

No previous Pod remains. Reuse the verified image/source pins on ONE new A40
Secure Cloud worker, only after input readiness. Query live availability and
price, enforce <=US$0.59/hour. Two-hour launch-relative watchdog and **US$2
allowance**: maximum US$1.18 compute plus ~US$0.023 80 GB ephemeral disk and
buffer, excluding tax. Expected setup, comparison, refinement and retrieval
30–90 minutes (~US$0.30–$0.89 compute). No persistent volume or extra worker.
Use a separate trial-state file and preserve old state/cleanup evidence.

Use minimal native-renderer dependencies and source archive checksums; no new
depth/tracking weight downloads or monocular retraining. Maximum 1,800 seconds
setup, 600 renderer checks, 900 per refinement. One implementation repair for
a software fault; no tuning sweep, more expensive fallback or automatic deadline
extension. If a gate fails, save a bounded failure and all reusable preparation.
Retrieve/hash-check output before cutoff. Keep a compatible Pod within that
cutoff as the user requested earlier; verify its independent watchdog and record
retention. Heavy footage/models/renders remain ignored/private. Version only
code, lightweight measurements and the actual outcome.
