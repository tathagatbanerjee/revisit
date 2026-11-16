> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/05-fusion-refinement/result.md`.
> Original SHA-256: `ccae081d698f3610f381e6fb03ed5d762dc5f53c92ca0e7b406e73d6492701a1`. Private media/logs are not included.

# Result

One bounded six-parameter B colour correction changes reserved source-pixel MAE by -0.65% improvement; worst source-view regression 1.57%.

Status: **FAIL appearance gate**. See numerical record (historical reference: `docs/result.json`).

Appearance-only development diagnostic on the same seen two source views. B geometry and opacity remain fixed; A is byte-identical. This is not joint geometric fusion, fresh-view validation or a fix for failed dynamic geometry.

A separately scoped bounded geometry trial (historical reference: `geometry-investigation.md`) updates512 B Gaussian positions over30 Adam steps, with A, colour/opacity/scales/orientation fixed. It improves reserved MAE by0.362%, below the same2% gate: **FAIL local geometry gate**. Both views improve slightly; initial differentiable-renderer parity is below1.6e-9. Independent NumPy rendering with recomputed support/depth order scores the exported model. No result is promoted. See geometry record (historical reference: `docs/geometry-result.json`).
