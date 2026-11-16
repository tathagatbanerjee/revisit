> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/assembled-hybrid/investigation.md`.
> Original SHA-256: `0fbb62dc87018d6656de821583be501b6be877f5d7bac148ba25e969180a5487`. Private media/logs are not included.

# Put the strongest compatible pieces together

17 October 2026. User requested an end-to-end integration attempt rather than
more isolated coordinate optimization. Use one coherent existing recording:
Panoptic 171204_pose1_sample cameras 00/24, whose image-only 1080p camera recovery
passed the known-calibration check, and whose complete-person two-view MoSca
refinement is saved. The phone three-camera map does not include its saved motion
lead; combining it without a validated bridge would add an avoidable unknown.

## Authorized bounded experiment

1. Fit one fresh masked Brush background with the recovered image-only SfM
   cameras and observed sparse points. Ten selected training images, 640x360
   fitting resolution after1080p camera recovery. Flatten image/mask names so
   Brush v0.3.0 mask lookup is unambiguous; match the verified source layout.
   Existing COCO person masks, sparse1044-point seed, DC degree0,3000steps,
   growth stop1800, maximum200k splats, timeout10minutes. No seed from people.
2. Reuse the saved two-view-refined, complete-person MoSca layer with fixed
   identities (including people originally in its static component). Place it
   into the recovered SfM world with one camera-correspondence similarity bridge.
   This bridge uses existing supplied training-camera calibration from the saved
   motion fit. It is a calibrated asset-reuse bridge, not a purely image-only
   dynamic pipeline. Require <=5degrees camera orientation discrepancy and
   <=3%baseline centre mismatch after the bridge. No hidden scale claim.
3. Export matched baseline, assembled hybrid and one bounded2000-step shared
   two-camera refinement. Both training losses must have finite nonzero gradients
   on shared people geometry; preserve20state clocks and fixed person membership.
   Keep Gaussian rotations fixed, bounded position/scale/opacity/DC residuals
   with temporal regularization. Use the same recovered mean fixed-camera poses,
   resolution and black compositing for comparison. No new MoSca scaffold fit.
4. Freeze and hash before diagnostic views. Camera02 is already seen and may be
   used only as a labelled stress diagnostic. If feasible, select one unused
   nearby camera from calibration alone, then download/decode its RGB only after
   freezing for a fresh viewpoint check. No model updates follow evaluation.
5. Inspect actual native images first, then sequences in the local harness:
   matched source-view, second-view, nearby orbit, playback and final state.
   Record failure/coverage, not just fitting loss. Preserve older quality baseline.

## Cost and cutoff

Reuse existing compatible A40 Pod01t386g2a65qpr at verifiedUS$0.59/hour, existing
US$2 session allowance and unchanged 20:25:35 Sydney cutoff. At19:54, about31min
remain. The independent watchdog is live. No new Pod or extension. Native job
commands have individual timeouts; stop launching GPU work if <=8minutes remain
so export/retrieval can finish. Expected5–12minutes native work/transfer, maximum
remaining launch-relative session interval; retained compute already shares the
existing allowance. Local preparation/inspection use existing CPU dependencies.
No additional paid worker, model or checkpoint download. Heavy outputs ignored.

## Source behavior checked

Brush v0.3.0 [mask lookup](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/formats/mod.rs)
locates a masks sibling based on the image parent; use flat unique image names.
[Image loading](https://github.com/ArthurBrussee/brush/blob/v0.3.0/crates/brush-dataset/src/scene.rs)
copies mask intensity into alpha and interprets it as a training mask. Use
camera-centre pixel conversion explicitly when downsampling COLMAP camera data.
