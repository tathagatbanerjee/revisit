> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/05-fusion-refinement/investigation.md`.
> Original SHA-256: `c5df3ecfe4d9af2bbc5188c62782f4ebf50909abe9d85965955632b747754635`. Private media/logs are not included.

# Fusion refinement — frozen procedure, 19 October 2026

One local bounded appearance-only refinement of consolidated real background: fit a six-parameter RGB affine correction for B using fixed alpha-compositing weights from two source views. Ridge toward identity(.01), gains bounded .9–1.1, biases +/-.05,200least-squares evaluations. Checkerboard source-pixel partition frozen before evaluation; reserved pixels are seen-view development, not fresh-view validation. Require reserved MAE improvement>=2% and no A source-view regression>2% versus unrefined. No geometry repair claim. If02/04fail, execute diagnostic but do not promote end-to-end fusion.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
