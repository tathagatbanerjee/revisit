> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-coordinates/result.md`.
> Original SHA-256: `8716b215d2a231c309518ea91c30fea52ae8eeb2f0aa34bb2691e6fa8dcea217`. Private media/logs are not included.

# Shared-coordinate recovery: first tests

17 October 2026. **A background-only joint map now connects three handheld
phones in the Medium recording**, including one visibly moving camera. Later
frames from those phones localize against that frozen map. This is a partial
camera-alignment result; it does not establish metric pose accuracy, full six-phone
coverage, independent timing accuracy or improved dynamic reconstruction.

## What ran

Existing local CPU environment: pycolmap 4.2.1, OpenCV 5.0, four extraction/matching
threads, affine DSP-SIFT, guided matching, fixed supplied per-frame intrinsics,
masked people. Extrinsics were recovered from image evidence, without using
phone metadata positions/rotations or Panoptic author R,t as initialization.
OpenCV-to-COLMAP principal points use the +0.5 pixel-center conversion.
No Gaussian fitting, new paid resources or model/media downloads.

| Test | Mapping images | Shared-map result | Native elapsed |
| --- | ---: | --- | ---: |
| Panoptic00/24 known-calibration control | 10 | No model; only one cross-camera pair, 22 inliers | 0.79s |
| Panoptic00/24 original 1080p, resolution control | 10 | All 10 images, 1,044 shared landmarks; pose gate passed | 18.95s |
| 4DM Easy, five training phones | 25 | Two images from two phones, 37 cross-phone landmarks; gate failed | 23.93s |
| 4DM Medium, five training phones | 25 | 15 images from three phones, 1,975 landmarks, 305 cross-phone landmarks; map gate passed | 22.15s |

These times include feature extraction, matching and mapping, excluding input
review/export/browser checks. Model0 in Medium is a separate five-frame,
one-phone map and must not be merged into the shared model by pretending its
scale/orientation matches. Another phone has no registered images. The whole
sixth phone is excluded from all three phone-map/localization steps.

Easy has phones held stably; Medium has three moving operators according to the
[official dataset description](https://github.com/fabiopoiesi/4dm). Easy alone
cannot test substantial trajectory recovery. Medium was added explicitly before
its run with unchanged configuration and gates; no parameter sweep was made.

The successful shared model contains:

| Display label | Phone prefix | Training states | Endpoint rotation | Displacement / median inter-phone baseline |
| --- | --- | ---: | ---: | ---: |
| Phone1, orange | 378d43ce | 5/5 | 0.84° | 0.0016 |
| Phone2, green | cc74017e | 5/5 | 8.32° | 0.0435 |
| Phone3, blue | d7ec5aa6 | 5/5 | 0.50° | 0.0006 |

These are recovered relative trajectories in arbitrary SfM units, not measured
metres or independent ground truth. They span event0–2s; the later localization
frames are at event2.5s (original source frame170). The strongest moving trajectory
is Phone2; the other two show limited motion in this short interval.

## Frozen-map localization

The 15-image map was frozen and its files hashed. Five later candidate frames
were reserved before mapping; only the three phones in the shared model were
localized. No map, intrinsic or existing camera updates were allowed. All hashes
are unchanged afterward. DSP-SIFT descriptors match existing 3D-point tracks;
2D/3D PnP-RANSAC uses a 2px threshold and refines only the new query pose.

| Query phone | PnP inliers | Median inlier reprojection | >=30 inliers / <=2px gate |
| --- | ---: | ---: | --- |
| Phone1 | 92 | 0.805px | Passed |
| Phone2 | 844 | 0.385px | Passed |
| Phone3 | 75 | 0.421px | Passed |

The main run took 1.84s. Most descriptor matches select references from the query's
own phone. Therefore a stricter diagnostic removes all same-phone references,
without changing thresholds: Phone3 passes with 45 inliers/0.353px; Phone1 and
Phone2 have tentative matches but no accepted PnP pose. This separate check took
4.69s. Cross-phone support remains uneven despite the shared training map.

Reprojection residuals on fitted inliers do not independently certify pose
accuracy. The diagnostic overlays show support concentrated on decking, static
props and wall panels, with poor coverage of some image regions. Shadows are not
removed by person masks. Planar/repeated textures, short baselines, mask misses
and distortion can still produce inaccurate geometry or ambiguous poses.

## Known-calibration control

The original 640px control did not reach its >=30-background-track map gate. A diagnostic
essential-matrix fit to the strongest existing 22-match pair yields 16 cheirality
inliers, 6.18° relative-rotation error and 14.07° baseline-direction error against
supplied calibration. This misses the declared 5° rotation gate and lacks enough
tracks. It is not a validated control success. No control thresholds were lowered.
Fixed cameras and repeated dome fixtures give little new background evidence
across time. The pair uses different times, which is acceptable for stationary
background recovery with people masked, not for triangulating a moving person.

The separate full-resolution control uses the existing original 1920×1080
recordings at the same timestamps, rectified with native calibration. The same
person masks are enlarged with nearest-neighbour sampling. Matching/mapping
options and success thresholds stay fixed; only source/extraction resolution
and corresponding intrinsics change. All 10 images register, with 1,044 shared
background landmarks and 0.891px median point error. No author extrinsic is used
for recovery.

Across all 25 recovered cross-camera pose combinations, median/worst relative
rotation errors are 0.439°/0.615°; baseline-direction errors are 1.759°/2.485°.
Every pair passes the original5°/15° gates. These combinations share observations
and are not 25 independent trials. Translation magnitude/metric scale is not
validated. The pose validation report (historical reference: `control-pose-validation.json`) retains all
pairs. This is evidence to recover cameras from original-resolution imagery
before downsampling for splat fitting, not a guarantee on every scene.

## Inspect the artifacts

At http://localhost:4318 select **Shared camera coordinates**, then
**Medium · three-phone sparse map and paths**. Orbit, or use **Recorded viewpoint**
for each recovered phone's start/last pose. The output contains 1,975 observed
background landmarks displayed as point glyphs, plus 207 coloured camera/path
glyphs. These are sparse diagnostic markers, not a trained Gaussian background
or reconstructed people. Scale and floor/up are not established. Blank regions
are expected and must not be interpreted as successfully reconstructed surfaces.

Native/private evidence:

- All Medium source/mask samples (historical reference: `../../working/shared-coordinates/phones-medium/all-mask-review.jpg`).
- Later-frame observation/projection overlays (historical reference: `../../working/shared-coordinates/phones-medium/localization/contact.jpg`): green observation circles, red projected crosses.
- Strongest Medium cross-phone matches (historical reference: `../../working/shared-coordinates/phones-medium/strongest-cross-camera-matches.jpg`).
- Browser diagnostic (historical reference: `../../working/shared-coordinates/browser/shared-coordinates-medium/side.png`).

All masks were inspected at contact-sheet scale; broad people coverage is visible,
while shadows remain. Strongest control/Easy/Medium matches and all three main
localization overlays were inspected. The native sparse point coordinates, camera
poses and browser rendering were checked. No anatomical reconstruction is shown.

## Verification and resources

Verification record (historical reference: `verification.json`) confirms 80 RGB/mask hash pairs, all 18
camera transforms and unchanged frozen-map hashes. Artifact validation (historical reference: `artifact-validation.json`) passed finite PLY/quaternion and
hash checks. Browser checks (historical reference: `browser-check.json`) passed load, orbit, reset and
all six recovered-camera pose/intrinsic selections. This is a static diagnostic;
no event playback capability is claimed. Chromium SwiftShader checks establish
interaction, not hardware rendering throughput. Source inputs and masks have
recorded hashes (historical reference: `input-provenance.json`). No source media enters Git.

The existing Runpod was read only to retrieve previously computed control masks;
no new remote job was launched. Its existing 20:25:35 Sydney deadline was not
extended. All feature extraction/mapping/localization occurred locally.

Commands, from the app root, using the existing local environment:

```sh
timeout 600 working/brush-mosca/tools/bin/python runpod/shared-coordinates.py control
timeout 600 working/brush-mosca/tools/bin/python runpod/shared-coordinates.py control-full
timeout 600 working/brush-mosca/tools/bin/python runpod/shared-coordinates.py phones
timeout 600 working/brush-mosca/tools/bin/python runpod/shared-coordinates.py phones-medium
working/brush-mosca/tools/bin/python runpod/inspect-shared-coordinates.py
working/brush-mosca/tools/bin/python runpod/localize-shared-coordinates.py
CROSS_PHONE_ONLY=1 working/brush-mosca/tools/bin/python runpod/localize-shared-coordinates.py
working/brush-mosca/tools/bin/python runpod/publish-shared-coordinates.py
```

Scripts refuse to overwrite existing run directories; preserve these results
before an explicitly scoped rerun. Inputs include the existing prepared RGB,
COCO masks, calibration and downloaded per-frame phone metadata.

## Camera handoff

Recovered cameras (historical reference: `shared-cameras.json`) export all 15 training and three later
localized camera poses in one named coordinate gauge, with per-frame K,
OpenCV camera axes/pixel convention, original source-frame ids, nominal event
timestamps, camera-to-world transforms and observed-point/PnP support. Metric
scale and world-up are explicitly unknown. This is the handoff for a later
Brush/MoSca trial, not a claim that every source phone was registered. Disconnected
maps are excluded. Regenerate with `runpod/export-shared-cameras.py` using the
same existing local Python environment.

## Implication

One shared background map is a workable foundation for a subset of our phone
recordings. Camera recovery must expose connected components and confidence;
a pretty lead view is insufficient. Next, validate pose accuracy and broaden
cross-phone support before passing recovered trajectories into dynamic fitting.
The locked MoSca quality baseline and previous calibrated refinements remain
unchanged.
