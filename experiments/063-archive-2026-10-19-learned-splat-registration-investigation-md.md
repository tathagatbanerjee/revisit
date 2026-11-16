> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/investigation.md`.
> Original SHA-256: `5f2202ae0a625a92259e214907873d9495b7dc901c8ab17c0c5b11c5b6c53348`. Private media/logs are not included.

# Investigation — 19 October 2026

## Question and smallest trial

Can pretrained registration recover a useful alignment between two independently
fitted full MoSca scenes? Compare GaussReg coarse registration with splatreg's
BUFFER-X initializer and its default overlap-aware Sim(3) refinement. Neither
method is assumed to solve independent dynamic reconstruction distortions.

Use the exact existing A18/B12 full snapshots, 65,507/62,380 Gaussians, at
1.5015 event seconds. No previously fitted transform enters the estimator.
Precede the actual pair with an exact transformed-copy control of A: scale1.12,
Euler XYZ [8,-12,20] degrees, translation [.2,-.1,.15] in native A units, shuffled
rows. Control truth is scoring-only and never uploaded to inference code.
Run the actual pair even if the control fails, but label the failure and do not
promote a real merge based on appearance alone. One fixed random seed12345.

Score the recovered transform using existing room physical-ID validation
(cell%5==2, six IDs), twenty seen person observations, and fixed camera renders.
Room/person pixel gates <=15px and native-distance gate <=.10m-equivalent.
Known-copy gates: rotation <=.5 degrees, relative scale error <=1%, translation
<=1% A bounding-box diagonal. Whole-scene fusion requires all applicable gates,
full point retention, and inspected views/time states. Missing semantic contour
coverage remains unvalidated. No labels used for inference, no candidate search
against score labels, no camera20 access, no new fit or adaptive threshold sweep.

Inspect full A, registered B and raw union through common fixed cameras at
A6/B0, A18/B12, A30/B24. The one transform is constant through time. Publish
diagnostics only if finite positive similarities are produced; preserve failures.
No deduplication/deletion, photometric correction or local shape warp in this test.

## Software and inputs

GaussReg official source: https://github.com/GAP-LAB-CUHK-SZ/GaussReg (MIT).
Main85df227f3bb842c82e605330cc5522335ac11fbc; refine branch
05f4669 inspected separately. Main demo provides pretrained coarse registration
and maps a normalized prediction back into native source/target coordinates.
It filters opacity>.7 and axis-wise5–95percentiles, samples at most30k points,
uses opacity and RGB features, and requires45 higher-order SH fields. Our saved
DC-only splats can be losslessly represented with zero higher-order SH fields.
This adapter changes no source appearance/geometry. Retain original exports.
Use torch.no_grad for inference; modern dependency compatibility patches must
be recorded. Upstream Python3.8/torch1.7.1/cu110 is old; modern isolated CUDA
environment is an installation feasibility question. Main's fine stage is TODO;
refine branch has a separate rasterizer and feature pipeline. This first bounded
comparison explicitly tests released coarse registration; fine-stage integration
is separately reported, not silently replaced with our old optimizer.

splatreg source: https://github.com/Archerkattri/splatreg (BSD-3-Clause),
db7c05aa127cbaac5bb139f7db44c3d9fe3c4d69, version1.5.0.
BUFFER-X: https://github.com/MIT-SPARK/BUFFER-X (MIT),
07dd9be5a58c9c02213584535592766c9023cebc.
Weights: https://huggingface.co/Hyungtae-Lim/BUFFER-X, revision
f657b1f737fce0a8eab40c56204abaea27316b4a, 3DMatch Desc/Pose only.
Splatreg loads both full-model checkpoints. Assert meaningful matching of all
descriptor/pose parameters and `used_bufferx=true`; any classical fallback is
a setup failure for this requested condition, not a BUFFER-X result.
Use separate inference processes to avoid conflicting `config` module imports.
Record compiler/CUDA/torch/numpy versions, patches, elapsed time, peak GPU memory,
RAM, input/output/checkpoint hashes. No benchmark dataset downloads or training.

Native BUFFER-X uses CUDA pointnet2, CPU neighbor/subsampling extensions and
legacy KNN/SVD packages. Its current upstream installer supports CUDA12.4.
Compatibility-only KNN/SVD torch equivalents and native compiler adaptations
may be used if necessary, with direct numerical checks and patch records.
Keep model architecture, checkpoints and matching settings unchanged.

## Cost estimate and run limits

User authorizes both tests on Runpod and, after A5000 capacity was unavailable,
an available GPU within US$2 and a two-hour cutoff. Official pricing checked
19 October2026: https://www.runpod.io/pricing. Live GraphQL returned no A5000
secure/community stock; community RTX5000Ada32GiB was available at$.49/hour.
Recheck rate/capacity before launch. One Linux on-demand Pod, one GPU, >=16GiB
host RAM, <=80GiB ephemeral disk, no paid persistent volume. Prefer RTX5000Ada
at <=$.59/hour; A5000 if capacity returns. No more expensive fallback.

Expected0.5–1.5hours including setup/download/build/inference/retrieval:
$.245–.735 compute at$.49/hour. Cutoff2hours at rate ceiling$.59 yields$1.18;
reserve$.82 for ephemeral disk/transfer/other charges, total allowance$2 before
tax. These are estimates, not measured inference costs. Stop if published
charges cannot fit the allowance. No paid license. No account-wide spend cap.

Launch a separate local watchdog process before creation; it polls a uniquely
named job state and terminates the owned Pod at the deadline independently of
SSH/model processes. Never terminate unrelated Pods. Maximum one successful
Pod; retry an unallocated capacity failure only after unique-name reconciliation.
Allow one compatibility repair per distinct setup error under the same clock;
no changed checkpoint/model/threshold fallback. Allocate setup time fairly,
retain partial logs, retrieve both results and terminate immediately when done.
Record exact billed duration estimate and independently verify Pod absence.
No retained paid volumes; keep source/checkpoints/results locally, ignored.

## Deliverable

Per-method numerical outcomes and actual rendered comparisons if inference
works; otherwise a precise checkpoint/build/capacity feasibility result. A
successful exact-copy control does not establish real independent-fit fusion.
