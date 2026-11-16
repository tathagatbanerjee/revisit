> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/splatreg-bufferx/investigation.md`.
> Original SHA-256: `3d51f1f73d2cb2bdd7b60f09aef63c976ee6309db285c6b6df681dd49f8e7a37`. Private media/logs are not included.

# splatreg / BUFFER-X implementation investigation

Pin splatreg1.5.0 and official BUFFER-X as in the
shared investigation (historical reference: `../investigation.md`). Use `register(..., init='bufferx',
transform='sim3')` with default overlap-aware refinement; no post-hoc best seed
selection. Keep actual BUFFER-X defaults and fixed random seed12345.

The loader resolves repo-root `third_party_models/BUFFER-X`, both 3DMatch
Desc/Pose checkpoints, and built neighbor/subsampling extensions. The current
official BUFFER-X forward accepts src_fds_pcd/tgt_fds_pcd and unaligned global Z.
Its pretrained model estimates SE(3); splatreg's subsequent refinement estimates
scale. Unknown independent scale therefore remains an important failure mode.

Record real seed execution and parameter-load coverage. Fail loudly if loading
or inference falls back; retain original exception evidence. Native CUDA
pointnet2 must build. KNN/SVD compatibility shims may preserve the exact operation
with bounded numerical checks; do not replace descriptors or learned weights.
Cost and cutoff are the shared one-Pod US$2/two-hour bounds, not a second budget.
