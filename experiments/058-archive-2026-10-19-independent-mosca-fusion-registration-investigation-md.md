> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/independent-mosca-fusion/registration/investigation.md`.
> Original SHA-256: `f45106d54a7c106b6a8671a1882924b7d00ba43beb9d2fb488b2795c4a3df246`. Private media/logs are not included.

# Direct background registration — 19 October 2026

The user approved a registration-only follow-up on the two saved full MoSca fits.
Keep A fixed; solve B directly into A with rotation, translation and positive
uniform scale. No reconstruction retraining, cloud worker, new checkpoint,
Gaussian edits beyond the global similarity, opacity adjustment or hybrid.
All earlier artifacts and failed readiness gates remain immutable. Camera20 RGB
stays sealed; only the previously seen00/24 training footage is used.

## Procedure fixed before registration

Use five matching native samples A[6,12,18,24,30], B[0,6,12,18,24]. Inspect source
images and conservative person/arm exclusions before matching. Reuse available
A masks or reviewed coarse source masks; never assume every MoSca static point
is background. Extract mutual SIFT matches, ratio0.75, supplied epipolar residual
<=1.5px, excluding foreground. Group repeats by16px reference-image cells;
reserve cellHash%5==2 for validation, so repeated source landmarks do not leak
between fitting and validation. These are seen training-camera diagnostics.

Associate source features with actual saved Gaussian depth using a CPU sparse
projection/alpha-composition adapter: full covariance, projected pixel footprint,
opacity and depth ordering. Compare this adapter with saved native-render anchor
samples before trusting associations. Do not substitute Metric3D prior depth
for the reconstructed geometry or call approximate CPU/native rendering exact.
Gate adapter on median relative depth discrepancy<2% on retained samples and
finite alpha/depth. If unsupported, record failure before treating registration
as established. Source pixels/3D matching are numerical associations, not proof
of physically correct surfaces.

Fit one full7-parameter B-to-A similarity from training background matches using
fixed-seed robust RANSAC,0.15m-equivalent residual threshold,1024 iterations,
then robust refinement. Require>=12 inliers and at least four validation
landmark cells for quantitative readiness; report validation median3D discrepancy
and projection in both fitted source cameras. Registration gate: validation
3D median<=0.10m-equivalent AND median maximum two-view residual<=15px. Source A's
old scalar gives only approximate meter conversion; no new metric accuracy claim.

Then one coarse-to-fine trimmed background ICP pass on high-opacity static
Gaussians outside reviewed foreground masks, after voxel reduction for matching
only (all output Gaussians retained). Use three correspondence-distance levels
0.20/0.10/0.05m-equivalent,10 updates each, retain the best70% correspondences.
Solve similarity updates; constrain total ICP changes from the feature estimate
to20% scale,10 degrees and0.25m translation. Preserve coarse/refined candidates
regardless of which scores better; no threshold sweep or post-inspection tuning.
This follows the coarse/global then local-registration pattern documented at
https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html;
use cached NumPy/SciPy/OpenCV rather than installing a new library.

Publish the old union, A, feature-registered union and ICP union in a new group,
with identical clocks, appearance and inspection cameras; retain original
camera A/B views plus the final registered B source pose as a third diagnostic
view. Same40-state interval composition,65,507 A points,62,380 B points,
127,887 in overlap. No geometry thinning, deformation interpolation or ended
actor freeze. Compare fixed-time viewpoint changes and three overlap instants,
plus first/final states. Report room alignment and person alignment separately.
A global transform need not correct different learned shapes/intrinsics.

## Cost estimate and run limits

Local cached Python3.12 CPU NumPy/SciPy/OpenCV/Pillow and cached Chromium; no
installation/network/model inference or paid compute. Expected5–20 minutes,
maximum30min registration process,<=4GiB RAM and<=2GiB additional local output.
Existing viewer service remains running; unrelated apps/Docker/WSL untouched.
No previous Pod is restarted. Close only our isolated browser. One bounded
adapter/implementation repair may address a programming fault, not a tuning
sweep. Save exact input/config/source hashes before solving; preserve failures.
Use focused geometry/artifact checks and browser inspection; no quality winner
or complete-person success follows from correctness tests alone.

## Preserved feature-preparation failure and separately scoped association

The fixed SIFT preparation produced8 matches in only4 reference cells, with
one validation cell: insufficient. Do not relax its ratio/epipolar settings or
call those repeats independent landmarks. The CPU depth adapter passed on59/49
native samples with median relative discrepancies about3e-7.

A preparation-only inspection found the tiny dark wall dots correspond to the
supplied VGA camera centres, whereas SIFT largely misses these few-pixel marks.
Use known calibration ONLY to establish visible landmark identity, not as the
3D target of registration. For the same five frames detect actual grayscale<100
connected blobs with area1–25px and aspect0.4–2.5. Project VGA camera centres into
each source using the existing supplied calibration; require unique nearest
blob within3px and a second-nearest margin greater than2*distance+1px. Require
background exclusion in both views, same camera identity, and the unchanged
1.5px epipolar check. Fit B Gaussian depths directly to A Gaussian depths.
Canonical16px A-image cells from the projected landmark identity prevent
repeated-frame split leakage. Preserve the earlier feature failure separately.
This is a calibration-assisted control, not blind phone correspondence recovery.
No camera20 RGB or other new camera images are read; existing calibration may
identify wall camera housings visible inside the already-seen00/24 recordings.
Keep the same7-parameter/ICP settings and gates fixed above. No output from the
registration solver has been inspected when selecting this association recipe.
