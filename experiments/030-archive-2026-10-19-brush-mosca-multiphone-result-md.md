> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/result.md`.
> Original SHA-256: `bb0a40cba3e8f16fdf6468c71ec9cab312e1543733207c44bf2262e198b16cb8`. Private media/logs are not included.

# Seven-scene test results

Follow-up: the whole-person partition experiment (historical reference: `whole-person-layer/result.md`)
now adds six separate matched outputs for two saved fits, restoring stationary
body parts and observers. This page retains the original seven-scene findings.

17 October 2026. **All seven scene sets were tested on the existing Runpod A40.**
Five fresh MoSca motion fits completed. The harness contains **14 outputs**:
five MoSca controls, five hybrid exports and four multi-view Brush backgrounds.
Exhibition and night fire have static-only results because their motion stages
failed. These are roughly three-second tests, not full-length reconstructions.

Open **http://localhost:4318**, refresh, and select
**Brush + MoSca · seven scene tests**. Pick the matching **MoSca control** and
**hybrid** outputs to compare them. Pause and drag to inspect another viewpoint;
then hold the camera and change the time. Earlier H1 results are preserved in
their original experiment entry.

## Per-scene outcomes

| Scene | Viewable results | Findings |
| --- | --- | --- |
| Day phones, easy (historical reference: `outdoor-day-phones-easy/test-result.json`) | MoSca control + lead-camera hybrid | Static registration failed. Performer motion is recognizable, but the hybrid loses mostly stationary phone operators and some body contributions. |
| Day phones, medium (historical reference: `outdoor-day-phones-medium/test-result.json`) | MoSca control + two-camera hybrid + Brush background | Two of five training phones contributed. Alignment passed at 2.76 px over only five withheld points; held-out camera localization failed. Background is coarse and people remain incomplete. |
| Day phones, hard (historical reference: `outdoor-day-phones-hard/test-result.json`) | MoSca control + lead-camera hybrid + three-camera Brush background | Static map used three of five training phones. Alignment remained outside the 3 px limit after one documented repair (6.33 px); the multi-view map is therefore separate. Ghosting and shifted-view tearing remain. |
| Indoor group conversation (historical reference: `indoor-group-conversation/test-result.json`) | MoSca control + lead-camera hybrid | Three people's movement is recognizable. Shared static registration and known-pose triangulation failed; the hybrid uses one camera's recovered context. Occlusion holes remain. |
| Indoor single person (historical reference: `indoor-panoptic-person/test-result.json`) | MoSca control + lead-camera hybrid | The full control retains the person. The hybrid loses the static head and much of the torso/legs while preserving moving arms. This exposes the foreground-partition defect directly. |
| Indoor exhibition (historical reference: `indoor-exhibition/test-result.json`) | Brush background, static only | Both training cameras registered, but motion resampling received an empty dynamic mask. The static Gaussian output is heavily blurred. |
| Outdoor night fire (historical reference: `outdoor-night-flames/test-result.json`) | Brush background, static only | Depth changes strongly with illumination. Stability filtering removed 486 of 500 candidate motion curves; 14 remained, and scaffold K=16 failed. The filter was not relaxed to manufacture a motion result. |

Every set reserves one camera. Its frames never fit geometry, motion or the
alignment. Frozen-map held-out localization succeeded for exhibition and night,
and failed for the two registered phone maps. Those PnP inlier residuals concern
localization, not independent image quality or full 3D accuracy.

## What this says about the selected approach

**Runpod works for actual Brush and MoSca fitting. The current hybrid does not
yet preserve complete people.** Brush excludes detected people, while our MoSca
foreground contains only its motion-selected component. Stationary bystanders
and stationary body parts can be discarded with MoSca's static layer. Pixel
mask precision alone does not fix that mismatch.

The native component renders make this visible without relying on the adapter:
the single-person static layer (historical reference: `../working/multiphone-tests/indoor-panoptic-person/lead/inspection/components/static-000.png`)
contains the head/torso/legs, while its
moving layer (historical reference: `../working/multiphone-tests/indoor-panoptic-person/lead/inspection/components/moving-000.png`)
contains mainly arms and fragments. The easy-phone static layer similarly
retains recording bystanders that disappear from the hybrid.

The first viewer export also thinned moving Gaussians too aggressively. That
was corrected without retraining: all moving Gaussians are retained in the five
final fitted cases. DC-only appearance and some control-background subsampling
still reduce native SH fidelity. Native fixed and shifted renders, full fitted
checkpoints and earlier export attempts remain under
`working/multiphone-tests/<scene>/`. Different inputs, background counts and
camera subsets prevent a matched quality benchmark.

Only medium motion produced a gate-passing multi-view-background hybrid, with
weak five-point validation. Four other hybrids use explicitly labelled
lead-camera context fallbacks. All motion fitting is monocular: **joint
simultaneous multi-phone motion fusion was not demonstrated**. Neither these
exports nor H1 establish a general quality advantage over MoSca alone.

## Verification and retention

All 14 outputs passed finite-field/hash checks and browser loading, orbit and
reset. The ten sequences additionally passed fixed-camera seeking, true final
snapshot selection, frozen-time orbit, rewind and play/pause. Background bytes
stay identical across time and moving geometry changes. Screenshots were
visually inspected separately; interaction checks do not certify reconstruction
accuracy. The harness's eight unit tests and configuration checks passed, and
all four original 900-frame source clips still verify unchanged.

The batch report (historical reference: `batch-report.json`), per-scene JSON reports,
environment pins (historical reference: `environment.json`), execution procedure (historical reference: `execution.md`),
lessons (historical reference: `lessons.md`) and next steps (historical reference: `next-steps.md`) retain measurements,
failures, provenance and limitations. Models, footage, screenshots, keys and
checkpoints remain ignored; only code and lightweight records belong in Git.

The Pod is idle and deliberately **left running**, as requested. Its watchdog
deadline is **17 October 2026, 14:28:28 Australia/Sydney**, under the US$4
allowance. The report records its verified status and elapsed-time compute
estimate; that estimate is not a provider invoice and excludes later retention,
disk charges and tax. The watchdog depends on this local host and API access.
