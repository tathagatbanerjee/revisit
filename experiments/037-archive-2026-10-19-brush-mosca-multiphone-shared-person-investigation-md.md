> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/investigation.md`.
> Original SHA-256: `44e6db3bd3a080de4c49f14d5c44da20e1507906265ce7917443209303d550ba`. Private media/logs are not included.

# Shared-person initialization: controlled architecture comparison

Follow-up: the dense investigation (historical reference: `dense-investigation.md`) and
actual result (historical reference: `dense-result.md`) now supplement the sparse readiness probe below.
Both initialization routes fail complete-person readiness; no Gaussian fit yet.

19 October 2026. The user requested proceeding with the immediate preparation
described in the resume plan. This phase is local input/readiness work. No paid
worker launch, old-session extension, or evaluated-model refitting is included.

## Question and comparisons

A: Can geometry initialized from simultaneous training observations recover a
more complete person than the saved lead-derived foreground? Use one instant,
state 000 / source time 0, chosen before matching. Fit one shared foreground with
observation-supported growth; hold the saved assembled Brush room completely
fixed. Both the inherited foreground control and new candidate must use the
same cameras, masks, DC renderer, room and black compositing. Preserve all old
outputs. Geometry initialization cannot use old person centers as its sole seed.

B: Only after A passes native inspection, extend to the existing twenty states
over 0–2.9029 s, with persistent identities and motion constraints. Independent
frame fits do not pass. C: compare a parametric body initialization with skeletal
and residual deformation after a separate model-access/license/readiness audit.
Neither B nor C is implemented by this preparation.

## Selected initialization route and local gates

First audit original-resolution, rectified, foreground-only mutual SIFT matches
and calibrated triangulation. This is the smallest observation-driven route
with existing local dependencies. It can fail on untextured skin/clothes and
occlusion; sparse matching is a readiness probe, not a dense-surface guarantee.
Use supplied Panoptic R,t/K as an explicitly known-calibration control. Convert
centimeters to meters; world-to-camera is R X+t. Rectify originals directly
using K/distCoef at 1920×1080, not upscaled640 px RGB. Existing automatic masks
are coarse640 px masks, conservatively eroded before nearest-neighbor upscaling.
Record their hashes and this limitation. Do not use author 3D body annotations.

Primary training cameras:00/24/21. Initial source inspection shows feet are
cropped from 00/24. Audit already-seen02 as a fourth training camera rather than
pretending that one foot view supplies stereo support. Save both subsets'
measurements. Reserve another camera using calibration alone, excluding all
previously opened cameras 00/01/02/21/24. An exclusion audit checks known local
source/evaluation records; absence is not a universal access log.

Fixed matching settings:8,000 SIFT features/image, mutual Lowe ratio0.8;
Sampson error<=1.5 px, reprojection<=1.5 px per participating image, positive
depth>0.1 m, triangulation angle≥ 2 degrees, world radius<10 m. Reject nonfinite
points. A feature observed in a third view may be checked there, but projecting
inside its mask alone never establishes correspondence or nonocclusion.

Predeclared minimum sparse-readiness gate:100 distinct 5 mm spatial bins, at least
10 accepted pair observations incident on each chosen camera, and five accepted
pair points in each manually reviewed head, hands and feet image-region group.
Region boxes are coarse visual diagnostics, not anatomical ground truth; even
a numerical pass requires mask/point overlays and credible distributed surfaces.
Retain failure at unchanged thresholds; do not pool different times to manufacture
one instant's geometry. A failed route blocks fitting until better observations
or a separately investigated dense-depth route addresses the missing support.

## Evaluation and acceptance

Reserve by minimizing the largest optical-axis angle to00/24/21 among unused
HD cameras, tie-breaking by sum then node. Save calibration hash, full ranking,
selected camera and selection time before any future fitting. Do not read its
RGB until the final completed A/B/C candidate set is selected, frozen and hashed.
Recheck exposure history before launch. Cameras21/02 are training/seen diagnostics.

For A, require all training-camera losses to yield finite nonzero gradients on
the shared foreground; retain the same fixed background hash throughout fitting.
Report person/background MAE separately and head/hand/foot crops, alpha/depth,
source renders and nearby orbits. Proposed promotion gate: no training-camera
person MAE regression>5%, ≥ 10% mean independent person MAE improvement over
the inherited control, and visually improved missing-body coverage without new
floaters. These are proposed trial thresholds, not measured results. Silhouette
and aggregate room error alone cannot pass. B additionally needs coherent motion
and no identity popping. Native/browser inspection remains required after fits.

## Implementation and dependency readiness

Local preparation pins Python 3.14.3, OpenCV wheel 5.0.0.93, NumPy 2.5.4 and
Pillow 12.2.0 in an isolated ignored environment. Only preparation is installed.
Existing source inspected: `runpod/prepare-calibrated.py`, `match-calibrated.py`,
`calibrated-refine.py`, `prepare-assembled-hybrid.py`. The saved refiner has fixed
topology and cannot test A's geometry growth; a new foreground trainer is needed.
The prior MoSca pin is02404d2841b4e0dc2d9074860950bce5da579656; Brush is v0.3.0.
Those are preserved regression assets, not a tested new environment. Local
PyTorch, its CUDA rasterizer, growth/export and candidate adapters are not ready.
The local8 GB GPU was detected, but renderer compatibility and fit memory have
not been tested. No claim that this training fits locally follows from detection.

Sources inspected19 October: [OpenCV camera projection/triangulation](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)
and [SIFT API](https://docs.opencv.org/4.13.0/d7/d60/classcv_1_1SIFT.html).
The browsed reference is4.13; check installed 5.0 APIs with the actual local run.
OpenCV is Apache 2.0; retain installed package metadata. Existing Panoptic source
manifest restricts footage to research/noncommercial use and redistribution
requires permission. Original/derived footage and person points remain private.
Any new training dependency or body model needs its own source/version/terms pin.

## Cost estimate and run limits —19 October 2026

Current route: local CPU preprocessing only, one instant, four existing videos,
no network media/weights download, no provisioned infrastructure. Disk available
at inspection:823 GiB; use <2 GiB for this preparation and stop matching after
10 minutes. No external service charges are incurred by this phase. Existing
Runpod account query returned an empty Pod list; old state stays closed.

Proposed later A-only GPU bound, pending readiness and a concrete run decision:
one compatible worker, two-hour launch-relative independent shutdown, US$2 total
allowance, no persistent volume, one software repair, no fitting sweep or fallback
worker. Historical A40 price wasUS$0.59/hour; it is NOT a current quote. Requery
price/capacity before selecting a worker and require<=US$0.59/hour. At that ceiling
expected 0.5–1.5h compute isUS$0.295–0.885; two-hour compute isUS$1.18. Other
storage/transfer/tax must be priced within the remainingUS$0.82 or the run cannot
start. Setup/download/export/retrieval time count. B/C require their own scope
after actual A readiness. Retrieve/hash artifacts, terminate and verify cleanup.

Deliverable for this phase: reproducible camera reservation, source/time/hash
manifest, source coverage and foreground matching overlays, sparse point file,
gate outcome and exact implementation/input blockers. No new model or viewer
candidate is promised by preprocessing.
