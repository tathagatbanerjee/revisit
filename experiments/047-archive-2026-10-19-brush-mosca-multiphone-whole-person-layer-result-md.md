> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/whole-person-layer/result.md`.
> Original SHA-256: `f8fb41a4d790e4b66430b764f440de41aedb2d0124ef707232661bce55bb3527`. Private media/logs are not included.

# Complete-person layer: result

17 October 2026. The first partition fix restores stationary body parts and
standing observers in two existing fits, without retraining. It does **not**
establish multi-camera motion fusion or an overall quality advantage over the
full MoSca control. The outdoor Brush background remains visibly weaker.

## Inspect the outputs

Open http://localhost:4318 and select **Brush + MoSca · whole-person layer**.
For **Indoors · single person**, compare these three outputs:

1. **MoSca control · all points**: full fitted person and surroundings.
2. **motion-only hybrid · baseline**: missing head and substantial torso/legs.
3. **whole-person hybrid · experimental**: head, torso and legs restored;
   arms still move from the same saved motion fit.

Repeat for **Day · phones, easy**. The new hybrid restores the recording
bystanders on both sides and more of the performer's body. At the final state
the observer behind the performer remains visible. Existing background streaks,
silhouette halos and hand/body ghosting are still apparent.

Play at the initial view; pause, move the camera slightly, then scrub while
holding that viewpoint. Reset returns to the same inspection camera for all
three variants. These are 20 genuine fitted snapshots per output, with both
event endpoints, not interpolated or invented movement. The original seven-scene
experiment and all prior outputs remain separate and unchanged.

## What changed

`runpod/partition-people.py` uses the pinned native renderer to accumulate each
Gaussian's visible contributions inside and outside automatic person masks.
Colour gradients provide alpha-composited weights including occlusion. Only
temporary probe colours require gradients; no fitted parameter is updated.
The largest contribution-total versus rendered-alpha relative discrepancy was
0.00000276. The procedure, fixed thresholds and frame split were recorded in
the investigation (historical reference: `investigation.md`) before execution, with no threshold retry.

Membership is selected from **both** MoSca components and fixed through time.
The single-person foreground retains 8,111 static and 11,567 moving Gaussians;
the phone scene retains 19,953 static and 25,154 moving Gaussians. Motion-selected
background fragments can now be excluded, while stationary people are retained.

Each scene uses its existing Brush lead-camera fallback, in the unchanged MoSca
world. All three new variants use DC appearance and **no point subsampling**;
no alignment or reconstruction parameter changes. The combined model is rendered
through a common depth-sorted Gaussian renderer, including mutual occlusion.
No full-scene MoSca background is added to the hybrid: only the selected static
people are added alongside Brush and selected moving people.

## Measurements and actual visual inspection

Every fifth source frame, offset two, was excluded from semantic assignment:
seven frames indoors and six outdoors. These frames were already used to fit
MoSca. They test the partition across poses, **not independently held-out
reconstruction accuracy**. Masks are automated silhouettes with their six-pixel
safety padding removed, not manually validated semantic ground truth.

| Diagnostic, mean over partition evaluation frames | Single person | Easy phones |
| --- | ---: | ---: |
| Person-mask pixels covered by foreground alpha >0.5, old → new | 41.3% → 94.0% | 46.5% → 95.5% |
| Foreground silhouette precision against masks, old → new | 65.4% → 91.2% | 53.9% → 91.5% |
| Silhouette intersection-over-union, old → new | 0.339 → 0.862 | 0.334 → 0.877 |
| RGB absolute error inside masks, old → new, range 0–1 | 0.266 → 0.032 | 0.199 → 0.046 |
| Same RGB error for full MoSca control | 0.026 | 0.028 |

The full control still has the lowest person-region image error. Mask overlap
can include background contamination; these numbers are not measured 3D body
recall. Visual inspection of original source images, native first/final,
an intermediate partition evaluation frame, isolated foregrounds and shifted
cameras confirms actual restored people/body parts rather than merely greater
opacity from a room background. Boundary halos remain, particularly around
the indoor head/shoulders and the outdoor observers' hands.

Native inspection examples in ignored local research storage:

- Indoor old split (historical reference: `../../working/multiphone-tests/indoor-panoptic-person/people-partition-v1/motion-only-fixed-000.png`),
  new split (historical reference: `../../working/multiphone-tests/indoor-panoptic-person/people-partition-v1/people-fixed-000.png`),
  final pose (historical reference: `../../working/multiphone-tests/indoor-panoptic-person/people-partition-v1/people-fixed-035.png`).
- Phone old split (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/people-partition-v1/motion-only-fixed-000.png`),
  new split (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/people-partition-v1/people-fixed-000.png`),
  shifted final view (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/people-partition-v1/people-alternate-029.png`).

The shifted outdoor view still tears through people and furniture. The indoor
shift reveals unobserved room strips and soft/ghosted hands. The fix preserves
existing observations; it cannot recover unseen backs or make inaccurate
geometry correct. Some semantic static points stay static by construction,
so later motion beyond this short clip may require changes to reconstruction.

## Verification

All six outputs passed actual browser loading, fixed-camera seeking to the
final snapshot, frozen-time orbit, rewind, play/pause and reset, without page
errors. First/final/shifted screenshots for every variant were inspected,
including a contact sheet of all eighteen views. Chromium used SwiftShader;
these are interaction checks, not hardware-rendering performance measurements.

All 120 published states passed finite fields, normalized quaternion, strict
source clock, immutable fixed-layer and changing-motion checks. Each state was
also compared byte-for-byte with the expected unchanged native source subset:
all static/moving MoSca points in controls and all Brush/moving MoSca points
in old-split baselines, with no subsampling in any variant. Transfer
archive hashes and per-file manifests were verified; heavy artifacts remain
ignored. Harness syntax checks, all eight existing tests, Compose configuration
and Python compilation passed. See verification.json (historical reference: `verification.json`).

## Reproduction and retention

Remote, using the existing pinned environment, once per named case:

```bash
timeout 900 /workspace/compat/mosca-env/bin/python \
  /workspace/compat/partition-people.py /workspace/compat/batch/SCENE
```

Outputs are immutable `people-partition-v1/` directories. Transfer the directory
and log, verify its archive SHA-256 and every file in `hashes.json`, then locally:

```bash
working/brush-mosca/tools/bin/python runpod/publish-people.py working/multiphone-tests/SCENE
working/brush-mosca/tools/bin/python runpod/validate-people.py
working/brush-mosca/tools/bin/python runpod/validate-batch.py \
  --prefix people- --report working/multiphone-tests/people-validation.json
```

Detailed measured records: single-person report (historical reference: `indoor-panoptic-person-report.json`)
and phone report (historical reference: `outdoor-day-phones-easy-report.json`). Native checkpoints and
masks are hash-identified there. Heavy footage, memberships, native images,
models, transfer archives and browser evidence remain ignored/private.

The native commands took 5.45 seconds indoors and 7.10 seconds outdoors,
including assignment, diagnostics and image exports. PyTorch peak allocated
GPU memory was 188.6 and 424.1 MiB respectively; that excludes driver/rasterizer
allocations and is not whole-GPU peak usage. No new paid resource was created.
The successful A40 remains available under its unchanged US$4 allowance and
17 October 14:28:28 Sydney watchdog cutoff. This result does not authorize
extending that deadline.
