> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/01-export-transforms/investigation.md`.
> Original SHA-256: `acafeea9465aa4f6c55aabbde55955f34440d596626916d3e1ce9b3d84600753`. Private media/logs are not included.

# Known-transform recovery — frozen procedure, 19 October 2026

Use saved A static Gaussians, partition by deterministic index into overlapping fragments. Apply known scale1.25, Euler17/-11/23deg, translation[.3,-.2,.4] to B. Fit using distinct covariance/DC nearest descriptors with mutual unique matches, no position or ID matching; reserve20% of actual matches. Recover inverse transform. Verify positions/covariances/DC/opacity and sparse rendered RGB. Gate: rotation<0.01deg,relative scale<1e-5,median positions<1e-5 native, RGB max<1e-4. This is an exact-fragment control, not independent reconstruction.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
