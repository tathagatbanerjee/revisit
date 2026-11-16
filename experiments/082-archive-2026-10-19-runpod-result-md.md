> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/runpod/result.md`.
> Original SHA-256: `605d0b8322be8845f074690372189c4dfb1a4ed2d464d56870f865a77ea6fa00`. Private media/logs are not included.

# Runpod A40 compatibility result

17 October 2026. **Runpod supports the tested Brush fit and native MoSca
rendering/export path.** The A40 Pod remains running at the user's request for
further testing, with the two-hour launch-relative watchdog still active. Use
Runpod for the next bounded experiment; retain AWS as the demonstrated fallback.

The live Pod is `m420vthqzdx8h0`, Secure Cloud in `EU-SE-1`, at US$0.59/hour.
It has one A40 (48 GB nominal VRAM; 46,068 MiB reported), nine allocated vCPUs,
50 GB allocated RAM and an 80 GB container disk. No persistent/network volume
was created. The host's `free` output exposes host memory and must not be read
as this Pod's RAM allocation. Driver: 580.126.20. The image is pinned by digest
in the investigation (historical reference: `investigation.md`).

## Checks that passed

| Check | Actual result |
| --- | --- |
| SSH and file transfer | Public TCP SSH authenticated using the dedicated local key; host key retained |
| CUDA | PyTorch 2.1.0+cu118 matrix forward/backward on the A40 |
| Vulkan | NVIDIA discrete A40 adapter available; GPU utilization observed during Brush fitting |
| Brush masked smoke | Released v0.3.0, exact reviewed H1 dataset, 20 steps; 4.52 seconds |
| Brush full baseline | Same data/cameras/masks, seed and 3,000-step schedule; 20.75 seconds; 9,817 Gaussians |
| MoSca CUDA extensions | simple-knn and both native rasterizer variants compiled and imported |
| Native numerical checks | PyTorch3D CUDA KNN backward, simple-knn CUDA distances, visible Gaussian rasterization and nonzero position gradients |
| MoSca modules | Preprocessing and reconstruction modules imported successfully |
| Real MoSca checkpoint | Original Guildhall checkpoint evaluated on A40 at 20 states; native fixed/alternate-view renders saved |
| Hybrid playback | 20 states, 24,005 displayed Gaussians each, 2.9167-second endpoint; browser checks passed |

Brush's maximum process RSS was 487,984 KiB for the 3,000-step command. A
15-second GPU sample during fitting showed 360 MiB / 66% utilization; sampling
can miss peaks. The earlier AWS precise-mask fit took 22.93 seconds on A10G.
This single repeat suggests similar fitting speed at a lower hourly price; it
is not a controlled hardware benchmark or a guarantee for larger scenes.

## What was inspected

Open http://localhost:4318, select **Brush + MoSca hybrid scene**, then
**Runpod A40 · precise-mask Brush + MoSca hybrid**. An untouched native Brush
background export is separately selectable. Existing H1 results were preserved.

Native and browser renders retain the recognizable monument, visitors and room
layout. The hybrid still has coarse floor/lower geometry and motion artifacts;
changing providers has not solved those reconstruction limitations. The new
background differs slightly in primitive count from the AWS fit, as can occur
when fitting on another device. No quality superiority is claimed.

All transferred model hashes were checked against the remote artifacts. The
three checkpoint hashes match the retained AWS checkpoints. All published
Gaussian fields are finite; background bytes are identical across the 20
states, while the moving component changes. Camera drift in browser checks was
zero. Checks covered frozen-time orbit, fixed-view seeking, alternate-view
rewind, play/pause, actual final-state loading and a manual inferred annotation.
Headless software rendering establishes interaction behavior, not laptop GPU
performance or calibrated geometric accuracy.

**MoSca motion was trained previously on AWS.** This trial tested its native
rendering, gradients, dependencies and checkpoint evaluation on Runpod. It did
not rerun depth/flow/tracking priors or fit a new dynamic sequence. A fresh MoSca
fit and joint multi-phone motion reconstruction are still untested here.

## Setup repairs and retention

The base image lacked `/usr/bin/time`; the first Brush command stopped before
fitting. Installing the utility and restarting on the same Pod resolved it.
CUDA's compiler existed but needed its path exported for noninteractive SSH.
MoSca reused the previously documented camera-stub repair. No replacement Pod
or destructive upstream installer was used.

A retrieval archive returned a tar warning because the GPU log/output directory
changed during capture. The downloaded gzip CRC and all stable model hashes
were verified; the completed import log was retrieved separately. This was not
a reconstruction or transfer-corruption failure.

Logs, models, native wheels, environment versions, screenshots and input hashes
remain in ignored `runpod/working/`. Viewer artifacts remain in ignored
`output/runs/runpod-a40-*`. The lightweight report (historical reference: `trial-report.json`) records
verification results. Credentials and media are absent from Git.

## Running cost and cutoff

Compute during the roughly twelve-minute setup/inspection was around US$0.12,
an estimate rather than an invoice. The Pod continues to accrue US$0.59/hour
plus disk while it remains active. The original US$2 allowance and two-hour
cutoff remain in force. A separate local watchdog is active and will terminate
only this trial Pod at **12:12:54 pm Australia/Sydney on 17 October 2026**.
Its ability to enforce that deadline depends on this local host and Runpod's
API remaining reachable. This is not a provider-enforced spending cap.

The user explicitly requested keeping a compatible Pod running for testing, so
no early teardown was performed. Query live state with `python3 runpod/trial.py
status`; use its scoped `terminate` action when finished. Verify Pod absence and
storage cleanup at that time; no cleanup success is claimed while it is running.
