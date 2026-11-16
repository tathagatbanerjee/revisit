> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/10-static-anchor-refinement/investigation.md`.
> Original SHA-256: `a666f687272463e5ecdfa7a6a2a96d1106705933560bae83345ad7b32de05c3f`. Private media/logs are not included.

# Investigation and controls

## What happened to the previous anchors

The494-track fixed-camera control has78 visible observations at the last frame,
but only60 initial and58 final mean anchors in front of that camera. The final
three frames fail the64-anchor guardrail before optimization; the last six fail
afterward. The original RGB at the final observation still shows the room and
statue. Review did not identify an edited dissolve in these sampled final frames;
the interval was not shortened to remove the failure.

The original native initialization replay has2.26px median and2.99px worst-frame
error using NumPy's midpoint median. The earlier2.23px summary used Torch's
lower median; those are different summaries of the same saved observations.
Refined error is1.50px overall and5.28px worst frame. More depth refinement
therefore improves the aggregate while worsening the endpoint and coverage.

A depth-independent diagnostic triangulates65 seeded two-ray hypotheses for
each original track using only supplied cameras and observed pixels. It chooses
the largest positive-depth4px consensus. For18/20 final-frame rejected anchors,
the last observation does not fit that static consensus. All58 accepted anchors
fit at the last observation. This supports investigating track identity/visibility,
rather than attributing every failure to Metric3D. It is a fitted diagnostic,
not a unique causal identification or independent ground truth.

## Replacement background observations

Use the existing qualified153-frame COLMAP map and all305 frozen poses. Gallery
points require at least three map observations and native point error at most2px.
Each point has a representative observed SIFT descriptor. The152 query frames
match descriptors at ratio0.7 with unique point identities and at most4px residual
against their already-frozen cameras. Neither poses nor points are optimized.

Only actual observed feature locations are exported. Projecting a map point into
an image never creates visibility. The existing normalized-depth boundary mask
is applied at rounded pixels; tracks need four surviving observations. Select up
to4,000 identities deterministically: greedily target160 observed features per
frame, then fill by observation length and point ID. Do not select using depth
residuals. This changes both identity method and density versus the historical494
tracks, so gains cannot be assigned to either factor separately.

The gallery has13,697 points. The4,000 selected tracks cover every frame with at
least288 observed, positive mean anchors. Frozen map binaries remain unchanged.
BootsTAPIR banks remain intact for a future motion stage; that stage is not tested
here. Person boxes are the existing imperfect feature masks, not ground truth.

## Exact replay and paired settings

The first export summary uses a conventional inverse-K pixel grid. Before any
allocation, a separate exact replay reproduces MoSca's linspace grid and rounded
depth query, verifies the historical native world points within5.97e-7, and uses
Torch lower medians. This exact check supersedes the approximate export summary
for the unchanged-depth baseline:1.293px overall,2.285px worst frame,288 minimum
anchors. All32,343,249 co-visible pairs have positive source, target and projected
depth. Every source/target pair is checked in32-target chunks to bound local RAM.

Both GPU arms use exactly these4,000 tracks,305 RGB/depth observations, camera
package, seed12345,2,000 native BA steps and existing positive-depth safeguards.
Cameras remain frozen with zero focal/rotation/translation learning rates.

| Control | Frame depth scale | Per-observation depth correction |
| --- | --- | --- |
| CPU unchanged-depth baseline | One | Zero |
| Native full-depth arm | Native learning rate0.001 | Native learning rate0.001 |
| Native scale-only arm | Native learning rate0.001 | Learning rate zero |

The two GPU profiles differ only in `ba_lr_dep_c`. The same native scheduling,
losses, correction activation boundary and geometry gates apply. The CPU control
is not a timed GPU fit. Full-depth and scale-only are independent predeclared arms:
a failure prevents promotion of that arm, but does not suppress the other test.
No automatic retries or threshold relaxation are allowed.

The64-anchor minimum remains an experimental guardrail, not a documented MoSca
hard requirement. All error thresholds and the camera-state invariance check
remain unchanged. Low static residuals do not establish moving-person quality,
surface completeness, physical scale or translated-view fidelity.

## Exploratory track-count sensitivity

While the pinned GPU environment prepared, a separate CPU-only check evaluated
the first494,1,000,2,000 and4,000 tracks in the already-frozen bank order. With494
observed-map identities, the unchanged-depth replay still has142 minimum usable
anchors,1.525px overall median and2.265px worst-frame median. This suggests the
coverage improvement is achievable without an eightfold track-count increase,
although selection policy and feature locations still differ from BootsTAPIR.

This post-preflight sensitivity is exploratory. It does not alter either frozen
4,000-track GPU arm or establish native training speed/quality for fewer tracks.
See track-budget sensitivity (historical reference: `docs/track-budget-sensitivity.json`). A smaller
background bank is a plausible later speed control if the full comparison passes.
