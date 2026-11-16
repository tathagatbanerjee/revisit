> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/guildhall-full-video/investigation.md`.
> Original SHA-256: `13102668772dc25e1ea73862cb2e84d14611a4266f08677cb85902b5634dc605`. Private media/logs are not included.

# Full Guildhall procedure and cost basis

The initial before-run record is the frozen protocol (historical reference: `docs/initial-protocol.md`), its shared plan (historical reference: `../fresh-video-mosca-alignment/docs/plan.json`) and pre-inference shot amendment (historical reference: `docs/shot-amendment.json`). This document consolidates them during execution. Use the existing native MoSca investigation (historical reference: `../pipeline/mosca-dynamic/investigation.md`) and workbook (historical reference: `../pipeline/workbook.md`); pinned source/environment and strict scene-cache exclusion are detailed in the shared investigation (historical reference: `../fresh-video-mosca-alignment/investigation.md`).

The original900-frame1920×1080/30fps file is30s long. Freshly decode the full span into181 unique640×360 observations at6fps plus the real final frame29.966667s. This samples the entire recording; it does not reconstruct all900 frames or interpolate unobserved motion. Preserve original PTS and source hashes.

Full source inspection identified a dissolve into a second statue shot. Before any successful prior inference, split153 interior observations0–25.333333s from19 outro observations27–29.966667s. Preserve9 sampled dissolve frames25.5–26.833333s as source-only. Separate shot coordinate systems; no spatial alignment across this edit is inferred.

Recompute Metric3D-small depth, RAFT flow and uniform/dynamic Bootstapir tracks for the interior. Fit fresh MoSca cameras,1000 scaffold geometry steps and3000 photometric steps. The mostly static-subject outro uses fresh depth/flow/uniform tracks, camera fitting and the native static-only3000-step photometric warm path. It does not invent a dynamic scaffold or require moving tracks. Review all priors before fitting; failed preparation/input/software phases remain failures rather than a reason to lower quality gates.

Export native full-SH renders at every modeled source pose and small shifted views. Compare the original full30fps video beside the6fps fitted samples over all30s; label the dissolve source-only. Interactive interior snapshots use the original source clock and become empty after the last supported state. Publish the outro as a separate static model with its own viewpoints. Preserve every fitted point, all old models and source clips. Native fitted-view PSNR is not held-out performance or verified human/unseen-side geometry.

The long shot receives the same3000-step budget as the previous short baseline. Average frame exposures are therefore lower; the trial measures this fixed baseline rather than equal training effort per frame. No automatic parameter sweep or longer run follows its result.

## Cost estimate and run limits — 19 October 2026

Share one bounded fresh GPU batch with A/B under the additionalUS$2 allowance; no separate allocation. Original cutoff11:13 UTC,7200s after initial09:13 launch, remains in force after replacing an unusable GPU. Initial Ada$.49/hour is terminated; replacement secure A40$.59/hour uses the same Torch2.1/CUDA11.8 environment. Rate basis: [provider pricing](https://www.runpod.io/pricing), checked during preparation, and retained actual API quotes. Linux CUDA,48GiB A40 VRAM,80GB ephemeral disk, no paid persistent volume or separate CPU worker.

The initial maximum GPU estimate was7200×$.59/3600=US$1.18, with space inside theUS$2 allowance for disk/billing differences. Setup, transfer, review and failed-worker time count toward the shared batch, not just optimization time. Expected useful work is tens of minutes; actual long-sequence fit time is measured rather than promised. Retrieve/hash-check all artifacts, terminate before the fixed cutoff and verify absence. Measured costs (historical reference: `docs/costs.json`), when present, report Guildhall preparation/fit/export separately from A/B, alignment, setup and initial failure. These are GPU-use estimates before ephemeral disk/tax and are not an invoice.

## Measured outcome

Execution is complete; see result (historical reference: `result.md`) and phase costs (historical reference: `docs/costs.json`). Guildhall processingUS$0.2292; whole fresh batchUS$0.7121 estimated GPU use before disk/tax. The long interior is visually poor; the short static outro is much better. Both workers are terminated and independently verified absent; no persistent paid volume remains.
