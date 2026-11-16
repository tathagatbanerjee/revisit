> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-static/result.md`.
> Original SHA-256: `3e83d2e0b8aa1ada33cceb2e00a6d229e8ceb521cfaa1afd1198563f49c2b002`. Private media/logs are not included.

# Brush first trial: result

Completed 2026-10-14. **Viable for multi-view static inspection.** The real
sculpture video produced one Gaussian scene that loads in our existing viewer
and supports much larger viewpoint changes than our bounded SHARP mode.
It does not reconstruct moving events through time.

Open **http://localhost:4318**, reload if already open, select **Brush static
reconstruction**, then its sculpture output. Drag to orbit, scroll to zoom,
right-drag to pan; reset restores the recorded camera at clip 5 s. Manual
markers and annotation export remain available. The source-video timeline
changes the evidence video, while the reconstructed geometry stays static.

## What ran

| Stage | Measured result |
| --- | --- |
| Input | 60 timestamped PNGs, clip indices 0–885 in steps of 15 |
| Cameras | COLMAP 3.7, CPU features/exhaustive matching/incremental mapper |
| Registration | 60/60 views in one coherent component |
| Sparse model | 18,309 points; mean reprojection error 0.5854 px |
| Feature extraction | 45.57 s |
| Matching | 528.19 s |
| Mapping | 47.79 s |
| Undistortion | 15.60 s; prepared images 1280×719 |
| Fitting | Brush v0.3.0, Tesla T4, Vulkan, seed 42 |
| Split | 54 fitting views / 6 evaluation views |
| Smoke | 2,000 steps, 63.13 s; 23,546 Gaussians |
| Main | Fresh 10,000 steps, 318.82 s; growth stopped at 5,000 |
| Final export | 111,906 Gaussians, 26,411,367 bytes (25.19 MiB) |
| Main evaluation | Mean PSNR 27.1295 dB / SSIM 0.8652 across 6 reserved views |
| Sampled GPU peak | 1,149 MiB, sampled every 5 s |
| Main process RSS peak | 845,652 KiB, approximately 0.81 GiB |

The one-million-splat ceiling was not reached. These memory measurements apply
to this small static dataset and configuration, not larger scenes or 4D methods.
CLI fitting times include loading, evaluations and exports. Camera preparation,
worker boot/installations and setup corrections are additional.

Frame 150 (clip 5 s, original recording 10 s) is among the evaluation images.
It was excluded from Gaussian image fitting, but included in COLMAP camera
estimation and sparse initialization. The metrics are therefore a reserved-view
rendering check, not an entirely independent geometric benchmark.

## What inspection showed

The front reference view reproduces the lettering, its thickness and openings,
ground, building and shadows. A substantial sideways orbit in the browser
reveals a recognizable solid object and useful parallax. Native reserved-view
renders also reproduce the reverse side seen later in the recording. This
establishes useful spatial coverage beyond one predicted camera image.

Lettering became substantially clearer between 2,000 and 10,000 steps.
Trees/backgrounds still contain elongated splats and floaters; ground and wall
textures are smoothed or streaked, and some thin edges are imperfect. High,
low, very close or unrecorded viewpoints remain weakly constrained. This is
not a complete surveyed model of the square.

SHARP's front view remains a useful visual baseline and can look sharper in
some regions. Brush's main benefit here is combining observed sides into one
shared scene. A source-view comparison does not establish a universal quality
winner: SHARP used an uncalibrated 30 mm focal assumption, while COLMAP fitted
889.07 px at original 1920-pixel width. Scale is arbitrary for Brush; do not
compare its movement distances with SHARP's nominal metres directly.

## Viewer validation

The harness now accepts a static `inspectionCamera` with full pinhole
intrinsics and a world-space pose. This leaves orbit/zoom/pan available.
Original COLMAP poses and the display conversion are preserved. The navigation
focus is estimated from the camera-trajectory centroid; it is not a measurement
of the object's physical center.

Real-output browser checks verified model loading/count, source seeking,
orbit, zoom, pan, marker creation, static representation while seeking the
video, and source reset. Reset camera position, orientation, target and
projection matched exactly (maximum numeric difference 0).

The first screenshot-only reset threshold of 0.5 mean channel values failed:
image variation was about 1.05 despite exactly identical camera/projection
state, including after a settling delay. We used exact pose equality as the
primary reset check and a secondary image tolerance of 2/255 mean channel
values. This records renderer-dependent variation rather than hiding pose
drift. Headless SwiftShader screenshots are not a normal desktop GPU speed
benchmark. Existing UI regressions and 8 server tests also passed.

## Cost and cleanup

All three sequential T4 workers are terminated. Their EBS volumes, temporary
roles/profiles, security groups and termination schedules are gone, independently
verified. The first two exited before Gaussian fitting due to runner setup
issues; the third reused the checked camera dataset and completed both fits.
No worker upgrade or additional clip was run. Every attempt retained the
original four-hour deadline and US$5 allowance.

At US$0.684/hour, summing launch-to-cleanup time for all workers gives a
**conservative compute estimate of US$0.6321**, not an invoice. It includes
shutdown waiting that AWS may not bill as running compute. Storage, IPv4,
requests, download transfer and tax are separate.

Private job storage retains 1,886,859,866 bytes across 546 object versions,
including inputs, the prepared dataset, periodic exports, renders and logs.
Sydney S3 Standard's first tier was rechecked at US$0.025/GB-month on
2026-10-14 (catalog effective 2026-10-01): roughly US$0.05/month for that
retention, plus the separately published inspected run. Versioned storage
needs review if repeatedly generating trials; deleting a current object alone
does not remove old versions.

[Official regional S3 catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/ap-southeast-2/index.csv).
See AWS trial verification (historical reference: `../../infrastructure/aws/brush-first-trial.json`)
for the selected jobs, resource checks and compute estimate.

## Artifacts and follow-up

The local ignored run is
`output/runs/brush-01-sculpture-orbit-60views-10000steps/`. It contains the real
PLY, run manifest, camera/provenance records, resource logs, preparation
measurements, native reference renders and browser inspection images.
Native cloud artifacts remain under `jobs/gsplat-brush-20261014-030905/output/`;
prepared-camera provenance comes from `jobs/gsplat-brush-20261014-024942/output/`.
The normalized inspected run is published privately under its `runs/` prefix.

See lessons (historical reference: `lessons.md`) and next steps (historical reference: `next-steps.md`). Do not launch a
longer fit or another package merely because this first trial worked.
