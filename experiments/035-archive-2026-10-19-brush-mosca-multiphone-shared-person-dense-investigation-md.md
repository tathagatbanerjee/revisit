> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/dense-investigation.md`.
> Original SHA-256: `c086d180b5bbd4dfae2ed38c07c6967a265ae2d3073601d11cdb28910941769a`. Private media/logs are not included.

# Dense foreground initialization: calibrated plane sweep

19 October 2026. The user requested continuing the dense initialization feasibility
check after the failed sparse probe. Select **one custom calibrated plane-sweep
depth matcher using the installed OpenCV/NumPy**, then reciprocal depth filtering
and fusion. This is local CPU work on one instant, not a new Gaussian fit.

## Why this route

Camera poses and intrinsics are supplied and already convention-checked. Plane
sweep can project each reference depth hypothesis into any training camera
without adding a learned depth prior, weights or another coordinate system.
Normalized cross-correlation (NCC) reduces sensitivity to affine brightness
differences. Local patch assumptions, textureless fabric/skin, occlusions and
large angle changes can still defeat it. Smooth or plausible depths alone do
not establish observed surfaces. Report failure rather than filling invalid pixels.

The only foot-observing pair in this audit is21/02, with a 54.5° optical-axis
difference. Other pairs to02 span74.7–86.5°; the primary three span30.7–32.2°.
These known geometric differences explain why adding02 may not provide useful
appearance matches, but do not determine the outcome in advance.

## Sources, implementation and terms

Read official OpenCV documentation on 19 October 2026:

- [Camera projection](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html):
  K[R|t] maps world points into cameras. The custom sweep uses this equation
  directly; it does not call an upstream pretrained reconstruction method.
- [Image remapping](https://docs.opencv.org/4.13.0/da/d54/group__imgproc__transform.html):
  use reference-to-donor pixel maps with bilinear RGB and nearest-neighbor masks.
- [Box filtering](https://docs.opencv.org/4.13.0/d4/d86/group__imgproc__filter.html):
  local means, products and variances implement the patch NCC objective.

Reuse Python 3.14.3, opencv-python-headless5.0.0.93, NumPy 2.5.4 and Pillow 12.2.0.
Installed package licenses were inspected: Apache2.0, NumPy's declared BSD/MIT/etc
license expression, and MIT-CMU respectively. No models, accounts or license
activation are added. The cited 4.13 docs describe APIs checked against the
installed 5.0 wheel by synthetic and real execution. Save the custom script hash.
Panoptic footage remains private, research/noncommercial, with no redistribution
without permission, as recorded in the existing source manifest.

## Fixed smallest trial and filters, declared before the run

Use `working/shared-person/verified/` only: one synchronized instant, training
cameras 00/24/21/02, supplied calibration, and checksum-verified1920x1080 rectified
frames. Downsample with area filtering to640x360 and transform K with the matching
pixel-center rule: principal point becomes(c+0.5)/3-0.5. This is a bounded dense
probe; unlike the earlier sparse1080p test it sacrifices image detail. Use the
same conservative foreground masks downsampled by nearest neighbor. Never open
camera 20 or any other new source. Verify the reservation and preserved control
hashes before and after execution.

Compute all twelve directed training-camera pairs,256 inverse-depth planes
uniformly spanning1–6 m in each reference camera,9x9 grayscale NCC patches.
The range is predeclared, broad compared to sparse observed depths2.30–3.22 m,
and is not estimated from evaluation or author body annotations. All patch pixels
must lie in the conservative reference mask; require≥ 98% warped donor-mask
occupancy, positive donor depths and source-image bounds. Reject patch standard
deviation<0.025 in either image, best NCC<0.75, or a uniqueness margin<0.05
against any depth outside the best plane's +/-2-plane neighborhood. Reject
search endpoints. Use parabolic sub-plane interpolation only at an interior
finite local minimum; never interpolate across invalid planes.

Independently compute both directions. Retain a correspondence only if its
donor-pixel reverse depth is also confident, depth residual<=max(0.03 m,1% of
donor depth), and the reverse point reprojects within1.5 reference pixels.
Require triangulation angle≥ 2° and world radius<10 m. These checks reject many
occlusions but cannot guarantee correct visibility or matching on repeating
textures. Do not infer support from a projected mask alone. Save independent
directional confidence/depth maps, accepted pair points and diagnostic overlays.
Do not smooth, inpaint, complete silhouettes or add the old person's centers.

Fuse accepted positions into 5 mm voxel bins, averaging position and observed
colour. Preserve per-point source/pair provenance in the raw private archive;
export the fused cloud in both author-world meters and the fixed Brush room's
SfM world using the existing similarity. This is a colored point cloud, not a
Gaussian model or temporally coherent representation.

Sparse thresholds and failures remain unchanged. Dense readiness requires:
≥ 500 distinct5 mm bins overall; ≥ 50 accepted reference-pixel observations per
training camera; ≥ 20 distinct bins in each head/hands/feet coarse image-region
group; and≥ 10% of conservative person-mask pixels supported per training camera.
Coarse regions are diagnostic boxes from the source audit, not anatomical ground
truth. A numeric pass still requires credible depth and body-region inspection.
Do not fit a person from scattered torso points just because its count is large.

## Checks, resources, cost and stop conditions

Before real input: test a known textured plane with a camera baseline against
known metric depth and reverse projection; test untextured inputs and missing
foreground evidence are rejected. Check image-resize projection consistency.
Use four CPU threads, one pair cost volume at a time (about225 MiB float32 plus
scratch). Expected peak<2 GiB, disk<1 GiB and<10 minutes total; measure actual
process RSS and runtime. Enforce a600-second process timeout, no cloud worker,
no GPU use, no new weights, no parameter sweep and no threshold relaxation.
One implementation repair for an actual software fault is allowed with failure
evidence retained. Network costs and paid service charges are zero for this run.
Machine electricity and existing hardware are not separately billed here.

Deliverable: real masked dense maps/cloud, per-camera/body-region support,
gate decision, inspection evidence, source/control/output hashes, repeatability
and the next decision. If this fails, identify whether correspondence, input
coverage or depth confidence blocks fitting; recommend a better-supported
training capture or a separately investigated learned/prior route. Reserve20
until all selected architecture candidates have frozen.
