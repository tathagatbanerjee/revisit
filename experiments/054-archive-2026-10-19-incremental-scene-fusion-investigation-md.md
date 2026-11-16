> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/incremental-scene-fusion/investigation.md`.
> Original SHA-256: `615e1bf6738147180fed9796d1f6b34ecc013061a56978c479b5e217d2f37522`. Private media/logs are not included.

# Late-upload Gaussian enrichment — 19 October 2026

## Question and scope

Can a new video enrich an existing Brush/MoSca reconstruction by adding geometry,
while keeping the old observations useful? This replaces complete joint
initialization as the immediate test. An incomplete addition is a valid
incremental result if it adds credible source-supported coverage without a
material regression. Do not call appearance-only gains true3D accuracy.

A is the frozen assembled Brush room plus saved complete-person MoSca foreground
at state000, built from seen00/24. B is previously seen21 at the same event time,
simulating later arrival. Camera13/02 are not inputs;20 remains sealed. All source
media is the existing private noncommercial Panoptic sample with preserved
attribution and terms. Upload arrival is simulated; the controlled clock is known.

Three candidates: A unchanged; A plus one insertion batch of B-derived Gaussian
proposals; the same union after joint-view refinement/pruning of additions.
Freeze original room AND original person parameters for this first comparison.
A's images still constrain additions through occlusion and photometric loss.
This is deliberately conservative incremental enrichment, not full retraining
or updating the motion scaffold. No promise that the new surfaces are accurate.

## Prior designs and implementation route

MoSca fuses Gaussian observations across time using its motion scaffold, but its
released monocular pipeline is not an asynchronous multi-upload merger:
https://arxiv.org/html/2405.17421v2 . Brush takes posed images and masks:
https://github.com/ArthurBrussee/brush/tree/v0.3.0 . Existing saved scene is reused;
neither upstream program is rerun for the initial A reconstruction.

Use cached/pinned MASt3R only to produce B point-map proposals conditioned on old
camera24. Run one21/24 CPU forward (no repeated descriptor search); use saved
21/24 correspondences and known-calibration triangulation to robustly align its
first-view point map to author-world meters. This is training-data initialization,
not independent3D truth. The first view is new B21; old24 supplies overlap.
No13 data enters proposal inference. Point maps and missing-surface depths remain
**model-inferred**, especially feet not visible in24; RGB is observed in21.
An incremental depth-proposal backend is being tested, not a newly fitted B MoSca
video. Full independent B reconstruction/motion fusion are later work.

Pin existing MASt3R source/checkpoint/environment hashes from shared-person.
Forward uses the exact verified crop transform and low-memory CPU loader. Fit
one robust similarity using saved accepted calibrated matches: five SVD/rejection
iterations, retain residual<=max(0.02m,3*median), capped0.15m. Require>=1000 anchors,
median residual<=0.08m and90th percentile<=0.20m before proposal insertion.
These gates test coarse registration; they do not validate unseen surfaces.

Load all21,096 original Gaussians; preserve their full covariance through inverse
bridge similarity. Convert the original recovered cameras exactly into that
world; B uses author calibration. Native images1920x1080, sources/masks resized
with documented pixel centers. No model subsampling or old Gaussian deletion.
Select proposals inside B's conservative person mask where A foreground alpha
is below0.5 or person RGB residual exceeds0.08. Use aligned model depths on calibrated B rays, camera depth1–6m and world
radius<10m. Record pre-correction model ray mismatch; exact B ray agreement is
by construction, not a validation. Voxelize at0.015m and keep at most
1500 deterministic samples; observed B colors, isotropic initial scale0.008m,
opacity0.5. The initial scale is a representation setting, not measured depth
uncertainty. Retain B pixel/model-depth provenance per addition.

## Renderer and inspection prerequisite

The local cached Torch is CPU-only; no CUDA compiler is installed. Use a small
CPU differentiable anisotropic Gaussian renderer, with perspective covariance
projection,0.3pixel low-pass, depth ordering and front-to-back alpha compositing.
The equations follow the original3DGS convention and the official gsplat
v1.5.3 PyTorch reference, inspected19 October2026:
https://raw.githubusercontent.com/nerfstudio-project/gsplat/v1.5.3/gsplat/cuda/_torch_impl.py .
No upstream source is vendored, patched or installed. This renderer is a local
experiment implementation, not native MoSca/Brush training.

Before fitting, test analytic occlusion/covariance and gradients, and compare a
frozen A render against an existing matching native reference. Stop if whole
image MAE>0.03 or person MAE>0.06 (both on0–1 RGB), or finite/positive covariance
checks fail. Record discrepancies, no assumption of pixel parity. Native
references are prior saved outputs, not new held-out images. Training160x90,
inspection640x360; same renderer/conventions for every candidate.

128 fixed Adam updates, cyclic00/24/21 views, balancing person RGB and foreground
alpha with outside-mask spill. Optimize only new positions (bounded±0.03m),
colors, opacity and scales (bounded multiplierexp(±0.35)); original scene fixed.
Regularize changes, require finite nonzero gradients from all three views on
additions where visible, and record visibility-driven zero gradients explicitly.
After fitting prune additions with opacity<0.03. No extra inference, settings
sweep, second growth batch or retry follows. Save the union before pruning.

Evaluate source RGB/person/background and foreground alpha coverage, both shoe
interiors, A-view regression and added count. Predeclared development signal:
B person MAE improves>=5%, A-view person MAE regresses<=5%, and either shoe's
foreground coverage increases>=0.05. Both visual and numerical evidence needed;
this signal does not certify full body geometry or unseen-view fidelity.
Save all source/reference panels and a nearby frozen-time orbit. After freezing
all candidates, inspect previously seen02 as a no-update stress diagnostic; it
is excluded from inference/fitting and is not a fresh evaluation camera. Do not open20:
this small study compares seen development views only. No dynamic claims.

## Cost estimate and run limits

Local cached Python3.12/Torch2.5.1+cpu environment, two CPU/BLAS threads. Existing
RTX4070 is left unused; no other application is stopped. Expected10–20minutes
including preparation, one forward, renderer validation,128steps and inspection;
maximum1800seconds per guarded child,5GiB RSS, initial available RAM>=5.5GiB.
Parent process-group watchdog enforces bounds even if the experiment stalls.
At most2GiB extra scratch. Maximum/expected paid compute US$0; existing local
storage/electricity unpriced. No downloads/installations, cloud resource,
credentials or service/API use. A setup correction may replay saved preparation
without neural inference; no parameter/input fallback or larger run. Preserve
failed receipts and artifacts; stop at a documented failed prerequisite if needed.

## Deliverable

Real A/union/refined PLYs and renders if prerequisites pass, measured bounded
runtime/RSS, input/model/source hashes, insertion provenance, frozen-old-scene
verification, focused tests, result/lessons/next steps. This isolates one-instant
late-upload enrichment. Automatic camera/time registration, independently fitted
B motion, temporal consistency and general multi-phone capture remain untested.
