> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/02-independent-registration/investigation.md`.
> Original SHA-256: `0a13f975fc1b8b8e60176615686a5e1aefd022eb9906e6bf6df99e914dd64970`. Private media/logs are not included.

# Independent-scene registration — frozen procedure, 19 October 2026

Reuse existing calibrated room correspondences from independent A/B fits,28 fitting/6 excluded identities. Fit robust7parameter similarity,1024RANSAC,.15m-equivalent inlier, soft-L1 .05m,200evaluations, no ICP/threshold sweep. Compare old transform. Gate reserved median pixel<=15 and3D<=.10m-equivalent. Reused seen data, calibration-assisted studio control. Export conservative static background layers excluding person in five previously reviewed source masks; no whole-person quality claim.

## Cost and bounds

Existing local Python3.12 numpy/scipy/OpenCV/PIL CPU environment and native exports only. No paid compute, downloads or new Gaussian training. Max120s for registration/refinement; max600s per other stage, peak target<2GiB. Results and previews go under ignored `working/splat-fusion-validation/`; durable numerical records here in `docs/`. Preserve source hashes and earlier failed outputs. Camera20 RGB stays sealed. If a gate fails, later independent controls still run in order; dependent real trials are labelled diagnostics, not a validated pipeline. No threshold relaxation or retry sweep.
