> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/mast3r-result.md`.
> Original SHA-256: `9665f6d9590d5329841804dfff7767bb0008dba35cf471b748ff6ebb1a9aba9a`. Private media/logs are not included.

# Learned matching trial: working inference, restrictive confidence policy

Current follow-up: native-detail audit and targeted shoe check (historical reference: `targeted-feet-result.md`).
The historical trial below stays unchanged; later tests support upper-body
consistency but still fail useful three-view foot support.


19 October 2026. **MASt3R now runs locally and proposes many geometrically
consistent person matches. The selected confidence-filtered initializer fails
readiness; this does not establish that the learned route is unsuitable.**
The main rejection happens at our uncalibrated descriptor-confidence cutoff.
No Gaussian fitting, paid compute or evaluation20 access occurred.

## What ran

The investigated route (historical reference: `mast3r-investigation.md`) uses one first-instant21/13
pair, original-resolution person crops, a 512-long-edge MASt3R forward pass,
reciprocal learned descriptor matches and supplied-camera triangulation.
Predicted point maps are retained separately as unregistered model inference;
they never seed the accepted point cloud. No camera optimization or author
3D body annotations are used.

Source/weight pins (historical reference: `mast3r-pins.json`) identify the official source and
2,754,910,614-byte checkpoint. The initial stream was slow; its preserved prefix
and four validated HTTP-range streams completed the same file in 589.56 seconds,
within the original 600-second bound. All1,013 archive entries pass CRC checks.
Source clone to pinned checkpoint took 809 seconds, under the 20-minute setup cap.
The original partial prefix remains as retrieval evidence; no second model was
downloaded. Code/checkpoint notices remain with the ignored source checkout.

The isolated environment freeze (historical reference: `mast3r-environment.freeze.txt`) uses Python 3.12,
PyTorch 2.5.1+cpu and torchvision 0.20.1+cpu. The memory-mapped/meta-device loader
materializes all 688,638,856 parameters with no missing/unexpected keys.
Two CPU threads, float32, one forward pair. No GPU or cloud allocation.
Optional compiled RoPE is absent; the upstream PyTorch fallback works. An
upstream disabled-autocast deprecation warning is retained without source edits.

Person crops differ from full-frame640 px NCC, so this is not a pure matcher-only
comparison. Crop tensors match the upstream loader exactly; recorded inverse
pixel transforms carry matches back to the original rectified calibration.
Camera 13's manual mask and 21's automatic mask remain unchanged/asymmetric.

## Frozen candidate and gate outcome

| Stage | Correspondences |
| --- | ---: |
| Reciprocal candidates, merged directions |24,808 |
| After network borders |23,621 |
| Inside both conservative person masks |11,500 |
| Both descriptor confidence scores≥ 1.5 |357 |
| Descriptor dot≥ 0.8 |357 |
| All calibrated geometric checks |357 |

The retained points fuse into **293 approximate5 mm bins**, with coarse
head/hands/feet counts **0/0/6**. Unique source-pixel coverage is **1.40%** in 21
and **1.91%** in 13. Seven accepted shoe pairs occupy six bins on the image-left
shoe tip; the other shoe has no accepted support. The images mostly show shirt
lettering and that tiny shoe patch. Numeric and visual initialization gates fail.
See frozen measurements (historical reference: `mast3r-report.json`).

Inspected private evidence:

- Accepted support and calibrated cloud (historical reference: `../../working/shared-person/mast3r/trial/observed-support-and-cloud.jpg`).
- Selected source-image matches (historical reference: `../../working/shared-person/mast3r/trial/matches.jpg`).
- Individual shoe correspondence check (historical reference: `../../working/shared-person/mast3r/trial/shoe-correspondences.jpg`).

The existing MoSca quality baseline and room/person controls are unchanged.
There is no new Gaussian model, moving-person scaffold or browser candidate.

## The confidence bottleneck: a separate rejection diagnostic

Our 1.5 descriptor-confidence cutoff was a predeclared conservative policy, not
an upstream-required threshold or calibrated probability. The official matching
example does not prescribe this cutoff. Keep its failed candidate frozen.

Analyze the **complement** of this fixed rule without a threshold sweep, new
inference, point-cloud replacement or promotion:

| Cohort | Candidate pairs | Pass the same geometric checks |
| --- | ---: | ---: |
| Frozen selected confidence cohort |357 |357 (100%) |
| Rejected only by confidence |11,143 |11,126 (99.85%) |

The rejected, geometrically consistent cohort includes 1,035 head-region,
405 hand-region and 794 foot-region pairs. These are correlated pairs, not
distinct anatomical surfaces. Its minimum-across-views confidence has median
0.763, versus 1.614 in the frozen cohort. These scores are not probabilities.

Orange rejection overlay (historical reference: `../../working/shared-person/mast3r/trial/confidence-rejection-diagnostic.jpg`)
shows broad person support that the rule suppresses. This identifies a policy
bottleneck; two-view consistency alone cannot prove those matches are correct.

A further **already-seen camera 02 diagnostic** projects each cohort into its
preserved source image without fitting or revealing evaluation20. Of the 11,126
rejected/consistent points,10,476 (94.16%) project inside the conservative person
mask. Median RGB MAE there is 0.0373 versus 0.0412 for the selected cohort. Visibility
is not independently known; occlusion, lighting and mask error affect these
figures. They are development evidence, not fresh evaluation or pointwise truth.
See the seen02 overlay (historical reference: `../../working/shared-person/mast3r/trial/seen02-cohort-diagnostic.jpg`)
and diagnostic measurements (historical reference: `mast3r-confidence-diagnostic.json`).

No initializer was exported from the rejected cohort. The 293-bin candidate and
its hashes remain exactly as selected before this diagnostic.

## Verification and resources

The forward pass took 9.92 seconds. Matching plus postprocessing took 163.57 seconds;
the worker completed in 177.38 seconds (parent wall180.30 seconds). Actual worker
peak RSS was3,304.22 MiB, below the 5 GiB limit; the 900-second watchdog completed
without intervention. The workspace, including environment/checkpoint/prefix,
uses about4.5 GiB. External service cost isUS$0.

All eight geometry tests pass in the actual inference environment; `pip check`
passes. Synthetic crop inverse/projection checks and upstream tensor parity
pass. Replaying saved matches reproduces the frozen calibrated PLY hash exactly.
Accepted geometry is finite and meets the fixed depth/angle/reprojection gates;
the Brush-world export agrees within 1e-7 SfM units. All frozen output, input,
mask/control and source/weight hashes verify. Media/weights/points are ignored.
No second neural inference was needed for these checks. See
verification (historical reference: `mast3r-verification.json`) and watchdog receipt (historical reference: `mast3r-bounds.json`).

## Next step

**Validate correspondence acceptance, rather than switch models or blindly lower
the cutoff.** Use additional already-seen training views and visible landmarks/
three-view correspondence cycles to test the rejected matches, including both
shoes. A projected silhouette or low RGB error alone is insufficient. Define the
acceptance rule and finite pair/resource scope before a new candidate; preserve
this failure. Existing raw correspondences and weights can be reused.

After that check, build one shared initializer from every selected synchronized
training camera, then the single-instant foreground fitter with observation-
supported growth. A two-view feasibility probe does not complete experiment A.
Keep the Brush room fixed, retain the inherited-person control, and keep20 sealed
until all selected architecture candidates freeze. Motion B and body-prior C
remain subsequent comparisons.

Attribution: Vincent Leroy, Yohann Cabon and Jérôme Revaud, *Grounding Image
Matching in 3D with MASt3R*, ECCV 2024; DUSt3R/CroCo source and checkpoint notices
are pinned in the investigation. This is a private noncommercial research trial.
