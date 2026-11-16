> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-static/investigation.md`.
> Original SHA-256: `af7ee03387ec028633411c3788dcce55a509143b34398efc1ee86b384b8ec9e8`. Private media/logs are not included.

# Brush investigation: a multi-view static scene from video

Investigated 2026-10-14. Status: the user authorized the bounded trial after this investigation;
the first trial is completed and inspected. See the result (historical reference: `result.md`) and
lessons (historical reference: `lessons.md`) for observed results and
setup corrections. The procedure below distinguishes plans from measurements. Follow the workbook (historical reference: `../workbook.md`). The first objective is
viability and useful inspection; processing time of a few minutes is acceptable.

## Recommendation

Use the released Linux Brush application, 60 frames from the sculpture clip,
COLMAP for cameras, and one bounded fit on a single AWS T4 worker. Export an
ordinary Gaussian PLY and inspect it in our existing harness. Keep camera
preparation and training as explicit commands. Start with the native/reference
viewer when available; a headless worker need not run a remote desktop.

There is no pretrained scene model to download for this path. We fit a new
scene from overlapping photographs. The critical prerequisite is a coherent
camera reconstruction, not a neural checkpoint. Unlike SHARP's single-frame
prediction, Brush can combine observations from different sides of the object.
That could give us better geometry and a larger useful navigation region;
neither improvement is established until we inspect our actual result.

This is one static reconstruction. Moving visitors may become artifacts. The
video can supply evidence at different timestamps, but changing the video time
does not replay events inside this model. It advances the viewpoint part of
**controlling time and viewpoint independently**.

## Version and installation decision

The GitHub latest-release API returned **v0.3.0**, published 2025-09-14, when
checked on the investigation date. Use that release first rather than compiling
a moving development branch. The Linux x86-64 archive is 44,242,224 bytes:

- Asset: `brush-app-x86_64-unknown-linux-gnu.tar.xz`.
- SHA-256: `4f0f9a8785d1951c62df26aae247c02c5bba32b00f40b06df4e1c9b867399e20`.
- Release tree: `3edecbb2fe79d3e2c87eeab85b15e0b1dd10d486`.
- Download page: [v0.3.0 release and checksums](https://github.com/ArthurBrussee/brush/releases/tag/v0.3.0).

Download into ignored `working/brush-static/` or worker scratch, verify the
archive checksum, inspect its contents, and locate the `brush_app` executable (confirmed from the archive).
Capture `brush_app --help` before fitting. Its help was checked during execution. Check dynamic-library requirements with
`ldd` and record OS/driver versions. A prebuilt Linux artifact is available;
its compatibility with our selected AWS image remains an execution check.
Code is [Apache-2.0](https://github.com/ArthurBrussee/brush/blob/v0.3.0/LICENSE).
Keep attribution and source footage terms with the derived run; this does not
change the footage's licensing.

Important version distinction: development main at
`1388f74c6fe0236f68ee4915564bf00e9d2e3747` has a separate `brush-cli` and uses
`--total-train-iters`. The release uses **`--total-steps`**. It also differs in
camera handling and dataset controls. Do not copy current-main commands into
the released binary. If the release cannot run, record the setup failure and
choose a pinned source build explicitly; do not silently switch versions.
[Release CLI](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-cli/src/lib.rs),
[current CLI](https://github.com/ArthurBrussee/brush/blob/1388f74c6fe0236f68ee4915564bf00e9d2e3747/apps/brush-cli/src/lib.rs).

## GPU and memory

Brush uses Burn/WebGPU rather than a CUDA training stack. On native Linux,
verify a hardware Vulkan adapter and actual GPU activity before accepting a
run. An NVIDIA driver or successful `nvidia-smi` alone does not prove Brush
is using that GPU. Use `vulkaninfo --summary`, application/backend logs and
GPU utilization/memory samples during a short fit. Stop on a software adapter
such as llvmpipe/lavapipe. Do not rely on unverified backend-selection environment
variables. [Brush overview](https://github.com/ArthurBrussee/brush).

Try **g4dn.xlarge: T4, nominal 16 GB GPU memory, 16 GiB host RAM** first. It
worked for SHARP and fits the current account quota; that is a practical
candidate, not a measured Brush requirement. Select 1280-pixel image width and
a one-million-splat cap to constrain the first fit. Actual GPU allocation,
optimizer storage, rendering buffers and image loading still need measurement.
A cap on splat count is not a hard RAM/VRAM cap.

If memory is insufficient, try the single allowed 960-pixel reduction within
the same session. Do not add workers or retry indefinitely. A roomier L4/A10G
worker is a later option, with a new resource decision. Provision 75 GB of
encrypted gp3 scratch, check free space, and retain only selected artifacts.
No SDK unpacking, SHARP checkpoint download, Rust toolchain, remote desktop,
Lambda, queue or general pipeline service is needed for the proposed release
route.

## Input and frame preparation

Use `data/clips/01-sculpture-orbit.mp4`: 30 seconds, 1920×1080, 30 fps. See
the footage manifest (historical reference: `../../docs/footage.json`) and
source terms (historical reference: `../../docs/footage-sources.md`). Its stationary textured sculpture
and changing camera position make it our strongest first static candidate.
Coverage is still limited to what the clip actually observes.

Extract frames at original indices `0, 15, 30, …, 885`: 60 images spaced by
0.5 seconds. Preserve original-resolution, zero-padded PNG names such as
`frame-000150.png`, and each decoded presentation timestamp. Clip 5 seconds,
frame 150, is the existing SHARP comparison view. Original recording time is
clip time plus the manifest's trim offset. Do not interpolate frames or replace
timestamp provenance with output image numbering.

Write `frames.json` with clip/source hashes, image hashes, original index,
actual timestamp and extraction command/version. Preserve original images;
undistortion and training resize are separate documented transformations.
Review a contact sheet for blur, cuts, changing zoom, weak overlap and moving
people. Begin without a mask-generation system. If visitors dominate matches
or produce prominent ghosts, document the issue and use a small manual mask
set later. Masks used by COLMAP and Brush have separate naming/loading rules;
verify alignment after undistortion rather than assuming they transfer intact.

## Recover cameras before fitting

Prepare a COLMAP dataset with one shared camera, starting with SIMPLE_RADIAL.
Use incremental sparse reconstruction; do not run dense stereo or meshing.
For 60 images, exhaustive matching means at most 1,770 distinct pairs. This is
simple and avoids choosing video-neighbor settings before we know we need them.
Use CPU feature extraction/matching initially if headless GPU configuration
is troublesome; optimize only if it blocks the bounded trial.

Install/pin the available COLMAP build and save its version and command help.
Flags differ across versions: current documentation uses
`FeatureExtraction.use_gpu`/`FeatureMatching.use_gpu`; older builds use
`SiftExtraction.use_gpu`/`SiftMatching.use_gpu`. The same distinction affects
some image-size/thread settings. Select flags from that binary's help, never
blindly mix versions. [COLMAP CLI documentation](https://colmap.github.io/cli.html).

The command sequence below is a **future procedure**, not a completed run.
`dataset` is a dedicated scratch directory containing only this preparation;
`selected_model` must be chosen after examining all reconstructed components.
Append version-checked CPU/thread options to the first two commands as needed:

```bash
colmap feature_extractor \
  --database_path "$dataset/database.db" \
  --image_path "$dataset/images" \
  --ImageReader.single_camera 1 \
  --ImageReader.camera_model SIMPLE_RADIAL
colmap exhaustive_matcher --database_path "$dataset/database.db"
mkdir -p "$dataset/sparse"
colmap mapper \
  --database_path "$dataset/database.db" \
  --image_path "$dataset/images" \
  --output_path "$dataset/sparse"
colmap model_analyzer --path "$selected_model"
colmap image_undistorter \
  --image_path "$dataset/images" \
  --input_path "$selected_model" \
  --output_path "$dataset/undistorted" \
  --output_type COLMAP --max_image_size 1280
```

Allow approximately 30 minutes for camera preparation in the first session,
with a diagnostic stop if it runs longer. This is a proposed allowance, not a
measured runtime. Save the database and camera model for later reuse by gsplat
or another static method, so future comparisons need not repeat this stage.

### Camera quality gate

Inspect the registered trajectory and sparse geometry before spending time on
Brush. Proposed acceptance criteria for this clip:

- At least 48/60 views in one coherent component (80% is our trial heuristic).
- Frame 150 has a valid pose for the SHARP comparison.
- Camera positions follow a plausible continuous path without large jumps.
- Sculpture/ground geometry is recognizable; focal estimates are plausible.
- No large disconnected fragments or obviously extreme reprojection errors.

Save registration counts, rejected filenames, component sizes, focal parameters,
reprojection statistics and a trajectory/point-cloud visualization. If a gate
fails, stop and diagnose blurred sampling, insufficient baseline, repeated
patterns, moving content or calibration. Do not interpret a camera-estimation
failure as a failed Brush representation.

Use the selected model alone in the exported dataset. v0.3.0 picks a camera
file from those it finds; exposing several reconstructions risks fitting the
wrong component. Its loader derives focal/principal-point cameras without
applying the original radial distortion coefficients. **Undistort first** and
retain the updated camera intrinsics, images and sparse points together.
The release accepts binary or text COLMAP files and sorts views by filename.
[Release COLMAP loader](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/formats/colmap.rs).

## Small bounded fit

Use the undistorted dataset, whose layout is approximately:

```text
undistorted/
  images/frame-000000.png …
  sparse/cameras.bin
  sparse/images.bin
  sparse/points3D.bin
```

Check actual files rather than assuming `sparse/0` is required. Reserve every
10th registered view from Gaussian fitting with `--eval-split-every 10` and
save the exact resulting filenames. If every sampled view registers, frame 150
is one of the evaluation views. Missing registrations change the sorted-index
split; verify the membership instead of promising that frame 150 is held out.
Evaluation images participated in COLMAP pose estimation and sparse initialization:
these are held out from splat fitting, not an entirely independent geometry test.

Start with a 2,000-step smoke fit, at most 20 minutes, to verify GPU use, finite
losses and a readable export. Then, if it is viable and the session has time,
perform one fresh 10,000-step fit, at most 90 minutes. Keep learning-rate
settings at the released defaults and stop growth at step 5,000 for the main
fit. This is a modest first quality trial, not a claim that 10,000 steps is
converged. The default 30,000 steps and ten-million-splat cap are unnecessary
for our first capability check.

Planned main command; validate against the downloaded binary's help:

```bash
brush_app "$dataset/undistorted" \
  --total-steps 10000 \
  --max-resolution 1280 \
  --max-splats 1000000 \
  --growth-stop-iter 5000 \
  --eval-split-every 10 \
  --eval-every 1000 \
  --eval-save-to-disk \
  --export-every 1000 \
  --export-path "$run_output" \
  --seed 42
```

For the smoke fit, set `--total-steps 2000` and `--growth-stop-iter 1000`, with
a separate output directory. A positional dataset disables the viewer by
default in v0.3.0. Capture complete logs, parsed options, loaded train/eval
counts, training steps, Gaussian count, wall time and sampled RAM/VRAM.
[Release training configuration](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-train/src/config.rs),
[dataset options](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/config.rs),
[export/evaluation options](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-process/src/config.rs).

Keep periodic PLY exports as recovery artifacts. Do not assume a Gaussian PLY
is a complete optimizer checkpoint or that `--start-iter` alone restores all
training state. A clean short smoke fit followed by a fresh main fit is simpler
than implementing resume semantics before we have a useful result.

## Export and minimum viewer work

First inspect native/reference renders at reconstructed camera poses and the
Gaussian export. If Brush's GUI is available on a GPU-capable local system,
open the PLY there. Otherwise keep its saved evaluation renders and use our
existing harness for interactive inspection; installing a cloud desktop is not
a prerequisite.

Preserve the original export, then publish the selected actual Gaussian file
as `output/runs/<run-id>/scene.ply`, with `run.json`, camera data, provenance,
configuration and measurements. Confirm finite positions/scales/opacities,
Gaussian properties and a plausible bounding box. A COLMAP point-cloud PLY is
not the trained Gaussian scene. Use the ordinary PLY first; compressed formats
are optional after compatibility is demonstrated.

The current harness can load Gaussian PLY and fit its bounding box. That is
enough for an initial spatial inspection after verifying orientation. Accurate
reset to clip 5 seconds needs additional care: our SHARP source-camera mode
assumes an origin camera and does not accept arbitrary COLMAP extrinsics.
Do not label a world-frame export `opencv` and assume this restores its pose.

Preserve `worldToCamera`, `cameraToWorld`, image name/time, dimensions, `fx`,
`fy`, `cx`, `cy`, camera model and any undistortion/export transforms. COLMAP's
pose maps world to camera; its camera center is `-Rᵀt`. Camera coordinates have
right/down/forward axes. Reconstruction scale is arbitrary without a measured
reference; do not call a movement distance metres just because the viewer
uses that label. [COLMAP format and pose conventions](https://colmap.github.io/format.html).

The smallest accurate harness extension is a recorded source-pose reset with
full intrinsics (including asymmetric focal/principal point if needed) and a
consistent conversion into Three.js coordinates. Alternatively rebase a derived
PLY into the selected camera frame; rotate Gaussian orientations/covariances
as well as centers and record the transform. Prefer the pose adapter if needed:
it preserves the original map and all registered camera poses. Do this only
after a viable splat exists. No new timeline, automatic annotations, scene
service or dynamic-model reader is required. See the
artifact contract (historical reference: `../../docs/artifact-contract.md`).

## How we decide whether it is viable

Inspect the sculpture lettering, thin edges, ground and background buildings
from clip 5 seconds and other recovered viewpoints. Then move between those
views and a little beyond them. Record useful navigation coverage, holes,
floaters, ghosted visitors, over-smoothed detail and browser responsiveness.
Do not claim unobserved rear surfaces are recovered evidence.

Compare with the actual SHARP sculpture run, using matched viewpoints and
image framing where possible. Report differences in assumed focal length and
scale. Inspect saved held-out renders and available PSNR/SSIM alongside visual
judgment; exposure changes and moving people can reduce those metrics even
when the stationary structure looks useful. Exact render comparisons must use
the same undistortion/resolution; an original distorted video frame is not a
pixel-perfect reference for an undistorted render.

Separate setup, COLMAP, fitting, export and retrieval times. Sample resource
usage throughout, including startup and refinement peaks. Measure real browser
interaction separately from screenshot capture; headless software-rendered
screenshots are not a desktop GPU performance benchmark.

Success means a real static scene navigable across several recorded camera
positions, with trustworthy reset/evidence and a clear visual comparison to
SHARP. Failure with saved diagnostics is also a useful trial result. Neither
outcome proves dynamic reconstruction.

## Cost estimate and run limits

Checked 2026-10-14 using the AWS Pricing API. Sydney `ap-southeast-2`, Linux,
shared tenancy, On-Demand, USD; catalog effective 2026-10-01. Rates are for the
whole instance. [Official regional EC2 price catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv).

| Candidate | Host RAM / GPU | USD/hour | Four hours compute |
| --- | --- | ---: | ---: |
| **g4dn.xlarge: first attempt** | 16 GiB / T4 nominal 16 GB | 0.684 | 2.736 |
| g6.xlarge | 16 GiB / L4 nominal 24 GB | 1.0464 | 4.1856 |
| g6.2xlarge | 32 GiB / L4 nominal 24 GB | 1.27107 | 5.08428 |
| g5.2xlarge | 32 GiB / A10G nominal 24 GB | 1.57584 | 6.30336 |

Current G/VT On-Demand quota is **4 vCPUs**, rechecked read-only. The xlarge
options use 4; 2xlarge requires 8 and cannot currently be assumed launchable.
The earlier quota request and regional availability remain external constraints.
A T4 was obtainable for SHARP, but that does not guarantee current capacity.
No Spot setup is needed for this short first test.

Plan for **1–2 hours total worker time**, including setup and camera estimation:
T4 compute about **US$0.68–1.37**. Runtime is not measured for Brush. Set an
independent **four-hour cutoff from launch**, including setup/debugging, giving
**US$2.74 maximum planned T4 compute**. Allocate **US$5 for this one session**
including a modest storage/request/transfer allowance, before tax. This is a
planning allowance, not a billing-enforced dollar cap.

75 GB gp3 at the earlier checked Sydney rate of US$0.096/GB-month is US$7.20
if left for a month, approximately US$0.04 for four hours on a 730-hour basis.
Recheck storage pricing at launch. Retained S3 objects/versions, public IPv4,
requests, logs and internet download charges are additional; keep outputs
modest and record downloaded bytes. Do not provision a NAT gateway. CPU
preparation on the same instance is already included in its hourly charge.

Execution bounds:

- One clip; 60 frames; 1280-pixel training width; one-million-splat ceiling.
- One released version; one worker; 2,000-step smoke and 10,000-step main fit.
- At most one 960-pixel retry within that worker's original deadline.
- No automatic worker upgrade, second clip or longer training sweep. A setup
  correction required replacing an exited worker; at most one worker runs at
  once, and all attempts share the original session deadline and allowance.
- Camera preparation ~30-minute allowance; smoke 20; main fit 90; all work
  still subject to the four-hour session deadline.
- Stop on incoherent cameras, software GPU, repeated out-of-memory, non-finite
  training, unreadable exports or exhausted time. Preserve diagnostics first.

Reuse the SHARP job's isolation/lifecycle pattern: job-specific S3 prefix,
least-privilege worker role, tagged resources, encrypted delete-on-termination
disk, IMDSv2 and an independent automatic termination deadline. Replace its
SHARP-specific payload with these commands; do not run `sharp-worker.py` as
though it implements Brush. The local project key cannot launch EC2; provider
administration provisions only the isolated selected job, while scoped worker
permissions handle its objects. Credentials never enter browser artifacts.

Upload periodic results, retrieve and verify selected outputs, then terminate
the instance and remove only this job's temporary resources. Confirm its EBS
volume is gone and the scheduled shutdown/role/network resources are cleaned
up. Merely stopping an instance leaves storage charges. Retain the camera
dataset and selected model/logs privately for follow-up, review S3 versions,
and record remaining storage. [EC2 lifecycle and charging behavior](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html).

## Original execution prerequisites (now checked for this trial)

The original research identified the following checks before fitting:
validate the release binary on the selected Linux image, observe hardware
Vulkan use, extract/register our frames and confirm export/viewer conventions.
These checks have now passed for the small sculpture trial. Measured memory
and stage timings are in the result; larger workloads remain unmeasured.

Any further requested trial should follow
its next steps (historical reference: `next-steps.md`), extend the existing
lessons file (historical reference: `lessons.md`), and deliver one inspected static run or a clearly
attributed failure with teardown evidence. Scaling and speed work can wait
until that result shows useful capability.

## Execution updates

See lessons (historical reference: `lessons.md`) for setup corrections and measured camera preparation.
All 60 views registered in one coherent model; the dataset passed visual review.
The simple runner now seeds a pending review object before launch and can reuse
a hashed prepared dataset after setup correction. No broader S3 listing
permissions or general job orchestration were added. All worker attempts remain
subject to the original cutoff/allowance; actual fitting and inspection results
are now recorded in the completed result (historical reference: `result.md`).
