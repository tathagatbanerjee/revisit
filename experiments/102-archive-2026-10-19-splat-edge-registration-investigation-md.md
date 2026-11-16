> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-edge-registration/investigation.md`.
> Original SHA-256: `894fe9f0f27ebd71cd9284035807704aa82d8306781ce077a545932526781907`. Private media/logs are not included.

# Edge registration investigation and proposed bounds — 19 October 2026

The user requests a new folder and a set of tests after committing/pushing prior
work. This is test preparation, not execution of the new experiments. The prior
source/results snapshot is commit9293dec. The completed integrated prototype
passes timing/room gates but fails person geometry; its full-context consolidation
and refinement gains are0.170%/0.00274%. Those are preserved baselines, not edge
method results. See `../splat-fusion-prototype/result.md`.

## Hypothesis

Corresponding physical scene edges, their surrounding appearance and multi-view
rendered contours may provide stronger registration constraints than nearest
Gaussian centres. Gaussian primitives themselves have no hard surface boundary.
Image intensity edges, alpha silhouettes, depth discontinuities, physical corners
and crop boundaries are different measurements. Test them separately.

A person's silhouette depends on viewpoint. Use it as a rendered-image constraint,
not an assertion that a contour pixel from each camera describes the same3D point.
Partial-scan boundaries have no obligation to match another scan. Missing edges
may mean occlusion or missing coverage rather than physical absence.

GaussReg provides a relevant established precedent: coarse point-cloud alignment
followed by rendered-image-guided fine registration. It is not evidence that an
edge-only method resolves our actor discrepancy. Source: the
[authors' ECCV2024 project](https://jiahao620.github.io/gaussreg/), reviewed during
the preceding discussion. Our proposed edge objective is a new local experiment,
not an implementation or reproduction of GaussReg.

## Existing implementation and inputs

- `../independent-mosca-fusion/geometry.py`: native PLY export, Sim(3) and covariance
  transformation. Current exports contain DC colour, not full SH appearance.
- `../independent-mosca-fusion/registration/sparse.py`: native-style expected-depth
  adapter; prior numerical agreement does not certify reliable depth on contours.
- `../splat-fusion-validation/common.py`: CPU RGB/alpha projection and compositing.
- `../splat-fusion-prototype/run.py`: clock, receipts, gating and publication.
- `../working/independent-mosca-fusion/retrieved/native/{a,b}/`: immutable complete
  independent reconstructions, fitted intrinsics/poses,36/34 native states.
- Seen training images00/24, saved reviewed masks and calibration-assisted matches.
  Clock A0–2.9029s; B0.5005–3.236567s. Reuse verified local PTS conversion.
- Existing room-feature, original constrained and scene-balanced alignments are
  fixed comparisons. No baseline is overwritten; matching source cameras and
  rendering settings are used for every comparison.

Some readiness inputs do not yet exist: reviewed physical-edge identities,
reserved edge groups and sufficiently accurate complete-person masks. Preparing
this plan does not claim those prerequisites are satisfied. Dynamic-only point
membership and the old B torso rectangle are insufficient for test04.

## Proposed implementation, before freezing each run

Use deterministic OpenCV Canny at the same luminance scale for both sources:
thresholds50/150 on8-bit luminance, aperture3, L2gradient=true, no auto-thresholding.
Start at320x180 while reporting distances in640x360-equivalent pixels. Inspect
native-resolution crops so tiny dots or aliasing are not mistaken for structure.
Mask unsupported/crop edges, and keep physical edges and silhouettes separate.
Any alternative extractor is a separately frozen trial, not a silent retry.

Match physical edge junctions/short segments using local texture, orientation and
visibility, with explicit unmatched/ambiguous states. Preserve data-association
errors; nearest edge alone is not identity. In calibrated controls, calibration
may establish identity, but true target coordinates/IDs cannot enter fitting.

For global refinement, use symmetric distance-to-edge terms plus unoriented
edge-angle disagreement. Use Huber delta3px with linear tails so widely displaced
contours retain a gradient; do not cap all mismatched body edges to a constant
zero-gradient loss. Normalize per-view/region contributions, with equal room and
person group weights in the combined condition. Fix the weight of orientation
before execution (proposed2px per radian). Keep empty/missing contours penalized,
not removed from scoring.

One Sim(3), initialized from the saved room-feature transform: scale ratio bounds
0.7–1.3, rotation update<=20deg, translation update<=2m-equivalent, at most200
objective evaluations. Test03's room-only, person-only and equal-weight conditions
are fixed ablations, not a weight sweep. Camera intrinsics remain unchanged.
Object-only04 is separately named and uses the same bounds with reviewed person
membership; no per-Gaussian deformation. Freeze exact optimizer and implementation
revision before any fit. Proposed values here are planning criteria, not successful
settings or post-result adjustments.

Use precomputed depth-supported physical-edge projections for inexpensive trials
where valid. Fresh re-rendered multi-view edges are the independent final check.
Silhouette objectives require rendering visibility correctly; a projected fixed
silhouette-point proxy cannot certify success. Benchmark the selected renderer
before fitting; do not run hundreds of costly full-scene CPU renders blindly.

## Costs, resource limits and preservation

All tests initially use existing local CPU code/weights/data. No training,
checkpoint downloads, new worker or paid service is needed for preparation.
The cached Python3.12 environment has numpy/scipy/PIL/OpenCV/torch; reuse it without
upgrading packages. Record actual library/source versions with each execution.

Proposed per-trial limits:120s input/edge audit,600s fitting/rendering budget,
200 objective evaluations and2GiB peak process RSS; software browser inspection
is separately measured. Benchmark10 objective evaluations first and record the
estimate. If the chosen renderer cannot fit the bound, stop at readiness and
scope another execution route; do not silently provision compute or call a
budget-limited run a scientific rejection. No paid resource or cloud teardown
applies to this plan. Keep existing viewer4318 and unrelated applications running.

Actual screenshots, fitted splats and temporary annotations go under ignored
`../working/splat-edge-registration/<trial-id>/`; supporting numerical evidence,
hashes, source/code versions, matching labels and frozen settings belong in the
trial's `docs/`. Never overwrite the completed trials. Camera20 RGB stays sealed.
No new viewer group is created until there are actual inspected artifacts.
