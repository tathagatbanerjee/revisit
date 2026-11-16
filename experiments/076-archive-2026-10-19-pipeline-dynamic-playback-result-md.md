> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/dynamic-playback/result.md`.
> Original SHA-256: `9c5e859bdff0308576011b6e286b01728b2d38854c439f2b6ca3beef906298aa`. Private media/logs are not included.

# Milestone 2 result: independent time and viewpoint

Completed 2026-10-14. **The interaction is demonstrated with a real published
time-dependent Gaussian reconstruction.** It does not establish reconstruction
of our own footage or automatic inference of missing chair movements.

## Try it

Reload http://localhost:4318. Select **Dynamic output playback**, then
**Moving boxes · published dynamic reconstruction**. Pause/scrub, orbit or pan,
then play from that viewpoint. Reset returns to the configured inspection view.
A manual annotation can be labelled **Best guess / inferred** and exported.

Run: `output/runs/dynamic-boxes-published-20frames/` (ignored).
It contains `run.json`, 20 PLY snapshots, `provenance.json`,
`export-report.json`, `conversion-check.json`, and `inspection/` screenshots,
annotations, browser checks, memory samples and screen recording.

## Input and conversion

The [Dynamic3DGaussians](https://github.com/JonathonLuiten/Dynamic3DGaussians)
`boxes` scene is a reconstruction of synchronized CMU Panoptic multiview
recordings. Credit Luiten, Kopanas, Leibe and Ramanan (3DV 2024), and Joo et al.,
*Panoptic Studio: A Massively Multiview System for Social Motion Capture*,
ICCV 2015. Research/noncommercial input; not commercially cleared or committed.
See investigation (historical reference: `investigation.md`) for the separate code/data terms.

Downloaded just one 1,954,472,326-byte compressed ZIP member, rather than the
11.57 GB six-scene archive. Download/decompression took 292.67 seconds, with
ZIP CRC verified. Checkpoint SHA-256:
`fc13fb5702d3888aa1adcf38c04a0583aee4719041ca48602e7d57afc3a9f4c7`.
Inspected native viewer source at `7dbbd4dec404308524ff402756bdb8143a2589b0`;
its CUDA/Open3D viewer was not installed. Used CPU memory maps and our
Spark 2.3.1 / Three.js 0.180.0 browser viewer. No training or neural inference.

Native data: 150 timesteps, 351,422 persistent Gaussians, 20 Hz. Exported indices
0,4,…,76 at 5 Hz, covering **0–3.8 seconds**. Retained every fourth Gaussian
index, consistently across time: **87,856 Gaussians/frame**. Positions, scales
and opacity logits match the retained checkpoint values exactly; RGB ↔ degree
zero SH differs by at most 7.63e-6, and normalized quaternion lengths by
1.79e-7. Coordinates are shared native OpenCV with a display X rotation of pi.

## Observed behavior

The scene shows a person bending down and lifting/handling a box near a stack.
That change is visible from the front and a side viewpoint, while wall/floor
landmarks stay in place. Rendered person and boxes are recognizable. There are
blurred edges, holes, colored speckles and background artifacts, particularly
with the reduced preview and alternative view. The default native inspection
pose crops some lower-body content; pan/zoom can change the framing.

- Seeking from 0 to 3.8 s preserves camera position, orientation and orbit target.
- Orbiting the paused 3.8 s scene changes viewpoint without changing time.
- Rewinding from the side view retains that viewpoint.
- Playing from the side and manually pausing at **1.2 s** retains the camera.
- Numeric camera changes during time-only operations: maximum error
  **0**, against a 1e-9 tolerance in the instrumented check.
- No unrelated source video is substituted. Scene-relative time is known;
  original recording/UTC time is not attached.
- Exported manual markers retain `evidenceStatus: inferred`, with null source
  clip/original recording time when footage is absent.

The position check also finds foreground median displacement ~0.2208 native
units between endpoints, versus ~0.000135 for background. Those are model
statistics, not calibrated metres or ground-truth tracking accuracy.

## Resources, playback and cost

Final export: **2.79 seconds**, **326.4 MiB process RSS**,
**119,493,900 bytes** of PLYs (~114 MiB; ~5.70 MiB/snapshot).
Final browser-inspection process tree sampled peak: **1519.9 MiB** (~1.48 GiB),
including Node, Chromium and the recording encoder; summed RSS can count shared
pages twice. Local source, outputs and preserved first-trial media remain well
within the 8 GB disk allowance. No AWS resources launched: **US$0 incremental
AWS cost**. Browser processes and temporary fixture servers exited; only the
existing viewer service was rebuilt.

This is nearest-preceding snapshot playback, without interpolation. The clock
waits during loading and advances at most 0.1 s per rendered frame to keep
Pause usable on slow software rendering. Scene time can run much slower than
wall time. SwiftShader screenshots prove interaction, not desktop GPU speed,
continuous 20 Hz replay, or source-image reconstruction accuracy.

## Verification and adjustments

Syntax checks, eight server tests, Compose validation, synthetic browser QA and
the real-asset browser inspection passed. The fixture checks include no-source
play/pause, pausing before completion, best-guess export and existing static
SHARP controls. The real asset was visually inspected from both views/times.

First export: 175,711 Gaussians/frame, 239 MB PLYs, 335.97 MiB export RSS.
Its inspection reached 1,562 MiB summed RSS, above the 1.5 GiB target; the
final preview halves the count. That full-density run is preserved in
`working/dynamic-playback/full-density-trial/`. Earlier checks exposed camera
inertia, floating-point comparison and screenshot-before-redraw issues. The
final checker flushes/disables test-page inertia, uses a 1e-9 pose tolerance,
and waits for rendered frames. The initial automatic clock could skip ahead
on slow renders; the bounded clock now passes an explicit mid-event pause.

A full actual screen recording is retained. `inspection/interaction-demo.mp4`
is a 30-second accelerated preview of that session, not a real-time performance
claim; `recording.json` records the speedup.

## What remains

Milestone 3 must reconstruct a short event from our footage. Unrecorded
transitions require separately labelled hypotheses and evidence intervals.
This test does not detect moved chairs, determine an actor/path/time through a
gap, combine asynchronous videos, persist annotations, or measure confidence.
See lessons (historical reference: `lessons.md`) and next steps (historical reference: `next-steps.md`).

## Source-camera previews added after the trial

Two real camera-image previews are now available separately: one fitting view
and one held-out view. See source material and provenance (historical reference: `../../docs/dynamic-playback-source-material.md`).
They are assembled from the authors' published JPEGs, not reconstruction renders.
Their timebase follows the authors' visualizer setting; original capture timing
and UTC are not independently verified. They are not attached automatically
to the harness timeline.
