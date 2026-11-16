> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/sharp-frozen/investigation.md`.
> Original SHA-256: `793c751c5014621d52b65b007536b81e222b2bf4da7654ee1c1afb1956de41d6`. Private media/logs are not included.

# SHARP frozen-frame investigation and execution plan

Investigated on 2026-10-14. The user has agreed to the two-frame capability demo
and authorized beginning it, using the scoped AWS worker and budget below.
Execution observations are recorded in `lessons.md`; the runbook itself is not
evidence that a command succeeded. Other pipeline experiments remain planned.

Execution has begun: two full-resolution frames are prepared with observed
timestamps and hashes, and the minimum frozen-frame viewer behavior is
implemented and checked. Sculpture frame selection changed from candidate 10 s
to 5 s for a clear view of the lettering and thickness. Guildhall remains 10 s.
Initial Sydney GPU launch attempts encountered capacity shortages; see
lessons.md (historical reference: `lessons.md`) for actual outcomes. No successful prediction is
claimed until real output has been inspected.

The first completed trial used `g4dn.xlarge` On-Demand in Sydney, selected after
L4/A10G capacity failures. AWS's live pricing API returned US$0.684/hour before
tax. It has 16 GiB host RAM and a T4 with 16 GB GPU memory, below the initial
conservative envelope. The trial runs sequentially, adds 8 GiB disk swap for
host-memory headroom, and stops on inference failure. The NVIDIA driver base AMI
requires a 75 GB root disk, encrypted and deleted on termination. A separate
AWS Scheduler target terminates the exact instance after four hours; the worker
also powers off after uploading results, with shutdown configured to terminate.
At the checked rate, four hours of compute would be US$2.736, excluding storage
and small ancillary charges. This is a capacity-driven trial, not proof that
the smaller worker is sufficient. Measurements will settle that question.

Temporary worker IAM access is limited to this job's S3 prefix; the shutdown
role can terminate only its exact instance. The existing project key remains
unchanged. No SSH ingress or credentials are placed in the viewer. The
worker controller (historical reference: `../../infrastructure/aws/sharp-worker.py`) uses the provider
administrator only for isolated compute/IAM setup and teardown, and the project
key for input/artifact transfers. Both frame predictions succeeded; the worker
and temporary infrastructure have since been removed. Real outputs are loaded
from local ignored `output/runs/`; measurements and visual observations are in
lessons.md (historical reference: `lessons.md`). No further compute is left running for inspection.

## Recommendation and scope

Use SHARP to test the smallest useful version of the braindance idea:

1. Pause a recorded video at a chosen moment.
2. Turn that single image into Gaussian geometry using pretrained inference.
3. Begin at the original camera view and allow modest spatial movement.
4. Inspect features while retaining the original image and timestamp as evidence.

SHARP is a strong first experiment because it avoids per-scene training and
camera registration across the whole recording. It tests whether a frozen
moment feels useful to inspect before we build a temporal reconstruction.

The paper targets nearby viewpoints and posture shifts, rather than walking
through an entire photograph. Its desired displacement is around half a meter;
that is an evaluation regime, not a guaranteed safe radius for our clips.
Depth errors, reflections and excessive movement are documented failure cases.
The advertised sub-second generation was measured on an A100, not our laptop
or an end-to-end AWS pipeline. [Paper, introduction and appendices D.6–D.7](https://arxiv.org/html/2512.10685v2)

Our proposed initial movement sweep is 0, 5, 10, 25 and 50 cm in the inferred
scene coordinates. Treat these as experimental settings: inferred metric scale
has not been checked against measurements in our footage.

SHARP does not jointly solve motion, recover hidden facts, or align separate
frames into one world. A person in an input frame becomes part of that frozen
prediction. Selecting a later frame produces another independent scene. A
frame bank may be useful, but calling it a coherent 4D reconstruction would
require additional evidence and machinery.

## First milestone: a small capability demo

Scope clarified on 2026-10-14: the first experiment only needs enough of the
interface to let us feel SHARP's actual capability. Full harness functionality
is not an acceptance requirement.

Start with two frozen moments: one sharp sculpture control frame, then one
Guildhall interior frame. Add a third frame only if those results leave a
specific question. Use one sequential GPU worker and the official prediction
CLI, with its fallback focal assumption explicitly recorded. Build an explicit
focal wrapper only if the baseline indicates a camera-geometry problem or we
choose to run a controlled focal comparison.

The minimum useful interface is:

- Load and switch between the two static splat results.
- Compare with the corresponding source image, or source video manually paused
  at the recorded frame time.
- Start near the source camera, allow modest camera movement, and reset to the
  source view. A correct camera/FOV setup matters more than extra controls.
- Display the frame timestamp and a short note that geometry is inferred.

The current harness already provides model loading, source-video seeking and
camera interaction. Reuse those. The highest-value small addition is a source
view/reset using a camera sidecar. Automatic seeking and a still-image panel
are conveniences; manual seeking or an image beside the viewer is sufficient
for the first demonstration. Disable or leave unused any controls that imply
unsupported playback or alignment.

Defer marker persistence, cross-frame annotations, dynamic timeline playback,
object recognition, quantitative image metrics and serverless orchestration.
They do not determine whether the frozen scene is useful to explore. Native
reference rendering is a debugging tool if the browser result looks wrong,
rather than a mandatory second pipeline before we can inspect anything.

Keep lightweight evidence even for this small demo: input/source timestamp,
focal assumption, pinned code and checkpoint hash, worker type, total runtime,
peak memory where available, output size and a few screenshots. Put actual
observations into `lessons.md` after running it. More detailed evaluation in
the runbook below is follow-up work, not a prerequisite for the first look.

The milestone succeeds when we can open both real outputs, compare each with
its source, move slightly and identify where the illusion holds or breaks. A
documented poor result is useful experimental evidence too. It does not need
to support walking around a whole scene or uninterrupted video replay.

## What was inspected

This investigation checked the official repository, paper, dependency files,
prediction/rendering code, image loader, PLY exporter and licenses. The source
revision resolved during inspection was:

```text
aed6527499ef91cba3b54c18d49a870f25947190
```

Pin that revision for the first experiment. Preserve the checkpoint SHA-256,
environment lock, input hash and worker image digest with each result. Links
below point at the inspected revision where possible, so a moving default
branch does not silently change the proposed procedure.

## Findings that affect implementation

### Input and inference

The CLI accepts images or image directories, not video. It has explicit input,
output, checkpoint and device options. Prediction supports CPU, CUDA and MPS;
optional trajectory rendering requires CUDA. The prediction path internally
resizes to 1536 × 1536, then unprojects using the original image dimensions and
focal length. We should preserve the frame's original aspect ratio and let the
official preprocessing do its work. Reducing the supplied PNG resolution alone
does not reduce the network's fixed internal resolution.
[Prediction implementation](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/cli/predict.py)

### Focal length is an explicit experimental variable

Extracted video PNGs generally have no camera EXIF. SHARP's loader then assumes
30 mm in its 35 mm equivalent convention. It converts using:

```text
focal_px = focal_mm × sqrt(width² + height²) / sqrt(36² + 24²)
```

At 1920 × 1080 this gives approximately 1527.44 px, or a 38.94° vertical field
of view. These are fallback assumptions, not measured intrinsics of Guildhall.
The loader also has a heuristic for small physical focal lengths, so an EXIF
`FocalLength` value alone should not be treated as calibrated video intrinsics.
There is no focal override flag in the inspected CLI.
[Image loader and conversion](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/utils/io.py)

Start with a clearly labelled fallback run. For the controlled variant, build a
small wrapper accepting `--focal-px`, calling `predict_image(...)` with that
value and passing the same value to `save_ply(...)`. Prefer this to inventing
EXIF or editing the upstream package. Record whether focal length came from
calibration, capture metadata, estimation, or a sweep. Video stabilization,
cropping, zoom and resizing can all change the effective intrinsics.

If horizontal field of view is known, calculate
`fx = width / (2 × tan(horizontal_fov / 2))`. If an image is resized uniformly,
scale its focal length by the same factor. Crop changes also require the
principal point to be considered; the official path assumes a centered camera
and a single focal value, so it does not represent every calibrated camera.

Do not start with equirectangular 360 imagery or raw fisheye frames. This input
path models a perspective image. A future 360 experiment needs a documented
perspective extraction with matching intrinsics, separate from this test.

### Environment and checkpoint

Upstream recommends Python 3.13. Its pinned requirements include Torch 2.8.0,
Torchvision 0.23.0 and gsplat 1.5.3, with Linux CUDA 12.8 runtime dependencies.
Use the repository's requirements rather than installing an unrelated package
called `sharp` from a package index. Confirm the actual driver/Torch/CUDA
combination on the worker. Optional gsplat rendering may require a compatible
CUDA compilation toolchain; test it separately from prediction.
[Setup instructions](https://github.com/apple-aiml-research/ml-sharp#setup)
[Pinned dependency list](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/requirements.txt)

The default checkpoint is
[sharp_2572gikvuh.pt](https://ml-site.cdn-apple.com/models/sharp/sharp_2572gikvuh.pt).
A headers-only request returned 2,809,738,232 bytes, approximately 2.62 GiB.
No checkpoint content was downloaded during this investigation. The first CLI
invocation downloads it automatically if `-c` is omitted. Our worker should
download it once to a controlled cache, hash it, and pass `-c` explicitly.
Checkpoint file size does not establish either peak RAM or peak VRAM.

### Output and browser compatibility

The exporter writes Gaussian PLY with positions, degree-zero color coefficients,
opacity logits, log scales and quaternion rotations. It additionally stores
image size, intrinsics, identity extrinsics and color-space metadata. Its
exported colors are converted to sRGB for public-renderer compatibility. Keep
this original file and camera metadata even if a later converter discards extra
PLY elements. Do not add a second gamma conversion without a comparison.
[PLY exporter and loader](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/utils/gaussians.py)

The default initializer has two Gaussian layers and stride two. At the CLI's
1536-square input, the expected count is `2 × 768 × 768 = 1,179,648`. With
14 float32 vertex properties, the calculated vertex payload is 63 MiB plus
headers/metadata. This is a source-derived estimate, not a measured output.
Check the actual count and size; browser allocations, sorting and textures use
additional memory beyond the file size.
[Initializer defaults](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/models/params.py)
[Initializer implementation](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/models/initializer.py)

Our existing viewer uses Spark `SplatMesh`, which accepts Gaussian PLY. Direct
loading is the first compatibility test; no new renderer is required initially.
Acceptance of the exact SHARP export still needs to be measured.
[Spark SplatMesh documentation](https://sparkjs.dev/docs/splat-mesh/)

### License boundary

The code and model have separate licenses. The model license restricts use to
non-commercial scientific research and academic development, and excludes
product development and commercial products/services. Calling something an
experiment does not remove that restriction. Keep this work scoped to research
evaluation; future product use needs an appropriate alternative or permission.
Retain notices and check redistribution terms before sharing weights or outputs.
[Model license](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/LICENSE_MODEL)
[Code license](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/LICENSE)

## Step-by-step first experiment

### 1. Define one bounded test and check capacity

Following this experiment's AGENTS.md (historical reference: `../../AGENTS.md`), begin with one frame
of `01-sculpture-orbit.mp4` as a static control. Then use
`03-guildhall-interior.mp4`, the SHARP package's primary interior test. Leave
the other clips for follow-up tests.

The first question is: **Can one frozen frame produce a useful nearby-view
inspection experience, with visible artifacts and resource costs recorded?**

Before installing or downloading anything, check free storage, RAM, VRAM and
other workloads. The local RTX 4070 Laptop GPU was previously observed with
8188 MiB VRAM; that is not a validated SHARP requirement. Existing WSL and
Docker tasks are active. Do not stop them to make room for this test.

For an isolated AWS trial, a GPU with roughly 24 GiB VRAM and 32–64 GiB host
RAM is a provisional starting envelope, not an upstream minimum or a guarantee.
Allow disk space for the checkpoint, dependency wheels/CUDA libraries, build
cache, source frames and outputs. Choose the exact worker after checking
availability, quotas and cost; nothing is provisioned by this document.

### 2. Select and extract a sharp frame

Review the existing contact sheets under `data/previews/`, then inspect the
actual candidate image at full size. Favor textured surfaces, clear depth
boundaries, limited blur and a meaningful feature to inspect. Avoid a visitor
covering the feature. Do not black out people before inference as an incidental
preprocessing step: that creates a new model input with its own failure mode.
Use masks for evaluation/exclusion if needed, with their purpose documented.

Use prepared-clip time 10 seconds as a candidate, not a preselected best frame.
At 30 fps, candidate frame index 300 is the zero-based frame at that time.
Confirm presentation timestamps rather than deriving time solely from frame
indices for any future variable-frame-rate input.

Example commands, from the experiment root, after execution is requested:

```bash
mkdir -p working/sharp-frozen/inputs
ffmpeg -i data/clips/01-sculpture-orbit.mp4 -vf 'select=eq(n\,300)' -frames:v 1 -fps_mode vfr working/sharp-frozen/inputs/sculpture-10s.png
ffmpeg -i data/clips/03-guildhall-interior.mp4 -vf 'select=eq(n\,300)' -frames:v 1 -fps_mode vfr working/sharp-frozen/inputs/guildhall-10s.png
sha256sum working/sharp-frozen/inputs/sculpture-10s.png working/sharp-frozen/inputs/guildhall-10s.png
```

Keep width, height and color conversion history. Lossless PNG does not undo
compression already present in the source clip. If quality is questionable,
compare against a timestamp-matched frame from the retained raw recording.
Verify the source timestamp and preserve source hashes from
footage-report.json (historical reference: `../../docs/footage-report.json`).

| Prepared frame | Candidate clip time | Original recording time |
| --- | --- | --- |
| Sculpture index 300 | 10 s | 15 s, using the 5 s trim offset |
| Guildhall index 300 | 10 s | 60 s, using the 50 s trim offset |

Record the final choice in `provenance.json`: source ID/URL/license/attribution,
raw and clip hashes, trim offset, frame index, observed timestamp, extraction
command, dimensions, input hash, and focal provenance. The full source terms
and limitations are in footage.json (historical reference: `../../docs/footage.json`).

### 3. Build an isolated, reproducible worker

Use a disposable environment under ignored `working/`, or a dedicated AWS
worker image. The existing Node viewer container is not the inference worker.
Example setup, assuming Python 3.13 is already available:

```bash
git clone https://github.com/apple-aiml-research/ml-sharp.git working/sharp-frozen/ml-sharp
git -C working/sharp-frozen/ml-sharp checkout aed6527499ef91cba3b54c18d49a870f25947190
python3.13 -m venv working/sharp-frozen/venv
source working/sharp-frozen/venv/bin/activate
cd working/sharp-frozen/ml-sharp
python -m pip install -r requirements.txt
python -m pip freeze > ../environment.freeze.txt
sharp predict --help
cd ../../..
```

Check `torch.cuda.is_available()`, device identity and available VRAM explicitly.
Record Python, Torch, gsplat, GPU, driver and CUDA versions. Verify that the
environment can import SHARP before adding optional native rendering. When
containerizing, pin the base image digest, match its CUDA/toolchain to the
installed Torch build, and test NVIDIA device access. Do not assume the
dependency runtime wheels also provide a complete `nvcc` toolchain.

### 4. Fetch and identify the checkpoint once

After confirming license scope and storage capacity:

```bash
mkdir -p working/sharp-frozen/checkpoints
curl --fail --location --output working/sharp-frozen/checkpoints/sharp_2572gikvuh.pt https://ml-site.cdn-apple.com/models/sharp/sharp_2572gikvuh.pt
sha256sum working/sharp-frozen/checkpoints/sharp_2572gikvuh.pt
```

Record the observed checksum rather than inventing a published expected hash.
For subsequent runs, require the same verified checksum and explicit checkpoint
path. Download time is a separate measurement from inference time.

### 5. Predict one frame without optional rendering

Start with the sculpture control, then repeat for Guildhall. Use separate output
directories to prevent frame names or reports from being overwritten.

```bash
mkdir -p working/sharp-frozen/predictions/sculpture
/usr/bin/time -v sharp predict -i working/sharp-frozen/inputs/sculpture-10s.png -o working/sharp-frozen/predictions/sculpture -c working/sharp-frozen/checkpoints/sharp_2572gikvuh.pt --device cuda --no-render
mkdir -p working/sharp-frozen/predictions/guildhall
/usr/bin/time -v sharp predict -i working/sharp-frozen/inputs/guildhall-10s.png -o working/sharp-frozen/predictions/guildhall -c working/sharp-frozen/checkpoints/sharp_2572gikvuh.pt --device cuda --no-render
```

Capture logs and `/usr/bin/time` output to run-specific files when implementing
the runner. These commands measure full CLI latency including checkpoint load
and export; they do not isolate neural-network inference. A later wrapper should
measure model loading, preprocessing, prediction, postprocessing and export
separately, with CUDA synchronization at GPU timing boundaries.

Record peak process RSS and Torch allocated/reserved VRAM. Device-wide VRAM
sampling is useful but can include other processes. Track failures and attempted
settings as well as successes. Stop at one frame if it exhausts resources; do
not launch a parallel batch or change precision/resolution without documenting
that deviation from the baseline.

For a warm-latency test, retain one loaded predictor and process the same frame
again, separately from the cold run. The normal directory CLI loads the model
once, but launching a new CLI process for every frame reloads it each time.

### 6. Validate the output before judging the model

Check that the expected PLY exists, has a nonzero Gaussian vertex count and
contains the required Gaussian fields. Validate finite positions/scales/colors,
quaternion validity, opacity ranges after decoding, bounding box, intrinsics,
image dimensions, file size and checksum. Use a PLY parser, not a mesh loader.

First preserve the direct export. Do not normalize/recenter geometry or strip
camera metadata to make it look tidy. Those transformations would need matching
camera and annotation transformations and would obscure scale evaluation.

Optionally run the official CUDA renderer as an independent reference:

```bash
sharp render -i working/sharp-frozen/predictions/guildhall/guildhall-10s.ply -o working/sharp-frozen/reference-renders/guildhall
```

Its video is a camera trajectory through a static predicted scene, not motion
recovered from the source video. If gsplat/toolchain setup fails, diagnose it
separately; failure of native rendering does not by itself invalidate the PLY.
[Rendering implementation](https://github.com/apple-aiml-research/ml-sharp/blob/aed6527499ef91cba3b54c18d49a870f25947190/src/sharp/cli/render.py)

### 7. Publish a static run into the existing harness

Follow the artifact contract (historical reference: `../../docs/artifact-contract.md`). Example layout:

```text
output/runs/sharp-guildhall-10s-default/
  run.json
  scene.ply
  source-frame.png
  provenance.json
  camera.json
  environment.freeze.txt
  report.md
  logs/
```

Copy `guildhall-10s.ply` to `scene.ply`, preserving the original prediction in
working storage. Store supporting files with the run; the current server does
not serve arbitrary reports or source-frame PNGs. The source video remains
available through its existing clip route.

```json
{
  "schemaVersion": 1,
  "experimentId": "sharp-frozen",
  "title": "SHARP Guildhall, clip time 10 s, fallback focal",
  "representation": "static",
  "model": "scene.ply",
  "sourceClip": "03-guildhall-interior",
  "coordinateSystem": "opencv",
  "notes": "Frozen at clip 10 s / original 60 s. Focal assumption: 30 mm equivalent. Hidden geometry is inferred; no temporal alignment has been performed.",
  "metrics": {"inferenceSeconds": null, "peakVramMiB": null}
}
```

Replace null metrics only with measurements. Local results under `output/runs/`
are ignored by Git. Reload the viewer at `http://localhost:4318` to discover a
new run. If the harness is not running, use its
documented Docker startup (historical reference: `../../output/README.md`) for this Compose project only.

### 8. Establish the source camera before exploring

SHARP uses OpenCV axes: X right, Y down, Z forward. Our viewer rotates the
model by π around X for display. With this transform the original camera remains
at the origin, looking along negative Z, with positive Y up.
[Upstream coordinate convention](https://github.com/apple-aiml-research/ml-sharp#coordinate-system)

The existing viewer camera code (historical reference: `../../output/public/app.js`) fits the full
bounding box and starts an offset orbit view. It does not read SHARP's embedded
intrinsics or restore the original camera. Upright orientation alone therefore
does not establish a fair source-view comparison. General orbit controls also
permit movement well beyond SHARP's intended view range.

Before quantitative or reproducible visual evaluation, add a small harness
extension, or use a dedicated reference-render script:

- Read camera parameters from a preserved sidecar and offer **Source view**.
- Position the displayed camera at `(0, 0, 0)`, facing negative Z after the
  OpenCV-to-display transform; target a point along that forward direction.
- Set vertical FOV to `2 × atan(height / (2 × focal_px))`, converted to degrees.
  Match source aspect ratio using a letterboxed viewport for image comparison.
- Keep the export's principal-point convention. For exact comparisons use its
  intrinsic matrix rather than only a centered Three.js FOV approximation.
- Choose near/far planes from valid geometry so nearby content is not clipped.
- Add bounded translation around the source camera. Avoid an unrestricted
  360-degree orbit as the default inspection mode.
- Show the frozen frame timestamp and seek the source video to that moment.

The initial viewer implementation now supports a static OpenCV run's
`sourceCamera` and `sourceFrameTimeSeconds`, including source pose/FOV, aspect
ratio, reset, bounded movement and automatic video seeking. See the updated
artifact contract (historical reference: `../../docs/artifact-contract.md`). Geometry remains frozen
while the source-video timeline changes. Full intrinsics and provenance remain
with the output; the browser uses a centered-camera approximation. Marker
controls are hidden in this mode. Exact projection and expanded evaluation are
follow-up work rather than requirements for the first capability demo.

If the official reference looks correct and Spark does not, investigate camera
pose, FOV, clipping, PLY loading and color handling before attributing the
difference to SHARP. If both fail similarly at the source view, investigate the
input/focal assumption and model prediction.

### 9. Evaluate quality and usefulness

Begin with side-by-side source image and source-camera render. Then perform the
bounded displacement sweep, retaining the camera pose and screenshot at each
step. Pick three features visible in the recording: for example a carved
surface, a column edge and a foreground/background occlusion boundary.

For each feature record:

- Source-view appearance, near-view detail and stability during navigation.
- Holes, floaters, smeared edges, wrong depth ordering and stretching.
- Where new background detail appears, and whether the video actually observes it.
- Approximate useful movement envelope and the first obvious failure pose.
- Whether a marker can be placed and revisited meaningfully.

Manual annotations should link back to observed source pixels/timestamps. A
raycast hit on an inferred splat is not an independently verified real location.
Export marker JSON to retain it; annotations are not automatically persisted.

Report load time, browser memory where observable, typical/low frame rate,
Gaussian count, file size, CLI time, warm prediction time, peak RAM and VRAM.
Separate browser performance from GPU inference performance. A proposed first
interaction target is responsive navigation around 30 fps on the test browser;
record actual hardware and viewport, and treat this as our criterion rather
than an upstream guarantee.

PSNR/SSIM/LPIPS against the input view can characterize reproduction once the
camera/color pipeline matches, but do not demonstrate correct novel geometry.
Neighboring video frames require known/aligned camera poses and handling moving
people before they become valid held-out comparisons. Until then, use them as
qualitative context and label that limitation. Do not compute misleading
pixelwise scores against an arbitrary camera view.

### 10. Expand only after the first result is understood

| Follow-up | What it isolates | What to retain |
| --- | --- | --- |
| Sculpture control, then Guildhall | Subject/scene sensitivity | Same environment and procedure |
| Sharp versus blurred frame in one clip | Input motion/compression sensitivity | Timestamps and blur observations |
| Focal factors 0.8×, 1×, 1.2× | Sensitivity to assumed camera geometry | Explicit focal values and camera-matched renders |
| Prepared versus timestamp-matched raw frame | Transcoding/resolution effects | Both image hashes and transformations |
| Three nearby frozen moments, e.g. 9/10/11 s | Independent-frame depth/scale drift | Separate runs and source cameras |

Focal variants need the wrapper described above. Freeze all other variables.
Do not select the nicest-looking focal value and report it as measured camera
calibration. For repeat frames, start with independent static runs. Never feed
them directly into the aligned snapshot contract just because timestamps exist.

If spatial drift is large, keep a per-moment inspection UI that resets to each
moment's camera. Persisting a world-space marker across independent predictions
would imply alignment we have not established. True continuous replay belongs
in the dynamic pipeline packages; multi-view static reconstruction is the
separate route to broader spatial coverage.

## AWS budget for the initial experiment

Prices checked on 2026-10-14 for Linux, shared-tenancy On-Demand instances in
Sydney (`ap-southeast-2`). Figures are USD before tax, without credits, Spot
discounts or reservations. The AWS regional catalog entries were effective
2026-10-01. These are planning estimates, not a quote or measured SHARP cost.

| Candidate | GPU | GPU memory | Host RAM | Compute per hour |
| --- | --- | --- | --- | --- |
| `g6.2xlarge` | NVIDIA L4 | 24 GB | 32 GiB | US$1.27107 |
| `g6.4xlarge` | NVIDIA L4 | 24 GB | 64 GiB | US$1.72042 |

[AWS Sydney regional price catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv)
and [G6 hardware specifications](https://aws.amazon.com/ec2/instance-types/g6/).

Start with `g6.2xlarge` as a candidate, subject to capacity/quota and a memory
check. If host RAM is insufficient, `g6.4xlarge` adds host RAM but keeps the
same GPU memory. A GPU out-of-memory failure needs a different response; moving
between these two sizes does not add VRAM. Neither has yet been validated for
this workload.

| Session | Assumed billed machine time | Compute estimate |
| --- | --- | --- |
| Setup, checkpoint download and a few frozen frames | 2–4 hours | US$2.54–6.88 |
| Further testing and debugging | 10–20 hours | US$12.71–34.41 |

The ranges span the two candidate instance rates. Setup/idle/debugging time is
likely to dominate a small test. We do not have a measured per-frame inference
time, so this estimate should not be extrapolated into a full-video throughput
or per-frame price.

A 50 GB gp3 disk at Sydney's checked US$0.096/GB-month costs US$4.80 if retained
for a full month, prorated for shorter retention. This assumes baseline gp3
performance without extra paid IOPS/throughput. Stopping the instance does not
delete its disk or stop storage charges. Add small allowances for S3 results,
logs, public IPv4 and any chargeable data transfer; those allowances depend on
retention, architecture and account-wide transfer usage.
[EBS pricing and billing behavior](https://aws.amazon.com/ebs/pricing/)
[VPC pricing](https://aws.amazon.com/vpc/pricing/)
[EC2 transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/).

Plan **US$5–10 for the first session**, or **US$30–50 for several iterations**.
These are allowances for a small experiment with prompt shutdown, not hard
spending limits. Four hours of `g6.2xlarge` compute is about US$5.08; leaving it
running for 24 hours costs about US$30.51 before storage and other charges.

For the first execution, set a four-hour automatic shutdown window, retain logs
and download results before teardown, and record actual billed runtime. A cost
alert can help visibility but is not a spending cap. Inspect results locally
after the worker is stopped. Avoid introducing a continuously running endpoint,
NAT gateway or other standing infrastructure for this two-frame test. Recheck
rates before launch; no compute has been provisioned by this document.

## AWS execution and later automation

The current AWS project (historical reference: `../../docs/aws-project.md`) has storage and a scoped
Lambda key, but no GPU worker. That key cannot launch EC2 or administer IAM.
Do not assume a resource group gives it those permissions. Selecting and
provisioning a worker requires a separate infrastructure change with access
limited to the selected job/worker resources.

The proposed execution flow is:

```text
source clip + explicit frame selection
  → input validation and immutable job manifest
  → GPU worker: extract frame → load SHARP → predict → validate export
  → private S3 run artifacts + report + completion manifest
  → download completed run into local output/runs/
  → Node/Spark inspection in the existing local viewer
```

Prepare frame selection and the viewer locally; run the first SHARP inference
on the isolated AWS GPU worker. A successful local GPU inference is not a
prerequisite. For the first demo, manual commands and copying validated outputs
back to the local harness are sufficient.

For later automation, prototype functions locally first: `select_frame`, `resolve_intrinsics`,
`predict_frame`, `validate_artifact`, `publish_run`. Keep SHARP behind a wrapper
so frame extraction, manifests and evaluation do not depend on its CLI layout.

Per the user's updated priority, use direct commands or a small runner on one
compatible bounded worker. Lambda validation/dispatch, Batch and queues are
optional later optimizations, not prerequisites for another SHARP trial.
Standard Lambda is not the CUDA execution target. Follow the shared
workbook (historical reference: `../workbook.md`), with costs and cutoffs saved in this investigation.
[AWS Batch GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html)

Use instance/job roles with narrowly scoped S3 prefixes, not the local static
key embedded in a worker image. Keep weights in a controlled cache and reuse a
loaded model within a job where appropriate. The viewer gets local artifacts,
not AWS credentials; direct S3 browsing is not currently implemented.

For repeatability, derive a job identity from input hash, frame timestamp,
focal parameters, source revision and checkpoint hash. Upload to a temporary
prefix, validate, then publish a completion marker last. On retry, avoid exposing
half-written runs. Persist failure logs and resource measurements. Set explicit
job timeouts and terminate disposable capacity when the job finishes. Review
retention, including S3 versions, before producing hundreds of snapshots.

## Decision gates and next implementation work

1. **Environment gate:** one sequential prediction runs within the chosen
   worker's measured limits. If not, record the failure and resize the worker
   deliberately before adding complexity.
2. **Compatibility gate:** direct PLY loads and the source camera agrees with a
   native/reference render. Resolve camera and renderer differences first.
3. **Inspection gate:** a selected observed feature is recognizable and useful
   under modest movement, with artifacts and evidence limitations documented.
4. **Frame-bank gate:** repeat moments have measured drift; select independent
   navigation or an alignment experiment accordingly.
5. **Cloud gate:** the same pinned wrapper succeeds remotely, produces complete
   artifacts, and shuts down its disposable GPU capacity.

For the first milestone, implement only frame extraction with provenance,
official CLI inference, basic artifact checks, and enough source-camera setup
to inspect the results fairly. Use manual source-video seeking if necessary.
The explicit-focal wrapper, detailed evaluation and automated cloud publishing
are subsequent improvements when an observed issue or repeated workload
justifies them. The first demo does not need a full serverless workflow,
automatic object recognition or dynamic-model training.

Use lessons.md (historical reference: `lessons.md`) for observations from actual execution. It now
contains the first trial's measurements and inspection notes. Keep measured
results separate from the assumptions and proposed thresholds in this plan.
