> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/11-fixed-world-appearance/investigation.md`.
> Original SHA-256: `a1dfdc0f7d41c639007b6fc540acc4363080495c377413053019a7e632ddaed4`. Private media/logs are not included.

# Downstream audit and observed limits

The previous experiment qualified cameras and sparse background depth corrections.
That does not automatically qualify the rest of the native MoSca pipeline.

## Depth propagation

Pinned `Saved2D.rescale_perframe_depth_from_bundle` reads `dep_scale` only. It
does not carry `dep_correction` into dense inputs. This continuation interpolates
the fitted corrections with the native16-neighbor camera-space RBF policy,
restricted to the existing depth mask and visitor-excluding feature masks. The
original depth files remain immutable; the loader applies the cached delta after
the existing frame scale and recomputes its depth mask.

CPU replay:0.765px median,1.062px worst-frame median,288 minimum usable anchors.
Actual pinned CUDA interpolation agrees with the CPU cache to at most3.16e-6
normalized depth units at6,144 sampled pixels across three source-time probes.
This validates implementation agreement, not independent physical depth.

## Camera reloads

Native warmup and photo code hardcode nonzero camera learning rates, and loading
a checkpoint recreates trainable parameters. Each load now checks the entire
reference state, freezes every parameter and removes camera optimizer groups.
The photo wrapper zeros camera rates/schedules as well. Every stage compares all
loaded camera state tensors exactly with the qualified reference.

## Motion support failure and separate exploratory arm

The original continuation stopped before scaffold construction/optimization at
the declared eight-visible-observations-per-frame check. A read-only replay
retains1,068 motion curves overall, but87 frames have fewer than eight visible
observations. Some have zero. Raw dynamic visibility also falls as low as one,
so the problem is not solely the3D refilter. Weak intervals are mainly11.5–16.57s
and20.23–22.43s. Source views include quiet architecture and distant people;
these counts cannot distinguish all quiet intervals from tracking gaps.

The original failed check and all evidence remain intact. A separate case,
`guildhall-fixedworld-exploratory`, was explicitly declared on the same bounded
allocation. It keeps the same priors and camera/depth package, while allowing
native scaffold optimization with the original full-motion coverage result
recorded as failed. It produces133 finite scaffold nodes with exactly unchanged
cameras. This is native eligibility for a labelled visual experiment, not a pass
of the original motion gate or quality promotion.

## Foreground initialization

Native foreground/background initialization averages the old long-span static
Boots tracks again. That would reintroduce the rejected background identities.
A pre-fit amendment replaces those means with qualified background anchors and
currently visible optimized scaffold nodes. The original protocol/code is saved
under `docs/pre-fit-original/`; allocation bounds did not change.

Manual review of the first appearance initialization found nearest-node Voronoi
assignments spilling into a statue, column and floor near the late visitor. That
initialization was rejected before the original photometric fitting function or
any Gaussian optimizer ran. The original mask, report, code, review and failed
stage are preserved in `docs/foreground-initialization-original/` and ignored
worker retrievals.

The corrected initializer intersects its foreground proposal with existing
visitor-box support, preventing those broad room assignments. These are padded,
temporally unioned detector boxes, not segmentation ground truth. It preserves
the unclipped fractions for comparison and requires a fresh manual review before
the first appearance optimizer step. Camera, source arrays, fitted scaffold,
original failed motion gate, budget and deadline are unchanged.

Only one actual appearance optimization attempt is planned. Pre-optimizer guard
failures and initialization corrections are distinct from trained alternatives;
none may be suppressed or represented as a successful original protocol.
