> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/06-l40s-full-guildhall/diagnosis.md`.
> Original SHA-256: `bce642e2e79f29b30546c747cf33df3e093b1359a62a472b90dd81b1b47efc12`. Private media/logs are not included.

# Why the full Guildhall camera solve failed

The evidence points to a numerical failure in camera/depth optimization:
**supposedly co-visible points projected behind a camera, yet remained in a
positive-depth ratio loss**. A small minority of these constraints overwhelmed
that loss. The optimizer then degraded an initially useful camera scaffold.
The L40S itself passed its native computation checks; the failure mechanism is
reproducible on CPU without allocating another worker.

This identifies a concrete failure mechanism. It does not establish which
upstream tracking/depth/initialization error first created the inconsistent
constraints, or prove that a candidate correction produces a good30s model.
No further reconstruction or paid session was run for this investigation.

## Evidence from the saved runs

The comparison is between the reviewed144-observation12s run and the
305-observation full-interior attempt. Source RGB shares the frozen original
frame grid, but the tracking queries and span differ; this is not a controlled
GPU or model comparison. The pinned camera, initializer and bundle-adjustment
source files are byte-identical between runs.

| Diagnostic |12s reference |Full interior |
| --- | ---: | ---: |
|Adjacent co-visible static tracks, median |354 |181 |
|Adjacent co-visible tracks, minimum |218 |74 |
|Initial median background projection error, CPU replay |2.21px |3.04px |
|Initial co-visible projection pairs behind camera |0% |2.87% |
|Initial depth-ratio loss, all targets |0.0524 |2056.54 |
|Depth-ratio loss on positive projected depths only |0.0524 |0.0713 |
|Depth-loss contribution from behind-camera terms |0% |99.9966% |
|First logged BA loss |0.0330 |158.9415 |
|Last logged BA loss |0.0100 |42.1534 |
|Final pooled median background projection error |1.07px |70.90px |
|Final median error on tracks with robust weight≥0.5 |1.07px |50.59px |

Initial values come from replaying the pinned adjacent-pair initializer on CPU,
then evaluating all target frames. The original GPU BA samples at most32
of305 target frames per step and includes camera smoothness. These data-loss
values therefore are not exact reproductions of its randomly sampled logged
total loss. The massive depth-loss dominance is nevertheless directly measured.

The final CPU reconstruction reproduces the stored per-frame review residuals
to better than0.001px. The error is not explained by a broken CPU/GPU diagnostic
or a few low-confidence tracks: even the higher-confidence subset is wrong.

## The problematic calculation

In the exact worker source, `lib_moca/bundle.py`:

- The cross-time mask combines source/target track visibility and robust weights.
- Its projection check excludes `abs(projected_z)<1e-5`; negative projected depth
  otherwise remains eligible. Finite camera matrices do not catch this.
- The depth consistency term includes
  `target_depth / clamp(projected_z, min=1e-6)`.

A point behind a camera has negative projected depth. Replacing that denominator
with0.000001 makes the ratio enormous, despite the point being unsuitable for
this visible positive-depth comparison. The gradient can favor reducing the
target depth instead of correcting the camera/visibility relationship.

One actual replayed constraint has target depth0.9688 and projected depth−0.0291.
Its unweighted scalar depth-ratio loss is about484,397, with a derivative of
500,000 with respect to target depth. The pinned source expression reproduces
this behavior in a CPU regression check. These are normalized scene units and
an individual term before robust averaging, not the full optimizer gradient.
Adam's adaptive updates also mean this derivative is not itself a huge parameter
step; it establishes how the wrong constraint can dominate the gradient direction.

Only2.87% of initially co-visible pairs are behind-camera in the full replay,
but they contribute99.9966% of its weighted depth-ratio loss. Restricting this
*diagnostic calculation* to positive projected depths changes that component
from2056.54 to0.0713. The12s case has no behind-camera pairs and is unchanged.
This is an isolated loss-domain counterfactual, not a tested production fix.

## What remains uncertain

The long span has fewer shared observations per camera pair, longer occlusions,
a wider camera sweep and independently inferred depths. Any combination of
track drift, false visibility/reacquisition, relative-depth inconsistencies and
accumulated camera-initialization error could create the offending constraints.
The CPU replay does not distinguish those upstream causes. It also does not
establish why the separate historical153-observation reconstruction failed.

Neither a uniformly wrong focal length nor an unusable initial camera path is
necessary to explain this attempt: the initializer's median background alignment
is about3px before BA, then degrades to about71px. Its minority invalid
constraints deserve attention before adding training steps or changing depth
models. Finite tensors and a surviving motion scaffold were insufficient gates.

## Recommended next controlled test

Keep original RGB,12Hz cadence,640×360 resolution, large Metric3D, BootsTAPIR
and the existing initialization. Reuse verified priors to avoid rerunning them.
Test a camera-solver correction first, with no appearance training until the
existing geometry review passes:

1. Validate projection depth and target depth before evaluating depth ratios.
   Handle behind-camera constraints with an explicit camera-facing/visibility
   treatment; do not feed a negative depth through a positive epsilon ratio.
2. Record rejected-pair fractions and spatial/time coverage. An optimizer must
   not appear successful by hiding or discarding difficult background points.
   Add a suitable camera-facing penalty or reject an initialization when support
   becomes inadequate. Retain robust supervision on valid observations.
3. Log separate flow, depth, correction and camera-smoothness losses, plus
   pre/post-BA geometry. A falling total loss did not imply improved geometry here.
4. Compare corrected and original geometry on the same cached inputs and seed.
   Check all time bins and the common12s region; preserve the failed control.
5. Only after geometry passes should we run the long appearance fit and separate
   outro. A new bounded manifest/session is required; earlier allocations stay
   closed and the cumulativeUS$10 ceiling remains in force.

`init_cam_with_optimal_fov_results: false` is another available *separate* test,
but is not the first recommendation: CPU identity initialization avoids these
negative depths while increasing initial median projection error to about63px.
It discards useful initial geometry. More BA steps alone also leave the bad
loss-domain treatment in place.

## Reproducibility and limits

- Final geometry reconstruction (historical reference: `docs/geometry-diagnosis.json`).
- Pinned initialization replay and loss decomposition (historical reference: `docs/initialization-replay.json`).
- Actual source-expression gradient regression (historical reference: `docs/depth-loss-regression.json`).
- Source hashes and CPU runtime (historical reference: `docs/diagnosis-provenance.json`).
- Original result, reviews and resource closure (historical reference: `results.md`).

Run from the Gaussian-splatting folder using the existing local CPU environment:

```bash
CPU_PY=archive/2026-10-19/working/shared-person/mast3r/venv/bin/python
"$CPU_PY" mosca-deep-dive/06-l40s-full-guildhall/runner/diagnose_geometry.py
"$CPU_PY" mosca-deep-dive/06-l40s-full-guildhall/runner/replay_initialization.py
"$CPU_PY" mosca-deep-dive/06-l40s-full-guildhall/runner/check_depth_loss.py
```

The scripts read the unchanged retrieved checkpoints/depths and selected pinned
source functions. Derived arrays stay in ignored `working/mosca-deep-dive/l40s-diagnosis/`.
No native run, camera20 footage, model weights or archived result was modified.
The proposed correction still needs an end-to-end reconstruction test.

## User-observed turn around16s

The user identified the camera turn at original-video16s. Temporal replay (historical reference: `docs/turn-analysis.json`)
places98.97% of behind-camera comparisons and97.39% of initial depth loss in
comparisons that cross that boundary. The largest initialized camera step is
15.733–15.833s. Footage inspection confirms a continuous pan toward a different
part of the hall, rather than the later edited dissolve. This strongly connects
the loss-domain failure to cross-turn constraints; it still does not establish
which individual tracks/depth estimates are physically wrong.

The authorized correction experiment (historical reference: `../07-depth-validity-correction/README.md`)
preserves the full clip and adds physical-depth validity and per-target support
checks. It does not assume that splitting at16s is already a validated fix.
