> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/04-overlap-consolidation/investigation.md`.
> Original SHA-256: `4c5b1b3e034e8483da67f44f6b6fd335bc3d232654703615785d4e99f32b81e1`. Private media/logs are not included.

# Overlap consolidation — frozen procedure, 19 October 2026

First exact-fragment control, then independent static backgrounds aligned by02. Preserve A, discard B duplicates only with mutual nearest centres distance<=.05m-equivalent, colour distance<=.15, scale ratio .5–2. Compare A/B/rawunion/consolidated at frozen background source-image sample grids; record alpha coverage, RGB MAE and duplicate residuals. Gate exact control render agreement<1e-4 and real consolidation improves overlap MAE>=2% without source-view regression>2%. Geometry inconsistencies remain possible; no novelty inferred solely from Gaussian count.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
