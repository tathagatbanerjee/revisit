> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-guided-mosca-registration/result.md`.
> Original SHA-256: `6d3e4c18fef26f91f6c6e38024e00e409e7820b44988b259d70af09ba38d2865`. Private media/logs are not included.

# Execution result — 19 October 2026

**Stopped at stage03: both independent Brush fits completed, but neither background proxy passed its quality gate.** No BUFFER-X registration or MoSca merge was attempted.

| Stage | Outcome |
| --- | --- |
|01 Transform controls | PASS: nonidentity bridges, covariance, inverse and projection controls |
|02 Inputs and bridges | PASS: conservative background inputs and explicit coordinate bridges |
|03 Independent Brush fits | FAIL proxy usability; both native fits completed |
|04–08 Registration, transfer, ablation and integration | NOT RUN: stage03 prerequisite failed |

Both fits used the frozen independent inputs, fixed native cameras,3000 steps and seed12345. A completed in24.05s with805 Gaussians; B in20.54s with1685. On the three frames excluded from Brush fitting per video:

| Proxy | Background PSNR loss | Alpha-supported coverage | Frozen gate |
| --- | --- | --- | --- |
| A |8.44–10.78dB |77.6–89.8% |Loss≤1dB; coverage loss≤2 percentage points |
| B |6.34–10.14dB |67.2–90.8% |Same |

The MoSca controls have100% supported coverage on these fixed background masks. Native Brush RGB visibly loses wall features and interior detail. Scoring uses fixed background masks and baseline support, never a smaller candidate-specific mask. These are source-scene diagnostics, not independent novel-view geometry validation.

Coordinate composition controls pass, and the audited Brush importer/exporter retains the constructed world coordinates. That establishes the engineering path; it does not establish useful cross-video alignment. **The central hypothesis—Brush alignment transferred to full MoSca—remains untested.**

A read-only seed audit shows the conservative all-frame footprint and opacity filters retained only651/47139 A static points and1363/45416 B static points. This is a plausible contributor to poor proxies, not an isolated causal finding. Broad manual background exclusions are not precise person segmentation; complete-person B membership remains unavailable.

All74 original full MoSca model/report files and74 source inputs are hash-identical. The input split and146 native dataset files verify. Existing viewer4318 is unchanged; camera20 RGB remains sealed. Failed outputs and logs are retained under ignored working storage.

The RTX5000Ada worker was terminated and independently verified absent. Launch-to-termination771.95s; estimated computeUS$0.1051 before disk/tax, not an invoice. No persistent paid storage remains. No extra fitting or parameter sweep followed the failure.

Evidence: stage03 measurements (historical reference: `03-independent-brush-fits/docs/result.json`), seed-retention diagnostic (historical reference: `03-independent-brush-fits/docs/seed-retention-diagnostic.json`), artifact verification (historical reference: `docs/verification.json`), retrieval (historical reference: `docs/retrieval-check.json`), cleanup (historical reference: `docs/cleanup.json`).

Local inspected comparisons: A (historical reference: `../working/brush-guided-mosca-registration/a-native-comparison.jpg`), B (historical reference: `../working/brush-guided-mosca-registration/b-native-comparison.jpg`). Columns show source RGB, unchanged MoSca reference and rejected native Brush proxy. Images are ignored and not distributed with Git.

## Controlled follow-up

The denser seed-policy comparison (historical reference: `proxy-seed-retention/result.md`) completed
subsequently. Every view improves over these initial Brush fits, but both proxies
still fail the same gates. This original result remains the preserved baseline.
