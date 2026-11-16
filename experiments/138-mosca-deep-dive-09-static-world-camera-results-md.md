> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/09-static-world-camera/results.md`.
> Original SHA-256: `d5a0931029d302982111f6cba95eab768c1d1b9c984dc515b5f17983c5d7a10b`. Private media/logs are not included.

# Static-world camera results

**The static map and supplied-camera integration work.** All305 interior cameras
qualify, and the native fixed-camera test removes the gross late-frame drift.
The experiment still stops before motion/appearance because the final six frames
fall below the frozen64-anchor continuation gate. This is not a full-length splat.

| Stage | Result |
| --- | --- |
| Architecture-only52-keyframe control |41/52 cameras,5,457 points,0.284px sparse median; coverage FAIL |
| Visitor-mask52-keyframe control |Separate41/17-frame maps, with six shared images; coverage FAIL |
| Reprojection-based map alignment |FAIL; no accepted similarity. Only two shared triangulated feature identities |
| Same visitor masks,153 keyframes |153/153 in one native component;14,415 points;0.343px sparse median; PASS |
| Remaining152 frame poses against frozen map |152/152 PASS; at least652 inliers, worst query median0.572px, worst query p901.130px |
| Full305-frame supplied-camera/depth test |All error and camera-lock gates PASS; final anchor coverage FAIL |

The denser mapping changes the keyframe schedule, retaining the person masks,
source RGB and quality thresholds. No failed control was overwritten, and no
artificial similarity was accepted to force the room into one frame.

The full camera path passes the supplied-camera contract and source projection
review. A single positive scale0.06026775 converts static-map units into the
unchanged normalized-depth convention; frame-level background depth ratios are
0.887–1.174 relative to this scale. No per-frame pose scaling or RGB changes.
Native CUDA projection/backprojection and pose conversion pass; conversion error
is at most2.09e-7 and intrinsics match exactly in native float32.

| Native camera/depth diagnostic | Previous corrected full-span BA | Static-map cameras locked |
| --- | ---: | ---: |
| Median of frame medians |1.75px |1.50px |
| Worst-frame median |175.82px |5.28px |
| Five successive time-bin medians |1.71 /1.43 /1.37 /9.40 /51.88px |1.27 /1.24 /1.48 /1.79 /2.14px |
| Source14–18s median |3.84px |1.74px |

All camera tensor state remains **exactly unchanged** through2000 native depth
BA steps. All40 recorded raw support checks pass; the last sampled pair-retention
fraction is97.59%, positive input-depth support99.99%. The native stage took52.73s,
excluding mapping, transfer and environment setup. These are observed-track
consistency checks, not independent physical or novel-view ground truth.

The continuation gate fails at source24.933–25.333s: six frames have58–62 usable
front-facing static mean anchors, below64. Their raw track observations are78–81.
The last three frames already had60–63 usable anchors before optimization; the
final solve reduces them by two. This distinguishes the remaining track/anchor
coverage problem from the camera drift addressed here. No threshold was relaxed.
Manual overlays show much better alignment, with some outliers still present.

No motion scaffold, appearance training, Brush Gaussian training, separate outro
or new3D export was started. The app shows the actual sparse world, source/map
projections, fixed-camera track overlays and source-time error/coverage chart.
Its98 existing models, including86 archived records, are unchanged.

Strict retrieval verified1,235 stable files with zero pending. The L40S worker
was terminated and independently verified absent; zero account Pods remain.
Session estimateUS$0.3187; cumulativeUS$4.3362 before tax; US$5.6638 remains of
the acceptedUS$10 ceiling. No automatic retry or new paid session is running.

Native outcome and closure (historical reference: `docs/locked-execution-results.json`),
geometry/camera gates (historical reference: `docs/guildhall-staticlock-full-geometry-evaluation.json`),
anchor coverage (historical reference: `docs/anchor-coverage.json`), camera contract (historical reference: `docs/camera-package.json`),
scale conversion (historical reference: `docs/depth-scale.json`), native checks (historical reference: `docs/locked-preflight.json`),
lessons (historical reference: `lessons.md`), next steps (historical reference: `next-steps.md`).
