> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/decision.md`.
> Original SHA-256: `b444645eda5742250542d67d6286c5c96bf38c73a1a87848b2f2f47cbb8e75a2`. Private media/logs are not included.

# Selected baseline and development path

Locked in with the user on 17 October 2026, after the seven-scene batch and
the complete-person partition follow-up.

- **Quality baseline:** full MoSca reconstruction, with both static and moving
  components. The easy-phone all-points control is the strongest current overall
  output. Keep it in future comparisons; do not replace it merely because a
  hybrid is the selected development direction.
- **Development path:** Brush environment plus the corrected MoSca people layer,
  selected from both static and moving components with fixed membership through
  time. The indoor single-person example is the strongest current hybrid.
- **Acceptance:** improve useful appearance and frozen-time navigation while
  retaining complete observed people and independent time/view controls. Compare
  the same cameras, event times and display settings. Record regressions and
  retain prior outputs. A failed improvement stays an experimental comparison.
- **Outstanding:** background streaks, silhouette halos, geometry/occlusion holes
  and jointly fitted simultaneous multi-camera motion. None is solved merely
  by locking in this direction. Do not present arbitrary unseen views as faithful
  observations.

Evidence: original batch (historical reference: `result.md`),
complete-person trial (historical reference: `whole-person-layer/result.md`).
The next isolated trial is background seed filtering (historical reference: `background-seeds/investigation.md`).

That trial has now completed (historical reference: `background-seeds/result.md`), including one
separate 12k optimization comparison. The new outdoor 12k hybrid is a useful
fitted-view candidate; it does not replace the overall MoSca baseline or prove
better novel-view geometry. The corrected indoor hybrid remains the reference
hybrid; retain all older outputs when assessing subsequent changes.

The first calibrated two-camera refinement (historical reference: `calibrated-multiview/result.md`)
now consumes two real synchronized videos in one shared optimization. It
improves the second fitted view but fails elevated held-out person appearance.
It remains an experimental integration case; it does not replace the locked
quality baseline or establish a jointly trained multi-camera MoSca scaffold.
Renderer checks expose compositing differences in earlier native comparisons;
keep those conventions explicit when reassessing appearance.

The assembled integration (historical reference: `assembled-hybrid/result.md`) now fits a fresh Brush
background with recovered indoor SfM poses, reuses the complete observed-person
MoSca layer through a labelled training-calibration bridge and refines against
both videos. It improves room/fitted-view context but worsens fresh-view person
appearance. Keep it as an integrated candidate; the overall quality baseline
is unchanged. No faithful unseen-body recovery is established.
