> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-guided-mosca-registration/investigation.md`.
> Original SHA-256: `f4ef4e14c032eba7c0b9346903092098c4881e00f8a645e1984dae20723971b3`. Private media/logs are not included.

# Investigation — 19 October 2026

## Hypothesis and scope

The last learned registration trial produced poor global alignments from full
independent MoSca snapshots. BUFFER-X passed an exact-copy control but failed
real room/person gates. Brush background models may provide more useful static
matching geometry. We will test this without replacing the final MoSca models
or correcting their people independently. No outcome is assumed.

This package prepares tests. Execution requires a subsequent request. Historical
Runpod sessions are closed; their previous allowances are not a live session.
No executable runner is being launched by these documents.

## Existing evidence and initial inputs

Use the exact existing independent full MoSca Panoptic camera00 A and camera24 B.
Native exports are under
`../working/independent-mosca-fusion/retrieved/native/{a,b}/` with report.json,
static.ply and per-state moving PLYs. A has65,507 Gaussians, B62,380; both together
have127,887 during overlap. Freeze hashes before any implementation.

A source images/masks are in
`../working/multiphone-tests/indoor-panoptic-person/lead/`. B images are in
`../working/independent-mosca-fusion/input/b/images/`; the original manifest
records event PTS and frame mapping. Full reviewed B per-frame masks are an
unmet prerequisite, not supplied by an old preview JPEG or camera02 masks.
Conservative room exclusions in the previous registration package can inform
review but do not certify a complete semantic partition.

Prepare at most the existing36 A/34 B images at640×360. Exclude A6/18/30 and
B0/12/24 from Brush photometric fitting, keeping them for proxy inspection and
transfer comparisons. Their RGB and MoSca models are already seen, and seeds
may inherit information from them: this is not independent evaluation.
Use all required mask reviews without describing reviewed pixels as unopened.

First transfer instant: A18/B12 at1.5015 event seconds. Later diagnostics:
A6/B0 and A30/B24, followed by the preserved40-state source-valid union timeline.
Do not replace actual PTS with median frame intervals or pad expired sources.
Camera20 RGB stays sealed throughout this suite. New virtual renders do not
make these scenes independent evaluation data. Moving-phone/general-scene
conclusions need a separately scoped recording with genuine parallax.

## Source/version investigation

Reuse Brush v0.3.0 from the prior successful local/Runpod experiments. The Linux
archive SHA256 in `../runpod/remote-setup.sh` is
`4f0f9a8785d1951c62df26aae247c02c5bba32b00f40b06df4e1c9b867399e20`.
Verify cached archive/executable and actual `--help` before forming commands.
Brush uses Vulkan/WebGPU; CUDA success alone is insufficient. Record actual
adapter/device and reject software-rendered training. Do not fetch a newer
release silently. Official source: https://github.com/ArthurBrussee/brush.

Reuse splatreg1.5.0 commit
`db7c05aa127cbaac5bb139f7db44c3d9fe3c4d69`, BUFFER-X commit
`07dd9be5a58c9c02213584535592766c9023cebc`, and the exact released Desc/Pose weights
and hashes from `../learned-splat-registration/splatreg-bufferx/docs/preflight.json`.
Those checkpoints, native extensions and recorded compatibility shims already
ran. Verify the model really executes (`used_bufferx=true`, full parameter-load
coverage); a classical fallback is a failed setup prerequisite. Use the same
seed12345 and default Sim(3) overlap refinement as the prior baseline. No
training, seed search or adaptive preprocessing/model change is included.

Read the implementation in `../learned-splat-registration/run_bufferx.py` and
its compatibility scope before reuse. Current splatreg's seed wrapper receives
Gaussian centers without reproducing the full upstream dataset preprocessing.
Keep that wrapper fixed here to isolate the reconstruction/input change.
Sources: https://github.com/Archerkattri/splatreg and
https://github.com/MIT-SPARK/BUFFER-X. Preserve upstream licenses; retain heavy
third-party code and weights in ignored working storage.

## Independent preparation and coordinate bridge

For each video separately, export its own native MoSca K, poses, static seed
geometry and timestamp mapping into a supported Brush dataset. Use fixed
intrinsics/poses from that video's actual fit, not a shared calibrated room
model. Remove visible people/motion from both loss masks and initialization
seeds, including head/torso Gaussians classified static by MoSca. Freeze masks,
seed selection and provenance before either fit. No cross-video matching,
joint Brush fit or existing A/B registration may initialize these proxies.

Use explicit constructed bridges wherever possible. Audit Brush's actual load,
normalization and export conventions rather than assuming identity. Map physical
camera centers and directions consistently, and keep intrinsics/resizing/crop
conventions separately recorded. A world similarity cannot compensate for an
incorrect focal length or pixel transform. Do not infer scale from one fixed
camera center or a degenerate trajectory. An unknown bridge stops transfer.

The earlier assembled hybrid has a camera-based motion bridge, but it used a
shared recovered/calibrated world. Reusing that A/B alignment here would leak
the answer into the blind Brush registration. Reuse code conventions only.

## Smallest fitting and matching run

After 01/02 pass, propose two sequential Brush fits, A then B, each3,000 steps,
seed12345, same native resolution and matched settings. Limit each fit to30min,
1million Gaussians and12GiB process memory as an initial bound; actual hardware
requirements are unmeasured here. A limit failure is retained, not silently
fixed with fewer points or more time. Inspect masks, camera layout, fixed-view
background renders and bridges before registering either real proxy.

Run 04 on a known transformed/shuffled Brush copy before 05 estimates real
Brush B→A. Test both full and fixed partial overlap, plus an explicitly planar
ambiguity negative control. Freeze the one actual transform before scoring.
If real Brush registration fails, stop scientific transfer; a labeled rejected
diagnostic may be rendered but cannot count as a successful pipeline stage.

If it passes, compose `inverse(C_A) @ G @ C_B` and apply it to every B Gaussian
in both static and moving arrays. A remains byte-identical. Transform covariance
by `s² R Sigma Rᵀ`; keep opacity and DC unchanged. No Brush points enter the final
union. Retain all points and all valid source intervals, without consolidation,
person-only correction, local warp, appearance fitting or MoSca retraining.
See the protocol (historical reference: `docs/protocol.md`) for fixed gates and fair comparisons.

## Cost estimate and run limits

Preparation costs no cloud compute. A later execution is proposed, not currently
authorized, as one Linux on-demand Runpod GPU session: prefer A5000 if available,
otherwise a compatible GPU at<=US$.59/hour. These are planning ceilings based
on the preceding19 October session, not a live capacity quote. Recheck
https://www.runpod.io/pricing, region, stock and actual allocation rate at launch.
No current worker/region is selected. Both Vulkan Brush training and CUDA
BUFFER-X must pass device checks on that one worker.

Proposed resources:24–48GiB VRAM, >=32GiB host RAM, <=80GiB ephemeral disk,
zero paid persistent volume. Expected45–90min including setup, transfer, two
fits, controls and retrieval givesUS$.4425–.885 compute at$.59/hour. A two-hour
launch-relative cutoff gives<=US$1.18 compute, with$.82 reserved for disk,
transfer and other charges: proposedUS$2 allowance before tax. This is neither
a training runtime promise nor an account-wide spend cap. Inspect input gates
locally first; stop if published charges cannot fit the allowance.

One successful worker, A then B sequentially; no automatic second session or
larger/more expensive GPU. Reconcile any failed allocation by unique name before
one capacity retry. One compatibility repair per distinct setup error is allowed
within the same clock; no threshold/seed sweeps or changed data. Per registration
case600s; each local render batch600s/2GiB; no background endless retries.

Before allocation, arm a job-specific watchdog independent of SSH/model scripts.
Retain remote logs while running; retrieve/hash-verify evidence and terminate
promptly when fitting/inference ends, then finish scoring/publishing locally.
Verify Pod absence, remove job-specific ephemeral resources, identify any
retained storage, and report actual billed-use estimates separately from invoices.
Existing Docker applications, viewer4318 and historical resource states stay intact.

## Expected deliverable and unresolved prerequisites

Eight separately recorded outcomes distinguishing setup/readiness failure,
control failure, registration failure, successful coordinate transfer and actual
full-scene fusion. The first unresolved work is validated B background masks and
seed exclusions, explicit per-video bridges, and fixed-camera observability.
No measured result is claimed by this document. Lessons/next-steps stay empty
until execution. The proposed first work is01/02, not paid fitting.
