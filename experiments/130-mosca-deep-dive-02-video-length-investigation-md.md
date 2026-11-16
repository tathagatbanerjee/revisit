> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/02-video-length/investigation.md`.
> Original SHA-256: `6a4338793cbfd2624fecec23712576756db88b7389cae54e82a7752ad2666dd6`. Private media/logs are not included.

# Deep dive 2: longer videos with higher-fidelity dynamic splats

28 October 2026. Proposed work only. Read the
duration experiment cards (historical reference: `experiments.md`), parameter audit (historical reference: `../parameter-audit.md`)
and evaluation protocol (historical reference: `../evaluation.md`). No full-video rerun is started.

## What failed last time, and what remains unknown

The 19 October source was 30 seconds/900 frames at 1920×1080. We sampled 181
observations at 6 fps plus the final frame, but split the edited source before
successful inference: 153 interior observations from 0 to 25.333333 s, nine
source-only dissolve samples, and 19 separate static-outro observations.
The long dynamic interior’s native fitted-view PSNR was 10.28/15.66/21.31 dB
minimum/median/maximum; start and end were smeared in native full-SH renders.
The separate static outro’s median was 38.85 dB. Those are seen source views.
Original result (historical reference: `../../archive/2026-10-19/guildhall-full-video/result.md`).

The short good run used 36 observations at nominal 12 fps over source seconds
8–11, with the **same saved prep/fit profile bytes** as the long run. Those
profiles select 512 uniform / 2,048 dynamic tracks, 1,000 scaffold steps and
3,000 appearance steps. The camera entrypoint supplies 2,000 BA steps by default.
Our evidence audit (historical reference: `../docs/evidence-summary.json`) verifies the profile equality
and records source hashes; it does not certify the camera solution.

Four unresolved explanations deserve separate tests:

1. **Less training exposure per observation.** With the default one primary
   sampled view per photo step, 3,000/36 ≈ 83.3 selections per short observation,
   versus 3,000/153 ≈ 19.6 in the long fit. Additional correspondence renders
   exist, so these are nominal primary selections, not equal information or
   complete loss counts. Matching this rough exposure suggests 12,750 photo
   steps for the 153 observations, not a guaranteed quality cure.
2. **Camera/depth inconsistency.** Longer spans cover more room/camera motion.
   Finite depths and plausible trajectory plots do not establish correct
   correspondence, focal length or depth scale. The existing start/middle/end
   evidence does not isolate which estimate first becomes inconsistent.
3. **Support gaps and tracking errors.** Average dynamic visibility was 19.19%,
   uniform visibility 41.07%. These values include legitimate occlusion/field-of-view
   exits. Inspect correct support over actual observable intervals and overlap
   chains, not a blanket percentage threshold or invented actor identities.
4. **Sampling changes alter motion supervision.** The same photo temporal
   offsets `[1,3,8]` span approximately `[0.083,0.25,0.667]` seconds at 12 fps
   and `[0.167,0.5,1.333]` seconds at 6 fps. The reviewed velocity/acceleration
   code uses index differences, without dividing by actual source Δt. This
   makes the cadence change a real confound; it does not prove it caused the blur.

The repaired file-descriptor error occurred before optimization. The successful
retry completed; neither a timeout nor a proven OOM explains its bad output.
The dissolve was already excluded, so “fit across a shot cut” is not the cause
of the reported interior failure.

## First inspect the retained long fit locally

L00/L01 require no new worker. Recover source/frame hashes and inspect native
camera trajectories, focal length, corrected depth and track overlays across
five time bins and at the poor endpoints/better middle. Audit background
reprojection using frozen supported static tracks and manually reviewed anchor
identities. Inspect depth residuals on common visible static points and camera
translation/rotation jumps relative to support. Isolated camera speed spikes,
low-parallax ambiguity and moving-person contamination get separate labels.

Overlay native source RGB residuals and error on fixed person/background masks.
Quantify how much error is already present after camera solving, after scaffold
optimization and after appearance fitting, when those saved stages are available.
Do not infer missing intermediate states from a final fit: mark the stage
comparison unavailable and request instrumentation in the next small run.

Depth median variation across frames alone is not drift: the camera can approach
surfaces. Use re-observed static geometry and its estimated camera transform.
The audit should distinguish a hypothesis supported by observations from a
controlled causal result. Its output is a defect map, not a corrected model.

## Extend duration while holding cadence fixed

Start at nominal 12 fps and 640×360. Proposed nested half-open source intervals:
`8,11)`, `[7,13)`, `[4,16)`, `[1,19)`, then the continuous interior through the
actual 25.333333-second endpoint. The first four nominal counts are 36, 72, 144
and 216; the last is nominally 305 observations when sampling a 12 Hz target
grid through that endpoint. Freeze the actual source-frame/PTS manifest before
any execution; 30 fps sources cannot represent every 12 Hz target with exactly
equal original-frame spacing. No synthetic duplicate/interpolated RGB is allowed.
Do not append a frame without reflecting its actual interval in the time map.

This ladder keeps a common central overlap, but it also changes scene content.
Score both the common overlap and newly added beginning/end regions. If a longer
interval fails, compare its difficult regions against separately fitted short
windows of the *same* source content; do not compare raw quality against a
completely different easy view. Window controls are diagnostics until aligned.

A new shorter control extracted directly from the original can differ from the
historical encoded input. S00/S02 must record that difference, reproduce the
historical input first if recoverable, and establish the new extraction control
before attributing differences to duration.

## Training effort and schedules must be an explicit comparison

For N training observations, choose baseline exposure E=3,000/36 and a proposed
photo budget `ceil(3000*N/36)`: 3k, 6k, 12k, 18k, and about 25,417 for the final
nominal count of 305. A photometric holdout reduces N; recalculate from the
actual training manifest. These are finite work budgets, not launch permission.
Camera/scaffold effort is first held at 2k/1k to expose their separate limits.
If either fails its geometry gate, stop the length ladder and test that stage.

Changing `photo_total_steps` alone is not an isolated “same training, longer”
experiment. The solver uses total steps in learning-rate scheduling and
ratio-based growth windows. Other important events remain absolute: track-loss
cutoff 2,500, camera updates/decay/geometry regularization around 1,000, skinning
correction 1,500, and densify/reset intervals. Repeated resets may have different
counts. Run three arms at the first failed interval:

- **A:** fixed 3,000-step reference with its original schedule.
- **B:** exposure-matched total steps, leaving other explicit YAML values
  unchanged; report the implicit total-step-dependent changes.
- **C:** the same long total with a declared schedule-normalization policy.
  Scale event times/frequencies and track cutoff by `q=steps/3000`, retaining
  ratio windows and learning-rate endpoints. Log actual draw and event counts.

This separates the practical longer-budget recipe from the extra effect of
schedule normalization. It still cannot identify every event’s independent
causal contribution. If C wins, follow up with a single schedule-family ablation
rather than claiming all scaled events were necessary. Do not reset/resume from
a model-only checkpoint and call it the same optimizer trajectory.

For the historical 153-observation diagnostic, q=4.25 and 12,750 steps give
proposed event times 4,250 (decay/camera/geometry), 6,375 (skinning correction),
10,625 (track cutoff). Round scaled intervals/events deterministically and
record the policy. Changes to BA/scaffold schedules remain separate experiments.
[Source-level mapping (historical reference: `../parameter-audit.md`).

## Cameras and priors before longer optimization

If reprojection/track/depth support fails, do not spend a much larger appearance
budget. First compare BA 2,000→4,000 on the same frozen priors; separately test
photo-camera freezing versus the original update policy. Compare native camera
conditioning and independent reserved background correspondences, with all
annotation selection fixed before seeing a candidate. Increased BA iterations
need the same explicit schedule accounting as photo iterations.

If poor priors dominate, return to S05–S09 using the shortest interval that
reproduces the defect. A stronger tracker/depth pair should be qualified on the
same difficult interval before extending to the whole shot. Do not silently
swap source models only for the longest candidate.

External SfM/SLAM camera initialization is a later, code-adapter experiment if
the native camera solve remains the bottleneck. The pinned `mode: wild` route
does not directly accept an arbitrary external camera YAML switch. A supplied
trajectory needs an explicit coordinate/intrinsic/scale bridge and real
reprojection controls; imported pose count alone is insufficient. No specific
external service or new model is selected by this plan.

## Cadence, temporal regularization and coherent motion

First hold 12 fps fixed; then compare 6 versus 12 fps on an already solved
interval, at approximately matched primary exposure and documented physical
supervision horizons. Distinguish the effect of denser observations from altered
regularization. For nonuniform timestamps, an explicit Δt-aware motion-loss
adapter is a new code experiment with finite-difference controls. Do not
pretend rounding integer offsets exactly matches every real-time interval.

A 6 fps export does not become a high-temporal-fidelity result by holding its
snapshots or interpolating them in a viewer. Inspect the native model at
supported observations first. Intermediate-time evaluation must use a verified
native query/resampling path or separately instrumented deformation path; prove
its time interpretation and compare against actually withheld RGB. If the
pinned model cannot evaluate arbitrary times through the retained interface,
label it unsupported instead of inventing interpolated states. Keep cameras and
source PTS synchronized. Reordered independent frame models are not coherent 4D.

## A controlled window fallback

If 6-second windows pass and one 12-second fit fails, first compare `4,10)` and
`[8,14)` against a matched `[4,14)` single fit. Keep the two-second overlap
observed in both windows. Establish a common static-camera/world gauge with
background correspondences, transfer full similarity/covariance conventions,
and keep actual source time. Prefer a validated common camera solution when
possible, but qualify it as another initialization variable.

Score room reprojection, actor geometry, matched-time overlap and boundary
motion/opacity discontinuity. Define a single owner in the overlap before
publication; blending colour is not proof of geometric alignment. Do not combine
two misaligned actors to hide a window failure. This is an experimental
single-video windowing approach, not built-in demonstrated MoSca streaming or
successful independent-upload fusion. The edited outro remains separate.

## Cost, stopping and final deliverable

The [shared cost model (historical reference: `../investigation.md#cost-estimate-and-run-limits--28-october-2026`)
uses current A40 Secure $0.59/h catalog pricing with a fresh launch quote
required. Historical long-fit time is only an anchor. Before each larger arm,
measure photo seconds/step and growth on the shorter arm; estimate fixed stages,
photo work, new prior cost, export and retrieval separately, with a 2× margin.
Abort the next expansion if this exceeds the selected block, disk, host memory
or device-memory budget. No automatic four-hour extension or GPU upgrade.

The final report must identify the **longest interval that passes every frozen
quality gate**, its correct clock, matched comparison scenes, native full-SH
movies, camera-motion tests, full processing/session/storage costs and remaining
person/coverage defects. If only three seconds pass, that is the result. No
promise of a 30-second high-fidelity result follows from the proposed plan.
