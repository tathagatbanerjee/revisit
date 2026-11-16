> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/mosca-observation-registration/learned-bufferx/result.md`.
> Original SHA-256: `a94ce365cc1465bc5ffb8bb579ba77f267c06a22c7e1ca55a918debaa4346b7c`. Private media/logs are not included.

# Learned background registration result — 19 October 2026

**STOP: both known-transform controls fail. No real A/B registration or merge was attempted.** Actual pretrained BUFFER-X loaded and ran successfully on the frozen MoSca background subset. The failure is registration accuracy, not a missing model or classical fallback.

| Control | Rotation error | Scale error | Translation / target bounding diagonal | Decision |
| --- | --- | --- | --- | --- |
| Exact transformed copy |0.450deg |7.445% |5.613% |FAIL |
| Middle70% partial overlap |1.190deg |9.966% |7.844% |FAIL |
| Required limits |≤0.5deg |≤1% |≤1% |All required |

The exact copy has16564 source/target points; partial overlap has11594 source/16564 target points. Copy inference took6.83s. Input self-symmetry checks do not flag these real backgrounds as exactly symmetric. The uniform planar-grid wrapper negative rejects as required; this is not a general repeated-room ambiguity test. The copy's rotational sensitivity is0.00605, below the fixed.02 ambiguity threshold.

Both controls complete with the actual Desc/Pose checkpoints and validated KNN/SVD compatibility. No classical initializer fallback, changed seeds, new fitting, density cap, parameter sweep or reporting-label assistance occurred. Since the known controls fail, real B-to-A inference is NOT RUN; reserved room/person scores, full-scene transfer and A+B union remain NOT RUN. We cannot compare real alignment accuracy with the previous full-MoSca result.

## What this suggests

Cleaner background evidence is not enough for this learned3D registration recipe. Even an exact transformed copy of that background is not recovered within the fixed scale/translation limits. This is evidence against using its real alignment unchecked, not proof that the underlying videos cannot be aligned.

The actual adapter supplies only Gaussian **centres** to BUFFER-X, followed by geometry-only overlap refinement. It does not exploit wall-marker RGB appearance, Gaussian colour or rendered video context. Visually recognizable wall markings therefore do not automatically become distinctive input features. Removing the person may also remove distinctive3D structure; density and selection changes prevent isolating that explanation here.

Inspected control overlays can look broadly plausible while known scale is wrong by7–10%. They illustrate why a pleasing source-view overlay cannot certify spatial registration. The images are known-copy controls, not a real two-video merge.

## Integrity, resources and limitations

All215 prior frozen source files and both16564/11780 subsets are unchanged. The194 checked dependency source files match the pinned archive before the documented CUDA architecture patch. The first setup stopped because Git metadata was intentionally omitted; a recorded pre-inference correction verified file hashes and resumed native building. Model code, inputs and registration settings were unchanged.

One secure RTX A5000 atUS$.27/hour was terminated and independently verified absent after352.42s. Estimated computeUS$0.0264 before disk/tax, not an invoice. No persistent paid volume remains. Existing MoSca models, source videos and viewer4318 are unchanged; camera20 RGB remains sealed.

See frozen procedure (historical reference: `README.md`), control scores (historical reference: `docs/control-scores.json`), preflight (historical reference: `docs/preflight.json`), copy inference (historical reference: `docs/copy.json`), partial inference (historical reference: `docs/partial.json`), verification (historical reference: `docs/verification.json`), setup correction (historical reference: `docs/setup-correction.json`) and cleanup (historical reference: `docs/cleanup.json`).

Local inspected images: copy overlay (historical reference: `../../working/mosca-background-bufferx/copy-control-inspection.jpg`), partial overlay (historical reference: `../../working/mosca-background-bufferx/partial-control-inspection.jpg`). These files are ignored and not distributed with Git.

The user subsequently requested a separate fresh run starting from both original videos under anotherUS$2 allowance. That fresh reconstruction is a separate experiment, not a rerun or relaxation of these failed controls.
