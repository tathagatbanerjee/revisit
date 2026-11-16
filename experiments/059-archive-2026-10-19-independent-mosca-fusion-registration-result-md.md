> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/independent-mosca-fusion/registration/result.md`.
> Original SHA-256: `2f2c0f48595014afda38cfb2b4f6fcf09fc9c222ca840be4ef55aec34428eb9a`. Private media/logs are not included.

# Registration result — 19 October 2026

Background registration succeeds for the selected room landmarks, but is not an
overall alignment fix: the independently reconstructed person then appears twice.
The original union and all unsuccessful candidates remain available. No winner
is promoted. A is unchanged, and each B candidate uses one constant full similarity
(rotation, translation and scale) across the whole clip.

## Evidence and procedure

The fixed mutual-SIFT trial produces only8 observations in4 reference cells and
fails readiness; it was not relaxed. A separately documented studio control uses
supplied calibration to identify visible tiny wall-camera housings. Matching uses
the actual observed dark-dot centres, conservative foreground exclusion, unique
association and the same1.5px epipolar gate. Calibration identifies landmarks; it
does not supply the fitted target 3D coordinates. Both point sets come from the
saved native Gaussian reconstructions' expected depths.

This yields120 observations of34 physical landmarks across five overlap instants.
Identity groups are split28 fitting/6 validation, with no identity split leakage.
This is calibration-assisted registration on seen studio cameras00/24, not blind
phone registration or fresh-camera evaluation. Camera20 RGB remains sealed.

The CPU depth adapter reproduces the native renderer's saved108 samples: median
relative differences about3e-7, maximum0.104%. It integrates opacity and occlusion,
covariance support and native pixel centres. An empty-support edge case was fixed;
all120 accepted associations replay exactly unchanged, so the solve was not rerun.
An initial module-path collision failed before solver execution and is preserved
in the working log; it produced no candidate.

A seven-parameter robust fit uses only fitting identities. One bounded local
trimmed ICP follows, with fixed drift bounds and three distance levels. Background
clouds contain2,058 A /1,956 B centres for registration only; publication retains
every original Gaussian. Validation labels are withheld from the optimizer, but
unlabelled ICP surfaces may include nearby landmark geometry. These are not
independent held-out surfaces or images.

## Room and person results

Room errors are medians over the same six reserved identities. Pixel error is
the maximum of symmetric reprojection errors in the two fitted source cameras;
3D distances use the old A scale as an approximate metre conversion.

| Alignment | Room pixels | Room 3D, metre-equivalent | Room gate |
| --- | ---: | ---: | --- |
| Original |59.84|0.891|Fail|
| Full background registration |8.10|0.0737|Pass|
| Background plus local ICP |6.99|0.0703|Pass|
| Additional scene-balanced diagnostic |27.84|1.010|Fail|

The room gate requires at least four validation identities, median3D<=0.10m and
median pixel<=15px. Passing it says nothing about the person. A frozen post-solve
diagnostic on20 previously seen person-region observations worsens from24.69px
original to219.82px full registration /219.92px ICP. Actual mid-clip A and B
browser views show two separated people for both room-only candidates, whereas
the original has overlapping head/limb ghosts. ICP cannot resolve this discrepancy.

After preserving those outputs, ONE separate scene-balanced diagnostic estimates
another global similarity with equal room/person group weighting and symmetric
source-view reprojection. It starts from the original transform, uses28 room
identities and17 person observations, and converges in12 evaluations /0.133s.
There is no weight sweep, per-Gaussian change or motion refit. The20 person
observations were already inspected before this method was selected and are
explicitly repurposed as development data. Three are excluded from this solve,
but are not independent validation. On those same three, pixel error changes
27.68→22.74 and approximate3D0.193→0.141m. Training-person pixel error changes
22.18→18.62 on17 observations. Room pixel error improves over the original, but
room3D error becomes worse, not better. This is a limited screen-space compromise
and still fails geometry, not evidence that the two models share consistent shape.

Actual balanced mid-clip renders from both shared recorded views bring the bodies
back together but retain doubled head and arm contours. The original and balanced
versions both remain imperfect; this inspection does not establish a clear overall
visual winner. The room-only feature and ICP candidates visibly separate the
people. At2.5025s the balanced A view still shows doubled raised arms, so the residual
shape/motion discrepancy persists beyond the middle pose. The side-by-side sheet is retained under
`working/independent-mosca-registration/final-comparison.jpg`.

## Publication and checks

Five runs in **Full MoSca / background registration** retain the A anchor, original
union, feature registration, ICP and separately labelled balanced diagnostic.
All40 timeline states retain valid-source activity:65,507 A points before B starts,
127,887 in overlap,62,380 B after A ends. No inactive-source padding, pruning,
opacity/colour edit or shared Gaussian fitting is introduced. Camera/time settings
and black/DC rendering match across candidates. The native source renderer's
white backfill is not browser pixel parity.

The original four-run browser pass checks five clock positions, both recorded
views at three overlap instants, the shared registered-B view, endpoint counts,
orbit/reset and playback/pause. It passes without uncaught exceptions or invalid
manifests. Screenshots wait eight rendered frames; software SwiftShader is not a
hardware performance benchmark. A viewport adjustment reduced software capture
cost; these are qualitative images, not pixel-error comparisons between captures.

Artifact checks verify160 first-phase and40 balanced snapshots: A is byte-identical,
original union is byte-identical, all B positions/scales/covariances exactly match
one global transform, static prefixes are fixed, all points and original opacity
and DC colour are preserved. Source hashes are unchanged. Three focused geometry
checks and ten viewer tests pass, as do viewer source and Compose checks. See the
JSON records in `docs/`. The separate balanced browser pass also succeeds at
all five clock positions and both views at three overlap instants, with no page
exceptions or invalid manifests. The catalog contains all five comparison runs.

After export, the A-only manifest's inherited union count was corrected to65,507;
models were unchanged. A refuse-existing guard was added to the publisher. Frozen
pre-run plans and their code hashes remain historical; post-run hashes record the
final source separately. Neither change reran or retuned a fit.

## Interpretation

A room-only similarity cannot fix the selected models' person discrepancy. This
does not prove that every possible global transform fails or that independent
reconstruction-then-merge is the wrong architecture. It does indicate that the
current monocular models' internal room/person geometry is inconsistent with
this registration. Learned focal lengths differ from supplied calibration
(A452.06 vs544.45; B316.65 vs466.54), a plausible unisolated contributor.

Next proposed experiment: preserve the per-video architecture while enforcing
consistent intrinsics/depth scale during independent fits, then repeat the same
registration and person checks. No such fit or paid worker was launched here.
No hybrid comparison follows automatically.
