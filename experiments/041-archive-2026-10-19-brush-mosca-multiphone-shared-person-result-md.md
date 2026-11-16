> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/result.md`.
> Original SHA-256: `f2e9b9fe6d7bdaa7763a195630bee94cde0bde28c166640dc8372b65061d1a31`. Private media/logs are not included.

# Single-instant foreground readiness result

**Subsequent dense follow-up:** 8,812 point bins, still incomplete feet and
camera 02 support (historical reference: `dense-result.md`). Camera13 is the next training-view proposal;
reserved 20 stays unopened. The sparse result below is preserved unchanged.

19 October 2026. **Local preparation is complete; the sparse foreground route
fails its input gate. No new Gaussian fit was launched.** The inherited MoSca
baseline and all assembled candidates remain intact.

One synchronized instant, state 000/source time 0, was rectified directly from four
checksum-verified1920×1080 originals. Known Panoptic calibration supplies cameras;
this does not test image-only camera recovery. All selected frame presentation
timestamps are0 with zero residual. This is clock consistency, not an independent
trigger-synchronization measurement. Existing640 px automatic exclusion masks
were conservatively eroded and upscaled; mask boundaries remain approximate.

| Training set | Accepted pair observations | Distinct5 mm bins | Head / hands / feet region observations | Gate |
| --- | ---: | ---: | --- | --- |
|00/24/21 |43 |32 |3 /3 /0 |Fail |
|00/24/21 plus already-seen02 |43 |32 |3 /3 /0 |Fail |

The predeclared gate requires 100 bins, 10 pair observations per camera, and five
per coarse body-region group. Incident observations are 00: 31, 24: 29, 21: 26, 02: 0.
These pair counts are not independent landmarks; repeated matches and nearby
features can describe the same surface. The body boxes are approximate image
regions, not anatomical ground truth. See full measurements (historical reference: `readiness.json`).

## What the sources and overlays show

At this instant00 and24 crop the person before the feet.21 shows both shoes;
02 also shows shoes, with substantial self-occlusion and a much different angle.
Adding02 as a training-coverage probe yields no accepted correspondences under
the unchanged filters. The other pairs' matches concentrate on shirt lettering,
waistband and a few head/wrist features. There is insufficient distributed
geometry to support the intended complete-person initialization.

This rejects this sparse route on this instant. It does not prove dense matching
cannot work, that another training view/instant cannot help, or that Gaussian
splatting cannot represent the body. Relaxing the gate or reusing the old person's
missing geometry would not test the architectural question.

Private local evidence:

- Source coverage/masks/region boxes (historical reference: `../../working/shared-person/verified/coverage.jpg`).
- 00/24 accepted matches (historical reference: `../../working/shared-person/verified/hd_00_00--hd_00_24.jpg`).
- 00/21 accepted matches (historical reference: `../../working/shared-person/verified/hd_00_00--hd_00_21.jpg`).
- 24/21 accepted matches (historical reference: `../../working/shared-person/verified/hd_00_24--hd_00_21.jpg`).
- Points and pair details: `working/shared-person/verified/foreground-points.npz`
  and `pair-points.json`. These are sparse observed candidates, not a body model.

## Evaluation reservation and preserved controls

Camera **hd_00_20** was selected using calibration only, before this preparation
decoded training videos. Its angles to00/24/21 are44.88°/20.67°/24.39°. Known local
corpus paths contain no RGB artifact for that camera. No20 video was fetched,
decoded or viewed. This is a reservation backed by known corpus checks, not a
universal history of access. Recheck before any future fitting. See
reservation (historical reference: `reservation.json`).21/02 are seen and may be used for training.

Control hashes (historical reference: `controls.json`) identify the fixed raw Brush room and inherited
foreground in the assembled-before-refinement frame. The foreground begins after
the report's static-Gaussian prefix. Fresh points are in author-world meters;
the recorded similarity bridge must transform them and their covariances into
the room's recovered SfM world. No foreground/background asset was rewritten.

## Verification, resources and next action

Two separate preparation outputs reproduce identical images/hashes, pair counts
and gate decisions at unchanged settings (~6.3 s each). Independent synthetic
geometry checks recover known points and reject a behind-camera point and a bad
correspondence; an untextured pair returns no geometry. Both tests pass. Package
dependencies pass `pip check`; existing output directories are protected from
overwrite. Source/mask/derived/script hashes were checked and actual coverage and
all three accepted-pair overlays were visually inspected. See
verification (historical reference: `verification.json`).

The isolated environment and evidence use277 MiB locally. The read-only Runpod
account query returned `[]`; no paid resource was created or extended. CUDA
training/rendering was not attempted; there is no new viewer candidate. The
existing refiner has fixed topology, so it also needs a new geometry-growth path
before it can implement A. No viewer source changed.

The subsequent dense investigation and run are now complete; see its linked
result and the package next steps. Keep the 20 reservation sealed until the
selected architecture candidates freeze.
