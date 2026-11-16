> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `guildhall-fixed-world-workflow/docs/sculpture-30s-results.md`.
> Original SHA-256: `277048dc88234d932963d03bf4aeb85000dc8724fdeedd0d12b01972b12b0f0a`. Private media/logs are not included.

# 30-second L40S trial: measured results

Completed 29 October 2026. **Estimated cost US$1.7925 before tax; rented time
1h 36m 42s; actual appearance optimization 14m 13s.** The worker was terminated
and independently verified absent, with zero account Pods and no new volumes.
This is one integration trial, including failures and repairs, not a clean
steady-state runtime measurement. No faster GPU was rented.

[Inspect the static scene](http://localhost:4319/?run=mosca-20261029-sculpture-30s-scale-only)
or [watch the source/native comparison](http://localhost:4319/previews/core-validation/mosca-20261029-sculpture-30s-scale-only/comparison.mp4).
The frozen trial protocol (historical reference: `sculpture-30s-benchmark.md`) records choices and amendments.

## Input and outcome

A continuous 30-second sculpture orbit, original source interval 5–35s: 360
frames at nominal 12 Hz, 640×360, with original timestamps. Local COLMAP registered
all 360 cameras in one component with 23,737 sparse points. Its median sparse
reprojection residual was 0.273px. Cameras remained exactly unchanged through
background refinement and appearance. All model tensors were finite.

The retained model has **332,079 static Gaussians**, exported as a 22,581,788-byte
PLY, plus all 360 native renders. This deliberately static control omits motion
scaffolding and dynamic fitting; it does not reproduce Guild Hall's joint
static/dynamic schedule or establish dynamic replay throughput.

Median native source-view PSNR is **19.60dB**, minimum 14.82dB. First, middle,
last, worst-fit and shifted views were reviewed. The sculpture and building are
recognizable, but floors and distant surfaces soften, sky coverage is incomplete,
and some views smear or ripple. It remains exploratory and is **not quality
promoted**. Guild Hall remains our stronger demonstrated full-interior result;
PSNR across different source videos is not a controlled quality comparison.

## Measured wall times

| Stage | Time | Outcome |
| --- | ---: | --- |
| Local decode, resize, timestamps and hashing | 55.36s | Completed before GPU rental |
| Local feature extraction + matching + mapping | 77.49s | All 360 cameras registered |
| Allocation to corrected model preflight | 10m 38s | Includes boot, transfer, setup, repair and operator wait |
| Original prior preparation | 16m 39s | Stopped after depth, flow and epipolar maps; tracking not reached |
| Tracking resumed from verified cached arrays | 36.69s | Completed, 512 finite tracks |
| Original full-depth background stage | 7m 41s | Sparse geometry passed |
| Original dense propagation | 26.49s | Failed positive-depth check at frame 132 |
| Separately declared scale-only background stage | 14m 35s | Passed original gates |
| Independent sparse diagnostic | 7.36s | Passed, cameras unchanged |
| Scale-only dense propagation | 6.12s | All dense depths positive |
| **Appearance optimization, 30,000 steps** | **14m 13s** | **Completed, 35.17 steps/s** |
| Appearance wrapper including initialization/diagnostics | 21m 45s | Final checkpoint saved; optional post-fit diagnostic stopped |
| Native export | 40.68s | Completed, all 360 renders |
| Final verified retrieval | 54.20s | Earlier retrieval also overlapped work |
| **Total paid allocation** | **1h 36m 42s** | **US$1.7925 estimated before tax** |

Rows are not all additive: the training loop is inside its wrapper; retrieval
also occurred earlier. Total rental includes review, code repairs and operator
wait between stages. Rate was US$1.09/hour on one L40S, with a US$3.50 cap and a
three-hour launch-relative watchdog. This is an estimate from rented duration and
the quoted rate with a small disk allowance, not a provider invoice. The previous
closed-session estimate was US$6.4328; the resulting cumulative estimate is
US$8.2253 before tax. No worker or automatic retry remains active.

## Failures are retained separately

The original full-depth solve had 1.042px median and 1.928px worst-frame median
sparse error, with at least 69 usable anchors per frame. Nevertheless, dense
interpolation produced nonpositive/too-near depths for 12,882 of 194,221 allowed
pixels at frame 132 (6.63%); minimum depth changed from 0.495 to −0.149. No
appearance fit ran on that arm. Good sparse error alone did not protect dense
inputs. No clipping or relaxed threshold was used to force it through.

The existing native scale-only option was declared separately before appearance,
with the same frames, cameras, priors and gates. Its median sparse error was
2.883px, worst-frame median 5.368px, minimum 69 usable anchors. Local additive
corrections were exactly zero. An equivalent fast path skipped unnecessary RGB
reload/interpolation, wrote exact zero deltas and checked every dense depth;
minimum final depth was 0.00765. No failed full-depth output was overwritten.

All 30,000 appearance steps completed and final model/camera checkpoints were
verified before export. The wrapper then stalled in an optional post-fit
diagnostic and was explicitly stopped. Consequently **optimization completed**,
but **the appearance wrapper did not exit cleanly**. All logs remain available;
this is not an uninterrupted pipeline success.

Initial preflight also referenced the old Guild Hall case; the case was corrected
before scene optimization. A saved-parameter detach issue was corrected before
CPU interpolation. Preparation's exact remaining slow call was not identified:
profiler attachment was denied. Neither an unverified CPU diagnosis nor a faster
GPU speedup should be inferred from this trial.

## What to optimize next

1. Make one command return after saving and verifying its required outputs.
   Move optional diagnostic videos behind an explicit flag, use the actual case
   in preflight, and reuse the verified small sparse diagnostic instead of
   reloading all dense RGB just to inspect background error.
2. Keep the dense positive-depth gate. Treat scale-only as an explicit baseline
   option, with its quality tradeoff recorded. Decide how full-depth correction
   should satisfy dense validity before claiming the original recipe generalizes.
3. Repeat a clean baseline on another ordinary continuous clip before enlarging
   the duration or running a hardware sweep. This trial's debugging overhead is
   too large to extrapolate total production throughput.
4. If training remains the bottleneck, time the same saved inputs and same
   30,000-step fit on faster hardware. The L40S training loop used roughly 75–80%
   GPU and about 3.4GiB; the pipeline peak was 17,293MiB (about 16.9GiB). More GPU
   memory alone is not needed for this clip. Longer clips require their own check.

At the quotes inspected for this trial, A100 80GB PCIe was US$1.79/hour and H100
SXM US$3.99/hour. Compared with US$1.09/hour, they need about **1.64×** and
**3.66× end-to-end speedup**, respectively, to reduce rental cost. These are
break-even calculations, not measured performance or guaranteed availability.
If only the 14m13 training loop were twice as fast, it would save about seven
minutes of this integration session; fixing its setup/diagnostic waits has
larger immediate potential. No additional paid test is running.

## Evidence and preservation

Runtime evidence is intentionally ignored under
`working/mosca-deep-dive/execution-20261029-sculpture30/`: stage receipts, GPU
samples, preserved failures/amendments, checkpoint hashes, native renders,
`retrieval-receipt.json`, `independent-closure.json`, `publication.json` and
`api-preservation.json`. Final strict retrieval verified 6,949 stable files with
zero pending files. Media, checkpoints, generated results and credentials are
not committed.

The viewer contains 100 valid runs with zero invalid runs. All 99 previous API
records, including the 86 archived records, remain unchanged. Camera20 remains
sealed. The app's 14 tests and five camera-contract tests passed; Python runner
compilation and whitespace checks passed. Browser QA is **partial**: Chromium loaded all 332,079 points and reported ready
without page errors, but software-rendered screenshot automation timed out.
Recorded-view pixel comparison and mobile assertions are not claimed as passed.
The original catalogue bind mount was stale; only the new viewer container was
recreated, after which its new experiment was present and all 99 old API records
were rechecked unchanged. Native source/shifted images were reviewed separately.
The local `browser-verification.json` records these limits.
