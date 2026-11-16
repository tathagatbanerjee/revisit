> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/background-seeds/investigation.md`.
> Original SHA-256: `329000ce298a9ffc8674128fa38bcf287a980ceefaeb31524a1c83a7e64893c3`. Private media/logs are not included.

# Background seed filtering

17 October 2026. The user locked in the MoSca quality baseline and corrected
hybrid development path, and requested further hybrid improvement. Test whether
initializing masked Brush with static-person points contributes to background
ghosts. The previous fallback seeded from all opaque static MoSca centers, even
though those include heads, bodies and observers excluded by the image masks.

## Bounded controlled attempt

Use the same single-person and easy-phone cases. Keep original images, masks,
camera poses, source clocks, semantic membership and dynamic checkpoints fixed.
Reconstruct the EXACT previous seed subsample, then remove its semantic static
person points. Do not resample other points or add new observations. Verify the
unfiltered points3D file is byte-identical to the original before fitting.
Fit one new Brush background per case using the same v0.3.0 executable, seed 42,
3,000 steps, resolution 640, growth stop 1,800 and maximum 1,000,000 splats.
Write separate datasets, fit directories and logs. Never overwrite a prior run.

Combine each new background with the unchanged corrected people layer. Compare
to the prior corrected hybrid and full MoSca control using matched DC appearance,
all points, source-camera first/final and a fixed small camera shift. Evaluate
RGB absolute error outside padded person masks, inside unpadded masks, and over
floor pixels (bottom 40% of the image, excluding padded people). Report per-frame
and mean values. These are fitted source views, not independent reconstruction
accuracy. No held-out camera enters fitting, partitioning or alignment.

Inspect actual renders before publishing. A cleaner source view cannot establish
novel-view geometry. If removing seeds reveals holes or worsens the scene, retain
the failed attempt and the old hybrid. No extra steps or mask/threshold tuning
are included. Keep both candidates for inspection rather than automatically
promoting the latest fit.

## Environment, cost and stop conditions

Reuse the pinned batch environment (historical reference: `../environment.json`) and compatible live
A40 Pod m420vthqzdx8h0. On 17 October at 13:08 Sydney, API confirms RUNNING at
US$0.59/hour and the existing watchdog heartbeat is fresh. No new service or
worker is needed. Confirm free space and idle GPU before fitting. Verify saved
membership/checkpoint/background hashes; transfer and verify new model/report
hashes before making local viewer outputs.

Expected two short fits plus rendering/retrieval: 5–20 minutes (~US$0.05–$0.20
compute), including uncertainty/setup on the already running Pod. Limit each
fit to 600 seconds and each whole case to 900 seconds. One implementation repair
for a software fault, no tuning retries or broader inputs. Retain the existing
**US$4 total allowance** and **17 October 2026 14:28:28 Sydney cutoff**, with no
extension. Fit must finish and results be retrieved before that deadline; the
independent watchdog remains active. Preserve the successful Pod within the
same cutoff as previously requested. Heavy private research outputs remain
ignored locally; commit only code, lightweight reports and documentation.

Deliver two honestly labelled new hybrid candidates with before/after/control
comparisons, actual browser time/view checks, recorded lessons and a decision
about whether seed filtering helps. Joint multi-phone motion is outside this
isolated background experiment.
