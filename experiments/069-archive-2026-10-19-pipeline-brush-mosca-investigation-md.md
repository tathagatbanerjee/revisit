> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-mosca/investigation.md`.
> Original SHA-256: `210667518e68a85176a3dadbe551c87e37f5fee9d2b3f21f1616e0e235bc6b07`. Private media/logs are not included.

# Brush + MoSca investigation

Prepared 2026-10-14. This package investigates compositing a separately fitted
static environment and reconstructed dynamic foreground. Input preparation is
complete; hybrid quality and resource requirements are not measured.

## Reusable implementation

Brush v0.3.0, already fitted in our static trial (historical reference: `../brush-static/result.md`),
reads recovered cameras and optimizes a static Gaussian scene. It uses
Burn/WebGPU/Vulkan rather than MoSca's CUDA training stack. Its actual release
CLI uses `--total-steps`; use the existing worker/profile as the reference.
[Brush release](https://github.com/ArthurBrussee/brush/releases/tag/v0.3.0).

MoSca commit `02404d2841b4e0dc2d9074860950bce5da579656` has already fitted
our three-second Guildhall event. Reuse its small Metric3D, BootsTAPIR and RAFT
profiles, dependency pins and explicit source repairs. Native outputs contain
separate static/dynamic models and camera checkpoints. Our current exporter
concatenates static then dynamic Gaussians; hybrid export needs a **dynamic-only**
path, preserving primitive identity and native evaluation over time.
[MoSca paper](https://arxiv.org/abs/2405.17421),
our exact trial (historical reference: `../mosca-dynamic/investigation.md`).

COLMAP should register the two Brush inputs jointly, including cross-clip
matches. Camera folders retain independent intrinsics where appropriate. Its
CLI and mask naming are version-dependent; capture actual installed help rather
than mixing our earlier COLMAP flags with current documentation.
[COLMAP CLI](https://colmap.github.io/cli.html).

## What compatibility does and does not establish

Both can export Gaussian positions, covariance/rotation/scale, opacity and
colour. Native models have independently estimated coordinates and scale.
A shared viewer alone does not align them. Estimate one positive-scale rigid
similarity transform from MoSca into the Brush world using matching **static**
landmarks and/or sufficiently informative corresponding cameras. Validate at
multiple source times. A single pose or a straight camera path is insufficient
to determine a reliable full transform; use spatially distributed static points.
A global transform cannot repair locally distorted monocular geometry.

MoSca's dynamic component is based on motion, not semantic person segmentation.
It can contain erroneous background motion or miss slowly moving objects. Inspect
component renders and apply an evidence-backed foreground selection/mask if
needed. The Brush environment must also exclude moving content. Mask interfaces
for COLMAP feature extraction and Brush photometric loss are separate; white
review templates are not completed masks. Confirm mask support/meaning in the
pinned Brush release, including a tiny masked-load check before paying for a fit.

Merged PLY snapshots can satisfy the current harness without a layered renderer:
repeat the same Brush background in each exported state, append transformed
MoSca foreground, and use one shared Gaussian depth ordering. This duplicates
background bytes but minimizes UI changes. Both primitive sets must be passed
to the same rendering/depth process; compositing separate flat RGB overlays
would get occlusion wrong. Use DC-only colour first because our MoSca exporter
already does so; rotating higher-order SH requires an explicit appearance adapter.

## Input coverage and chronology

The case matrix includes static controls, one hybrid event, repeated-event
clock/deduplication controls, separate events, true simultaneous independent
cameras, and a deliberately trimmed timing offset. Local moving-camera clips
are segments of one source recording, not two simultaneous views of a person.
Identical raw source intervals in two trims supply no new viewpoint information.
UTC is unknown; retain seconds relative to each original recording.

The CMU `171204_pose1_sample` is a real synchronized multi-camera studio sample.
We fetched three HD views plus author calibration, about 27.7 MB total, not the
full collection. Two are training candidates and one is reserved for validation.
The videos are only about 3.37 seconds long. Three-second clips and a one-second
trim control are enough to prepare timing/registration tests, but fixed cameras
and narrow spatial coverage can make monocular depth/camera solving unstable.
Use supplied calibration as an evaluation reference and an explicit future
adapter; do not claim our current MoSca CLI accepts joint calibrated multi-camera
training. [Official toolbox and synchronized sample](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox).

## Terms and provenance

Guildhall and museum clips retain the source authors, CC BY-SA 4.0 attribution,
trim/transcode records and source hashes. Sculpture is an official Jawset tutorial
sample with no independent redistribution license identified. Panoptic is shared
for non-commercial research and prohibits redistribution of originals or
modified versions without organizer permission; keep media and derivatives private. Its public
HTTP download route is documented by the authors; downloaded hashes identify
our retained bytes, not authenticated upstream release hashes. The HTTPS endpoint
failed certificate verification; the official HTTP route worked without bypassing
TLS verification. No credentials were sent to the source servers.

Brush code is Apache-2.0. MoSca core is MIT, with separately licensed priors and
native rasterizer dependencies; our previous trial records their restrictions.
This experiment does not imply blanket commercial permission for all components
or input footage. No new libraries, model weights or paid services were installed.

## Cost estimate and run limits — 2026-10-14

Preparation uses local CPU/FFmpeg, bounded downloads and ignored disk storage;
there is no incremental cloud compute charge. Raw Panoptic download is under
30 MB. Actual derived asset sizes/counts are in `resources/asset-report.json`.
Masks are unreviewed and fitting is not launched.

For a later **single H1 trial**, propose one sequential GPU session, with the
same A10G `g5.xlarge` Linux US East route if Brush's Vulkan adapter checks pass.
The previous same-day trial verified US$1.006/hour On-Demand. This is historical
price evidence, not a launch-time quote; recheck rates/capacity before execution.
A10G has roughly 24 GB VRAM and g5.xlarge 16 GiB host RAM. Use at most 150 GB
scratch, preserve the existing private Sydney bucket and avoid new credentials.
See the measured previous cost (historical reference: `../mosca-dynamic/cleanup-report.json`).

| Bound | Proposed first hybrid session |
| --- | --- |
| Inputs | H1: at most 48 Brush candidate frames, 36 MoSca event frames at 640×360 |
| Expected session | 1–3 hours including install, masks/poses review, fitting, export and retrieval; not measured |
| Compute estimate | US$1.01–3.02 using the earlier US$1.006/hour rate |
| Maximum runtime | 4 hours total from first launch, including any sequential replacement |
| Other allowance | Up to US$1 for short-lived disk/IP, requests/transfers; tax excluded |
| Proposed maximum | US$6, including failures; reject incompatible/new price without revising estimate |
| Retry boundary | One setup/profile repair within original clock; no automatic extra dataset or worker upgrade |
| Shutdown | Independent launch-time termination schedule plus local worker cutoff |
| Retention | Retrieve model/cameras/masks/logs; remove compute/disks/access resources, verify; identify retained S3 versions |

At the original rate, cutoff compute is about US$4.02 plus the US$1 non-compute
allowance. This is a proposed operational envelope, not an account-wide spending
cap or authorization to start a worker. Sequential static and dynamic tools on
one worker minimize setup costs; reusing existing Guildhall MoSca checkpoints
could reduce paid work further. Subsequent cases need their own selected scope;
do not launch the seven-case matrix as a batch. Pure registration/export/viewer
work can run locally once the necessary artifacts are available.

## Recommended first attempt

Use H1, validate masked static registration and Brush alone, then align the
existing Guildhall native MoSca model and export a coarse hybrid. Compare it to
both parents before increasing duration, camera count or fitting complexity.
Resolve masks and transform quality before touching simultaneous motion fusion.
The implementation plan (historical reference: `implementation-plan.md`) defines the gates and evidence.

## Authorized H1 execution and measured outcome

On 2026-10-14 the user authorized the first H1 hybrid run within the proposed
US$6/four-hour envelope, with explicit GPU termination after completion. We
performed local preparation and alignment, reused the completed MoSca motion,
and fitted only a small masked Brush background on one A10G worker. No other
case was fitted. Result (historical reference: `result.md`) records scope changes and visible failures.

The first 39-frame camera set registered only 33 views, failing the per-clip
gate. A narrower later interval (≤68 s) registered 30/30 selected views. Mask
review keeps the top 220 pixels; floor/lower coverage is deliberately sacrificed.
Pinned Brush mask source was checked at
[lookup](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/formats/mod.rs),
[alpha loading](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/scene.rs)
and process masked-view handling. Runtime passed a 20-step mask/load smoke.
PyCOLMAP 4.2.1 and local dependency versions are saved in `local-requirements.txt`.

The 3,000-step Brush command took 23.88 s, generating 9,912 Gaussians. We aligned
MoSca's moving component using 1,235 static point correspondences with 247
withheld; training-only refinement reduced withheld median reprojection error
to 1.509 px. Twenty 24,100-Gaussian hybrid states were inspected in the viewer.
Integration and independent controls work, but the broad mask leaves holes and
streaks and the moving component includes carpet artifacts. Overall hybrid
quality improvement was **not** established. Next steps prioritize masks and
foreground separation, not longer training or simultaneous-camera fusion.

All worker outputs were retrieved. Automatic self-shutdown was followed by
verified termination and removal of job volumes, temporary roles/profile,
security group and termination schedule: cleanup report (historical reference: `cleanup-report.json`).
Conservative launch-to-cleanup compute allowance: **US$0.148**, including the
post-shutdown interval; allow **US$0.20–0.40 total before tax**, not billed usage.
No GPU resources remain. Job storage retains 16.2 MB current / 20.7 MB including
versions; at the earlier indicative Sydney rate this is below US$0.001/month
while unchanged. The trial did not create new model weights or project keys.
