> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/investigation.md`.
> Original SHA-256: `de4dd235c404481f4ab20fb9c46ecd5c4360b73de6df945446a160a552495be6`. Private media/logs are not included.

# Investigation: a reproducible MoSca quality and duration program

28 October 2026. Preparation only; use the exact spelling **MoSca** when locating
source and checkpoints. This package supersedes no archived result and launches
nothing. Its two tracks answer different questions: which setup reliably
reconstructs our short input, and how far that configuration can extend in time.

## What the method and our evidence establish

MoSca uses inferred depth and point tracks to estimate cameras, construct a
motion scaffold and fit static plus deforming Gaussians. Its paper describes
monocular reconstruction as an underconstrained problem; unseen surfaces are
not recovered observations. Better fitted-source RGB alone cannot establish
better geometry. [Paper, sections 3.1–3.2](https://www.jiahuilei.com/projects/mosca/pub/mosca_v2.pdf).

Our short result (historical reference: `../archive/2026-10-19/pipeline/mosca-dynamic/result.md`)
demonstrates coarse dynamic replay, not arbitrary-view fidelity. The
long result (historical reference: `../archive/2026-10-19/guildhall-full-video/result.md`)
failed even at its fitted cameras. We need controlled experiments, rather than
an assumption that this is either an intrinsic 30-second limit or purely an
iteration shortage.

The reviewed upstream `main` is still
`02404d2841b4e0dc2d9074860950bce5da579656`, the revision we already used.
Source receipt (historical reference: `docs/upstream-source.json`) records the API check and raw-file
hashes. Reproducing our working environment also requires our documented patches,
which are distinct from that upstream revision.

## Recommended order

1. Run the CPU-only historical input/configuration audit, S00 and L00. This
   package includes a metadata/source audit; exact short-frame recovery and
   numerical camera/track diagnostics remain proposed work.
2. Define one launch manifest and budget. Run S01 hardware/native-math checks,
   then S02 exact short-control replay/reconstruction. Stop on incompatibility
   or failure to recover the control before any duration experiment.
3. Use the fixed short interval for S03–S09 quality hypotheses. Run only the
   ablation indicated by the diagnosed defect, preserving its control.
4. Freeze a short candidate and apply L01–L06: long-fit diagnosis, controlled
   length ladder, training-exposure and schedule comparisons, then camera and
   sampling checks. Skip redundant arms when an earlier gate fails.
5. Use L07–L10 only if prerequisites pass: scaffold regularization/capacity,
   separately aligned windows, observed-state playback, and confirmation of the
   longest acceptable interval. Record failures as results.

This is a conditional program, not a request to execute every listed experiment
or the Cartesian product of all settings. `experiment-plan.json` supplies
explicit dependencies, primary variables and upper work-unit counts.

## Smallest proposed paid trial

One A40 Secure Cloud Pod, one worker, one source stack and no hybrid/fusion.
First replay the saved short Guildhall checkpoint with native forward/backward
checks. Then independently rebuild the same 36-frame short input using the
recovered decode and profiles, if the input audit passes. Proposed camera,
scaffold and photo budgets: 2,000 / 1,000 / 3,000 steps, with the archived
schedules unchanged. No automatic alternative GPU or prior model.

Expected deliverable: source/environment receipts, one independently rebuilt
short control, matched native source and shifted views, foreground/background
residuals, resource/time accounting, and an independently verified closed worker.
If it fails, deliver the retained failure and the stage that failed.

## Cost estimate and run limits — 28 October 2026

Current public Runpod GraphQL catalog fields were read without account access:
A40 Secure $0.59/hour, RTX A6000 Secure $0.59/hour, RTX 4090 Secure $0.89/hour,
L40S Secure $1.09/hour, A100 PCIe Secure $1.79/hour, all USD. These are public
catalog values, not availability or regional quotes. The actual chosen region,
CPU/RAM allocation, image availability and complete rate must be recorded at
launch. Rate receipt (historical reference: `docs/runpod-rates.json`),
[API schema](https://graphql-spec.runpod.io/).

Recommended first-trial resources: Linux Ubuntu 22.04, one A40/48 GB, at least
4 vCPUs and 16 GiB host RAM (prefer 8 vCPUs/32 GiB if available at the quoted
whole-Pod rate), 80 GB ephemeral scratch, no persistent cloud storage. These are
proposed allocations, not measured minimum requirements for stronger priors.

| Scenario | Worker time | Compute at $0.59/h | Running 80 GB disk at $0.10/GB/month* | Before-tax estimate |
| --- | ---: | ---: | ---: | ---: |
| Warm setup, replay and one short rebuild | 0.5–1.5 h | $0.295–$0.885 | $0.006–$0.017 | $0.301–$0.902 |
| First-trial hard cutoff | 2 h | $1.18 | $0.022 | $1.202 plus declared overhead |

*Planning approximation using a 720-hour month. Runpod bills by elapsed time;
actual storage billing may use different month/hour rounding. Rates and disk
lifetimes are documented in [Pod pricing](https://docs.runpod.io/pods/pricing).
Do not add storage twice if a deployment quote already includes it.

**Proposed first-session allowance: US$2 before tax; proposed maximum running
time: two hours from launch attempt. Neither is authorized by this document.**
Reserve at least 20 minutes for collection and teardown; no new job starts when
its conservative estimated time plus that reserve exceeds the remaining window.
Stop setup after 20 minutes without working SSH/CUDA/native forward+backward.
One identical infrastructure retry within the same deadline is the maximum;
no changed GPU/model or extra session follows automatically.

For later quality/duration work, propose separate four-hour blocks with at most
$0.59/h compute and a US$3 before-tax allowance each. Four hours at this rate plus
80 GB running scratch is about $2.404 before other overhead. A more expensive
GPU, persistent cache, or larger disk needs a rewritten cost calculation and
explicit selected scope. A four-hour allowance does not authorize all experiments.
Stronger priors or a full-length fit may exceed a block and must be re-estimated
from the small measured arm before launch, rather than extending a live session.

The prior long Guildhall interior needed 227.63 s preparation, 833.69 s fitting
and 26.42 s export on the successful A40. Those figures establish one historical
configuration only; they do not predict a 12,750-step run or DepthCrafter runtime.
For an unmeasured run estimate fit cost as measured fixed-stage overhead plus
measured seconds/photo-step × proposed steps, with a 2× uncertainty margin and
separate export/transfer time. Record the assumption and stop on growth beyond
its resource ceiling. See the setup cost comparison (historical reference: `01-runpod-setup/investigation.md`).

Before creation, arm an external process that can terminate only this named
trial Pod at its launch-relative deadline and verify its heartbeat. An in-Pod
watchdog is a second defence, not sufficient by itself. The external watchdog
still depends on its host and provider API; it is not an account-wide billing
cap. Retrieve outputs incrementally, hash-verify local copies, terminate and
verify absence. Container-only storage cannot survive teardown. No cloud disk
is retained by default. Tax, exchange-rate conversion, pre-existing retained
storage and third-party charges are excluded and must be declared if applicable.

## Execution boundaries and records

Preserve original video, old source/fit/prior artifacts, all failed candidates,
existing viewer groups, and sealed camera20 RGB. Historical seen cameras and
Guildhall footage are development evidence. We have no new independent
Guildhall camera ground truth. Do not describe virtual views as held-out RGB.

For every run retain: `input-manifest.json`, `environment.json`, effective
`prep.yaml`/`fit.yaml`, patched-source diff and hashes, prior receipts, source
PTS, camera/depth/track summaries, per-stage logs/timing, sampled peak VRAM/RAM,
primary frame-draw counts, native checkpoints and full-SH renders, all-point
exports, evaluation masks/protocol hash, costs, transfer hashes and closure
receipt. Raw outputs belong in ignored `working/mosca-deep-dive/`, not Git.

A fit checkpoint is not necessarily a resumable training checkpoint: inspect
optimizer, RNG, topology and schedule state before claiming exact resume. For
the first controlled comparisons, restart from the same audited input and
initialization instead of extending a model-only saved state.
