> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/guildhall-full-video/result.md`.
> Original SHA-256: `965637d3f27c5184fa907436d44d4f91e71cd466c316064f6b0ae04bccb63b6d`. Private media/logs are not included.

# Full Guildhall result — 19 October 2026

The full-source experiment completed, but the long interior reconstruction is poor. The separate short statue outro is much sharper. The earlier short Guildhall results remain unchanged.

Watch the full30-second original/native comparison (historical reference: `../working/fresh-video-mosca-alignment/guildhall-full-source-native.mp4`). Original30fps footage is on the left; fresh native full-SH renders are on the right. The source/native/shift contact (historical reference: `../working/fresh-video-mosca-alignment/guildhall-native-inspection.jpg`) shows the interior failure clearly; the outro contact (historical reference: `../working/fresh-video-mosca-alignment/guildhall-outro-native-inspection.jpg`) shows the successful short static fit.

Interactive models are in [the local viewer](http://localhost:4318), experiment **Guildhall full video / fresh shot-aware MoSca**. Select the interior or separate outro, choose a recorded viewpoint, then orbit. Interior playback follows the original clip and becomes empty after its last supported state. The outro is a static model in its own coordinate frame. Viewer snapshots retain DC colour; the comparison movie uses native full-SH appearance.

## What ran from scratch

Original `data/clips/03-guildhall-interior.mp4`:30s,1920×1080,30fps,900 frames. Freshly decode the whole span at6fps into640×360 and append the actual final frame29.966667s:181 unique observations. This covers the full recording, with sampled reconstruction rather than900 reconstructed states.

Full source review found a dissolve into a second shot. The amendment (historical reference: `docs/shot-amendment.json`) was fixed before successful prior inference:

| Source interval | Observations | Processing |
| --- | ---: | --- |
| 0–25.333333s |153| Fresh Metric3D-small, RAFT, uniform/dynamic Bootstapir, MoSca cameras,1000 geometry/3000 photo steps |
| 25.5–26.833333s |9| Original edited dissolve only; no single physical camera/model fitted |
| 27–29.966667s |19| Fresh priors/cameras and native static-only3000-step MoSca fit |

No old Guildhall depth, tracks, camera estimates or scene checkpoints were reused. Pinned code/pretrained prior weights were reused. Shots remain spatially independent; no merge across the edit is claimed.

## Observed quality

| Model | Static / dynamic Gaussians | Native fitted-view PSNR min / median / max |
| --- | ---: | ---: |
| Long interior |189,587 /76,505|10.28 /15.66 /21.31dB|
| Short static outro |174,111 /0|33.78 /38.85 /40.68dB|

The interior start is smeared, the middle monument is recognizable but soft, and the end is badly blurred with poor recovery of the moving person. Nearby camera shifts retain the defects. The short outro reproduces the statue/architecture sharply and supports modest nearby movement, with boundary gaps. These observations come from native renders, before video encoding and before the common viewer adapter.

These are seen fitted-source views, not held-out geometry scores. More Gaussian points did not rescue the long fit. The fixed3000-step budget averages about19.6 frame draws per interior observation versus157.9 per outro observation; camera motion, tracking coverage and scene dynamics also differ. This trial does not isolate the cause or prove that more steps alone would fix it. Full interior track visibility averaged19.2% for dynamic tracks and41.1% for uniform tracks; preparation passed its finite/support gates, which do not certify long-range camera accuracy.

## Measured cost and resources

| Work | GPU-worker wall time | Estimated GPU cost |
| --- | ---: | ---: |
| Interior preparation, failed file-limit attempt, successful fit and export |18.33min|US$0.1803|
| Separate outro preparation, fit and export |4.98min|US$0.0489|
| **Guildhall measured processing total** |**23.31min**|**US$0.2292**|

This is Guildhall's measured processing inside the shared batch, not a standalone cold-start invoice. A/B processing costUS$0.1685, learned setup/controls/diagnostic including packaging failuresUS$0.0363, shared A40 setup/review/transfer/collection gapsUS$0.1587, and the unusable initial Ada workerUS$0.1194. **Whole fresh batch estimated GPU cost:US$0.7121**, within the combinedUS$2 allowance. Ephemeral disk, tax and billing granularity are excluded; actual invoice may differ. Full phase accounting (historical reference: `docs/costs.json`).

The successful interior fit took833.69s, with sampled peak process RSS6.35GiB and sampled GPU memory4,249MiB. Its first camera/FOV attempt exceeded a1,024 soft open-file limit before optimization. A65,536 limit was verified on the retry; source, seed and fitting parameters stayed unchanged. The12.18s failed attempt remains charged and retained. No longer/higher-quality fitting candidate was run.

The first RTX5000Ada could not create a CUDA context and was terminated before priors. Replacement secure A40 atUS$0.59/hour passed actual CUDA forward/backward/native-KNN tests; its original11:13 UTC deadline stayed unchanged. Both workers are terminated and independently verified absent, with no retained paid volume. All3,170 final files passed transfer hashes. The full comparison is exactly30s/900 encoded frames. Original clips and previous run assets remain protected; shared verification (historical reference: `../fresh-video-mosca-alignment/docs/verification.json`) and video audit (historical reference: `../fresh-video-mosca-alignment/docs/video-audit.json`) record checks.

See lessons (historical reference: `lessons.md`), next steps (historical reference: `next-steps.md`) and the shared A/B result (historical reference: `../fresh-video-mosca-alignment/result.md`).

Inspection and checks: five-run browser record (historical reference: `../fresh-video-mosca-alignment/docs/browser-check.json`), three-time virtual-camera record (historical reference: `../fresh-video-mosca-alignment/docs/virtual-browser-check.json`) and check summary (historical reference: `../fresh-video-mosca-alignment/docs/checks.json`). All five runs passed applicable count, timeline, recorded-view and orbit/reset checks; play/pause was exercised for the four sequences. There were no uncaught page exceptions or invalid manifests. Browser rendering used SwiftShader; no browser hardware performance claim. These checks preserve the reported quality failures.
