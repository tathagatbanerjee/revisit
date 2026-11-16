> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/03-persistence-and-change/investigation.md`.
> Original SHA-256: `ae2bbecfebfbbc29b23ffcf9dc3228ca8b657934d616bd1429c06cc34c99bb1f`. Private media/logs are not included.

# Persistence and change — frozen procedure, 19 October 2026

Construct a documented changed copy of selected saved A Gaussians with stable room, moved and removed patches, added patch, and an occluded patch. Position/colour matching and explicit visibility queries must distinguish absence from occlusion; retain uncertain conflicts. Score known labels, gate macro precision/recall>=.95 and zero false removal of occluded patch. This is injected change ground truth, not a real recapture. Audit available actual inputs; report missing real changed-scene validation.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
