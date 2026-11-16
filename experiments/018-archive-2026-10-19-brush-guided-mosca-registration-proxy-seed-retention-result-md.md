> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-guided-mosca-registration/proxy-seed-retention/result.md`.
> Original SHA-256: `d1e30c3be37febd58cb8097c7985da090adbcf12c697ad511db7f60a3497da09`. Private media/logs are not included.

# Controlled seed-retention result

**FAIL proxy gates**. Both fixed fits completed; no registration or MoSca transfer ran.

The revised policy improves PSNR by1.32–3.17dB and coverage by7.9–19.6percentage points over the first Brush fits. Native comparisons show more wall detail, especially B, but extensive blur remains. This is a useful improvement, not a usable registration proxy yet.

Only the seed inclusion policy changed:651→5281 A seeds and1363→7887 B seeds. Cameras, source/mask bytes, excluded frames, Brush binary/GPU type and fitting settings are unchanged. The policy jointly changes footprint aggregation and the native opacity cutoff; their individual effects are not isolated.

| View | Baseline → candidate PSNR (dB) | Candidate loss vs MoSca (dB) | Baseline → candidate coverage | Frozen gate |
| --- | --- | --- | --- | --- |
| A06 | 28.42 → 30.69 | -8.14 | 77.6% → 94.8% | FAIL |
| A18 | 29.16 → 31.53 | -8.41 | 78.8% → 97.3% | FAIL |
| A30 | 30.32 → 32.23 | -6.54 | 89.8% → 99.9% | FAIL |
| B00 | 29.20 → 30.52 | -8.70 | 71.4% → 88.6% | FAIL |
| B12 | 30.30 → 32.03 | -8.41 | 67.2% → 86.8% | FAIL |
| B24 | 33.04 → 36.21 | -3.16 | 90.8% → 98.8% | FAIL |

Every view must lose≤1dB versus MoSca and≤2percentage points of supported coverage. Coverage uses the original frozen background mask; PSNR uses baseline-only support, with unchanged pixel counts. Native Brush RGB and shared-reference alpha are scored exactly as in the first trial. Seen source-scene diagnostics do not establish correct depth or novel-view quality.

All74 original full MoSca files and74 source inputs are unchanged. The paid worker is terminated and verified absent; estimated computeUS$0.0316 before disk/tax, not an invoice. No persistent paid storage remains. The first failed trial and existing viewer4318 are preserved; camera20 RGB remains sealed.

Evidence: comparison (historical reference: `docs/comparison.json`), quality (historical reference: `docs/quality.json`), input verification (historical reference: `docs/verification.json`), export and local rescoring checks (historical reference: `docs/output-verification.json`), visual inspection (historical reference: `docs/visual-inspection.json`), cleanup (historical reference: `docs/cleanup.json`). Local comparisons: A (historical reference: `../../working/brush-proxy-seed-retention/a-comparison.jpg`), B (historical reference: `../../working/brush-proxy-seed-retention/b-comparison.jpg`). Each row shows source, unchanged MoSca, baseline Brush and denser Brush candidate.
