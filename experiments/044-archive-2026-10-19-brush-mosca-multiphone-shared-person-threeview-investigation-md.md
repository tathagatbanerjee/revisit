> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/threeview-investigation.md`.
> Original SHA-256: `dcf2ab9dcaa93af375bd509abc968f58caa061bcaf4e47e1d56433c934fc71d3`. Private media/logs are not included.

# Seen three-view acceptance check — 19 October 2026

This continues the cached MASt3R experiment, not a new initializer or Gaussian
fit. Source/model/license/environment pins remain those in mast3r-investigation.md.
The current model runs; its confidence cutoff discards most body support.
Two-view geometry, mask projection and color similarity cannot establish that
those discarded correspondences refer to the same observed surface.

## Fixed procedure before execution

Use synchronized state 000 only, native rectified1920x1080 RGB and author-world
calibration in meters. Reuse the saved21/13 raw correspondences. Run exactly two
new descriptor pairs:21/24 for upper-body visibility and13/02 for feet. These
are already-seen training cameras. No20 RGB, additional video or checkpoint.
Keep upstream512px person crops,32px640-equivalent margin, reciprocal stride2,
dot similarity>=0.8,3network-pixel border and existing conservative masks. Keep
finite descriptor confidence but impose no new confidence cutoff. Report the
frozen>=1.5 cohort separately from its complement; do not sweep thresholds.

Join tracks through the shared image (21 or13), using mutual nearest coordinates
within 0.75px at640-equivalent resolution. Require nearest/second-nearest distance
ratio<=0.7 in both directions; repeated exact shared pixels are ambiguous and
rejected. This is spatial association of descriptor matches, not an independent
anatomical annotation. Both pairs must independently pass the previous calibrated
geometry gates (1.5px640 epipolar/reprojection,1–6m depth,>=2degree ray angle,
world radius<10m). Additionally require the old21/13 point to project within1.5px
of the **observed** third-view match, positive third depth1–6m, and triangulated
pair positions to agree within 3cm. No tolerance changes after seeing results.

Before inference, inspect source crops and record approximate visible features:
head/hair, both hands, and each shoe. Use existing head/hand boxes and separate
left/right image-side boxes as diagnostic regions, not anatomical ground truth.
Camera24 crops both feet;02 hides the far hand. Do not count those invisible
regions against their respective validation pair. The21/13/24 trio should support
head and each hand;21/13/02 should support each shoe. A readiness signal requires
at least20 distinct5mm bins per jointly visible region, with visual inspection
of all accepted regional tracks. Sparse regional counts cannot prove complete
surface coverage. Camera 20 remains required for a future frozen-candidate test.

The coarse region/feature selections and actual input hashes are saved before
launch in threeview-plan.json. Source crops are retained privately in working/.
No point cloud initializer is exported from this diagnostic. Even passing this
check still requires joint initialization from all selected training views,
surface inspection, and a new fitter with observed-surface growth.

## Cost estimate and run limits

Local isolated Python3.12 CPU environment, cached weights/source, no downloads or
installations. Two sequential forwards/matching operations, expected6–8minutes,
900second total child deadline, two Torch/BLAS threads,5GiB RSS limit, at least
5.5GiB available RAM before launch. Child process group only is stopped on limit;
no unrelated jobs are changed. Expected and maximum paid compute US$0; existing
local electricity/storage unpriced. Maximum additional scratch1GiB, retained in
ignored working/shared-person/mast3r/threeview. One attempt, no model/parameter
fallback. Parent watchdog is independent of worker progress. Save raw matches,
input/output hashes, crop tensor parity, measured time/RSS, cohort/region counts,
reprojection/depth agreement and visual panels. Preserve the old293-bin output.
