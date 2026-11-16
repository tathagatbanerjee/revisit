> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/independent-mosca-fusion/investigation.md`.
> Original SHA-256: `b3ac58bd4cacff041df4cf9c443b0ba35cec7862a417fcdee75e37aafcd90f31`. Private media/logs are not included.

# Independent full-MoSca fusion — 19 October 2026

The user explicitly requests independently reconstructing another angle and
merging full MoSca splats first; hybrid comparison waits. This is different from
our earlier MASt3R-addition/shared-refinement experiment. Preserve that history
and the Guildhall comparison. No assumption that concatenation improves quality.

## Selected smallest trial

Use existing Panoptic `171204_pose1_sample` fixed cameras hd_00_00 (A) and
hd_00_24 (B), approximately 31.5 degrees apart. A is the saved independent
monocular MoSca fit from 36 images (0–2.9029 seconds). Independently fit B on
34 images sampled at 12 Hz from nominal 0.5–3.25 seconds (actual decoded PTS
retained). This deliberately staggers the valid intervals and extends the union
past A. The available recording is only 3.37 seconds: this is a short temporal
composition control, not a demonstration over the user's illustrative 30-second
offset. No new recording, synthetic padding or repeated frame as new evidence.

Use the original 640x360 rectification recipe, pinned MoSca source archive
85c39fe5d137beaa025b1a8920cc69969389913185d6e4d1d80a9ed89dade169,
tested small Metric3D/BootSTAPIR/RAFT priors, 2000-step camera/depth bundle,
1000-step scaffold and 3000-step photometric fit. Reuse the known compatibility
repairs, not a new method/configuration sweep. Inspect priors before fitting;
retain one bounded software repair if necessary. Full means all static and
dynamic Gaussians; the shared viewer exports DC colour, native renders retain SH.
A and B do not share parameters or training losses. No Brush, joint refinement,
new body prior or per-Gaussian consolidation in this first test.

## Alignment and timeline

Independent monocular fits have different scale/world/focal estimates; neither
concatenation nor different start times removes spatial/temporal alignment.
Use training cameras 00/24 and existing author calibration plus their source
correspondences to estimate/diagnose alignment. Prefer one fixed positive-scale
similarity per fit in a common world; transform orientations/scales as well as
centres. Record reprojection residuals and any model mismatch rather than
pretending supplied poses make learned geometry exact. If that representation
cannot align, publish the actual naive merge with its failure clearly marked,
or stop if even source poses are invalid. Do not silently introduce the earlier
nonrigid depth-affine repair or shared-view optimization as independent fusion.

Evaluate all native states from each fitted checkpoint so overlapping clocks
can pair the same source samples, retaining actual PTS and any quantization.
For the staggered timeline use only active videos' states. No holding a moving
person from an ended clip, inventing motion outside coverage, or applying a
constant timestamp shift as if it were new captured time. The static component
of a monocular fit may contain stationary people and is not assumed timeless.
All points of an inactive fit disappear in this simple control; test seam/popping.
Publish A, aligned B and the additive union with matched inspection views and
clock. More points are not proof of useful coverage or no duplicated people.

Inspect full-SH native first/final renders and merged DC renders from both
training cameras and a nearby orbit. Report ghosts, overlap opacity, structural
misregistration and missing surfaces. Camera20 RGB stays sealed. Cameras00/24
are training; any previously seen02/21 use is a diagnostic, not fresh evaluation.
No new evaluation RGB is needed for this demonstration.

## Setup, provenance and cost estimate and run limits

Local RTX4070 Laptop/8GiB is visible but there is no compatible CUDA compiler or
MoSca CUDA environment; do not alter the host or unrelated Docker applications.
Use one isolated A40 Secure Cloud Pod with the existing pinned PyTorch2.1/cu118
image and tested setup. Stripe Directory query Runpod returned no entry. Existing
account status is empty. Live GraphQL on 19 October reports High availability
and US$0.59/hour; recheck at launch. Provider billing/storage basis:
https://docs.runpod.io/pods/pricing (checked today). No subscription/top-up.

Expected setup, model downloads, fit, native rendering/export and retrieval
30–90 minutes: US$0.30–0.89 compute. Maximum two hours from launch: US$1.18
compute plus approximately US$0.023 for 80GB ephemeral disk at $0.10/GB/month;
US$2 session allowance before tax includes buffer. One worker, no persistent
volume, no extensions/more expensive fallback. Setup bound1800s, preprocessing
1200s, one fit1800s, export/render600s; respect remaining launch deadline first.
Arm independent local watchdog using a new `independent-mosca-session.json`
before deployment; verify heartbeat. It depends on local host/API availability.
Retrieve/hash-check native checkpoints, all-point exports, logs and renders,
then terminate and independently verify absence. Preserve old trial state.

Source permissions: existing Panoptic manifests and calibration are retained;
research-only/noncommercial, no media redistribution. Keep originals, models,
checkpoints and previews ignored/private in working/ and output/runs/. Source
terms and input/checkpoint hashes accompany the trial. No credentials are
transferred into the worker payload or viewer. No larger run follows failure.

Pre-result alignment detail: select a fixed camera-orientation-anchored
similarity using author R and fitted first-camera R; fit positive scale and
translation robustly to native-rendered training anchor depths and triangulated
00/24 points. Reserve anchorIndex%5==2 for a loose 15px maximum-two-camera median
reprojection gate. These anchors include moving points at corresponding instants
and are not exclusively static landmarks. Record camera-centre disagreement.
An unconstrained RANSAC similarity is a diagnostic only, not an automatic
alternative to promote if the selected mapping fails. Preserve failed gates in
the published naive-union description. More than one view of the same instant
still requires matched source clocks.
