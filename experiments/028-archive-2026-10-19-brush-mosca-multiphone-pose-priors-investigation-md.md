> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/pose-priors/investigation.md`.
> Original SHA-256: `ae75eae7ddaf300a59ce37c112d7633ccca33051aca93f9ef62cb92de32f478f`. Private media/logs are not included.

# Verify phone SLAM priors and shared geometry

17 October 2026. User authorized proceeding after the first shared-coordinate
trial. Keep its image-only model/queries/control unchanged. This follow-up tests
whether existing recorded SLAM poses strengthen the shared static map. No new
Gaussian fit, cloud worker, GPU/model download or watchdog extension.

## Verified source convention

Pinned official 4DM reconstruction source, commit
`1c0d65cd3dc45062b98acd0a9a317bd61983214d`, SHA256
`3c718c0d7492d4ab96d23d58ae6b4de3cbbcd9c34e7be908966658a6268029db`:
[gen_viz_skeleton.py](https://github.com/fabiopoiesi/4dm/blob/1c0d65cd3dc45062b98acd0a9a317bd61983214d/reconstruction_sw/code/gen_viz_skeleton.py).
Lines256–265 convert metadata quaternion(x,y,z,w) to(-x,y,-z,w), camera centre
to(x,-y,z). R is camera-to-world; projection uses K[R^T|-R^T C]. Read source only;
do not execute its unrelated visualization/native-library setup. This is
estimated SLAM, not measured calibration or independent ground truth.

## Smallest trial and predeclared gates

Use existing Easy/Medium25 training RGB/mask/feature records per set, five phones,
with the same fifth-time samples reserved for later PnP and the same sixth phone
excluded. No new images or matching model. Reuse existing affine DSP-SIFT databases.

1. Compare verified cross-phone image correspondences with supplied pose geometry:
   Sampson distance, positive depth and triangulated reprojection, without fitting
   poses. Median Sampson distance<=5px and >=50% of correspondences satisfying
   positive-depth reprojection<=5px are required before pose-seeded triangulation.
   Compare image-only shared-map orientation/centres after one proper Sim(3)
   alignment; disagreement is not absolute pose error.
2. If a set passes, triangulate static feature tracks with supplied poses fixed,
   using<=2px final point filtering. Prove poses unchanged. Minimum50 cross-phone
   landmarks with each of at least three phones observing>=30 such landmarks.
   Importing25 supplied poses alone does not pass; require actual observed links.
3. If supported geometry passes, localize reserved later frames against that
   frozen map with the original >=30inlier/<=2px PnP gate. Separate all-reference
   matching and cross-phone-only matching. Query metadata positions/rotations
   must not initialize or select poses. Preserve failed phones/queries.
4. A single optional robust image-based bundle adjustment, initialized from
   accepted prior triangulation, may be compared if the fixed-pose map fails
   final2px support despite passing5px prior compatibility. Keep lens parameters
   fixed, at most 50 iterations/60s, no parameter sweep. Record pose changes and
   prohibit claims that optimization proves the priors correct. Stop rather than
   weaken gates if the prior compatibility test fails.

Inspect native match/reprojection overlays, numerical rotations/axes, geometry
coverage and common-viewer diagnostics where real supported geometry exists.
No dynamic training follows these camera tests. Keep an explicit common-camera
export identifying image-only versus supplied-pose provenance and unknown
metric accuracy. Independent floor/scale accuracy remains a separate question.

## Cost estimate and run limits

Existing local CPU environment only, four threads per native operation. Expected
2–10minutes, maximum30minutes native processing, 10minutes per stage; <=2GB new
scratch. No new paid resource, model weight or footage download. Official source
retrieval is ~20KB. Cloud Pod remains under its existing20:25:35 Sydney watchdog
cutoff, unchanged. Do not extend/relaunch it for this phase. Preserve originals,
old map hashes and private media; commit only scripts/lightweight reports.

Before query evaluation: use only landmarks actually observed by ≥2 phones,
so points triangulated solely within a supplied phone's trajectory cannot
masquerade as independently linked global geometry. Query only phones with
≥30 cross-phone landmarks in the frozen map. Run all-reference and other-phone-only
reference variants on that same subset. This is stricter than the earlier map's
localization, so report it separately rather than claiming a matched improvement.

## Bounded correction comparison, specified before execution

Fixed maps pass structural gates but later-frame localization remains weak.
Allow one Medium-only robust image-based BA comparison (same50iterations/60s
bound). Keep only the three phones with>=30observed cross-phone landmarks;
remove unsupported supplied camera frames before optimization. Keep K fixed,
Huber 1px loss, proper two-camera gauge. Refine existing geometry/poses only;
no new matching or threshold sweep. Freeze before querying; report changes from
the supplied poses. These query frames are now seen diagnostics, not an independent
method-selection test. Run the prior image-only map through the exact same
cross-phone-landmark query filter as a matched comparison. The sixth phone
remains excluded; no final unseen-view accuracy claim follows this comparison.
