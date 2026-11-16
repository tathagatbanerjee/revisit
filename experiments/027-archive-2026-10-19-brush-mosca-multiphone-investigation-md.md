> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/investigation.md`.
> Original SHA-256: `9b30edd467217dbd7dad059fb43e5219082ffe7a4936ad9ed57a11cfe04d27d9`. Private media/logs are not included.

# Seven scene reconstruction batch

Continuation: the subsequent calibrated multi-view trial (historical reference: `calibrated-multiview/result.md`)
now fits two synchronized recordings into shared Gaussian states, with an
independent camera evaluated only after model freezing. Its elevated-view
person reconstruction fails visibly. This document retains the original
seven-scene batch scope and costs; the new session has separate bounds.

17 October 2026. The user requested running all downloaded video tests and
viewable outputs in the local harness. This supersedes the earlier restriction
to compatibility-only testing. Use the existing A40; no additional Pod.

## Scope and interpretation

Seven scene-level tests, covering all sets in SAMPLES.md. Use all available
training cameras for a masked static registration attempt and reserve the
manifest's withheld camera. Fit a fresh short MoSca event from one clearly
identified training camera per scene. The tested MoSca runner is monocular;
do not concatenate simultaneous views into a time sequence or claim jointly
fitted multi-camera motion. Record unused/failed views and calibration gates.

Use original 4DM JPEGs at their native 10 Hz. Use originals for the fixed-array
sets, undistorting the documented fisheye model. Use the downloaded Panoptic
excerpts/originals with their supplied intrinsics. Prepare about three seconds
per event: 30 phone frames or 36 samples at 12 Hz for the other recordings.
Night fire uses seconds 6.5–9.5 of its source clip; other events begin at zero.
Preserve source frame IDs, presentation timestamps, camera identity and source
terms. Do not repeat frames to fabricate timing or coverage.

Automated COCO person instance masks replace the earlier manual H1 visitor
rectangles for this batch. Review masks in contact sheets before static fitting;
retain shadow, missed-person and fire/smoke limitations. They are not exact
silhouettes or evidence that all motion is removed.

## Execution and gates

Reuse the pinned MoSca source, small Metric3D depth model, BootSTAPIR and RAFT
settings from the earlier successful experiment, including its documented
compatibility repairs. Pin/check previously recorded weight hashes. Inspect
priors and track visibility before expensive fitting. Use the established
1,000-step scaffold and 3,000-step appearance configuration as a small baseline.

Attempt masked static registration with each phone/camera's own intrinsics.
Inspect registered-camera counts and reprojection error before Brush fitting.
Align a successful multi-view static fit to the MoSca world using training-only
static correspondences and withheld validation. Publish a combined hybrid only
if the alignment gate passes. If a scene needs a fallback based solely on the
lead camera's recovered poses, identify that loss of multi-camera context in
the viewer title/notes and report. A failed motion fit may still produce an
honestly labelled static-only result; never invent a dynamic output.

Retain real native renders, model exports and reports. Use aligned timestamped
snapshots in output/runs and test fixed-camera playback, frozen-time orbit and
the actual final state in the browser. Keep earlier H1 and A40 baseline results.

## Cost estimate and bounds

The same A40 Secure Pod costs US$0.59/hour. Expected preparation/fitting/export
for seven short events is 1–2.5 hours (US$0.59–$1.48 compute), with uncertainty
from source limitations and setup repairs. Maximum four hours from this batch
phase's start: US$2.36 compute, plus roughly US$0.045 for the 80 GB disk over
four hours at $0.10/GB/month. The **US$4 session allowance before tax** includes
the earlier setup interval and a buffer. Do not provision more workers or
automatically enlarge inputs after failures.

The existing watchdog reads the updated deadline from runpod/working/trial.json;
verify its heartbeat. It is independent of fitting but depends on the local
host/API. Use per-case stage timeouts, keep progress in remote logs and retrieve
results after each case. Preserve a successful Pod for testing as requested,
within the updated cutoff. No persistent/network volume or ongoing extra
storage is included. Record failed attempts alongside successful outputs.

## Actual outcome, 17 October 2026

All seven short scene tests completed, with five fresh motion fits and two
motion-stage failures. Four multi-view Brush backgrounds and four explicitly
labelled lead-camera fallback backgrounds were fitted. Fourteen inspected
viewer outputs retain controls and failures; only medium motion passed the
multi-view alignment diagnostic, on five withheld static points. No jointly
fitted multi-phone motion is claimed. See the results (historical reference: `result.md`).

At the 11:35 Sydney report, estimated launch-to-report compute was US$0.81,
excluding disk/tax and subsequent retention. This is elapsed time × the verified
US$0.59/hour rate, not a provider invoice. The Pod remains running at the user's
request, with its unchanged 14:28:28 Sydney watchdog deadline and US$4 allowance.
The five completed motion-fit commands took 438–626 seconds each; those wall
times include their built-in evaluation/visualization. Whole-GPU samples every
15 seconds reached 3,792 MiB and 100% utilization during the batch; sampling can
miss peaks and overlapping work prevents per-case attribution. Allocated host
resources remain 9 vCPU/50 GB RAM; peak host RSS was not measured.

Final viewer PLYs total about 954 MB. Native fitted checkpoints, stable transfer
hashes, source clocks and full-SH reference renders remain in ignored working
storage. Pixel/semantic inspection reveals missing stationary people and body
parts in the hybrid, which the interface/finite-field tests do not detect.
