> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/mosca-dynamic/investigation.md`.
> Original SHA-256: `cdae25ba89522fed0aae923a2da03428d2191770ae424ee793c53e56f3f76727`. Private media/logs are not included.

# MoSca investigation and bounded first trial

Started 2026-10-14 under the user's explicit request to run MoSca according to
the workbook (historical reference: `../workbook.md`). This is the active custom-video dynamic test.
The three Brush motion approaches remain future work in Brush's next steps.

## Aim and input

Recover a shared static scene plus deforming/moving foreground from a single
video, then independently navigate and select time. MoSca uses depth and point
tracking priors to build a 4D motion scaffold, jointly estimate camera geometry,
and fit Gaussian appearance/geometry attached to that scaffold. This is fitting
our own video, unlike Milestone 2's downloaded completed reconstruction.
[Paper](https://arxiv.org/abs/2405.17421),
[official code](https://github.com/JiahuiLei/MoSca).

Pin MoSca `02404d2841b4e0dc2d9074860950bce5da579656`. Source is cached under
ignored `working/mosca-dynamic/source/`; no third-party code is vendored in Git.
Start with a short subset of the bundled duck example to validate setup and
motion fitting. These example images are retained privately as a research demo,
not claimed as our footage or commercially cleared media. If that succeeds,
use the prepared Guildhall 8–11 s interval: 36 frames, 640×360, 12 fps, original
media 58–61 s, two visitors walking before stable monuments. Its source/provenance
and limitations are recorded in the RiGS investigation; preserve that input.
Limited camera translation, occlusions and weak depth/track estimates can fail.

## Selected simple route

The default demo uses DepthCrafter + SpaTracker with large inference/track
batches. For a small bounded test, use supported **Metric3Dv2 small**, **BootsTAPIR
v2**, and **RAFT** instead; no diffusion depth model or SpaTracker installation.
Metric3D depth is estimated, not measured ground truth. Use 512 initial tracks
plus 512 dynamic tracks, 128-query chunks, one-step optical flow and four CPU
threads for epipolar analysis. Pin and hash source/checkpoints where downloaded.

Run direct native Python commands on one isolated CUDA worker. Install an
isolated Python 3.10 environment with PyTorch 2.1/CUDA 11.8-compatible binaries,
PyTorch3D/PyG geometry support and only selected inference dependencies. The
original installer deletes its named conda environment, installs all rendering
backends and evaluation/JAX tools, and is not run unmodified. Compile
`simple-knn`, `native_add3`, and the native renderer imported by its visualization helpers, with two build jobs.
No Lambda, queue, API service or new deployment framework.

Metric3D's small-model selector is already supported by `MoCaPrep`; its public
CLI factory does not expose that argument. A small documented patch passes the
profile setting through. Record any other compatibility changes rather than
silently treating this as an untouched reference run. Adaptations must not
replace motion estimation with scripted animation or independent frame fitting.

## Terms

MoSca author code (principally `lib_moca` / `lib_mosca`) is MIT. The author
explicitly excludes third-party priors/renderers from that blanket grant.
Metric3D source is BSD-2-Clause; RAFT BSD-3-Clause; TAP-Net Apache-2.0.
The bundled modified Inria/MPII rasterizer has its research/evaluation license,
so keep this trial and native derivatives private; not commercially cleared.
Inspect official checkpoint distribution notices as well as source licenses.
Do not redistribute SDK, raw footage, model weights, screenshots or third-party
binaries in our repo. Retain licenses and hashes with private artifacts.
[Metric3D](https://github.com/YvanYin/Metric3D),
[RAFT](https://github.com/princeton-vl/RAFT),
[TAP-Net](https://github.com/google-deepmind/tapnet),
[MoSca source terms](https://github.com/JiahuiLei/MoSca#updates).

## Execution steps and gates

1. Verify source revision, image counts/resolutions/hashes and CUDA adapter.
2. Install native dependencies and fetch selected weights; run import/build
   checks before preprocessing. Save logs remotely during setup.
3. Precompute depth, flow, tracks and epipolar motion evidence for the small
   duck control, using `mosca_precompute.py --cfg <prep> --ws <workspace>`.
4. Inspect priors: finite positive depth, track visibility/continuity and dynamic
   evidence. No placeholder depth/flow/cameras or invented priors if a model fails.
5. Fit camera/background, motion scaffold and photometric Gaussians using
   `mosca_reconstruct.py --cfg <fit> --ws <workspace> --no_viz`. Proposed small
   schedule: bounded camera solve, 1,000 scaffold and 3,000 photometric steps,
   reduced Gaussian counts and appropriately adjusted refinement schedules.
   The exact profile is saved with the run. This is a viability smoke, not
   paper-quality convergence. Initialization adds work beyond photo-step count.
6. Render true checkpoint-evaluated snapshots from fixed and alternate cameras.
   Check static landmarks and foreground motion, preserving the native world.
7. Only if the control is usable and time remains, run the same small pipeline
   on the 36 Guildhall frames. Native checks precede any harness adapter.
8. Export at most 20 timestamped Gaussian snapshots if straightforward. Preserve
   activation, deformation/rotation, colours, camera transforms and source-time
   offsets. Initial point clouds/static renders are not dynamic success.
9. Retrieve checkpoint/priors, quality/resource reports and inspection outputs;
   terminate worker and verify disks/IAM/network/shutdown schedule cleanup.
   Populate lessons/next steps from the actual outcome, including bounded failures.

## Cost estimate and run bounds

Sydney `ap-southeast-2`, Linux shared-tenancy On-Demand, one **g6.xlarge**:
L4 nominal 24 GB VRAM, 16 GiB host RAM, four vCPUs. Rate **US$1.0464/hour**,
verified 2026-10-14 from the AWS Pricing API (effective 2026-10-01), with quota
rechecked at four On-Demand GPU vCPUs and no active project workers.
[Official regional price catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv).
Recheck exact price before launch. No larger worker or Spot fallback automatically.

Expected total session **1–3 hours**, including installation, downloads, example,
custom input and retrieval: **US$1.05–3.14 compute**. Hard **four-hour cutoff**
from initial launch: **US$4.19 compute**. **US$6 total session allowance** before
tax, reserving up to US$1.81 for 150 GB encrypted gp3 disk, requests, public IPv4,
bounded retrieval and short S3 retention. This is a session estimate/bound,
not an account-wide billing cap. gp3 (~US$0.096/GB-month) and S3 standard
(~US$0.025/GB-month) were verified earlier today; identify retained versions.

One worker/session; a short control (up to 30 frames), then one 36-frame custom
interval if viable. Model downloads at most 10 GB; retrieve at most 5 GB of
artifacts, initially logs and key outputs. Peak memory has not been measured;
stop on persistent OOM or unusable priors rather than renting a larger worker.
Allow bounded dependency repairs within the same deadline, never reset the
session clock. Setup cutoff 90 minutes; fitting stopped if the remaining session
cannot accommodate inspection/retrieval. Local WSL's 8 GiB GPU / RAM pressure
is avoided. Do not disrupt other Docker or Windows tasks.

Use the existing AWS project bucket and isolated-job approach. Worker instance
role grants only this job prefix; project credentials are not sent to the VM.
Configure independent EventBridge termination plus local timed poweroff;
shutdown terminates the instance. Verify schedule before proceeding with work.
Retain source/weight/config hashes, stage times, sampled RAM/VRAM, failures and
launch-to-termination cost estimate. Cleanup verifies instance, volume, IAM role/
profile, security group and schedule absence; permanent project resources remain.

## Expected deliverable and current status

Either a real moving reconstruction inspected from two viewpoints and times,
or a bounded failure report identifying setup/prior/camera/motion/fitting limits.
No successful custom reconstruction, convergence or throughput is assumed from
repository examples. Investigation and missing empty lessons/next-step files
were initialized before execution. The worker/result record follows below once
actual execution provides evidence.

## Capacity fallback before any billed launch

The initial L4 launch failed with insufficient capacity in Sydney zones a/b/c;
no instance was allocated. Retry the same prepared job with **g4dn.xlarge T4**,
16 GiB host RAM / nominal 16 GB VRAM, US$0.684/hour (checked earlier today).
This is a smaller, cheaper worker, with the same reduced inputs/track counts and
US$6 allowance/four-hour cutoff. Maximum compute becomes US$2.736. Stop on
insufficient memory; no larger or Spot worker follows automatically.

## Spot fallback after both On-Demand types lacked capacity

L4 and T4 On-Demand attempts failed in all Sydney zones without allocating a
worker. Read-only Spot check: 64 GPU vCPU quota, g6.2xlarge L4 / 32 GiB RAM
listed at US$0.6185 (zone b), US$0.715 (c), US$0.7245 (a). Select one such worker
with **US$1.0464/hour price ceiling**, same US$6/four-hour allowance and small
workload. This replaces the earlier no-Spot choice after concrete capacity
failures; it does not add another billed worker or a higher cost allowance.
The GPU is the originally selected L4; additional host RAM helps compilation.
Checkpoint/log retention and independent termination remain in place. Stop on
interruption; no automatic relaunch/reset of session budget.

## Region fallback while no instance had launched

Sydney also lacked L4 Spot and A10G On-Demand capacity. The A10G attempt used a
shortened three-hour cutoff at US$1.308/hour, but allocated no worker. Read-only
quota checks found US East (`us-east-1`) On-Demand GPU quota 768 vCPUs; Singapore
had zero. Choose **one US East g6.2xlarge L4 / 32 GiB RAM**, with its actual
On-Demand rate verified against the same US$1.0464/hour ceiling before launch.
Retain the **US$6 total / four-hour cutoff**. Sydney job security group is
removed; job IAM/profile and the original private Sydney S3 prefix are reused.
This is one billed session, not a parallel regional sweep. Cross-region input/
output transfer is included in the non-compute allowance; retrieve at most 5 GB.
Cleanup follows the region persisted in job state, including the independent
termination schedule. No changes to other AWS/Docker applications.

Metric3D source pin selected for the Torch Hub loader:
`eb5b6fac0dc155e4e52f576e304fbf11655ff339`. Record downloaded weight hashes and
all setup repairs in retained logs. Small-model configuration is passed through
by the saved one-argument factory adaptation.

## Actual bounded launch

US East L4 capacity also failed without allocating a worker. The actual trial
launched **one g5.xlarge A10G**, nominal 24 GB VRAM / 16 GiB host RAM, in
`us-east-1b` at **2026-10-14 07:04:09 UTC**. Verified On-Demand Linux price:
**US$1.006/hour**. Independent termination deadline: **11:04:10 UTC**;
maximum four-hour compute is US$4.024, within the US$6 session allowance.
The encrypted 150 GB root volume deletes on termination. Private artifacts
remain under the existing Sydney job prefix; no inbound network access.

For isolated setup repairs, the temporary worker role may additionally receive
only SSM instance registration and message-channel actions (no parameter-store
access). These are removed with the job role. The project API key is unchanged.

## First setup failure and bounded replacement

The first worker failed before preprocessing: isolated MMCV packaging lacked
`pkg_resources`. The attempted control-runner replacement also reused a repair
trigger and shared mutable status/log files; concurrent writers caused S3
`IncompleteBody`. This is an experiment-wrapper failure, not evidence against
MoSca reconstruction. Initial logs are retained under `attempt-1/`.

Corrections: install MMCV without isolated build in the pinned setuptools
environment; use Python 3.10-compatible streaming hashes; upload stable live-log
snapshots; make repair triggers unique to the numbered attempt; execute repair
commands without a second status writer; keep source adaptations idempotent.
A replacement worker is permitted only after the first is terminated, keeping
the original 11:04:10 UTC deadline and combined US$6 allowance. No overlapping
workers or reset of the session window. The temporary one-IP SSH repair rule
and provisional SSM permissions are removed; the replacement has no inbound
access. Explicit prior-review gates now precede fitting.

## Control footage and installation refinements

The bundled control is the author’s giant yellow duck-over-street example.
A contact sheet of original frames 0/10/20/30/40 was inspected: the duck’s pose
and the camera/background change. Its unusual appearance is not evidence of
real-world capture. No recording UTC or calibrated source frame rate is supplied;
retain native frame indices and label any nominal replay clock. Guildhall remains
the real-world input with known derived 12 fps timing.

A second setup conflict was concrete: scikit-image 0.22 requires imageio >=2.27,
so the earlier imageio 2.25 pin cannot coexist. Use imageio 2.34.1. Pin plyfile
1.0.3 and Hugging Face Hub 0.20.3 for this older environment. MoSca eagerly imports
benchmark helpers even in `wild` mode, requiring LPIPS 0.1.4, pandas 2.1.4 and
evo 1.29.0; these imports are installed but no benchmark quality is claimed.
The selected TAPIR inference implementation is PyTorch; unused JAX/TensorFlow
training utilities are not installed. Preserve separate package licenses.

`export-native.py` queries the actual static/dynamic checkpoints in their common
world and renders both endpoints from a fixed and a slightly translated camera.
Its PLY export retains position, rotation, scale, time-dependent opacity and DC
colour only: MoSca’s higher-order appearance is expressed in each Gaussian’s
local frame, so blindly copying its SH coefficients into an ordinary PLY would
be incorrect. Native previews keep learned appearance. This simplification
limits viewer appearance fidelity, not the evaluated motion geometry.

## Source-release import repair

At the selected commit, `lib_mosca/camera.py` is a tracked regular file (Git mode
100644) containing only `../lib_moca/camera.py`, rather than runnable Python or
a symbolic link. Native imports therefore raise `SyntaxError`. Restore its
contents from the matching tracked `lib_moca/camera.py`; preserve that source’s
MIT terms. The saved runner includes this explicit idempotent repair. No camera
estimation is fabricated or replaced. Native import checks then passed and the
control preprocessing began.

## Prior-review control failure and final bounded attempt

The second worker completed real depth, RAFT flow and BootsTAPIR tracking.
The review gate then read an absent S3 object. With job-scoped Get/Put access
and no bucket-list permission, S3 returned AccessDenied rather than NoSuchKey,
so the controller stopped. Retained priors establish preprocessing viability,
not dynamic fitting. Pre-create false review objects before opening the launch
gate; no broader bucket permission is needed.

The dynamic resampling option is named `n_track_pdynamic`; `n_track_dynamic`
was ignored, causing 24,576 dynamic control tracks instead of 512. Correct the
profile key before fitting. Preserve original oversized priors as evidence.

One final sequential worker may use the corrected scripts, still sharing the
original 11:04:10 UTC termination deadline, US$6 combined session allowance,
instance price ceiling and small inputs. The prior workers must be terminated
first. This replaces the earlier single-replacement limit after the concrete
controller failures; it adds no parallel worker, session-time reset or increased
budget. No further worker replacement follows this final attempt.

## Fitting fallback: motion-node support

With 512 uniform plus 512 dynamic tracks, camera/background solving completed,
but motion-curve filtering and spatial resampling left **19 scaffold nodes**,
below the native minimum of 32. This is a concrete small-input/sampling failure,
not successful dynamic reconstruction. Retain the rejected curves and logs.

Try one controlled density increase to **2,048 dynamic queries** (512 uniform,
same 128-query chunks), regenerate the actual priors on the same 25 frames,
check numerical validity/visibility, then retry the unchanged fitting schedule.
The worker, resolution, Gaussian initialization, cost and original deadline
remain bounded. Apply this density to the subsequent Guildhall preprocessing
only if the control succeeds. Do not lower the native minimum or invent motion
curves merely to bypass the failure. No further worker launch follows.

The denser fallback completed 1,000 scaffold optimization steps and entered
photometric fitting. At step 132 it requested a three-frame flow pair that the
reduced preprocessing profile had not computed. Align
`track_flow_interval_candidates: [1]` with `flow_steps: [1]`; long-track and
multi-frame geometric regularization remain active. This is a profile
consistency repair, not invented flow or a successful finished fit.
Native camera bundle adjustment uses its unchanged **2,000-step** default in
this profile, preceding scaffold and photometric fitting.

The upstream example also uses an ignored flow option name. The actual CLI
factory reads **`photo_track_flow_interval_candidates`**, so changing the
unprefixed example key did not fix the missing pair. Save the actual prefixed
key `[1]`, and assert it at the resume call. This is another configuration-path
issue, not a completed reconstruction.

The existing final worker was preserved during failure-evidence upload and
resumed directly through `photometric_reconstruct` using its already completed
camera and 1,000-step motion checkpoint. No new instance, camera solution or
scripted motion was introduced. A one-address temporary Instance Connect repair
rule was removed immediately after launching the resume process. The resumed
runner uses the original launch-relative cutoff and independent termination
schedule. Prior failed stages remain in `previous-status.json` and failure logs.

## Completed Guildhall fitting and optional preview failure

Guildhall completed its 3,000 photometric steps and saved all three native
checkpoints. The subsequent optional FPS helper tried to write float32 RGB as
JPEG, which the current Pillow/ImageIO writer rejects. Retain the completed
fit and reuse its checkpoints; do not rerun training solely for that report.
Checkpoint loading and fixed/alternate-view renders in `export-native.py` remain
required. No FPS result is claimed from the failed helper. Future runs cast its
0–1 RGB preview to uint8 explicitly; the saved runner records this adaptation.
The one-off completed-fit guard used in the repair is limited to this Guildhall
workspace and consumed once.

The viewer deterministically samples up to 100,000 native Gaussian indices per
state for the small MVP. The control therefore displays 76,385 of 229,155
Gaussians using stride 3. Full native snapshots/checkpoints and native renders
remain separate. Both subsampling and DC-only colour reduce appearance fidelity.
No cross-frame realignment, invented actor animation or interpolation is used.

## Final execution, cost and teardown — 2026-10-14

The author control and Guildhall native fits completed. The result (historical reference: `result.md`)
records actual profiles, timings, sampled memory, source previews and visible
quality limits. Browser checks demonstrate independent time/viewpoint control
and the fractional Guildhall replay endpoint. Twenty native time states per
input were exported; the lightweight viewer uses consistent stride-3 Gaussian
selection and DC colour. Full native checkpoints/renders remain private.

The final worker was terminated and cleanup finished at 2026-10-14T09:21:32.096353+00:00.
Independent verification at 2026-10-14T09:28:26.417355+00:00 found no job volumes, worker
roles/profile, scheduler role/schedule or either temporary security group.
Earlier instances were verified terminated before replacement; EC2 no longer
returns them at the final audit. The cleanup report (historical reference: `cleanup-report.json`) records
the exact resources, retained objects and verification scope.

The US East A10G rate was US$1.006/hour. Earlier launch-to-observed-shutdown
intervals plus final launch-to-cleanup allowance total 1.980 hours, or
**about US$1.99 compute**. This includes failed setup attempts and
inspection/transfer pauses and conservatively overcounts the final shutdown
interval. It is an operational estimate, not AWS billed usage. Allow roughly
US$0.20–0.60 extra for short-lived 150-GB gp3 disks, public IPv4, requests and
regional/download transfers: **roughly US$2.20–2.60 before tax**, comfortably
within the original US$6 session allowance. Check the bill for actual totals.

The job retains 970 current S3 objects
(1.218 GB) and
3450 versions
(2.883 GB including current objects).
There were no incomplete multipart uploads. Retained versions also incur
storage charges: at the investigation's indicative Sydney Standard rate of
US$0.025/GB-month, about US$0.07/month while unchanged. This storage remains
private deliberately; no model/media/credential files entered Git.

After the run, the runner was adjusted to avoid a duplicate final workspace
upload on success and to cast the optional FPS preview to uint8. These changes
passed syntax checks but were not verified in another paid run. No further
cloud fitting is authorized by this completed trial.
