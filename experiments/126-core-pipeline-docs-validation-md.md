> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `core-pipeline/docs/validation.md`.
> Original SHA-256: `1fc5ca0ddb251d34a883c539bf2608f27019bac2deb1759574dfb5e06aa18a74`. Private media/logs are not included.

# Standardization results — 29 October 2026

The **30s static baseline is validated** across outdoor sculpture and indoor
Guild Hall detail clips, including an outdoor repeat. Every required stage
returned cleanly, all30,000 appearance steps completed, raw model tensors were
finite and camera tensors stayed exactly unchanged. The visitor/motion candidate
was rejected before appearance. Its later dynamic stages remain unvalidated in
this adapter; this is not a stable generalized dynamic-replay pipeline.

The new folder is core-pipeline (historical reference: `../README.md`). The historical Guild Hall
full-interior exploratory result remains the quality reference. The new detail
shot covers a different interval and does not establish matched improvement.

## Measured outcomes

All cases are30s,360 observations at12Hz,640×360, using original source timestamps.
Local camera mapping registered every camera in one component. The tested clips
come from **two recordings**, with both indoor shots sharing the Guild Hall
recording. These are not three independent locations.

| Measurement | First sculpture | Sculpture repeat | Guild Hall detail |
| --- | ---: | ---: | ---: |
| Fresh GPU priors and required QC | 6m47.66s | 6m38.12s | 6m58.13s |
| Fixed-camera background stage | 3m46.57s | 3m46.75s | 3m36.58s |
| Dense validation | 6.12s | 6.11s | 6.12s |
| Appearance wrapper, clean completion | 14m54.17s | 14m14.64s | 18m21.50s |
| Native export | 34.68s | 32.64s | 36.68s |
| Required GPU stages summed | **26m09.19s** | **25m18.26s** | **29m39.01s** |
| Static Gaussians | 328,656 | 330,657 | 515,594 |
| Median native source fit | 19.648dB | 19.630dB | 27.828dB |
| Minimum native source fit | 14.669dB | 14.617dB | 24.906dB |

Local feature extraction/matching/mapping took2m00.64s for sculpture,6m55.95s
for detail and5m42.16s for visitors, excluding decoding/person detection. GPU
stage sums exclude upload, cold setup, human/agent review and retrieval.
Appearance wrapper includes initialization and saving. Instrumented native fit
including final save took13m47.17s for the repeat and17m52.88s for detail.

First/middle/final, three worst source-fit frames and three shifted views were
reviewed for each output. The sculpture repeats retain the same exploratory
quality: recognizable sculpture/building, soft floor/far surfaces, missing sky
and backside ripples. Indoor statues, relief and columns remain coherent, with
mild softening/text blur and an expected blurred moving visitor in a static fit.
No physical or independent-view accuracy is established by source-view PSNR or
shifted self-renders. No quality promotion is claimed; camera20 stays sealed.

[First sculpture](http://localhost:4319/?run=mosca-20261029-core-sculpture-clean)
· [repeat](http://localhost:4319/?run=mosca-20261029-core-sculpture-repeat)
· [Guild Hall detail](http://localhost:4319/?run=mosca-20261029-core-guildhall-detail)
· [detail source/native comparison](http://localhost:4319/previews/core-validation/mosca-20261029-core-guildhall-detail/comparison.mp4).

## Visitor/motion case: retained rejection

Guild Hall original222–252s completed preparation in483.623s, background in
230.941s and dense validation in6.106s. Geometry passed unchanged gates:
median1.321px, worst5.542px, minimum472 anchors, minimum dense depth0.0058089.
Six background overlays align with hall structure; camera invariance is exact.
Both original finite Boots banks were retained:512 uniform and2,048 dynamic
tracks, source-query p90 error below1px. Source/depth and mask reviews passed.

Motion exited1 after22.496s, before scaffold optimization. Only34 curves
survived native filtering. Its0,10)s source-visible support interval was
**declared before GPU inference/fitting** and failed in116/120 frames: minimum0
visible retained curves against required8. The historical all-frame gate also
fails. Reviewed overlays show sparse early actor support and some later curves
on ceiling detail. Finite/shape checks marked `numericPassed` in the input report
are distinct from its explicitly false motion-coverage gates.

No motion/foreground acceptance receipt, appearance fit, export or fallback
publication was issued. Failed stage evidence and its original interval remain
intact. This validates rejection, not the later dynamic fitting stages. Use the
static branch as the standard baseline; improved actor replay is further work.

## Cost and closure

The user explicitly authorized a **fresh cumulative US$10** allowance, excluding
historicalUS$8.2253. All new attempts use L40S, at an actual quotedUS$1.09/hour,
with conservative ephemeral-disk allowance. These estimates include launch/setup,
failed probes, idle/review and retrieval time; they are before tax, not invoices.

| Allocation | Paid interval | Estimated US$ | Outcome |
| --- | ---: | ---: | --- |
| a | 4m30.97s | 0.083716 | Slow single-stream transfer; no scene fit |
| b | 42m51.39s | 0.794434 | First clean static output |
| c | 1m24.09s | 0.025980 | Network-only rejection |
| d | 1m01.52s | 0.019007 | Network-only rejection |
| e | 1m07.46s | 0.020841 | Network-only rejection |
| f | 1h53m23.91s | 2.102073 | Two clean static cases; motion rejection |
| **Total** | | **3.046050** | **All closed, independently absent** |

Batch f transferred534,043,114bytes in26m18.87s, with128 chunks, eight connections
and whole-payload SHA verification. A parallel16MiB probe passed in44.798s.
Cold setup, review and network time materially affect paid duration. This is an
integration exercise, not an amortized production quote or GPU comparison.
The earlier US$1.7925/96m42s trial included failed geometry and interrupted optional
diagnostics; the static training loop itself already took about14minutes.

First strict collection verified3,981 files; final batch collection verified
**11,546 stable files, zero pending**. Independent final API query confirmed zero
account Pods. No persistent/network volumes were created. External termination
watchdogs and unextended deadlines covered every allocation. AboutUS$6.95 remains
unspent; no further paid job is active or queued.

## What was stabilized

Immutable configuration/source/runner hashes; locally packaged payloads before
rental; bounded checksummed parallel upload; same-worker SSH/preflight readiness;
explicit review prerequisites; a process-held exclusive GPU-stage lock; scale-only
fixed-camera background refinement; sparse inspection without dense RGB reload;
optional diagnostic suppression retaining optimizer/checkpoint code; clean fit
receipts; raw-model/camera verification; strict retrieval; owned-resource closure;
and full-density reviewed publication. Numerical gates and failed results remain.

Retained failures include the museum title transition/wide-angle source rejection,
visitor confidence0.5 missed-person masks, all network-only allocations, and the
motion failure above. The separate confidence0.15 masks conservatively cover
people but exclude some stationary pictures; their static map retains505 raw
observations at minimum. No failed preparation or fit was relabelled passing.

Six contract tests, Python compilation, pinned-source patch compilation/AST/
idempotence checks, and a local changed-config cache rejection passed. Deployment
refused an actual simultaneous GPU stage before creating its claim/process;
the original completed and released its lock. Viewer syntax and14 tests pass.
There are103 valid viewer records, zero invalid; all101 earlier API records match
exactly. Native media routes respond successfully. No successful headless browser
screenshot automation is claimed. The archived4318 app remains untouched.

30s is the tested limit.60–120s duration scaling and generalized dynamic replay
require separate measured tests. See [machine-readable measurements (historical reference: `measurements.json`).
Runtime evidence is retained under ignored `working/mosca-deep-dive/execution-core-*`.
