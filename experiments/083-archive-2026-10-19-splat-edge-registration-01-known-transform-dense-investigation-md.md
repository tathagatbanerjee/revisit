> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-edge-registration/01-known-transform/dense-investigation.md`.
> Original SHA-256: `48a17e8fc82d661ff10d0f8c4a3d0d2542aac3c73eab16ef5be1fb90e8429ef2`. Private media/logs are not included.

# Separate direct-edge control — scoped after sparse matcher readiness failure

The original fixed SIFT-near-Canny bootstrap yields only one supported match and
is preserved as not ready. Its matcher thresholds and result remain unchanged.
Within the authorized edge hypothesis, perform one separately identified method:
use the same saved Gaussian fragments, baseline renders, cameras, physical room
mask, Canny50/150 and depth reliability gates. Optimize the symmetric physical-
edge distance/orientation proxy directly from identity, without discrete SIFT
correspondences, point IDs or the known inverse transform. The known transform
is used only to score the final result. No alternate starts or weight sweep.

Use the existing refine_edges implementation,20 nfev/<=200 objective calls,
Huber3px,2px/rad orientation, per-region equal weighting. Ten-evaluation timing
benchmark precedes fitting. Re-render all three cameras for independent final
scoring with the original0.5deg/1%/1% and90%-within2px gates. Preserve all outcomes.
600s/2GiB local CPU bound, no paid work. Original sparse result remains separate;
this additional trial cannot be silently substituted for a passed bootstrap.
