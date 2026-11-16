> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/01-runpod-setup/investigation.md`.
> Original SHA-256: `11b8d8cff4518e36359f70839df858e80491277106a79476323d28e02769554c`. Private media/logs are not included.

# Deep dive 1: setting up MoSca on Runpod and improving the short result

28 October 2026. Proposed work, not an executed deployment. Read the
shared cost limits (historical reference: `../investigation.md#cost-estimate-and-run-limits--28-october-2026`)
and experiment cards (historical reference: `experiments.md`) alongside this investigation.

## What “best setup” means

Evaluate reliability, reproducibility, reconstruction quality, setup time,
processing time, peak host/device memory, and dollars per accepted result.
A faster GPU changes throughput; input geometry, priors and optimization affect
what it can reconstruct. Keep these questions separate so a machine change
cannot masquerade as a method improvement.

Our initial comparison input is the exact good Guildhall 8–11-second segment:
36 decoded observations at nominal 12 fps, 640×360. The earlier prepared input
MP4 has SHA-256 `af8be7089bdead75657f3f443213599aeb59af82a43193f66c432bd12db7c843`.
Decode hashes and actual source timestamps still need recovery in S00. The
36-frame final fit/prep profiles are present locally and equal the later
long-run profiles byte for byte; audit receipt (historical reference: `../docs/evidence-summary.json`).

## Recommended Runpod environment

Use one dedicated on-demand Pod. Start with A40 Secure because our successful
19 October run actually used it; do not make Spot interruption or a new GPU
architecture another variable in the first reproduction. Use SSH for jobs and
transfer, with a process that survives a disconnected terminal. Runpod documents
SSH as the suitable connection for long-running processes:
[connection options](https://docs.runpod.io/pods/connect-to-a-pod).

Select the previously tested `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04`
family, verify its actual registry digest and contents before creation, then
pin the selected digest. The historical digest in our
Runpod investigation (historical reference: `../../archive/2026-10-19/runpod/investigation.md`) is evidence
of the old image, not proof it remains pullable. If unavailable, report that
prerequisite and prepare an equivalent isolated environment; do not silently
switch to the current template’s Python/PyTorch/CUDA stack.

Use the existing
successful setup script (historical reference: `../../archive/2026-10-19/fresh-video-mosca-alignment/setup-worker.sh`)
as a source of known dependencies and repairs, not as an unquestioned lockfile:
it still contains unpinned packages and a historical architecture setting.
The reviewed source
[installer](https://github.com/JiahuiLei/MoSca/blob/02404d2841b4e0dc2d9074860950bce5da579656/install.sh)
removes/recreates a named conda environment and installs more backends/evaluation
packages than this trial needs. Prepare a minimal isolated environment instead.

| Layer | Initial choice and why | Record before fitting |
| --- | --- | --- |
| OS/runtime | Ubuntu 22.04, Python 3.10, PyTorch 2.1.0+cu118, torchvision 0.16.0 | Image digest, OS, driver, compiler, actual runtime versions |
| Native code | `simple-knn`, native rasterizer and `native_add3`; `GS_BACKEND=native_add3` | Source/patch hashes, architecture, build logs, forward/backward results |
| Compatibility pins | NumPy 1.26.4; preserve the known PyTorch3D/PyG/MMCV compatibility set | Complete historical `pip-freeze.txt`, wheel/archive hashes, dependency resolution |
| Priors | Metric3D-small, RAFT things, BootsTAPIR-v2 | Exact model selectors, weight hashes and generated prior hashes |
| Execution | Four CPU inference threads and two compilation jobs initially | Host resources, max jobs, thread counts, stage wall times |
| File handles | Raise soft limit to 65,536 within available hard limit, verify in child process | Both limits and effective epipolar worker count |
| Storage | 80 GB proposed ephemeral scratch, verified available space; local incremental retrieval | Actual mounts/free space, peak use and transfer receipts |

Our prior failures included a CUDA-context failure on an Ada worker and an
open-file failure before bundle optimization. These are environment failures,
not evidence that the completed model failed because it ran out of memory.
Do not infer whole-pipeline compatibility from imports or `nvidia-smi`.

The first preflight must exercise CUDA allocation/matmul, native KNN and
rasterizer forward **and backward**, depth/track inference on a small saved
sample, saved-model loading, native render/export and artifact retrieval. Test
finite values and nonzero gradients. Verify `nvcc`/Torch CUDA compatibility and
the *actual* GPU capability before building; do not reuse an A40-only extension
binary on a different candidate without checking its compiled architectures.

MoSca’s code and dependencies are separately licensed. Retain the archived
source/weights notices and review any newly selected model terms. A generic MIT
label for MoSca does not cover every renderer or prior. New DepthCrafter/SVD
weights may add access and license prerequisites; resolve them before a paid
session. [Author’s scope](https://github.com/JiahuiLei/MoSca/blob/02404d2841b4e0dc2d9074860950bce5da579656/readme.md).

## Cold installs, a reusable image, and cached data

Start by recovering the known environment. After it passes, build a private,
versioned image containing pinned dependencies, patched source and the tested
extensions; keep footage, credentials and run outputs outside the image.
Measure build/pull/setup time, not just inference time. Runpod supports custom
images/templates; packaging can reduce repeated initialization work but does
not itself change reconstruction quality.
[Custom templates](https://docs.runpod.io/pods/templates/create-custom-template).
No registry upload or image publication is requested now.

Compare a cold source install against that image using the **same GPU and
same input**. Test cache invalidation: an incompatible Torch/backend/source
hash must invalidate compiled extensions. Test that a fresh workspace does not
accidentally load a prior run’s depth, tracks or checkpoint. Reuse prior caches
only for declared ablations with matching frame/model/selector hashes.

Default to local verified retention between these bounded trials. If repeated
weight/environment setup dominates measured cost, consider a separately scoped
50–100 GB network cache with a named expiry and removal owner. Network volumes
persist independently of Pods and constrain placement; Pod volume disks survive
stops but disappear on termination, and container storage is ephemeral.
[Storage lifetimes](https://docs.runpod.io/pods/storage/types).
A stopped Pod is not a verified cleanup result if billable disks remain.

At published storage rates a 50 GB network cache costs about $3.50/month or
$0.117/day using a 30-day approximation. Compare that to measured rebuild time
saved: 15 A40 minutes are $0.1475 compute before disk. This is an illustrative
break-even calculation, not a claim that our rebuild takes 15 minutes. Include
cache creation/transfer, placement constraints and all retained days.

## Hardware comparison and cost — checked 28 October 2026

The public catalog snapshot (historical reference: `../docs/runpod-rates.json`) gives these USD/h values;
region-specific availability and full deployment rates remain unchecked.

| GPU | VRAM | Secure / Community catalog | Role in this program |
| --- | ---: | ---: | --- |
| A40 | 48 GB | $0.59 / $0.35 | First reproducible control; prior local success |
| RTX A6000 | 48 GB | $0.59 / $0.33 | Same-price candidate after compatibility checks |
| RTX 4090 | 24 GB | $0.89 / $0.34 | Potential speed candidate with less memory; new architecture build checks |
| L40S | 48 GB | $1.09 / $0.79 | Potential faster high-memory candidate; measure complete stage mix |
| A100 PCIe | 80 GB | $1.79 / $1.19 | Only if measured memory/throughput requirements justify it |

Compare the same cloud tier and work unit. Ignoring fixed overhead, L40S Secure
must finish over 1.85× faster than A40 Secure to reduce compute cost; RTX 4090
Secure over 1.51×, A100 PCIe Secure over 3.03×. Real break-even includes cold
startup, compilation, downloads, CPU-bound preprocessing and retrieval. Equal
seeds need not yield bit-identical results on different hardware; compare
quality under predefined tolerances and retain nondeterminism evidence.
A40 Secure remains a recommendation, not an asserted optimum.

Follow the proposed two-hour/US$2 first-trial envelope in the shared
investigation. For S04–S09, estimate from the actual prerequisite runs and select
one arm per bounded block. New prior-model memory and setup time are unknown.
The standalone DepthCrafter project reports different memory needs at different
resolutions; those figures do not establish the memory of MoSca’s bundled
wrapper or combined pipeline. [DepthCrafter instructions](https://github.com/Tencent/DepthCrafter#-inference).

## Quality changes worth testing, in order

**1. Reliable frame support before larger geometry.** Audit uniform tracks on
the background and dynamic tracks on the whole observed person. Increase one
query population at a time. A low average visibility over a long video is not
a standalone failure: an actor may leave the image. Measure visibility within
its observable interval, support per time bin, correct track identity and
long-range connections. Do not weaken filters simply to inflate counts.

**2. Stronger depth priors.** Compare Metric3D-small with the supported `large`
Metric3D variant first, keeping the tracker fixed. Then, if temporal depth
inconsistency is the bottleneck, compare DepthCrafter with an explicit alignment
policy and conversion check. It is a candidate for temporal consistency, not
measured depth ground truth. Its bundled wrapper resizes to multiples of 64;
record inference resolution and resampling back to the reconstruction grid.
Audit boundary alignment and static-point depth consistency before training.

**3. Tracker alternative.** Compare BootsTAPIR-v2 with a pinned CoTracker3
variant at identical frame/query support policy. MoSca’s wrapper already names
CoTracker3, but the CLI factory does not expose every version/online option.
Trace the wrapper/API/weights and add an explicit documented adapter if needed.
CoTracker distinguishes online/offline APIs; neither a moving window nor a
newer name proves correct long-term correspondences.
[Tracker’s official API](https://github.com/facebookresearch/co-tracker#quick-start).
SpaTracker/UniDepth remain later alternatives, not an all-at-once model sweep.

**4. Camera optimization and schedules.** First reproduce the control, then
compare 2,000 vs 4,000 BA steps with its other inputs fixed. Freeze vs enable
photo-stage camera updates only after a valid camera estimate. Do not expect
appearance optimization to repair an arbitrary camera failure. Schedule
comparisons are detailed in track 2.

**5. Resolution and representation.** Compare 640×360 vs 960×540 by freshly
decoding the original, not upscaling old pixels. Recompute intrinsics/priors at
the proper grid; score at a common grid and retain native-resolution crops.
Then test dynamic initial capacity separately from static capacity and, only if
needed, scaffold resolution/node growth. Native higher-order appearance and
viewer DC exports must be assessed separately. More foreground points can
fit the wrong shape more densely; foreground coverage and shifted-view geometry
remain gates.

Avoid first-round changes to mixed precision, Torch major versions, renderer
ports or multi-GPU fitting. Each needs its own compatibility/equivalence test;
MoSca’s multi-GPU reproduction script assigns independent jobs and should not
be treated as proof of distributed single-scene training. The upstream TODO
still lists a newer GSplat renderer rather than providing a drop-in switch.

The first useful outcome is a **reproducible short control plus an identified
bottleneck**, followed by one measured improvement. That is the entry gate to
longer-video experiments.
