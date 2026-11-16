> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/dense-result.md`.
> Original SHA-256: `eaec4769b67161465bb076b672077fc8af37bfb1dc9030e472ea21d4c3da210b`. Private media/logs are not included.

# Dense foreground initialization result

Subsequent work: the camera 13 audit and fixed pair comparison (historical reference: `camera13-result.md`)
is complete.13 is now seen; it improves foot sampling slightly but still fails
readiness. The proposals and unopened-camera statements below describe this
earlier phase. Evaluation20 remains sealed.

19 October 2026. **Dense matching adds useful observed point samples, but does
not produce a complete person. The initialization gate still fails.** No new
Gaussian fitting or paid compute was used. Camera20 remains unopened.

The predeclared trial (historical reference: `dense-investigation.md`) ran one instant from training
cameras 00/24/21/02 through a custom calibrated plane sweep: 256 inverse-depth
planes over 1–6 m,9x9 NCC patches, conservative masks, uniqueness checks and
independently computed reverse depths. No learned depth model, generated view,
silhouette filling or inherited person geometry supplies the points.

Original1080p rectified training frames are area-downsampled to640x360 with
the matching pixel-center intrinsics conversion. This limits detail and may
lose useful texture; this failure does not establish that all dense methods or
the original-resolution footage are insufficient.

## Actual support

| Training camera | Pixels supported by reciprocal matches | Conservative person-mask coverage |
| --- | ---: | ---: |
|00 |3,313 |13.32% |
|24 |3,220 |16.90% |
|21 |2,686 |15.15% |
|02 |151 |2.15% |

The run retains 11,629 directed pair observations, fused into **8,812 approximate
5 mm bins**. Coarse head/hands image-region groups contain1,865/2,401 bins;
the foot group contains only **two**. Those two come from forward/reverse
estimates of essentially one ankle/shoe neighborhood: source 21 pixel315,338
and source 02 pixel318,254. They are not two independently supported feet or
a recovered shoe surface. Region boxes include nearby clothing and do not
establish anatomical accuracy.

The dense gate required≥ 500 bins overall,≥ 50 supported pixels per camera,
≥ 20 bins per head/hands/feet group, and≥ 10% mask coverage per camera.
It fails on foot support and camera 02 coverage. The old sparse gate/failure
remain unchanged. Higher point counts are denser sampling, not proof of better
geometry or a complete body. See measurements (historical reference: `dense-report.json`).

## Inspected outputs

- Reciprocal support on the training sources (historical reference: `../../working/shared-person/dense/support.jpg`).
- Source, accepted depth and fused point-cloud renders (historical reference: `../../working/shared-person/dense/depth-and-cloud.jpg`).
- The ankle/shoe candidate crops (historical reference: `../../working/shared-person/dense/foot-candidate-crops.jpg`).

The images show recognizable head/neck, arm edges, shirt details and waistband
fragments. Most shirt/pants surfaces and lower legs remain empty. Camera02 has
very sparse direct evidence; rendering the union of points into it does not
create additional observations. A few floating samples remain. Depth confidence
and reciprocal consistency reduce false matches but do not guarantee correctness,
particularly across wide angles and repeated dark clothing.

Private exports in `working/shared-person/dense/` include directed depth/confidence
maps, observation provenance and colored point clouds in author-world meters
and the fixed Brush room's SfM world. These are initializer candidates, not
Gaussian models or dynamic playback outputs. No viewer candidate was added.
The existing room and person controls were hash-checked before and after and
remain untouched.

## Verification and resources

The first run took 48.78 s and peaked at 633.96 MiB process RSS; a repeat took 39.99 s
and634.11 MiB. All depth-map, point-cloud, provenance and support-image hashes
match between runs, with identical numeric results. The two sets use about44 MiB
on local disk. Both ran under a600-second external timeout with four OpenCV
threads and no CUDA execution. No new dependencies or weights were downloaded.

Four independent dense checks pass: a textured plane recovers its known metric
depth and reverse projection; inconsistent reverse depths are rejected;
untextured/missing-mask evidence is rejected; and resized K preserves pixel
projections. Both earlier sparse checks and `pip check` also pass. A warning
from invalid, rejected synthetic projections was corrected before the real run;
tests then pass without that warning. Actual retained depths are finite and
meet the cycle bound. Exported world conversion agrees to5.73e-8 SfM units,
within ASCII export precision. See verification (historical reference: `dense-verification.json`).

## Next decision: improve overlapping body observations

Do not fit a supposedly complete person from these fragments. First audit one
better-overlapping full-body training view. Using calibration and the seen
matched head/ankle anchors, **camera 13** is the preferred proposal:26.22° from
camera 21, versus54.5° for02, with both anchors projecting at least211 pixels
inside its1920x1080 rectified frame. See the reproducible
training-view proposal (historical reference: `training-view-proposal.json`).

Camera13 RGB has not been fetched or inspected. Anchor projections are noisy
proxies; they do not prove visibility, complete feet, texture or synchronization.
Next check its source terms, source-clock alignment and actual head/hand/foot
coverage, then repeat a separately bounded21/13 dense comparison at the same
settings if those input gates pass. Keep all failures. Reserve20 unchanged;
exclude13 from future fresh evaluation as soon as its RGB is opened.

If an improved pair cannot supply credible surfaces, investigate one learned
multiview/depth route or the planned body-prior comparison with its dependencies
and terms explicitly pinned. More photometric steps on the old person are not
a substitute for this missing geometry. Motion experiment B remains after A.
