> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/independent-mosca-fusion/result.md`.
> Original SHA-256: `7cf30b7fb0ce2cbb63a5a0b0b1955b1feb5be7d33145e84963a1f352dd87df5f`. Private media/logs are not included.

# Two independent full MoSca fits, then raw splat fusion

19 October 2026. A genuinely independent camera24 MoSca fit was completed and
merged with the saved camera00 MoSca fit. **The temporal composition works;
the raw geometric union is visibly ghosted and is not promoted as a better
reconstruction.** Both single-video controls and the failed union remain
inspectable. This is the user's proposed reconstruction-then-merge architecture,
without Brush, MASt3R point proposals or shared Gaussian refinement.

## Inputs and actual execution

Panoptic `171204_pose1_sample`, two fixed training cameras about 31.5 degrees
apart. A is the untouched monocular camera00 checkpoint, 36 native states from
0 to2.9029s. B is freshly trained on camera24 alone, 34 images from0.5005 to
3.236567s. Original input/checkpoint hashes are in input (historical reference: `docs/input.json`),
receipt (historical reference: `docs/input-receipt.json`) and source terms (historical reference: `docs/source.json`). Research/
noncommercial footage and derivatives stay private. No camera20 RGB was opened.

B uses the same pinned MoSca/small-Metric3D/BootSTAPIR/RAFT pipeline and 2000
camera/depth,1000 scaffold,3000 photometric steps. Preprocessing:65.43s;
independent fit including built-in evaluation:432.90s; all-state export:10.06s.
Preprocessing/fit sampled process-tree peaks were2.36/4.08GiB, whole-device GPU
memory peaks1811/1385MiB. Five-second sampling can miss peaks. These numbers
exclude worker setup and transfers. Stage receipts (historical reference: `docs/fit-status.json`).

All34 depth maps pass positive/finite checks;2035 of2048 motion tracks and all512
uniform tracks are visible in at least four frames. First/middle/final source
and depth sheets were inspected before fitting. Native full-SH source and nearby
shifted-camera renders were inspected after fitting. The moving hands remain
soft/ghosted even in individual source views.

A has47,139 static and18,368 moving splats; B has45,416 static and16,964 moving
splats. Every point is retained. Raw overlap has127,887 splats. All36 A and34 B
native states are evaluated from the fitted checkpoints;40 event states cover
the combined timeline, with30 overlapping samples. The original A checkpoint
hashes are unchanged. B never receives A images or geometry in its training loss.

## Alignment and appearance result

A fixed positive-scale similarity maps each fit into the supplied author world.
Rotation is anchored to its source camera orientation; scale and translation
use robust registration of native-rendered training anchor depths to existing
00/24 triangulated correspondences. AnchorIndex%5==2 is reserved for the same
loose15px readiness check. These training-camera points are previously seen and
include moving correspondences at matching instants; they are not a new
independent evaluation or exclusively static landmarks.

| Fit | Fit / validation points | Validation median maximum two-view residual | Gate |
| --- | --- | ---: | --- |
| A | 47 / 12 | 31.71 px | Fail |
| B | 39 / 10 | 37.89 px | Fail |

Alignment report (historical reference: `docs/alignment.json`) retains all residuals, positive observed
depths and the unselected unconstrained-similarity diagnostics. The selected
mapping fails; it is not proof that every possible registration must fail.
We did not relax the gate, introduce a depth-affine warp, or optimize shared
Gaussians to disguise the independent-fit result.

The models learned focal lengths452.06px(A) and316.65px(B), versus supplied
rectified fx544.45px and466.54px. This discrepancy plausibly contributes to
inconsistent shape/depth; a fixed-intrinsics rerun has not been performed, so
its causal contribution is not isolated.

Matched native and actual browser images show duplicate head/face and arm/body
contours and mismatched wall features in the union. The opposite fit alone also
shows missing coverage/distortion when viewed from the other source camera.
The union combines their coverage but does not reconcile the surfaces into a
single correct person/room. No improved quality or independent accuracy is claimed.

All shared-viewer comparisons use DC colour and black backfill. Native source
references retain learned SH; native nonempty matched-union references use white
backfill. The archived native render report incorrectly labels that default
black; corrected inspection notes (historical reference: `docs/render-inspection.json`) record the actual
setting and preserve the archive unchanged. Empty native controls are black.
No pixel-parity score between the two renderers is claimed; ghosting is visible
in both. Post-run correction (historical reference: `docs/post-run-corrections.json`).

## Timeline result

The paired overlap has **zero decoded-PTS discrepancy**. B genuinely begins
0.5005s later and extends0.333667s beyond A. The union changes from65,507 points
(A only), to127,887 (both), to62,380 (B only). Neither source contributes outside
its interval; empty controls are actual zero-point PLYs, not invented content.
This tests unequal intervals, not clock recovery from unknown phone recordings,
UTC synchronization, long-event scalability or inferred motion across gaps.

Both static and moving content from an expired clip are removed in this simple
control. A learned MoSca static component can contain stationary body parts, so
blindly persisting it across other times could preserve an old actor pose.
The test does not yet maintain one enriched permanent room across the whole
extended timeline. Source handoffs can change appearance/coverage abruptly.

## Verification and cleanup

Four geometry/interval tests pass. All120 published snapshots pass finite-field,
positive-scale, normalized-quaternion and hash checks. Each union equals the
byte-exact concatenation of its currently active A/B controls. Static prefixes
stay fixed, dynamic positions change, original A checkpoints and native source
files stay unchanged. Artifact check (historical reference: `docs/artifact-check.json`).

The browser passes all three model counts, empty inactive controls, first/middle/
final seeks, both recorded viewpoints, frozen-time orbit/reset, and playback/
pause. Screenshots wait eight rendered frames to avoid stale GPU images.
No uncaught page exceptions or invalid manifests. SwiftShader is not a hardware
performance benchmark. Browser check (historical reference: `docs/browser-check.json`). Viewer syntax,
ten harness tests and Compose configuration pass.

Retrieved archive118,453,384 bytes, SHA-256 verified; B's checkpoint hashes and
native copies match. All36 matched native images and source renders are local.
Retrieval (historical reference: `docs/retrieval.json`). The one A40 worker was terminated and the
account independently returned no Pods. No persistent volume was created.
Launch-attempt-to-termination22.81min gives an estimatedUS$0.228 before tax,
including ephemeral disk, not an invoice. Cleanup (historical reference: `docs/cleanup.json`) and
[provider billing basis](https://docs.runpod.io/pods/pricing). No extra fit,
worker or hybrid comparison followed.
