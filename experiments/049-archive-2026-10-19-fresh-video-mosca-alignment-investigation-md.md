> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/fresh-video-mosca-alignment/investigation.md`.
> Original SHA-256: `2ccfa3d7b119c5cd7b7c7c5e8519bf6f1b175188d0a56eda25f60d4e85274a72`. Private media/logs are not included.

# Fresh video reconstruction and learned alignment

This page consolidates the procedure already frozen in the original protocol (historical reference: `docs/initial-protocol.md`), initial plan (historical reference: `docs/plan.json`), shot amendment (historical reference: `docs/shot-amendment.json`) and registration plan (historical reference: `docs/registration-plan.json`). Those timestamped/hash records, rather than this later consolidation, establish the pre-execution decisions. Follow the workbook (historical reference: `../pipeline/workbook.md`).

Use the previously investigated native MoSca route (historical reference: `../pipeline/mosca-dynamic/investigation.md`), source archive SHA256 `85c39fe5d137beaa025b1a8920cc69969389913185d6e4d1d80a9ed89dade169`, Torch2.1.0/CUDA11.8, native_add3 renderer and SH order1. Resolve the source camera-file symlink and reuse the pinned pretrained Metric3D-small, RAFT and Bootstapir weights. Sequence depth/tracks/camera/geometry/photometric checkpoints are all fresh. Reusing pretrained models and pinned software is compatible with reconstructing a new scene from scratch.

A/B each use640×360 original-video samples at12Hz over their explicitly recorded intervals. Own intrinsics/distortion rectify each video; calibrated cross-camera extrinsics are excluded. The previous source decode and all previous artifacts stay immutable. Input original-frame IDs, actual PTS, hashes and original source terms are retained. Camera20 RGB stays sealed.

Generate depth, flow, uniform/dynamic tracks, review depth contacts and numeric validity, then independently estimate cameras, fit1000 scaffold geometry steps and3000 photometric steps. Record per-phase wall time and sampled process/GPU memory. The Guildhall addition has a separate investigation (historical reference: `../guildhall-full-video/investigation.md`); its two-shot amendment precedes all successful prior inference.

Export every fitted Gaussian, native full-SH source-camera RGB for every modeled state and three small shifted-view samples. Publish original A and transformed B independently and as an all-point raw union only if the learned backend returns a finite proper similarity. Preserve A bytes and B appearance/opacity; rotate covariance and scale lengths correctly. Source-valid event intervals prevent expired observations from persisting. Known studio PTS are not an unknown-upload clock solution.

Recreate conservative masks, apply the unchanged native observation-support selection to new static indices, and forbid old semantic membership arrays. Run actual pretrained splatreg/BUFFER-X with strict weight coverage and KNN/SVD preflight, seed12345 and default Sim3 settings. Preserve .5degree/1% scale/1% bbox-translation copy/partial gates and exact-grid negative. Numerical control failure rejects promotion but does not prevent the one explicitly scoped real-pair visual diagnostic. Software, weights, input selection or finite/proper-transform failure stops that diagnostic. No fitting-label access, seed sweep, corrective opacity, local person warp or joint refit.

Fitted-view PSNR is descriptive, not held-out geometry validation. Native full-SH appearance and DC snapshot appearance must remain distinct. Inspect independent time/viewpoint controls, raw alignment, temporal artifacts and unseen-side holes. No merge is promoted without independent spatial/person evidence; this batch does not supply complete B-person membership.

## Cost estimate and run limits — 19 October 2026

Before-run bounds were US$2 combined additional allowance and7200s from initial launch09:13 UTC, cutoff11:13 UTC, actual worker rate≤US$.59/hour, one active worker and independent watchdog. This bounds GPU compute to≤US$1.18, leaving allowance for ephemeral80GB disk and billing differences. Expected useful work spans tens of minutes, with setup/retrieval included; cold build time was uncertain. [Runpod pricing](https://www.runpod.io/pricing) was checked; actual API quotes determine this batch's rates. USD Linux CUDA GPU worker, secure/community availability recorded in receipts,48GiB A40 VRAM on replacement; no persistent volume or separate CPU worker.

The initial RTX5000Ada$.49/hour could enumerate but could not create a CUDA context. Its termination/absence and estimatedUS$.1194 overhead are retained. Replacement secure A40$.59/hour passed actual CUDA math/native KNN before setup; the original deadline and allowance remain unchanged. Only this compatible replacement is permitted, no budget extension. Stop phases early enough for retrieval; hash-check retained artifacts, terminate and independently verify absence. Models, media and checkpoints remain locally ignored; no new paid persistent storage. Measured costs (historical reference: `docs/costs.json`), when present, separate exclusive job phases from shared overhead and remain estimates before disk/tax, not invoices.

## Measured outcome

Execution is complete; see result (historical reference: `result.md`) and phase costs (historical reference: `docs/costs.json`). Guildhall processingUS$0.2292; whole fresh batchUS$0.7121 estimated GPU use before disk/tax. The long interior is visually poor; the short static outro is much better. Both workers are terminated and independently verified absent; no persistent paid volume remains.
