> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/11-fixed-world-appearance/results.md`.
> Original SHA-256: `728fb767db7cecfc207abdfcddd143ea58cc1f1726f21a3b23142926e51d24a5`. Private media/logs are not included.

# Full-interior fixed-world appearance results

Native appearance fitting and export completed for the original0–25.333s
Guildhall interior, including the16s turn. All305 source cameras remain exactly
unchanged. The exporter retains397,518 static and77,839 dynamic Gaussians:
475,357 points in each observed state, with all305 timestamps preserved.

Median native fitted-source PSNR is27.988dB; the worst observation is24.950dB.
The old153-observation long-interior attempt scored15.66dB median. This is a
descriptive comparison across different pipelines and exposure, not a controlled
attribution to one setting. The native renderer uses full learned SH colour on
white; the interactive viewer uses DC colour on black.

The original motion coverage gate **failed on87 frames** before scaffold
optimization. A separately declared exploratory arm produced133 finite scaffold
nodes and proceeded while preserving that failed result. The model cannot be
quality-promoted. Quiet intervals, distant people and weak tracks remain
ambiguous; source fit does not validate actor shape, identity or novel views.

One foreground initialization was rejected before any appearance optimizer
because dynamic assignments leaked onto architecture. Intersecting proposals
with existing visitor-box support reduced maximum foreground coverage from
25.17% to7.39%. The original protocol, rejected initialization and all pre-fit
amendments are preserved. There was only one actual appearance optimization.

The retained profile uses1,000 scaffold steps and25,417 appearance steps.
The successful scaffold stage took95.19s. Appearance took2,269.00s including
initialization and the manual review pause, with6,191MiB peak device memory;
native export took34.80s. No new camera BA, depth/flow inference, Brush fit,
edited-transition reconstruction or separate-outro training was performed.

See investigation (historical reference: `investigation.md`), lessons (historical reference: `lessons.md`),
recommended next steps (historical reference: `next-steps.md`) and the machine-readable evidence in
`docs/`. See verified closure and API preservation (historical reference: `docs/execution-results.json`),
export checks (historical reference: `docs/export-verification.json`), native source metrics (historical reference: `docs/guildhall-fixedworld-exploratory-scores.json`)
and visual review (historical reference: `docs/visual-review.json`).

The common8–11s overlap scores30.088dB median, +0.930dB against the fresh3s
reference; all predeclared source-appearance thresholds pass. Five full-span bin
medians are27.082,28.490,31.198,26.777 and29.380dB. The original full-motion
coverage gate remains failed, so the combined numeric result remains false.

Manual review found coherent observed room structure, softer people with
ghosting, turn-region blur and uncovered/smeared edges in a shifted final view.
This supports exploratory publication, not validated actor/novel-view fidelity.

Strict final retrieval verified4,668 files with zero pending. All305
exported RGB images and states are present; native hashes match retrieval and
all final camera tensors exactly match the qualified input bundle. The worker
is terminated and independently verified absent, with zero account Pods and no
new persistent/network volumes. Session estimateUS$1.7082;
cumulativeUS$6.4328 before tax, leavingUS$3.5672 ofUS$10.
These are conservative launch-relative compute/storage estimates, not invoices.

Published: http://localhost:4319/?run=mosca-20261028-fixedworld-exploratory .
The app has99 valid models; all98 prior API records and86 archive records remain
identical. The new result is labelled exploratory/sparse motion;12s remains the
longest passing duration trial. All305 observed states and475,357 points per
state are retained. Native checkpoints and media stay ignored outside Git.

Browser verification passes for the actual first/turn/final states, camera
translation with unchanged event time, seeking with unchanged translated view,
MP4 byte ranges and mobile layout. The older duration-card/navigation/playback
regression also passes. Final evidence (historical reference: `docs/final-verification.json`) combines
these checks with retrieval, native export and closure. Unit/syntax checks passed
for the app; screenshots and actual model media remain ignored locally.
