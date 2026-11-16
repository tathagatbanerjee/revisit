> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/mosca-dynamic/result.md`.
> Original SHA-256: `aa7d5f917a594f72b983aa77b375f156e44e808d20cc5ce1cdf4aa1a91d3df38`. Private media/logs are not included.

# MoSca bounded trial result

2026-10-14. **A short real-world video was fitted into a time-dependent Gaussian
scene, and time/viewpoint controls were inspected independently.** This is a
coarse capability demonstration with visible reconstruction errors, rather
than a validated forensic memory or a general solution for arbitrary footage.

Open **http://localhost:4318**, select **MoSca dynamic reconstruction**, then
**Guildhall moving visitors**. Pause and move the camera modestly; hold the view
and play or seek time. **Author duck control** is a separate supported example.

Source previews, served locally and retained outside Git:

- [Exact Guildhall test input](http://localhost:4318/clips/mosca-guildhall-input.mp4):
  prepared clip 8–11 s / original recording 58–61 s, 640×360, 12 fps. Acabashi /
  Wikimedia Commons, CC BY-SA 4.0; original source/attribution remain in the
  footage records. Input SHA-256:
  `af8be7089bdead75657f3f443213599aeb59af82a43193f66c432bd12db7c843`.
- [Author demo preview](http://localhost:4318/clips/mosca-duck-control-source.mp4):
  25 original frames at stride 2, displayed at nominal 10 Hz. Its capture rate,
  UTC and real-world capture status are not established. Private research demo.

The reconstruction clock is independent; these source videos are available
separately rather than automatically synchronized or attached to annotations.

## What was actually run

Pinned MoSca `02404d2841b4e0dc2d9074860950bce5da579656`, Metric3Dv2 small,
BootsTAPIR v2 and RAFT. Real estimated depth, optical flow and point tracks feed
camera solving, motion-scaffold optimization and Gaussian appearance fitting.
There is no Brush fitting, manually scripted actor motion, or SHARP frame bank
in this run. See the investigation (historical reference: `investigation.md`) for dependencies, component
terms, cost bounds and explicit source/profile repairs.

The final profile uses 512 uniform and 2,048 dynamic queries, 128-query chunks,
one-frame flow pairs, 2,000 camera-bundle steps, 1,000 scaffold steps and 3,000
appearance steps. The initial 512-query control failed the scaffold minimum;
its denser retry completed. Appearance fitting resumed from a completed motion
checkpoint after correcting an ignored upstream profile option. Guildhall's
completed model was retained after an optional FPS JPEG-writing failure; no
native FPS benchmark is claimed.

| Measurement | Duck control | Guildhall |
| --- | --- | --- |
| Native input | 25 frames, 854×480 | 36 frames, 640×360 |
| Native Gaussians | 229,155 | 232,566 |
| Static / dynamic Gaussians | 171,902 / 57,253 | 204,190 / 28,376 |
| Displayed Gaussians per state | 76,385, stride 3 | 77,522, stride 3 |
| Exported states | 20 | 20 |
| Replay endpoint | 2.4 s, nominal clock | 2.9167 s, derived capture clock |
| Preprocessing | Initial stage 98 s; denser native rerun reported 71 s internally | 82 s |
| Successful appearance / fitting command | 575 s appearance stage, including checkpoint/plot saving | 510 s camera/scaffold/appearance command; failed only after saving at optional FPS preview |
| Sampled peak device memory | 2,807 MiB appearance stage | 1,775 MiB fitting stage |
| Sampled peak process-tree RSS | 4.83 GiB appearance stage | 2.79 GiB fitting stage |

Clean installation on the final A10G worker took about 12.7 minutes. The full
session included earlier failed setup/controller attempts, inspection pauses,
repairs and artifact transfer. Fifteen-second sampling can miss short memory
peaks and RSS is not a unique whole-host memory measurement.

## Inspection and practical limits

Native checkpoint hashes were verified after retrieval. The checkpoints were
evaluated at 20 integer time states in one world. Native first/last renders used
the same fitted camera; a translated camera independently changed viewpoint.
The duck visibly moves across the fixed street view. Guildhall's visitors change
position while the monuments remain stable. New viewpoints expose parallax,
holes and poorly reconstructed surfaces.

The viewer displays true checkpoint-evaluated snapshots with native positions,
rotations, scales and time-dependent opacity. It uses only DC colour and a
consistent Gaussian index subsample, which reduce appearance fidelity. Full
native snapshots, checkpoints and higher-order-appearance reference renders
remain in ignored working/private storage. Snapshots hold until the next state;
there is no motion interpolation or independent per-frame alignment.

Browser inspection checked fixed-camera time seeking, frozen-time orbit,
rewinding from an alternate view, play/pause, camera preservation during playback
and a manually inferred annotation. Maximum camera-pose differences were below
`2e-15`. Guildhall's final frame was reached at its fractional endpoint; the
range control now permits fractional sequence times. These checks establish
interaction behavior, not geometric accuracy or desktop GPU performance.

Visible limitations include blurred/duplicated people, smeared surfaces and
missing coverage. Final 2,048-query dynamic tracking visibility was about 91% on the control
and 59% for Guildhall. Only 97 Guildhall
tracks were visible at both endpoints. Unseen trajectories/surfaces remain
estimates. Monocular scale and camera intrinsics are estimated; no source UTC,
calibrated metric accuracy, semantic object recognition or multi-video merging
is demonstrated.

## Records and follow-ups

- Lightweight native artifact report (historical reference: `artifact-report.json`)
- Lessons (historical reference: `lessons.md`), next steps (historical reference: `next-steps.md`)
- Native evidence: `working/mosca-dynamic/cloud-output/`
- Browser evidence: `working/mosca-dynamic/browser-duck-2/` and
  `working/mosca-dynamic/browser-guildhall/`
- Viewer models: ignored `output/runs/mosca-duck-control-20frames/` and
  `output/runs/mosca-guildhall-20frames/`

Cloud cost, retained storage and verified teardown are recorded in the final
execution section of the investigation and cleanup report (historical reference: `cleanup-report.json`).
All trial instances were terminated before replacements or final cleanup.
No trial compute, root disk, temporary worker role/profile, shutdown schedule or
security group remains. Private S3 artifacts and their versions remain retained.
