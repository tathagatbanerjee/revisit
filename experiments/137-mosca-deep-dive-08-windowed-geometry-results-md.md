> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/08-windowed-geometry/results.md`.
> Original SHA-256: `511de28bd5ec72f2962d9ba4e767a7f1e982d6d3359224d9a16a0cb3c4e7d314`. Private media/logs are not included.

# Windowed camera-geometry results

The0–18s window passes the exploratory camera review. The independently
initialized14–25.333s window fails. No motion scaffold, appearance fitting,
stitched scene, separate outro or new3D model was produced.

| Camera diagnostic |0–18s |14–25.333s |
| --- | ---: | ---: |
| Observations |217 |137 |
| Initial median of frame medians |2.54px |2.65px |
| Final median of frame medians |1.21px |13.79px |
| Final worst-frame median |6.26px |149.18px |
| Five time-bin medians |1.35 /1.17 /1.15 /1.15 /1.96px |6.00 /32.40 /134.39 /9.16 /2.10px |
| Shared14–18s median |1.94px |11.03px |
| Minimum static observations/frame |121 |77 |
| Camera-BA stage time |81.10s |64.98s |
| Numeric and manual review |PASS, endpoint outliers remain |FAIL, gross18–22s mismatch |

The later window begins reasonably aligned, then deteriorates during BA. Its
logged sampled total loss rises from0.0379 at step0 to0.7283 at step100 and ends
at0.1586 at step1950. Each log samples target frames, so these are not identical
paired objective evaluations; the independent final projection diagnostic also
confirms deterioration. Its focal estimate changes382.48→422.80px, without an
independent calibration to establish which value is physically correct.

All40 recorded raw support checks pass in each window. That does not guarantee
strong effective support: the late solve's tracks with robust weight<0.01 increase
from15 to51, and its single-observation weight proxy falls0.834→0.708. Actual BA
multiplies weights across source/target observations. We have not isolated which
parameter updates cause the instability.

The overlap has283 shared static identities. A similarity fitted on192 identities
leaves91 for alignment-only checking; withheld median world disagreement is
0.156 in arbitrary early-window units,22.3% of withheld anchor radius. These
tracks participated in camera optimization, so this is not independent geometry
ground truth. No stitch was accepted, especially with the late camera gate failed.

The first early-window attempt stopped before BA due a diagnostic accessor error.
Its original protocol/source/logs are preserved; a documented diagnostic-only
amendment and native CUDA regression preceded recovery. Solver settings, gates,
budget and the allocation deadline were unchanged.

Strict collection verified2,673 stable files with zero pending. The L40S worker
was terminated and independently verified absent; zero account Pods remain.
Session estimateUS$0.4169; cumulativeUS$4.0175 before tax; US$5.9825 remains of
the acceptedUS$10 ceiling. All98 existing app records, including86 archive records,
are identical to the baseline. The app shows the chart and both camera overlays.
Its12s splat remains the longest published dynamic result.

Execution and closure (historical reference: `docs/execution-results.json`),
early gate (historical reference: `docs/guildhall-before-turn-geometry-evaluation.json`),
late gate (historical reference: `docs/guildhall-after-turn-geometry-evaluation.json`),
initialization/overlap comparison (historical reference: `docs/window-comparison.json`),
robust support and loss trace (historical reference: `docs/robust-support.json`),
diagnostic amendment (historical reference: `docs/diagnostic-amendment.json`),
native CUDA checks (historical reference: `docs/preflight.json`), lessons (historical reference: `lessons.md`),
next steps (historical reference: `next-steps.md`).
