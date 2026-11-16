> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-coordinates/investigation.md`.
> Original SHA-256: `ebc9458f16578552565f22b5bfa2374e38cabbc4e445c11c0ef6660d4dcc224b`. Private media/logs are not included.

# Shared-coordinate recovery trial

17 October 2026. User requested tests of aligning independently moving cameras
before further multi-view reconstruction. This phase performs camera recovery
only; no dynamic fitting, new cloud worker or existing watchdog extension.

## Method and evidence

Use the existing local pycolmap 4.2.1 / OpenCV 5.0 environment in
`working/brush-mosca/tools`. Recover poses from stationary background features,
excluding saved COCO person masks. Put all cameras into one bundle-adjusted map;
do not stitch independent monocular maps with arbitrary scales. Intrinsics are
supplied priors, held fixed for this first diagnostic. Camera extrinsics are
not supplied to the mapper. Reprojection error alone cannot prove correct poses.

[COLMAP official FAQ](https://colmap.github.io/faq.html) recommends affine-shape
DSP-SIFT and guided matching for sparse matches, supports fixed intrinsics and
feature masks, and describes disconnected submodels. Check actual installed
options rather than assuming the newest web documentation matches the wheel.
Convert OpenCV principal points to COLMAP's pixel-center convention (+0.5).

## Bounded tests and gates, defined before execution

1. Known-calibration control: only cameras00/24 from the existing Panoptic
   trial, five samples per camera. Mask people; recover extrinsics without
   author R,t. Compare recovered relative rotation and baseline direction with
   supplied calibration afterward. Target <=5 degrees rotation and <=15 degrees
   baseline-direction error; >=30 shared background tracks. No camera02 images.
2. Handheld baseline: existing 4DM easy, five training phones, five samples
   per phone from the existing 3-second interval. Keep the previously reserved
   sixth phone excluded. Recover a joint map using per-frame phone intrinsics,
   not phone position/rotation metadata. Target >=3 phones with >=4/5 frames in
   a single component, >=50 cross-phone 3D tracks, median point reprojection <=2px.
3. If a joint phone map passes, localize one later saved frame per registered
   phone against its frozen background map. Target >=30 2D/3D inliers and median
   residual <=2px. These are diagnostic localization frames from a previously
   explored dataset, not a fresh reconstruction-quality test set. If map fails,
   report why and do not manufacture a shared trajectory.

One affine/DSP-SIFT + guided-matching attempt per dataset, four CPU threads,
maximum 10 minutes for each process (including feature extraction); no broad
parameter search. Preserve failures and verified pair graphs. Visualization:
background feature/mask overlays, pair connectivity and recovered camera centers
where available. Hold reconstruction quality and clock synchronization separate.
4DM source clocks are nominal; this trial does not establish independent sync.

## Cost estimate and run limits

Local CPU, no new paid resources, no new footage/model downloads. Reuse existing
originals/masks; at most 60 mapping images and ten localization images, <=640px.
Expected 2–10 minutes per dataset, maximum30minutes CPU plus inspection; working
storage <=2GB. Cloud session remains under its existing 20:25:35 Sydney cutoff.
No new GPU training or spending allowance. Local feature/reconstruction outputs
are private ignored artifacts; commit only code and lightweight reports.

## Dataset correction before the motion test

The official [4DM README](https://github.com/fabiopoiesi/4dm) distinguishes
Easy (all phones held stably), Medium (three moving phones) and Hard (all moving).
Easy tests cross-phone alignment with limited handheld motion; it cannot alone
validate repositioning trajectories. Therefore add one identically configured
25-image Medium run under the same local-only bounds, with its own reserved
whole phone and five later localization frames. Maximum60 mapping images across
all three cases, ten localization candidates, no additional downloads or cloud
work. No parameter retuning or weaker success thresholds follows Easy's failure.

After Medium passes the unchanged map gate, perform an additional stronger
localization diagnostic with identical thresholds: exclude reference descriptors
from the query's own phone. This tests cross-phone support explicitly. Keep its
results separate from ordinary later-frame PnP; no changes to map or settings.

## One resolution control, specified before execution

The 640px Panoptic control has too few background correspondences. Preserve it
and run one full1920x1080 variant from the existing original videos, same five
timestamps, same masks enlarged with nearest-neighbour interpolation, same
affine/DSP features, guided matching and unchanged pose/track gates. Rectify
with the original lens calibration and native focal length. This changes source
resolution, not pose priors or success thresholds. Maximum70 mapping images in
total; existing local-only30minute/2GB bounds remain. No model fitting follows.
