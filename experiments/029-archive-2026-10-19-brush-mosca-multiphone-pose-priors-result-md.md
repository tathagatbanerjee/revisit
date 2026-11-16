> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/pose-priors/result.md`.
> Original SHA-256: `d5017737f0aa6590b9f0ef2225debd92e72f95cdb00b38bfb37daf2c76252f9f`. Private media/logs are not included.

# Phone-pose priors: verified, not promoted

17 October 2026. The existing 4DM metadata supplies a usable coarse common world
frame once its official axis/quaternion conversion is applied. However, fixed
supplied poses and one image-based correction do **not** improve the stricter
later-frame localization test. Keep the previous image-only Medium map as the
preferred camera-recovery result and the locked MoSca quality baseline unchanged.
No new dynamic reconstruction was trained.

## Coordinate convention

The pinned author reconstruction source (historical reference: `source-report.json`) converts metadata
quaternion(x,y,z,w) to(-x,y,-z,w), camera centre to(x,-y,z), then projects with
K[R^T|-R^T C], where R is camera-to-world. We implemented that convention and
checked it against actual masked background correspondences. The source was
read and hashed, not executed. These are globally localized on-device SLAM
estimates; their existence is not independent proof of metric pose accuracy.
Ordinary MP4 uploads generally do not provide this instrumented-capture metadata.

## Prior compatibility and fixed geometry

Reuse the preceding affine DSP-SIFT databases and exactly the same 25 training
frames per set, with their person masks and per-frame lens intrinsics. Exclude
the sixth phone and the later query-frame extrinsics. No new matching model,
feature threshold sweep or additional footage download.

| Set | Cross-phone matches checked | Median Sampson distance | Positive-depth triangulation within 5px | Fixed-pose cross-phone landmarks |
| --- | ---: | ---: | ---: | ---: |
| Easy | 954 | 3.844px | 69.8% | 76 |
| Medium | 855 | 3.175px | 69.5% | 141 |

Both meet the predeclared coarse-compatibility gate (median<=5px, >=50% positive
triangulations within 5px). Final fixed-pose triangulation uses 2px filtering.
Median cross-point error is 0.899px for Easy and 0.612px for Medium. Camera matrices
change by at most 4.4e-16, confirming fixed poses; point positions can optimize.

Twenty-five camera poses were imported in each case, **zero camera poses were
newly recovered by that import**. Success is based on real observed cross-phone
tracks, not the number of imported cameras. Three phones per set observe >=30
cross-phone landmarks. Easy has a fourth phone with 12 landmarks and a fifth
without supported links; Medium's remaining two phones have no such links.

Easy's supported phones are 4846a8bc/cc74017e/d7ec5aa6; Medium's are 378d43ce/
cc74017e/d7ec5aa6. These are different subsets. Medium's 5,130 total landmarks
include same-phone-only geometry from other supplied trajectories; the public
local harness diagnostic deliberately displays only 141 cross-phone landmarks.
Importing all five trajectories must not be reported as validated five-phone
recovery.

## Later-frame tests and matched comparison

Only phones with≥30 cross-phone landmarks proceed to localization. The map is
frozen and hashed before queries. PnP uses **only landmarks seen by≥2 phones**;
this excludes isolated per-phone structure whose world placement comes solely
from the supplied SLAM pose. The two variants allow all reference descriptors,
or exclude every descriptor from the query's own phone. The success threshold
remains>=30PnP inliers and<=2px median inlier residual. Query poses are estimated
from images without their metadata extrinsics.

| Medium map, same query/landmark-selection protocol | Cross-phone 3D landmarks | All-reference queries passing | Other-phone-only queries passing |
| --- | ---: | ---: | ---: |
| Previous image-only map | 305 | 3/3 | 1/3 |
| Fixed supplied SLAM poses | 141 | 1/3 | 1/3 |
| SLAM-initialized image adjustment | 141 | 1/3 | 1/3 |

Image-only all-reference inlier counts are 97/38/77; supplied-pose counts 12/10/59;
adjusted-pose counts 11/11/60. Other-phone-only localization succeeds only for
d7ec5aa6, with 51/46/46 inliers respectively. The two other phones produce no
accepted other-phone-only PnP pose.

Easy fixed-pose queries pass 0/3 in both variants: all-reference inliers 26/26/12,
other-phone-only 19/17/no pose. We do not lower the 30-inlier gate to call those
successes. The prior Easy image-only map did not have a usable three-phone
trajectory, so no matched Easy three-phone localization claim is made.

The protocol is stricter than the earlier all-landmark localization, which also
allowed points triangulated only within a phone. We reran the image-only Medium
map through this exact new protocol before comparing methods. Query descriptors are byte-identical across the three
Medium map variants. All runs preserve
their frozen-map hashes. Residuals on fitted inliers remain diagnostic, not
independent pose truth. The query frames have already been inspected in earlier
phases; these comparisons are regression evidence, not a fresh held-out accuracy
benchmark. No sixth-phone imagery enters this experiment.

## Bounded image-based adjustment

One Medium-only robust BA uses the supported 15 camera frames, fixed intrinsics,
Huber 1px loss, at most 50 solver iterations/60s. No new features or tracks are
introduced. The first setup attempt failed before optimization because
unregistered images remained in the reconstruction container; filtering on
`has_pose` corrected the API handling. Both logs are preserved privately.

The actual solve took~0.15s, reached the iteration limit and reported
**NO_CONVERGENCE** (Ceres counts 51 iterations for the configured 50). Median
cross-observation residual fell to 0.295px, but localization did not improve.
No refit followed its query evaluation.

The optimizer's gauge handling changes scale substantially: refined-to-original
proper similarity scale is 0.552. Raw centre shifts up to 4.49 SLAM units include
that coordinate-scale change; they are not a measured 4.49m camera correction.
After proper Sim(3) alignment, median/worst centre disagreement is 0.027/0.040
SLAM units and orientation disagreement 1.03°/1.15°. Metric accuracy is not known.
See gauge-aware comparison (historical reference: `gauge-comparison.json`).

A lower fitting residual does not validate a camera solution. This candidate
is retained as evidence and not promoted. A prior is useful for initialization,
but it does not replace accurate cross-camera image observations.

## Inspect in the harness

At http://localhost:4318 select **Phone SLAM pose priors**. Three static outputs:

- **Easy · supplied SLAM poses**.
- **Medium · supplied SLAM poses**.
- **Medium · SLAM-initialized image adjustment**.

They display observed cross-phone background landmark glyphs and coloured
camera-path glyphs, without reconstructed people or event playback. Only three
supported phones are selectable; labels identify phone prefixes. There are
76/141/141 background points, so these views are deliberately sparse and mostly
black. They are diagnostic evidence, not a scene-quality improvement. Source
projection conventions are preserved, and floor/up remains unverified.

Private native evidence:

- Easy prior-pose reprojection (historical reference: `../../working/pose-priors/phones/prior-reprojection.jpg`).
- Medium prior-pose reprojection (historical reference: `../../working/pose-priors/phones-medium/prior-reprojection.jpg`).
- Easy query overlays (historical reference: `../../working/pose-priors/phones/localization/contact.jpg`).
- Medium query overlays (historical reference: `../../working/pose-priors/phones-medium/localization/contact.jpg`).
- Adjusted-map cross-phone query (historical reference: `../../working/pose-priors/phones-medium/localization-refined/d7ec5aa63b32a4878ca037e2a7fec252-cross.png`).
- Image-only matched-query check (historical reference: `../../working/pose-priors/phones-medium/localization-image-only/cc74017ee8081c07917f03332f92ede6-all.png`).

Green observations/red projections in query overlays show agreement only on
selected inliers. The initial-prior overlays colour incompatible triangulations
red. Support is clustered on decking/props/windows, with weak coverage elsewhere.
All three sparse browser outputs were inspected; native prior overlays and query
contacts, plus adjusted/image-only comparison overlays, were reviewed.

## Verification, timing and retention

Verification (historical reference: `verification.json`) records source/metadata hashes, fixed-pose
invariance, frozen map hashes, finite camera transforms and real artifact/browser
checks. All three outputs pass PLY/hash checks, orbit/reset and all 18 calibrated
view selections. SwiftShader verifies interactions/projections, not hardware
throughput. No harness source changes or Docker rebuild were needed.

Coarse compatibility checks each take~0.02s; fixed triangulations 1.04/1.08s;
Easy/Medium fixed queries 3.26/1.98s, adjusted queries 1.98s and matched image-only
queries 2.04s. These native times exclude research, setup, source retrieval,
inspection and documentation. All computation ran locally in the existing CPU
environment. No model weights or footage were downloaded, and no new paid resources were created.
The existing Runpod deadline 20:25:35 Sydney was not extended.

Versioned `runpod/phone-pose-priors.py`, `triangulate-phone-priors.py`,
`localize-phone-priors.py`, `refine-phone-priors.py`, `inspect-phone-priors.py`
and `publish-phone-priors.py` preserve the procedure. Run with the existing
`working/brush-mosca/tools/bin/python`. Directories refuse overwrite. Medium
localization variants use `--variant fixed|refined|image-only`; query evaluation
must follow freezing and must not be relabelled as independent after tuning.

The next target is stronger, spatially distributed cross-phone image matches.
Keep both image-only and supplied-pose routes labelled; neither common coordinate
metadata nor a low training residual establishes reliable multi-view replay.
