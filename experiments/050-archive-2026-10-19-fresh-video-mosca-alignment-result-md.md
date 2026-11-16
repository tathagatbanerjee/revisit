> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/fresh-video-mosca-alignment/result.md`.
> Original SHA-256: `6b82220a37beef3a619c980da415bb267c9fe40a070714d8eff6e7037ae75bf1`. Private media/logs are not included.

# Fresh original-video batch — 19 October 2026

Fresh independent A/B reconstructions and the entire Guildhall source test completed. The short A/B rooms reconstruct well with softer/ghosted moving people. The long Guildhall interior fails visual quality; its separate short outro looks much better. Learned A/B registration still fails its known-transform controls and remains a rejected raw-union diagnostic.

Inspect [the local viewer](http://localhost:4318), groups **Fresh original videos / full MoSca + alignment** and **Guildhall full video / fresh shot-aware MoSca**. Original A, transformed B and their raw union share the recorded source-valid event clock; expired sources contribute no points. The Guildhall shots have separate spatial frames. Native full-SH appearance references: A video (historical reference: `../working/fresh-video-mosca-alignment/a-source-native.mp4`), B video (historical reference: `../working/fresh-video-mosca-alignment/b-source-native.mp4`), full30-second Guildhall comparison (historical reference: `../working/fresh-video-mosca-alignment/guildhall-full-source-native.mp4`). Viewer snapshots use DC colour for matched independent/union comparison.

## Fresh work and reconstruction results

A36/B34 original-video observations were newly decoded and rectified using each camera's own intrinsics/distortion. No cross-camera extrinsics, old depth/tracks/camera checkpoints, fitted models or previous transforms entered the fresh reconstruction/matching. Pixel differences from previous exports were audited, not substituted as input. All four prior sets passed numerical checks and start/middle/end depth review before fitting. Source/pinned pretrained-model hashes and actual environment are retained.

| Case | Observations | Static / dynamic points | Fit wall time | Median native fitted-view PSNR |
| --- | ---: | ---: | ---: | ---: |
| A |36|47,078 /18,291|434.87s|33.88dB|
| B |34|45,146 /17,343|444.77s|34.44dB|
| Guildhall interior |153|189,587 /76,505|833.69s|15.66dB|
| Guildhall separate static outro |19|174,111 /0|255.92s|38.85dB|

Native source/shift contacts were inspected for all four. A/B room structure is clear, but hands, faces and shifted-view person silhouettes remain soft or ghosted. Source-view PSNR is room dominated and does not validate person shape. The long Guildhall shot has strong smearing at the start/end even in native renders; its middle is recognizable. See full Guildhall result (historical reference: `../guildhall-full-video/result.md`) for its6fps full-span sampling, pre-inference shot split, source-only dissolve and per-frame fidelity evidence.

## Actual learned registration on fresh outputs

The unchanged observation policy retained16,481 A/11,489 B fresh static Gaussians, with at least three clear source-supported observations spanning12 frames. Fresh indices were used; old semantic membership arrays were forbidden. Neither fresh set has complete certified person membership.

Actual pinned BUFFER-X weights loaded with full parameter coverage; KNN/SVD numerical preflight and original source-content checks passed. No classical fallback, old alignment, calibrated extrinsic bridge or reporting-label fit was used. One seed/default Sim3 configuration, no sweep.

| Control | Rotation error | Relative scale error | Translation / target bbox | Decision |
| --- | ---: | ---: | ---: | --- |
| Transformed copy |0.4268°|7.9327%|6.2576%|FAIL|
| Middle70% partial |1.1327°|10.3022%|8.2858%|FAIL|
| Limits |≤0.5°|≤1%|≤1%|Unchanged|

The exact repeated-grid wrapper negative rejects as planned; it is not a general ambiguity certificate. Unlike the prior gated trial, this frozen visual protocol permits one real-pair estimate despite numerical control failure. That real inference completed in4.68s with scale0.942594. Its rotation sensitivity0.01489 is below the0.02 ambiguity flag. The returned transform was frozen before reporting-label access; no old3D labels were used as fresh truth, and no room/person accuracy scores or promotion are claimed.

Browser captures show a doubled person with a large vertical offset and misaligned/duplicated room details in the raw union: A viewpoint (historical reference: `../working/fresh-video-mosca-alignment/browser/fresh-video-union-1.5015-a.png`), B viewpoint (historical reference: `../working/fresh-video-mosca-alignment/browser/fresh-video-union-1.5015-b.png`).

Every native A point and attribute is retained exactly. Every B point transfers by the same similarity, including rotations/scales, with original opacity/DC colour. The union does no deduplication, body warp, joint refinement or opacity correction. Failed controls remain visible in the result; inference completion does not establish alignment quality. Measured registration evidence (historical reference: `docs/results.json`), publication (historical reference: `docs/publication.json`), artifact verification (historical reference: `docs/verification.json`).

## Cost and closure

Whole fresh batch estimated GPU cost **US$0.7121**, including the unusable first worker and all setup/review/transfer time, versus the combinedUS$2 allowance. A/B processingUS$0.1685; Guildhall processingUS$0.2292; learned setup/diagnostic including packaging failuresUS$0.0363; shared replacement overheadUS$0.1587; failed AdaUS$0.1194. These are GPU-use estimates before ephemeral disk/tax/billing granularity, not invoices. Full accounting (historical reference: `docs/costs.json`).

Initial Ada failed actual CUDA context creation; replacement A40 passed real math/native-KNN checks. The long-shot file-descriptor repair occurred before optimization with identical fit parameters. Registration required pip24.3.1/setuptools77.0.3/packaging24.2 after all model exports, before any learned preflight/inference. Failures and pre-repair evidence remain retained. Source/model code, learned weights, thresholds and seed stayed fixed except declared source compatibility/build patches; see file-limit (historical reference: `docs/open-files-amendment.json`) and packaging (historical reference: `docs/packaging-amendment.json`) amendments.

Both Pods are terminated and independently verified absent. The A40's allocated lifetime was3,616.32s; initial failed Ada877.12s. Original cutoff was not extended; no paid persistent volume remains. Core archive and final changed-file bundle reconstruct3,170 individually hash-verified files; transfer receipts (historical reference: `docs/retrieval.json`). Old assets/source validity and Gaussian/timeline contracts are checked separately. Source originals, camera20 RGB sealing and the existing viewer remain protected.

Inspection and checks: five-run browser record (historical reference: `docs/browser-check.json`), three-time virtual-camera record (historical reference: `docs/virtual-browser-check.json`) and check summary (historical reference: `docs/checks.json`). All five runs passed applicable count, timeline, recorded-view and orbit/reset checks; play/pause was exercised for the four sequences. There were no uncaught page exceptions or invalid manifests. Browser rendering used SwiftShader; no browser hardware performance claim. These checks preserve the reported quality failures.
