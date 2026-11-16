> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/whole-person-layer/investigation.md`.
> Original SHA-256: `16b1c535de8761a0f64954ec738bce61168482b3273c1bc6d1bcd9b7a3a45675`. Private media/logs are not included.

# Whole-person layer follow-up

17 October 2026. The user authorized proceeding with the complete-person fix
after reviewing the seven-scene results. Start with the existing single-person
and easy-phone checkpoints, without retraining or acquiring footage. This is
a semantic partition experiment, not multi-camera motion fusion.

Reuse the recorded batch environment (historical reference: `../environment.json`), including pinned
MoSca source `02404d2841b4e0dc2d9074860950bce5da579656`, native_add3 renderer,
PyTorch 2.1.0+cu118 and Brush v0.3.0 artifacts. Verify checkpoint hashes against
the original native export before loading; verify the existing masks and
background hashes in the partition report. No dependency upgrade is included.

## Implementation and evidence

The pinned native MoSca renderer accepts per-Gaussian precomputed colours and
supports their gradients. For fixed geometry and opacity, colour gradients
measure each Gaussian's alpha-composited contribution to selected pixels,
including visibility/occlusion. Accumulate person and non-person contributions
across source views, rather than selecting solely from the moving component
or projecting centers through occluders. No model parameter is optimized.

Use the saved COCO person masks, eroding their six-pixel padding. Reserve frames
whose native index modulo five is two from semantic assignment. These frames
evaluate the partition only: they were already used for reconstruction training,
so this is not independently held-out reconstruction accuracy.

Fix membership for the whole sequence: retain Gaussians with >=65% of visible
contribution inside person masks, >=1 accumulated pixel of visibility, and
person-majority evidence in at least two assignment frames. Apply to BOTH static
and moving components. Preserve geometry, opacity, motion and appearance.
An individual supporting frame must contribute more than 0.01 pixel of total
weight and more than half of that weight to person pixels; these constants are
fixed in the script, not adjusted per scene.
Background seen through gaps and imperfect masks can still contaminate labels;
unobserved body surfaces cannot be recovered by partitioning.

Reuse each scene's existing Brush lead-camera fallback in the identical MoSca
world. No alignment change or new fit. Render combined Gaussian tuples through
one depth-sorted rasterizer, not an always-on-top image overlay. Keep native
full-SH references, but use matched DC appearance and no subsampling for the new
control, motion-only baseline and semantic hybrid comparisons. Preserve old runs.

Inspect original first/final source images, isolated foreground, fixed-view
time changes and a small frozen-time camera shift. Measure silhouette coverage
and leakage against automatic masks, and source-image error within masks;
these diagnostics do not establish true 3D people recall. Check gradient
contribution totals against rendered alpha, model hashes, immutable background,
time endpoints, fixed membership and independent browser time/view controls.

## Cost estimate and execution bounds

Reuse Pod m420vthqzdx8h0 only, after checking actual status and watchdog. The
existing verified rate is US$0.59/hour, A40 Secure Cloud EU-SE-1. Expected work
is 10–30 minutes of selection, rendering and retrieval (~US$0.10–$0.30 compute,
already within the running session). No new worker, model download or fitting.
Retain the existing US$4 total allowance and **17 October 14:28:28 Sydney**
cutoff, without extending either. The watchdog remains independent of scripts.
Limit each scene command to 900 seconds. One implementation repair is allowed
for a software fault; retain failures and do not tune thresholds on evaluation
frames. Leave the compatible Pod available until its existing cutoff as the
user requested. Retrieve/hash-check compact selection arrays, reports and
renders; use locally retained native PLYs to produce harness artifacts. Heavy
artifacts remain ignored, private research material.

## Deliverable and boundary

Two bounded comparisons with inspectable harness outputs and a written outcome,
including a failure if the semantic split cannot preserve whole people. Do not
call this complete multi-phone reconstruction. Joint use of simultaneous camera
observations remains a subsequent integration stage.
