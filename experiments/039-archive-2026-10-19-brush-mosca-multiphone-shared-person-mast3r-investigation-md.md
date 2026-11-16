> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/mast3r-investigation.md`.
> Original SHA-256: `9103ae6b92201e4ef7315c92538d3efefaaf5d93321ca1cc3d1b06ef85871d50`. Private media/logs are not included.

# MASt3R descriptors with calibrated triangulation

Completed: see the actual trial and rejection diagnosis (historical reference: `mast3r-result.md`).
The frozen confidence policy fails; learned matching itself remains promising.
The post-run complement/seen02 analyses are diagnostics, not replacement candidates.

19 October 2026. The user requested proceeding with one learned initializer
investigation. Selected route: a minimal local MASt3R pair inference on seen
21/13, learned reciprocal descriptor matches, then known-camera triangulation.
If source/setup/coordinate checks pass, one bounded run is included. No Gaussian
fit, new video, paid worker, time extension or evaluation20 access is included.

## Selection and source pins

[MASt3R](https://github.com/naver/mast3r) adds dense local descriptors to DUSt3R's
pair-conditioned point predictions. The official example exposes reciprocal
matching directly. We can keep supplied camera calibration and triangulate
image correspondences instead of promoting the network's inferred point map as
observed body geometry. DUSt3R alone is less direct for this matching experiment.
Only MASt3R is selected for implementation; no several-model sweep.

Official source inspected locally and online on 19 October 2026:

| Source | Exact checkout |
| --- | --- |
| MASt3R | `f5209afc300cec36239a7ac992263f36847bbba0` |
| Its DUSt3R submodule | `3cc8c88c413bb9e34c41db0e0eef99c2ee010b12` |
| Its CroCo submodule | `d7de0705845239092414480bd829228723bf20de` |

Reviewed model loading, heads, image resize/crop, fast reciprocal NN, positional
embeddings and dependency imports. Source is 12 MiB in ignored working storage.
No optional retrieval/ASMK, SfM, GLOMAP, Gradio server or compiled CUDA RoPE is
needed for direct pair inference. Use the pinned pure-PyTorch RoPE fallback.
References: [model](https://github.com/naver/mast3r/blob/f5209afc300cec36239a7ac992263f36847bbba0/mast3r/model.py),
[matcher](https://github.com/naver/mast3r/blob/f5209afc300cec36239a7ac992263f36847bbba0/mast3r/fast_nn.py),
[image loader](https://github.com/naver/dust3r/blob/3cc8c88c413bb9e34c41db0e0eef99c2ee010b12/dust3r/utils/image.py).

Checkpoint: `MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth`, exact official
[download](https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth).
HEAD returned2,754,910,614 bytes, ETag `a4349996-61ce5970b7b3e`, modified10 July 2024.
Download only this checkpoint, cap at 2.8 GB, stream/hash and pin the retrieved
SHA256 before loading. No retrieval weights or automatic model-hub downloads.

## Terms and access

The code is CC BY-NC-SA 4.0; the checkpoint's
[notice](https://github.com/naver/mast3r/blob/f5209afc300cec36239a7ac992263f36847bbba0/CHECKPOINTS_NOTICE)
also incorporates training-source terms. Read its actual contents rather than
treating code license as the complete weight license. Notices include modified
IndoorVL restrictions, CO3D and other research datasets, Map-Free exclusions for
commercial use (personal experimentation is included among noncommercial uses),
and synthetic-model restrictions. This repository's private personal research
trial is the selected use; no commercial/production deployment or redistribution
is included. Preserve all source/weight notices and attribution; no new account,
gated access or license activation is required by this download path. Panoptic
footage separately remains noncommercial/research/private. These findings are
scoped to this test, not blanket product licensing clearance.

## Minimal environment and resource readiness

The local machine has15 GiB RAM, about6.5 GiB available at inspection,4 GiB swap
partly used, and an8 GiB RTX4070 Laptop GPU with other local activity. Do not
disrupt existing applications. Choose **CPU-only** inference with two Torch/BLAS
threads and no GPU allocations. Use an isolated Python 3.12.3 environment;
PyTorch 2.5.1+cpu and torchvision 0.20.1+cpu are an official paired release
([installation reference](https://pytorch.org/get-started/previous-versions/)).
Pin NumPy 1.26.4, SciPy 1.14.1, Pillow 11.0.0, OpenCV 4.10.0.84, einops0.8.0,
huggingface-hub0.26.2 and packaging24.2. Freeze transitive dependencies after
installation. No change to the existing preprocessing environment.

Avoid double materialization of the 2.75 GB state: load the official zip checkpoint
with `torch.load(mmap=True, weights_only=False)`, construct the architecture on
the meta device and assign the pinned state dict without copying. Check every
parameter is materialized and missing/unexpected keys before inference. This
adapter differs from the upstream convenience loader; verify an actual forward
pass. No source patch, kernel compilation or model retraining is planned.

## Inputs and coordinate contract

Use only first rectified1920x1080 states from seen21/13 and their preserved masks.
Keep Brush and inherited-person control hashes fixed and evaluation20 sealed.
Crop each person using its existing mask bounding box plus32 pixels margin at
640 px scale, clamped to the original frame. This is an explicit foreground-crop
change from full-frame640 px NCC, not a clean single-variable matcher comparison.
The crop retains original resolution and makes small shoes less tiny to the net.

Use the upstream512-long-edge resize and patch16 center crop; record original
ROI, rounded resize dimensions, crop offsets and exact model-to-original pixel
transform. Inverse uses pixel centers, not merely image-size ratios. Check
custom prepared tensors exactly match the upstream loader. Track valid mask
and source/body-region coordinates through this transform. Test synthetic
known-world projection/triangulation and crop inverse before real inference.

Batch1, one forward pair, float32, no gradients. Retain predicted point maps
and confidence as explicitly **model-inferred, unregistered predictions**.
They do not seed accepted geometry. Extract learned descriptors, then call the
pinned reciprocal NN implementation in both descriptor directions with stride2,
dot distance and 2048-point score blocks. Filter actual mask pixels in both views,
three-pixel network borders, finite descriptors, descriptor confidence≥ 1.5 and
descriptor dot similarity≥ 0.8. Save raw candidates and each filter's counts.
These confidence thresholds are predeclared method settings, not probabilities.

Map matches back to original rectified pixels. Use supplied K/R/t (centimeters
converted to meters), Sampson and per-view reprojection<=1.5 px at 640 px equivalent,
positive depth>0.1 m and within 1–6 m in both views, ray angle≥ 2°, world radius<10 m.
Do not optimize cameras or use evaluation RGB/body annotations to resolve scale.
Fuse5 mm bins and export author/Brush-world colored point clouds with provenance.

## Evaluation and bounded first attempt

Report unique bins, model/raw/filtered matches, head/hands/feet bins, separate
left/right visible-shoe image regions, depth spread/outliers and supported
**unique640 px source pixels** (no dilation or inpainting to inflate coverage).
Use the existing pair gates:≥ 500 bins,≥ 50 supported pixels and≥ 10% mask
coverage in each view,≥ 20 head/hands/feet bins; visual coverage/geometry must
also pass. Nearest-neighbor reciprocal matching is not independent ground truth.
Reject semantic lookalike matches on opposite shoes even if epipolar error is
small. Compare actual crop/source/point/depth views with fixed NCC, preserving
mask/crop differences. This is an initializer trial, not coherent motion or a
Gaussian reconstruction; no fitting follows a failed gate.

Cost/run limits, dated19 October 2026: local compute only, external service cost
US$0. Source/dependency/checkpoint setup<=20 minutes, checkpoint transfer<=600s,
total new disk<=8 GiB. One900-second inference/matching process, max5 GiB RSS
enforced by a parent watchdog polling that process only; two CPU threads. Stop
before launch if available RAM<5.5 GiB. One software repair for a real code fault;
no threshold/model/crop sweep or automatic cloud fallback. No paid resources,
overnight services or GPU use. Retain failures and completed outputs locally.
An unchanged repeat is permitted for verification if the first run completes.

Expected runtime/memory are unmeasured; CPU inference may fail its bound. A
setup/resource failure is not a method-quality result. Deliver source/model/
environment pins, crop tests, actual pair evidence or exact blocker, and a
decision about whether observation-driven foreground fitting is ready.
