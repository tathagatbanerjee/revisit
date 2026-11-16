> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-edge-registration/result.md`.
> Original SHA-256: `df5e9001b5ca0aa318bcb62680ea8db9a1d0707317ae62bffba66c0de227d113`. Private media/logs are not included.

# Edge registration results — 19 October 2026

Edges provide usable room identity evidence at native resolution and can improve
some projected image agreement. **These tested methods do not produce a good
merged reconstruction.** The known-transform recovery attempts fail, a room-only
fit worsens3D consistency, and motion still shows two separated people. Complete
person/equal-weight silhouette fitting remains unrun because B membership is
unverified. Do not interpret that missing experiment as a silhouette-method failure.

## Stage outcomes

| Stage | Result and practical limit |
| --- | --- |
|01|Fixed Canny-near SIFT bootstrap finds only one supported match across two fitting views, so no sparse fit. A separately scoped direct edge-distance/orientation proxy starts at identity but ends12.32deg /19.92% scale wrong. Strict known-answer gates fail.|
|02|At320x180 none of18 tiny physical groups survives source/render edge gates. Native640 recovers16, but only2 reserved identities at midpoint. Same-threshold audit across already-seen grids6/12/18/24/30 supplies31 distinct groups,4 reserved,6 spatial regions. No split or threshold relaxation.|
|03|Room-only grouped-boundary proxy improves source-view edge F1 from0.174→0.257 and0.093→0.216, but reserved virtual F1 only0.199→0.208. Room reprojection improves8.10→7.41px while3D discrepancy worsens0.0737→0.1453m-equivalent, failing geometry. Person remains193.13px /1.238m-equivalent. Person-only/equal-weight conditions are unrun.|
|04|Existing A complete-person membership matches its checkpoint version. B lacks verified complete-person membership. Actual renders show its head/torso in the static layer; moving-only content is fragmented. Readiness audited; person-only transform not fitted.|
|05|Scaling source positions and covariance1.2 about one camera leaves first-view edge F1 exactly1.0 while depth differs20%. Other views reduce F1 to0.452/0.372 and expose the wrong solution. Negative control passes; no transform-recovery claim.|
|06|Known same-physical-view controls pass baseline,75% coverage, shifted patch and lighting change.40% coverage and nearer occlusion each leave only3 matches and remain not ready. Periodic stripes admit two equally good hypotheses and are marked ambiguous. Four positive cases plus one negative case pass; this is not wide-view registration robustness.|
|07|A single room-edge transform fits only grids12/18/24, then renders6/18/30. Actor remains187.97px /1.201m-equivalent; room7.28px /0.168m-equivalent also fails. Both views visibly contain two people during motion. Full person-contour/region-coverage metrics are unavailable, not passed.|
|08|Publish unchanged A/B controls and previous union, plus the raw edge candidate, on identical40-state clocks/cameras. All A/B points/opacity/DC retained. Merge rejected, originals retained; consolidation/refinement skipped.|

The original320 audit, native midpoint diagnostic and temporal expansion are
separate records, as is the extra direct-edge01 method. No failed trial is replaced
by a later success. Native temporal object-boundary grouping is a separately scoped
room-only diagnostic, not execution of every originally planned global/person
objective. See per-test scopes, frozen run plans and JSON results for exact settings.

## Interpretation

We have evidence that edge correspondence can work in easier same-view conditions
and that a better starting transform helps room-only refinement. We do not have a
reliable edge-based coarse registration method: the sparse bootstrap lacks matches,
and the direct distance objective settles on a wrong solution in the known-source
control. Physical object identity was supplied by earlier calibration-assisted
camera-housing associations; individual boundary pixels are not guaranteed to be
homologous surface points. The projected-curve objective is an approximation,
checked afterward by fresh common-camera renders and excluded landmarks.

Both real proxy fits hit the fixed20-nfev iteration limit without convergence;
actual objective calls are132 and125, under the200-call limit. No longer fitting,
new initialization, weight sweep or best-step selection was used. These outcomes
do not bound every possible contour optimizer's performance.

The strongest counterexample is05: perfect edge agreement in one view coexists
with wrong3D scale/depth. Multi-view and geometry checks are essential. Conversely,
raw edge distance improving does not make3D room geometry better here. The existing
room/person gate correctly rejects the result despite source-view edge gains.

04 is a prerequisite gap, not evidence against separate-person contour alignment.
Moving Gaussians alone cannot represent the whole person in these models. An
exact B semantic layer is needed to test that hypothesis meaningfully. The cached
mask preview is not a per-Gaussian assignment or pixel-accurate silhouette truth.

All images/source observations were already seen development data. Reserved virtual
views are new render directions of seen models, not fresh camera evidence. Test07
excludes grids6/30 from its refinement optimizer, but its initializer and prior
experiments used seen room observations; no independent temporal generalization
claim follows. The+1-state clock perturbation is saved as an uncalibrated rendered
edge difference and remains ambiguous for acceptance without valid person masks.

## Artifacts, checks and preservation

Viewer group **Edge registration / diagnostics** retains originals, previous union
and edge-aligned raw union. Shared A/B source cameras plus one reserved virtual
camera, black/DC rendering,40 states0–3.236567s. A contributes65,507 points through
2.9029s; B contributes62,380 from0.5005s. Full overlap contains127,887 points.
No pruning, per-limb deformation, opacity reduction, retiming or source padding
conceals the remaining double person. Source-local clocks are unchanged.

The tile renderer matches the independent sparse renderer on63 native-resolution
samples to floating-point precision (RGB<4.5e-16, alpha<5.6e-16, depth<1.4e-15).
That verifies batching, not physical surface accuracy. Gaussian depth uncertainty
is checked at boundaries before lifting samples. All trial runtimes/RSS are
recorded in their result/runtime JSON files; local execution remains under its
600s/2GiB bounds. No new reconstruction training/checkpoint download, paid resource or camera20 RGB.

Artifact verification checks160 published states,99 immutable inputs, exact A/B
control and baseline bytes, disjoint physical identity groups, constant candidate
B transform, all original opacity/DC, source activity and rejection policy. Ten
viewer tests, syntax and Compose checks pass. Browser inspection passes all four models at five clock positions, both source
views plus the reserved virtual view for both union candidates, endpoint counts,
playback/pause, orbit/reset and camera changes preserving time/model. No uncaught
page exceptions or invalid manifests. Captures wait eight rendered frames; the
software renderer is not a hardware benchmark. See browser record (historical reference: `08-integration/docs/browser-check.json`).

Actual CPU previews inspected: failed known-answer alignment, source/render native
edge audit, room-only fixed-view comparisons, static-vs-moving person audit,
scale/depth ambiguity, nuisance controls and merged motion states. The room-only
and temporal unions visibly retain duplicate people. See ignored work outputs
under `working/splat-edge-registration/` and the new viewer group.

## Next useful experiment

Prepare and verify complete-person B masks/membership, then run the untested
person-only multi-view contour objective while keeping room geometry fixed. This
is a concrete missing test, rather than more room-edge threshold tuning. Retain
known-answer/ambiguity controls and improve coarse association before claiming
blind registration. Independent-fit intrinsics/depth consistency remains another
unisolated possible cause; no new MoSca fit is launched by these results.
