> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-mosca/person-masks-investigation.md`.
> Original SHA-256: `1fd8dc1782f457093a2ab4a70b29479bfdaec0c73b47da4a3f4b16d80cff2ab1`. Private media/logs are not included.

# Visitor-mask follow-up

Authorized 2026-10-14 after the first H1 hybrid exposed missing floor geometry.
This repeats only the selected Guildhall test, with a separate working/job/run
scope; original H1 outputs and failure evidence are retained.

## Selected change and controls

Replace the top-220 architecture band with manually reviewed, padded exclusion
rectangles around each visible visitor, plus localized crowded-person regions
where individual silhouettes are ambiguous. These are conservative masks, not
exact silhouettes or an automatic segmentation model. Thirty frames are small
enough to inspect directly. Six clean views keep all pixels. The recipe is
versioned in `resources/person-mask-recipe.json`; overlays are ignored evidence.

Keep the source bytes, train/holdout split, H1 camera poses/intrinsics, sparse
initial points, world alignment, previous MoSca model and 3,000-step Brush
settings unchanged for the first comparison. Both methods remain inspectable.
No new MoSca fitting, generated floor, multi-camera fusion or source-video edit.

Reviewed masks retain about **92.7%** of image pixels and **81.5%** of the lower
140 rows on average. The earlier mask excluded that lower band entirely.
Actual counts/hashes are saved with the new dataset. Brush grayscale-alpha
mask naming and consistent image/mask undistortion use the already verified
pipeline. Floors permanently occluded by people still have no direct evidence;
rectangles also exclude some adjacent background and may leave boundary errors.

## Resources, costs and run limits

`HYBRID_TRIAL=person-masks` isolates state, inputs, cloud outputs and the original
four-hour deadline under `working/brush-mosca/person-masks/`. New viewer runs
have a `-person-masks` suffix. Never overwrite or relaunch the cleaned-up H1 job.

One sequential A10G g5.xlarge On-Demand session, same pinned AMI/release and
US East region. The launch queried the AWS Price List API and enforced
**US$1.006/hour**. Maximum combined session **US$6 before tax**; no input/session
upgrade follows automatically. At most four hours from the initial launch,
including setup repair and retrieval, with independent termination schedule
and worker self-shutdown. Expected charges are a small fraction of the earlier
US$2–4 planning range if setup and the short Brush fit work as before; the full
allowance covers failures. Identify retained versioned S3 storage after cleanup.

The first worker stopped before reconstruction because Ubuntu unattended
updates held the dpkg frontend lock. Its EC2 console was retained (the control
venv was not yet installed, so bootstrap S3 upload could not run). The boot
wrapper now uses a 300-second dpkg-lock wait. One replacement is permitted only
after the previous instance is verified terminated and its disk removed, under
the **original deadline**, original prefix-only access and budget. This is a
setup repair, not a reconstruction/profile change. No parallel workers.

## Inspection

Compare old/new Brush backgrounds and old/new hybrids with exactly the same
source/held-out camera poses. Check whether visible carpet, pedestal and lower
walls return; look for permanent visitor ghosts and projection/stretch errors.
Record lower-image rendered coverage as an appearance diagnostic only, not a
metric floor area or verified 3D reconstruction score. Inspect the original SH
export separately from matched DC comparisons.

Repeat frozen-time camera movement, fixed-view seeking/playback and endpoint
loading. Check that the background is byte-identical across sequence states
and the reused foreground remains unchanged. Retain real outputs and logs,
terminate/retrieve promptly, then independently verify compute, disk, IAM and
scheduler teardown. Add measured result/lessons after inspection.

## Completed result

The result (historical reference: `person-masks-result.md`) records visible lower-scene appearance
improvement and unchanged motion/control checks. The floor remains coarse.
The successful Brush command took 22.93 s and produced 9,801 Gaussians. The
first apt-lock failure and one replacement both fit the original US$6/four-hour
scope. Both instances/disks and temporary access/schedule resources are removed;
conservative combined compute allowance US$0.255, roughly US$0.30–0.50 total
before tax. No native MoSca retraining or further case followed.
