> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/03-mosca-variant-tests/investigation.md`.
> Original SHA-256: `35c72cb143457f5cbe05119b414861bad3aa67ba876098824fcc9f7b1448260b`. Private media/logs are not included.

# Deep investigation: feasibility of the recommended MoSca variants

28 October2026. Evidence: pinned MoSca source, official model repositories,
public model-file metadata and our archived baseline. Source inspection and
metadata checks are complete; no model has been loaded or run for this package.
See machine-readable sources (historical reference: `docs/model-sources.json`) and
feasibility audit (historical reference: `docs/feasibility.json`).

## What the comparison answers

Our baseline uses Metric3D-small depth, RAFT optical flow and BootsTAPIR-v2
tracks. Each new arm changes depth, tracking or both, keeping the renderer,
video, frame count, resolution, fitting schedules and worker constant.
This tests four reconstruction **pipelines**. Tracker wrappers have different
internal resolutions, visibility decisions and sampling behavior, so a result
is not a pure comparison of transformer architectures at identical computation.

The question is whether a different supported input-analysis pipeline improves
observed people and navigable geometry on the same three-second clip. More
tracks, larger weights, an import success or faster rendering do not answer it.
Use the shared evaluation (historical reference: `../evaluation.md`) and retain all failed arms.

## Source and model availability

MoSca pin: `02404d2841b4e0dc2d9074860950bce5da579656`.
The reviewed adapters already contain Metric3D `small`, `large`, `giant2` model
selectors and a CoTracker3 online loader. No new Gaussian representation or
fundamental MoSca rewrite is required for the four proposed arms.

Official model code was resolved to these revisions on the checked date:

| Model code | Reviewed revision | Relevant interface |
| --- | --- | --- |
| Metric3D | `eb5b6fac0dc155e4e52f576e304fbf11655ff339` | `metric3d_vit_small(pretrain=...)`, `metric3d_vit_large(pretrain=...)`; inference returns depth/confidence/other outputs |
| CoTracker | `82e02e8029753ad4ef13cf06be7f4fc5facdda4d` | `cotracker3_online(pretrained=...)`; predictor initializes each video and then processes chunks |

Sources: [Metric3D hub constructors](https://github.com/YvanYin/Metric3D/blob/eb5b6fac0dc155e4e52f576e304fbf11655ff339/hubconf.py),
[CoTracker hub constructors](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/hubconf.py),
[online predictor](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/cotracker/predictor.py).

Public Hugging Face metadata reports these exact files in repositories marked
public and ungated. Metadata access is not a completed binary download, weight
load or permission guarantee for every future request.

| Weight | Size, decimal GB | Recorded SHA-256 |
| --- | ---: | --- |
| Metric3D-small800k |0.1501|`b34b2a2be9148054991cef7e417930e1320602ba7bc503b0ee4e7888543728f6`|
| Metric3D-large800k |1.6480|`15328ffc42b528b95f188687418f6f03b3f123eb34ccdbd686c112abbea6d972`|
| CoTracker3 scaled online |0.1017|`205d34789f19699d64b22cf93f9b697f15f28d4025240e31532e504109837218`|

The small-model hash matches the retained historical weight receipt. Large and
CoTracker3 add about1.75GB of selected weight files, before source/dependencies
and cached archives. File size does not predict peak VRAM. The weight repository
revision hashes, file sizes and LFS hashes are in the source receipt; use those
immutable revisions rather than `/resolve/main/` for a later download.

[Metric3D weight metadata](https://huggingface.co/api/models/JUGGHM/Metric3D?blobs=true),
[CoTracker3 metadata](https://huggingface.co/api/models/facebook/cotracker3?blobs=true).
No binary range/full-weight request was made during this investigation.

## Configuration needs to reach the selected model

Writing a different YAML value is insufficient if the factory ignores it.
Upstream `get_moca_processor` does not forward `metric3d_depth_version`; our old
small-model run used a documented forwarding patch. Recover the actual executed
source for the exact baseline, not just the unmodified cached checkout.

For an explicit common factory, forward the model selectors through to
`MoCaPrep`, preserving all existing arguments:

```python
metric3d_depth_version=getattr(pre_cfg, "metric3d_depth_version", "small"),
cotrakcer_version=str(getattr(pre_cfg, "cotrakcer_version", "3")),
cotracker_online_flag=getattr(pre_cfg, "cotracker_online_flag", True),
```

`cotrakcer_version` is the constructor's actual misspelling. The proposed
profiles use it deliberately. Record the patch and constructor arguments;
assert the instantiated model name, expected weight hash and tracker mode.
Do not use the misspelling as an excuse to guess additional unsupported flags.

Metric3D's wrapper calls `torch.hub.load(..., pretrain=True)`. CoTracker uses
`pretrained=True`. Their current hub loaders reference moving source/weight
URLs. Pinning MoSca alone therefore does not freeze either model.

Prepare local pinned checkouts and local hash-verified weights. Instantiate
Metric3D from its pinned local hub with `pretrain=False`, then load the selected
`model_state_dict`. Instantiate CoTracker online with `pretrained=False`, then
load the scaled-online state into `predictor.model`, matching the official hub
implementation. This loader adjustment is implementation work to complete before
execution, not a patch already applied here. Save strict load coverage; Metric3D's
official hub uses `strict=False`, so report missing/unexpected tensors and fail on
unexplained learned-parameter omissions rather than assuming a partial load is fine.

Use one common pinned Metric3D implementation for small and large in the new
matrix. If it differs from the historical cached implementation, qualify the
new small-model control before comparisons. Retain the exact historical replay
separately. No change to the pretrained models' own training is proposed.

## CoTracker needs a real adapter preflight

MoSca's processor emits a forward/backward-inference warning. The current
CoTracker3 online predictor initializes a new stream with `is_first_step=True`
and returns `(None,None)` for that call. Its16-frame model window gives an
8-frame step. MoSca implements its own forward/reversed passes and fuses the
results around each query's starting time.

Static inspection finds a concrete short-smoke hazard: the old wrapper only
makes its initialization call at a positive multiple of `model.step` in the
frame loop. For sequences of≤8 frames that branch never runs, yet the final
prediction call still occurs. The proposed36-frame input reaches initialization,
but that does not prove correct tail coverage, memory-state resets or coordinates.
Do not use an8-frame smoke to certify this adapter. Either reject such short
inputs explicitly or repair initialization under a documented new adapter.

Before a real fit, test the pinned model and wrapper with16,36, and a
non-step-aligned37-frame input, including query times at first/middle/last frame.
Require a finite `[T,N,2]` track array and boolean `[T,N]` visibility with exactly
T original-time rows, no duplicated query identities and no skipped tail. Reset
stream state for every query chunk, direction and new video. Check manually
identifiable source points in forward/reversed video. A synthetic API mock can
catch calling errors but cannot establish learned tracking accuracy.

Both adapters save compatible `tracks`/`visibility` NPZ fields and use
tracker-specific filenames that MoSca can discover. Keep only the declared
tracker's generated priors in a job-unique workspace. Test the reconstruction
loader on that file before any full fit.

## A fair comparison needs controlled queries and conventions

The BootsTAPIR wrapper resizes to256×256 and uses integer `[t,y,x]` queries;
CoTracker takes `[t,x,y]` with its own internal resize. Track outputs must be
restored to the original640×360 grid. The TAP coordinate helper's implementation
uses size ratios, whereas CoTracker's internal conversion uses endpoint ratios.
A naïve shared resize formula can introduce a systematic offset.

For a matched-query comparison, generate one canonical source-coordinate query
manifest and freeze it before any arm. Choose points representable on the TAP
integer query grid, convert using the actual pinned TAP helper, and feed their
corresponding source-grid floating coordinates to CoTracker. Retain query IDs,
source time, axis order, masks and per-wrapper round trips. Check corners,
interior points, chunk boundaries and full query count. Do not assume equal
seeds produce the same queries across two different wrappers.

The existing CoTracker wrapper serializes `queries` from the final chunk while
concatenating track arrays from all chunks. That field cannot serve as complete
query provenance for this trial. Persist the full canonical query list and its
chunk-to-output mapping in a separate receipt or fix serialization explicitly.
Do not reorder an array and silently lose physical-point identity.

Its predictor combines visibility/confidence and applies its own0.6 threshold;
BootsTAPIR's adapter applies a different model-specific occlusion rule. Keep each
frozen native policy for the initial comparison and report correct visible
support. Equal threshold values would not make their confidence calibrated.
No threshold search against final person crops is included.

If shared-query injection is deferred, the first four runs can compare native
sampling **pipelines**, provided input/query counts and policy are documented.
They cannot claim that tracker model alone explains the difference. Choose and
freeze one comparison mode before running; do not switch interpretation afterward.

## Environment compatibility: what is and is not confirmed

Start with the known Python3.10/PyTorch2.1+CUDA11.8 A40 fitter. The Metric3D
requirements file names older Torch/TorchVision/NumPy/xformers pins; applying it
wholesale would change our working stack. Preserve our compatible environment
and test the selected model on it first. CoTracker's setup metadata has no full
runtime dependency lock; a successful `pip install` is not a compatibility proof.
[Metric3D requirements](https://github.com/YvanYin/Metric3D/blob/eb5b6fac0dc155e4e52f576e304fbf11655ff339/requirements_v2.txt),
[CoTracker package metadata](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/setup.py).

If a candidate genuinely needs an incompatible environment, generate its priors
in a separately pinned process and feed validated saved arrays to the unchanged
fitter. Do not upgrade Torch, change the GPU and replace the tracker in one arm.
We have **not** demonstrated the larger model's VRAM use or CoTracker's operation
on our exact worker. Those are explicit preflight gates, not hidden assumptions.

Record each component's notices. Metric3D source is BSD-2-Clause; the reviewed
CoTracker repository is labelled CC BY-NC4.0. Keep this research trial and its
artifacts within the already recorded research scope; a permissive MoSca label
does not clear every dependency or checkpoint for a commercial product.
[Metric3D notice](https://github.com/YvanYin/Metric3D/blob/eb5b6fac0dc155e4e52f576e304fbf11655ff339/LICENSE),
[CoTracker notice](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/LICENSE.md).
This records the notices, not a comprehensive legal determination.

## Verdict and first action

**Yes: the proposed four combinations have identified model constructors,
public weight metadata, and a compatible saved-prior interface into MoSca.**
The work required is a bounded adapter/environment qualification, not inventing
another reconstruction method. An unconditional end-to-end readiness claim
would be premature until the weights load, priors pass and the new control fits.

First recover the short input and exact baseline environment, then use **one**
A40 setup to validate and reproduce it. Compare V10/V01/V11 on the same worker.
Only after a useful variant is identified should we measure whether another
Runpod GPU/image reduces its total cost. The infrastructure check is a prerequisite;
a broad hardware benchmark is not. Keep longer-video trials after the short
variant decision so a change in duration does not hide the source of a gain.
