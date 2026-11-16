> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/gaussreg/result.md`.
> Original SHA-256: `ddf3e9dd2ae02e25b4712ebde111ffe9e13d15b21d4480c959933742b19f60af`. Private media/logs are not included.

# GaussReg coarse result

**Inference completed; real merge rejected.**

The exact-copy control fails the fixed rotation gate: rotation 0.551654deg (gate0.5deg), relative scale error 0.2474% (gate1%), translation 0.3204% of A bounding-box diagonal (gate1%). No threshold changed after scoring.

Blind actual A18/B12 registration gives room 308.52px / 2.1159m-equivalent and person 72.62px / 0.4765m-equivalent. Both fail15px/.10m-equivalent gates. The transform remains constant across the40-state timeline. All source Gaussians, opacity and DC are retained; original A is byte-identical.

Inspected A-view/source-B-view/virtual-view comparisons retain actor duplication and room misalignment. BUFFER-X puts a larger side-facing B person beside A; GaussReg tilts B and badly misaligns wall features. The published raw unions are rejected diagnostics, not successful dynamic fusion.

Timed registration/model call 1.439s; whole inference process 4.804s; peak CUDA tensor allocation 484.4MiB on A40. These exclude installation and are not full video reconstruction runtimes. GaussReg times model forward; BUFFER-X times seed plus overlap refinement, so these are different operations.

See numerical result (historical reference: `docs/result.json`), actual inference (historical reference: `docs/actual-inference.json`) and control inference (historical reference: `docs/control-inference.json`). Paid worker terminated and verified absent; both methods share one590.55s session.

Official checkpoint retrieval succeeded through public OneDrive Download after initial direct401 failures. First inference launch failed on missing ipdb before any model forward; error logs and receipts are preserved. Strict checkpoint loading then succeeded. This is the released coarse path; separate image-guided fine registration was not run.
