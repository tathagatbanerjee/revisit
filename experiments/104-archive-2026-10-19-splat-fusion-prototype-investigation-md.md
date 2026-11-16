> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-prototype/investigation.md`.
> Original SHA-256: `2231b201788b960ce67f2589dd710ed9076acf61229be1b879b12be1f9b0c717`. Private media/logs are not included.

# Integrated cached-upload prototype — 19 October 2026

User approves a small end-to-end integration using saved independent reconstructions.
Run one command with two upload descriptors. Ingest A then B using immutable full
MoSca native exports/checkpoint receipts as cache hits; no fresh video training or
web upload service. Existing source images00/24 only. Camera20 RGB stays sealed.

## Frozen sequence and decisions

1. Hash and ingest both cached reconstructions separately with source-local PTS.
2. Recover B-to-A event offset using motion-distance quantiles (2048 sampled
   dynamic point pairs, five quantiles, index shifts[-12,12], >=18 overlap), then
   actual local PTS median conversion. Require best/second margin>=5%. No known
   event start enters estimation; known source event clock is scored afterward.
3. Full7parameter room registration from saved calibration-assisted34 identities,
  28fit/6reserved, RANSAC1024/.15m-equivalent, robust loss .05m-equivalent/200eval.
   This is seen studio data, not blind phone registration. Room gate<=15px/.10m.
4. Separately check20 seen person observations excluded from room fitting, with
   median<=15px/.10m and successful room/timing gates required for acceptance.
   These observations were used in an earlier separate development diagnostic;
   not independent evaluation. Failed merges remain candidates, A/B primary.
5. Full-point raw merge then background-only consolidation using conservative
   existing masks, mutual nearest centres<=.05m-equivalent, colour<=.15, scale
   ratio .5–2. Preserve every dynamic Gaussian and all A points. No point removal
   outside the overlap: B-only tail restores original B; boundary pops possible.
6. One local XYZ refinement on full mid-clip compositing context. Up to512 retained
   background B Gaussians within .15m-equivalent of A background, selected by
   fitting-pixel contribution. A fixed, B colour/opacity/covariance unchanged.
  30 Adam steps/.05lr, tanh bounds .01 A-native per axis, .01 displacement penalty.
   Use the previously checked differentiable ray renderer and independent NumPy
   export scoring; initial parity<=2e-5. Colour correction is omitted because its
   separate trial regressed. Preserve raw/consolidated/refined candidates, not a
   best-checkpoint selection. Appearance gain>=2%, view regression<=2% for success.
7. Publish A,B,raw,consolidated,refined on identical observed40-state clocks, matching
   A/registered-B source camera views, black/DC. Edits apply only in overlap;
   original sources alone before/after. Record decision and stage journal before
   promotion. Current actor failure must keep accepted outputs as separate A/B.

## Validation

Verify all source hashes and every exported state: activity, exact A prefix,
full dynamic point count, documented B static deletions/position-only updates,
opacity/DC unchanged, finite covariances, shared clocks/cameras. Compare actual
viewer frames at matching time/views; counts at endpoints, playback/pause,
orbit/reset and camera changes preserving time/model. Artifact success is not
quality success. Preserve prior eight-stage suite and every existing viewer run.

## Costs and bounds

Local Python3.12 CPU environment already cached (numpy/scipy/PIL/OpenCV/torch),
no installs/downloads/GPU/cloud. Processing target<180s, bound600s, optimizer
<=100s and target<2GiB peak RAM; disk under2GiB models with current free-space
check. Viewer inspection is separate software rendering, not GPU performance.
No paid resource, cleanup means stop only isolated inspection browser and retain
ignored working/results; leave existing localhost4318 viewer and unrelated apps.
