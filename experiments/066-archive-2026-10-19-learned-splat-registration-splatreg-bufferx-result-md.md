> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/splatreg-bufferx/result.md`.
> Original SHA-256: `ec9ebe630c88064ff7b2b5c7c5b9e3471466f667164965325d717e2a80deefcc`. Private media/logs are not included.

# splatreg + BUFFER-X result

**Inference completed; real merge rejected.**

The exact-copy control passes: rotation 0.194104deg (gate0.5deg), relative scale error 0.1396% (gate1%), translation 0.0878% of A bounding-box diagonal (gate1%). No threshold changed after scoring.

Blind actual A18/B12 registration gives room 163.60px / 1.5804m-equivalent and person 54.89px / 0.4218m-equivalent. Both fail15px/.10m-equivalent gates. The transform remains constant across the40-state timeline. All source Gaussians, opacity and DC are retained; original A is byte-identical.

Inspected A-view/source-B-view/virtual-view comparisons retain actor duplication and room misalignment. BUFFER-X puts a larger side-facing B person beside A; GaussReg tilts B and badly misaligns wall features. The published raw unions are rejected diagnostics, not successful dynamic fusion.

Timed registration/model call 2.434s; whole inference process 5.537s; peak CUDA tensor allocation 4227.9MiB on A40. These exclude installation and are not full video reconstruction runtimes. GaussReg times model forward; BUFFER-X times seed plus overlap refinement, so these are different operations.

See numerical result (historical reference: `docs/result.json`), actual inference (historical reference: `docs/actual-inference.json`) and control inference (historical reference: `docs/control-inference.json`). Paid worker terminated and verified absent; both methods share one590.55s session.

Both105-key Desc/Pose checkpoints load with no missing or unexpected keys. Actual learned seed execution is verified; no classical fallback. Native pointnet2 and neighbor extensions built; KNN/SVD compatibility checks passed. This tests splatreg’s current whole-Gaussian-center wrapper, which does not reproduce the full upstream dataset preprocessing pipeline.
