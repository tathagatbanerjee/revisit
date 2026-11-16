> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/06-time-alignment/investigation.md`.
> Original SHA-256: `65198ca310d1f4261cf6de53ef10f75fc5ae3b3fc141f047e3a7313051bf090c`. Private media/logs are not included.

# Time alignment — frozen procedure, 19 October 2026

Derive camera-invariant pairwise-distance motion signatures from all native dynamic states, robustly centred/scaled per pair. Add known offset+.75075s to B local clock; search integer shifts[-12,12] grids with>=18overlap and compare dynamic shape-change signatures. Recover offset within one frame and best-vs-second cost margin>=5%; compare before/after sources and exact PTS. Also exact same-source cropped motion control. No interpolation beyond support, no source-end padding. Real different-view motion ambiguity may fail.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
