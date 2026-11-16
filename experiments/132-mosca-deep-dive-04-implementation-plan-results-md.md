> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/04-implementation-plan/results.md`.
> Original SHA-256: `fce5bed9a0835e167d92f3f631d54910ceb986216fa01463bcecfcf40965b086`. Private media/logs are not included.

# Execution results —28 October2026

The A40 environment works reproducibly. Model changes are **content dependent**:
large depth improved Guildhall fitted-view PSNR by1.282dB, reduced the studio
score by0.574dB, and failed duck's3D curve refiltering. Keep small-depth/BootsTAPIR
as the general control; large Metric3D with BootsTAPIR is a promising
**Guildhall-specific** candidate. CoTracker3 worked through the adapter but did
not improve Guildhall's whole-frame scores under these fixed downstream settings.

Nine fits were attempted: eight completed and were published; one failed before
appearance training. This includes the additional same-worker shared-query
qualification allowed by the plan. The first historical reproduction is separate
from the eight-row model screen below.

## Measured screen

V00=Metric3D-small+BootsTAPIR-v2; V10=Metric3D-large+BootsTAPIR-v2;
V01=small+CoTracker3-scaled-online; V11=large+CoTracker3.

| Scene | Recipe | Median native PSNR(dB) | Change from scene V00 | Gaussians/state |
| --- | --- | ---: | ---: | ---: |
| guildhall | V00 | 29.657 | — | 233,656 |
| guildhall | V10 | 30.939 | +1.282 | 237,584 |
| guildhall | V01 | 28.978 | -0.679 | 224,663 |
| guildhall | V11 | 30.319 | +0.662 | 232,503 |
| panoptic00 | V00 | 33.848 | — | 65,175 |
| panoptic00 | V10 | 33.275 | -0.574 | 62,253 |
| duck | V00 | 24.215 | — | 233,257 |
| duck | V10 | Failed before appearance fit | — | — |

Scores use full learned SH, the same white native-render background and
**training/source views**. The same-worker baseline matches the first reproduced
control:29.657dB versus29.643dB; the historical checkpoint scores29.253dB with
the same renderer. Absolute scores across different scenes are not directly
comparable. These are not independent novel-view evaluations.

Profiles held seed12345,512 uniform/2048 dynamic queries, query chunks128,
RAFT-things,2,000 bundle steps,1,000 scaffold steps and3,000 appearance steps
fixed. Trackers share exact query positions and identities; RGB hashes are
checked. The eight-row matrix ran sequentially on one A40 worker. See the
frozen protocol (historical reference: `exploratory-protocol.md`), selection (historical reference: `docs/frozen-selection.json`)
and machine-readable results (historical reference: `docs/execution-results.json`).

## Why the duck arm failed

Large-depth duck had finite depth and valid2D tracks. Its queries, track
coordinates and visibility arrays are **identical** to the successful small-depth
duck run. The divergence occurs after depth/camera lifting and3D refiltering:
small depth retained57 of1,742 candidate dynamic curves after the minimum-slot
filter; large depth retained0 of1,761. The latter then crashed when a debug
renderer received an empty point set. Skipping that renderer would not restore
the missing scaffold.

This narrows the problem to the depth/camera/3D-filter interaction, rather than
GPU capacity or different2D tracking. The exact causal split is unresolved.
No filter threshold, recipe or optimization budget was retuned after failure.
Failed inputs, camera bundle, logs and receipts are retained. See
failure diagnosis (historical reference: `docs/duck-failure-diagnosis.json`).

Studio snapshots retain ghosting around fast-moving hands; larger depth has not
removed it. Guildhall shifted views retain railing/disocclusion artifacts.
The duck baseline also has visible deformation artifacts. No result is promoted
as a validated quality winner.

## Artifacts and cost

The app at http://localhost:4319 has94 valid runs: all86 archived runs with
identical API metadata, plus eight new full-density results. The failed duck arm
has no empty substitute. Every static/dynamic Gaussian is retained at each
exported observation. Native full-SH RGB/checkpoints remain separate from the
DC browser exports.

Runtime evidence is under ignored `working/mosca-deep-dive/execution-20261028*/`;
published assets are in ignored `app/runs/`. Guildhall/Panoptic00 have36 observations
at640×360; duck has25 at854×480. Clocks stay distinct: prepared12Hz Guildhall,
actual source PTS for Panoptic00, nominal10Hz duck with unknown capture timing.
Snapshots hold between observations, including a nominal final sample slot.

The conservative total is **US$1.3373 before tax** against the acceptedUS$10
ceiling. It includes launch/setup, failed work, GPU idle and80GB ephemeral disk;
it is a lifetime/rate estimate, not an invoice. First session:US$0.2915;
matrix session:US$1.0458. Both Pods are terminated and independently verified
absent; the account has no Pods. Persistent/network volumes were not created.
Final matrix collection verified5,074 regular files with zero pending hashes.
See closure verification (historical reference: `docs/final-resource-verification.json`).

## Limits and next work

Actual CUDA gradients, native KNN/rasterization, both depth models and both
trackers were exercised. Query/time contracts, immutable inputs, separate
publication roots and verified teardown are implemented. The longer-video ladder
and alternative-GPU benchmark were not started.

Reviewed person masks/MAE/coverage, physical background anchors, independent
novel-view targets and paired-seed confirmation remain unavailable. The protocol
was classified as an exploratory screen before candidate fitting. Full quality
promotion stays false. Camera20 RGB remains sealed.

Next: diagnose the failed3D curve lift and measure region/geometry quality, then
run a bounded Guildhall duration test with the large-depth candidate and its
small-depth control. Avoid another blind full-length fit.
