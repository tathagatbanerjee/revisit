> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/05-fusion-refinement/geometry-investigation.md`.
> Original SHA-256: `d38ac3e65bd0b486a32da78d8e076e0ca8c2630a99afd78b984629750b69f057`. Private media/logs are not included.

# Additional local geometry refinement — scoped before execution

The six-parameter appearance diagnostic fails its fixed reserved-pixel gate.
Preserve it. To test actual geometric refinement rather than substitute colour
correction for that component, perform ONE separate bounded CPU trial on the
uncoloured stage04 consolidated room. This is not a tuned retry of the affine fit.

Keep A fixed and B opacity, colour, scale and covariance orientation fixed.
Select up to512 retained B Gaussians with nearest A centre within0.15m-equivalent,
ranked by their summed contribution to fitting pixels only. Optimize their XYZ
using differentiable native-style full-covariance projection and alpha compositing
against the same frozen fitting source pixels. Fixed initial depth order/support
is an optimizer approximation; require initial RGB parity<=2e-5 with the independent
NumPy renderer. Score the exported result using the NumPy renderer with fresh
support and depth sorting, including all reserved pixels. No held-out camera RGB.

Use30 Adam steps, learning rate0.05 on tanh-bounded position variables, maximum
position displacement0.01 A-native units per axis; robust RGB loss sqrt(error²+1e-6)
plus0.01 mean squared normalized displacement. No colour/opacity optimization,
weight sweep, best-checkpoint selection or threshold change. Stop training by100s;
whole trial budget240s, peak target<2GiB, local CPU only. Same gate: reserved mean
MAE improvement>=2%, no source-view regression>2%. Report this trial separately,
even if it fails; do not replace failed04/05 results. This tests a small local
geometry update, not full-model densification or actor fusion.
