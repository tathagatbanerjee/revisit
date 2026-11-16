> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/guildhall-comparison/investigation.md`.
> Original SHA-256: `004ba7f370a3b6308dc3744c3fa7a6e02887ce651d2c629b3996dfb63f0ccb6f`. Private media/logs are not included.

# Matched saved Guildhall comparison — 19 October 2026

The user wants to judge full MoSca on the same Guildhall clip as the H1 precise
mask hybrid they prefer. Results on other scenes do not establish a winner on
Guildhall. Reuse the completed MoSca checkpoint-evaluated snapshots and original
precise-mask Brush fit; no inference, training, reconstruction repair or merge.

The older aligned MoSca viewer shows77,522 of232,566 points (stride3). The old
H1 precise-mask hybrid has9,801 Brush points plus14,188 of28,376 dynamic points
(stride2). Build a separate Guildhall comparison group with:

1. Full MoSca, all232,566 static and dynamic points, transformed by the original
   fixed H1 similarity into the same world as the hybrid.
2. Exact H1 precise-mask hybrid, unchanged23,989 points and snapshots.
3. Same precise-mask Brush background plus ALL28,376 dynamic MoSca points,
   totaling38,177. This removes motion subsampling as a comparison confound.

Twenty saved native states use frame/12 seconds,0–35/12. Preserve every Gaussian
field under the fixed similarity: positions, complete rotation and scale;
opacity/DC color unchanged. Both appearance exports use DC only, matching the
available snapshot representation. All-points does not imply native higher-order
SH rendering, new geometry, temporal interpolation or better visual quality.
This remains the original H1 moving-only split, without silently introducing the
later complete-person semantic correction. Preserve the exact original hybrid.

Use identical full camera intrinsics and inspection poses from the existing H1
comparison, with identical0x141b16 clear color (the legacy viewer default), same
clock, first/middle/final state and nearby fixed-time orbit. The full original
MoSca checkpoint has204,190 static and28,376 dynamic points. Brush was fitted
from30 masked source views; MoSca from36 frames in the event. Their context is
therefore not identical training data; this is the actual saved-output comparison.
Native source is the public Guildhall recording, Acabashi/Wikimedia Commons,
CC BY-SA4.0, source58–61s for the moving event. Existing attribution and provenance
remain in pipeline/mosca-dynamic/result.md and the H1 resource records. No media
or reconstructed geometry is added to Git.

Verify all source hashes/counts, transform agreement with the old stride3 parent,
unchanged hybrid files, dynamic subsampling equality, fixed Brush prefix,
positive scales/finite fields/normalized quaternions and exact clocks. Inspect
actual browser images and first/last playback, frozen-time orbit/reset. Do not
claim an automatic quality winner or repeat cross-scene rankings as evidence.

Cost estimate and limits: local cached Python3.12 NumPy/SciPy and cached browser,
no installation/download or GPU fitting. Expected1–5minutes,600s export timeout,
under1GiB additional artifacts and under2GiB exporter RAM. Browser SwiftShader
is software rendering and not a performance benchmark. No paid worker/service,
credentials or fresh-evaluation imagery. The existing viewer remains running;
close only our temporary browser. Source models and prior run directories are
immutable; new publication refuses existing destinations. Save bounded failure
if the full-density browser cannot load, rather than subsampling silently.
