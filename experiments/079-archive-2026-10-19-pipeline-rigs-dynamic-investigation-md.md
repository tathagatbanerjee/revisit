> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/rigs-dynamic/investigation.md`.
> Original SHA-256: `ed1ee8e876188c809979a970e44f6a86493dcffad261983b1b15ac04c59920fd`. Private media/logs are not included.

# Milestone 3 investigation: reconstruct a short event from our video

Investigated and started 2026-10-14. The user's request to move to Milestone 3
covers investigation and one bounded custom-video experiment. First run a
readiness check; do not rent hardware to discover an unusable entry point.

## Aim and chosen input

Fit a shared 3D scene whose foreground changes over time from **our own
monocular recording**, then test the Milestone 2 controls. This adds motion
reconstruction rather than modifying Brush's static trainer. Keep the room
stable while two visitors walk across it. Hidden geometry and estimated motion
remain reconstruction hypotheses, not new observations.

Prepared and visually inspected `03-guildhall-interior.mp4`, prepared-clip
seconds **8–11**, original media seconds **58–61**. Downsample to **640×360,
12 fps, 36 frames**, with no audio. This interval includes the SHARP source
moment at clip 10 s and clear walking motion in front of stationary monuments.
There is camera panning, limited translation and foreground occlusion: this is
useful but not guaranteed geometric coverage. Preserve original input unchanged.
Source terms/credits remain in footage sources (historical reference: `../../docs/footage-sources.md`).
Recording UTC is unknown; media-relative offsets are retained.

Ignored local files: `working/rigs-dynamic/input-review/guildhall-08-11.mp4`,
contact sheet and `provenance.json`. Fully decoded/verified: 3 seconds,
36 frames, 640×360. Prepared SHA-256:
`af8be7089bdead75657f3f443213599aeb59af82a43193f66c432bd12db7c843`.

Preparation commands, run from the experiment root (choose a fresh destination
if repeating; `-n` preserves existing files):

```bash
ffmpeg -n -ss 8 -i data/clips/03-guildhall-interior.mp4 -t 3 \
  -vf 'fps=12,scale=640:360' -an -c:v libx264 -crf 18 -pix_fmt yuv420p \
  working/rigs-dynamic/input-review/guildhall-08-11.mp4
```

## Source pins and release readiness

[RiGS](https://github.com/ladvu/RiGS) revision
`f89bd0c224aee46bdafd2a6327775aabfad9b3c4`.
[Modified ViPE](https://github.com/ladvu/vipe) revision
`5165cffc18f6ee239fd376f8a35cc06ad6e60b9e`.
Both are cloned to ignored working directories for source inspection only.

The current release cannot be run unmodified using its documented setup:

1. `.gitmodules` advertises `dependencies/vipe` but the tracked tree has **no
   gitlink**. A recursive clone or submodule update does not supply that code.
   The fork is public and contains `motion_aware.yaml`; it can be checked out
   separately and pinned, rather than guessing a nonexistent submodule revision.
2. `src/main.py` assigns the `FusedRunner` class and calls its instance `train`
   method without constructing it with `cfg`. The constructor accepts `cfg`.
   Training needs an initialized runner. Check checkpoint loading separately;
   do not apply a blanket one-line change and assume evaluation also works.
3. The README's `dog-example` data and a fitted checkpoint are **not included**,
   and no example download link is supplied there. That prevents the promised
   ready-made example reproduction from being assumed available.
4. Requirements pin `torch==2.11.0+cu128` / torchvision CUDA variants, but provide
   NVIDIA's package index rather than the matching PyTorch CUDA wheel index.
   PyPI metadata has `torch 2.11.0`, not `2.11.0+cu128`. Resolve correct wheel
   indexes/toolkit/driver versions before installation. Several Git dependencies
   have unpinned revisions; freeze those rather than installing moving heads.
5. **No project-wide RiGS license was found** in the tracked tree or README.
   Some imported files have Apache headers; those do not grant terms for all
   original RiGS code. Do not call the whole project permissively open-source
   or redistribute its implementation. Its reuse permission remains unresolved.
   [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
   explains why a public repository does not imply a general license.

The local `preflight.py` performs a read-only AST/Git/file audit; its status 2
means readiness gaps found, not a GPU training failure. Findings are saved in
`working/rigs-dynamic/preflight.json`. No model weights or CUDA packages have
been installed, and no author has been contacted on the user's behalf.

## Pipeline after readiness is resolved

1. **Environment:** isolated Linux Python 3.10, compatible PyTorch/CUDA 12.x,
   native ViPE CUDA extensions, gsplat and fused-SSIM. RAPIDS `cuml` is imported
   for HDBSCAN/KMeans initialization, so it cannot simply be dropped from
   requirements. Audit which additional listed RAPIDS/UI packages are actually
   needed; do not install the complete development environment blindly.
2. **Preprocessing:** supply our short MP4 and matching indexed PNGs. The pinned
   ViPE fork's `motion_aware` configuration uses optical-flow geometry plus SAM
   for dynamic masks. Use MoGe keyframe depth and `adaptive_moge` alignment,
   following the RiGS helper, avoiding default VideoDepthAnything alignment
   unless needed. Exact runtime compatibility and memory are not measured.
3. **Artifacts:** preserve RGB images/video, EXR depth ZIPs, flow ZIPs,
   flow-consistency ZIPs, intrinsics/pose NPZs and static-mask ZIPs. RiGS expects
   those named per scene. Inspect image dimensions, frame counts, positive
   finite depth, camera continuity and foreground mask coverage before fitting.
4. **Tracking:** download the explicitly referenced BootsTAPIR v2 checkpoint,
   inspect its terms, run TAPIR on the 36 frames/masks, and examine track
   continuity. Default tracker resizes to 256×256. Pair outputs are quadratic
   in frame count; 36 frames means up to 1,296 named pair files. Record the
   coordinate conversion back to the dataset image dimensions.
5. **Fitting:** initialize the runner with the actual configuration and use
   native 3DGS mode for a standard 3D Gaussian snapshot adapter. Default RiGS
   mode is 2DGS; its disk primitives are not automatically equivalent to our
   3DGS PLY contract. Proposed first smoke: batch 1, 10k foreground primitives,
   point cap 100k, 3k iterations using schedule scaling, with matching save/eval
   steps. The default 5k initialization phase must scale too; lowering only
   `max_steps` would miss joint fitting. Initialization has additional work not
   covered by the outer training step count. This smoke is not convergence.
6. **Native inspection:** use the saved checkpoint in its native viewer. Verify
   time normalization/indexing, camera poses, world normalization and component
   fusion. Pause moving visitors and shift viewpoint; advance time at a fixed
   alternate view while checking the monuments remain stable.
7. **Export only if practical:** query the fitted scene at selected times using
   native component evaluation, activate scales/opacities/colours, apply lifespan
   behavior, and fuse the chosen components. An initialization point-cloud PLY
   is not the trained dynamic model. Retain per-time geometry in one world frame.
   First export 12–20 snapshots; no generic service or Lambda conversion needed.
8. **Evaluate and stop:** compare source and nearby renders, preserve failures,
   retrieve checkpoint and priors, stop/verify cloud cleanup. Broader footage,
   repeated attempts or larger hardware are separate choices based on evidence.

## Reuse terms and prerequisites

ViPE's main code is Apache 2.0 with documented third-party exceptions (including
Unik3D CC BY-NC-SA, which is not selected here). MoGe, SAM, SLAM/flow networks,
TAPIR checkpoints, CUDA packages and gsplat have separate terms; source code
license and checkpoint terms must be checked independently. ViPE's
[third-party notices](https://github.com/ladvu/vipe/blob/main/THIRD_PARTY_LICENSES.md)
are the starting point. RiGS's missing project license remains a substantive
prerequisite, rather than assuming Apache headers on copied helper files apply
throughout. No RiGS code/weights are vendored into our repository.

## Cost estimate and run limits

Current stage is **local source audit + input preparation: US$0 AWS cost**.
No paid worker is running. WSL reports an RTX 4070 Laptop GPU with 8,188 MiB
VRAM (6,734 MiB free at inspection), ~3.5 GiB host RAM available and nearly full
swap. That does not establish sufficient memory for this multi-model pipeline;
no training/model installation is attempted on the user's active workstation.

If RiGS becomes runnable with clear reuse terms, provisional worker selection:
**one Sydney g6.xlarge**, Linux On-Demand, 4 vCPU, 16 GiB host RAM and L4 nominal
24 GB. Rate **US$1.0464/hour**, verified earlier on 2026-10-14 using the AWS
Pricing API, catalog effective 2026-10-01:
[official regional catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv).
This is a sizing candidate, not a demonstrated memory requirement. Recheck rate,
quota, capacity and compatible AMI at launch. The previously checked On-Demand
quota is four GPU vCPUs, so a 32 GiB 2xlarge worker cannot be assumed available.

Expected **1–3 hours** including setup/checkpoints, preprocessing, tracking,
short fitting and retrieval: **US$1.05–3.14 compute**, plus disk/transfer/storage.
Hard cutoff **3 hours from launch**, independent termination schedule and worker
poweroff configured before execution. **US$5 total session allowance**, including
up to US$1.86 for 150 GB temporary disk, bounded transfer/requests, public IPv4
and short retention; before tax. Estimate only, not a billing/account-wide cap.
Use at most one scene/worker attempt, at most 20 GB checkpoint downloads and
5 GB retrieved artifacts. Stop on setup, preprocessing or memory failure; no
larger paid fallback automatically. Delete worker/job disk/network/IAM/schedule
resources and verify absence; retain only identified private inputs/results.

## Decision after the first readiness test

**Input prepared; unmodified RiGS run failed the readiness gate.** No dynamic
reconstruction or quality result is claimed, and no paid job is justified yet.
Resolve the project reuse terms and entry/environment gaps before RiGS execution.
MoSca is the already-shortlisted alternative if RiGS cannot be made runnable:
its own code has explicit MIT terms and bundled small demos, though its model
priors/renderers still require their own audit. We inspected its documentation
and source as a fallback; have not installed/trained it or silently advanced
Milestone 4. See lessons (historical reference: `lessons.md`) and next steps (historical reference: `next-steps.md`).
