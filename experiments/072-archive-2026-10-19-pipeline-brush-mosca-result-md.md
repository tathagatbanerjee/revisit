> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-mosca/result.md`.
> Original SHA-256: `f87cf3478ef42a1c42c1dd29c79fb2b79d897f8b994fe4906841a2769e6e8bfb`. Private media/logs are not included.

# H1 result: Brush background + reused MoSca motion

2026-10-14. **One shared scene now contains a fitted Brush architectural background
and the moving component of the existing Guildhall MoSca model.** Its time and
viewpoint controls work independently. The bounded first test is completed and
GPU resources are removed. This establishes integration feasibility, **not an
overall quality improvement over MoSca alone**: conservative masks remove much
of the lower architecture/floor and leave visible streaks at the boundary.

Open **http://localhost:4318**, select **Brush + MoSca hybrid scene**, then
**H1 · Brush + MoSca hybrid**. Freeze time and orbit modestly; hold the camera
while seeking or playing the 2.9167-second sequence. The event comes from original
Guildhall recording 58–61 s; source UTC is unknown. Source previews remain under
`/clips/brush-mosca/guildhall-a.mp4` and `guildhall-later.mp4`.

## What actually happened

- We reused the prior 36-frame MoSca fit and its 20 full native snapshots, not
  retrained motion or invented trajectories. The exporter concatenates static
  then dynamic Gaussians, so the retained static count identifies the moving
  slice consistently at every time. The camera checkpoint was hash-verified and
  read through an allowlisted tensor-state reader; camera zero/K match the prior
  native export. All 36 poses were preserved.
- CPU PyCOLMAP 4.2.1 registered the reviewed Brush frames locally. The first two
  39-frame attempts registered 33 views: 20/20 from A and 13/19 from later, below
  the proposed per-clip gate. Their logs/models remain retained. We narrowed the
  later input to source time ≤68 s rather than silently lowering the threshold.
- The final 30-frame input registered **30/30**, comprising 20 views from A and
  10 from later. Median sparse reprojection error **0.291 px**, 5,501 points;
  final registration took **10.49 s**. Both inputs share one camera's estimated
  intrinsics; they are adjacent segments of one moving-camera recording, not two
  simultaneous independent camera captures.
- Manual whole-grid review supported a conservative mask keeping the top 220 of
  360 pixels. The first 160-pixel band was too restrictive; both attempts remain
  documented. This excludes visitors but sacrifices lower surfaces. COLMAP
  feature masks and Brush same-stem grayscale masks use different paths.
  Images/masks were undistorted together into the same PINHOLE camera/world.
- One US East A10G `g5.xlarge` worker verified its hardware Vulkan adapter. A
  20-step masked-load smoke completed, then Brush v0.3.0 fitted **3,000 steps**,
  growth stopping at 1,800, producing **9,912 Gaussians**. Smoke command took
  **8.12 s**, fit command **23.88 s**; the native fit log reports about 22 s.
  Fifteen-second sampling observed **367 MiB GPU memory and 63% utilization**
  during fitting. That is sampled device use, not a complete peak/host-RAM claim.
- One positive-scale similarity aligned MoSca to the Brush world. Static Gaussian
  centers were matched to repeated source-image observations of static COLMAP
  points: 1,235 correspondences, 778 fitting inliers, 247 withheld points.
  RANSAC/Umeyama initially gave 3.16 px withheld median. Reprojection refinement
  used only fitting points and yielded **1.509 px withheld median**, passing the
  diagnostic three-pixel gate. Validation points did not tune the transform.
  Median camera-orientation disagreement is **1.44°**. This is not calibrated
  geometry: native Gaussian centers approximate surfaces and both cameras are
  estimated. Scale is **15.795**, in arbitrary world units, not meters.
- Means, orientations and log-scales were transformed consistently, once for
  all times. MoSca's native static background is excluded from the hybrid. Its
  28,376 dynamic Gaussians use a fixed stride 2 (14,188 displayed); all 9,912
  Brush background primitives are kept. Hybrid total: **24,100/state**, 20 states,
  about **32 MB** in the viewer run. DC colour matches the comparison exports;
  the untouched higher-order-SH Brush model remains separately inspectable.

## Inspection

Four matched comparison runs use the same initial source camera and three
held-out camera poses:

| Viewer run | Content |
| --- | --- |
| `brush-h1-background` | Brush background, DC colour |
| `mosca-h1-aligned` | Complete prior MoSca scene in Brush coordinates, DC colour |
| `mosca-h1-foreground` | Aligned MoSca moving component alone |
| `brush-mosca-h1` | Brush background plus that moving component |
| `brush-h1-background-native` | Untouched Brush export with original SH appearance |

Seven withheld Brush images were localized against the **frozen** training map
using SIFT/PnP, with 166–427 inliers and median pose reprojection errors
0.286–0.640 px. They did not update map geometry, Brush fitting or alignment.
Sixteen matched screenshots cover four conditions and four viewpoints; additional
screenshots inspect the untouched Brush export. Held-out camera positions outside
the event interval provide static-context evaluation and alternate event views,
not simultaneous ground truth for the reconstructed visitors.

Actual render inspection shows recognizable upper monuments/windows and a
blue-clothed visitor changing position over time. The moving component also
contains a red carpet patch and other artifacts: motion separation is not
semantic person segmentation. The mask boundary leaves large holes/streaks.
The complete MoSca parent has more lower-scene coverage. The hybrid does not yet
establish a wider *usable* world or consistently correct actor/architecture
occlusion, particularly around missing surfaces. A small sideways view exposes
additional errors; far navigation remains unsupported.

Browser QA passed frozen-time orbit, fixed-camera time seeking, alternate-view
rewind, play/pause, fractional endpoint loading and a manually inferred marker.
Maximum camera-pose drift was **1.07e-14**. Exact background bytes are identical
across all 20 states; moving primitive IDs stay consistent, fields finite and
quaternions normalized. No per-frame registration or motion interpolation is
used. Chromium SwiftShader checks prove interaction behavior, not desktop GPU
throughput. No harness source change or Docker rebuild was needed.

## Cost and cleanup

The worker self-shut down after exporting; models/logs were retrieved. Cleanup
completed **2026-10-14T10:17:33.858990Z** and independent verification confirmed
termination, no job volumes, and removal of temporary IAM roles/profile,
shutdown schedule and security group. Cleanup report (historical reference: `cleanup-report.json`).

US$1.006/hour; conservative launch-to-cleanup allowance **US$0.148 compute**,
including the interval after automatic shutdown. Allow roughly **US$0.20–0.40
before tax total**, not an AWS invoice. Reusing MoSca and doing cameras/alignment
locally made this much cheaper than the planning allowance. Private S3 retains
about 16.2 MB current objects / 20.7 MB including versions; media/models remain
outside Git. No GPU worker or extra batch continues.

## Evidence

Lightweight trial report (historical reference: `trial-report.json`), lessons (historical reference: `lessons.md`),
next steps (historical reference: `next-steps.md`), implementation plan (historical reference: `implementation-plan.md`).
Ignored native evidence: `working/brush-mosca/cloud-output/` and `h1/`.
Ignored browser evidence: `working/brush-mosca/browser-hybrid/`,
`browser-comparison/`, `browser-native-brush/`.
