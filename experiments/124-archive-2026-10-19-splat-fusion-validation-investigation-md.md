> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/investigation.md`.
> Original SHA-256: `6ce550241dc8ed78b148107ed036c1264eaade44527c47891e90fca381679fe8`. Private media/logs are not included.

# Sequential validation suite — 19 October 2026

The user requests all eight proposed validation stages in a new suite. Each numbered folder freezes its procedure before execution; execute01→08, preserve failures and continue independent controls. Existing independent Panoptic00/24 full MoSca exports and their known limitations are development inputs. No fresh evaluation camera is opened. Exact-fragment and injected-change controls establish mechanics only. Missing actual recaptures/third independent video are reported as unmet validation, never passed by proxies. Local CPU only, no paid worker or downloads, eight bounded trials each<=600s and target<2GiB. Use immutable inputs, frozen numerical gates and actual output inspection.

Prior implementation research: `../independent-mosca-fusion/geometry.py`, `../independent-mosca-fusion/registration/{sparse,solve}.py` and `../incremental-scene-fusion/raster.py`. Geometry transforms preserve log scale and quaternion covariance; sparse projection matches native covariance/occlusion and half-pixel conventions. Preserve existing shape inconsistency; do not claim colour-only correction fixes geometry.
