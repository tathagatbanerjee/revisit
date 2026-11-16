> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-prototype/result.md`.
> Original SHA-256: `746abe55ac96bb4a1a74693ef30e134b27bf342c92eebf7d7ce45251723830a1`. Private media/logs are not included.

# Integrated prototype result — 19 October 2026

The two cached independent reconstruction uploads run through one local job and
publish five comparisons. **The integrated merge is rejected; A and B remain
separate retained source assets.** No rejected candidate replaces either source.
See the machine-readable decision (historical reference: `docs/decision.json`).

| Stage | Result |
| --- | --- |
| Reconstruction ingestion | Two independent full MoSca cache hits;36 A /34 B frames; source-local clocks |
| Clock recovery | B→A offset+0.5005s, zero reference error,12.89% best-vs-second motion margin; actual PTS used |
| Room registration | Pass:8.10px /0.0737m-equivalent on six reserved identities |
| Person agreement | Fail:219.82px /1.352m-equivalent on20 seen observations excluded from room fit |
| Background consolidation |641 B static Gaussians removed only during overlap;0.170% reserved source-pixel gain, below2% |
| Local refinement |512 retained background B positions,30 Adam steps;0.00274% reserved gain, below2%; no colour/opacity edits |
| Overall decision | Rejected: person, consolidation and refinement gates fail; no promoted merged run |

The refinement now uses the actual full mid-clip scene, including all static and
moving Gaussian contributions. Its tiny benefit differs from the masked-background
component test, illustrating why full-context integration matters. Reserved pixels
are a checkerboard of seen source images, not independent camera evaluation.
Initial differentiable versus independent CPU renderer parity is below4.5e-9;
export scoring recomputes support and depth order. No tuning sweep or best-step
selection was used.

## Artifacts and source validity

All candidates share40 observed event states from0 to3.236567s. A has65,507 points
through2.9029s; B has62,380 from0.5005s onward. The raw overlap has127,887 points;
consolidated/refined overlap has127,246. A and B controls intentionally contain
zero points outside their observed source interval. Every A and moving B point
is retained. Only documented B static points can be deleted or position-updated.

Consolidation/refinement apply only when A and B are both active. B-only tail
restores all original B points and positions, avoiding deletion of a surface
whose A replacement is no longer active. That state transition can cause visible
pops; this prototype does not solve temporal blending. It does not extrapolate
A, retime motion to hide ghosts, or turn stationary people into permanent room
content.

All five runs use the same A and registered-B inspection cameras, black backfill
and DC rendering. New coordinates use A's native gauge; A's arrays are byte-identical
to its native exports, rather than the older viewer runs' author-world coordinates.
B gets one constant global similarity before overlap-only background edits.

The local job takes30.15s, peaks at842.77MiB RSS and preserves90 frozen inputs.
No new MoSca/Brush fit, checkpoint download, paid resource or fresh evaluation
image is used. Camera20 RGB stays sealed. Intermediate upload receipts, clock
candidates, transform, deletion indices, position deltas, stage journal and
refinement losses are retained in ignored `working/splat-fusion-prototype/`.
The model counts and per-frame hashes are in publication (historical reference: `docs/publication.json`).

This is a cached processing integration, not arbitrary raw-video upload support:
room matching and foreground exclusions use earlier calibrated studio evidence.
The same20 person observations were previously seen in another development
experiment. Passing the limited clock/room checks establishes no fresh-view
quality, generic phone synchronization or successful dynamic fusion.

## Checks and inspection

The exported200 snapshots are checked for exact source activity, shared cameras
and clock, native A byte preservation, full dynamic retention, documented B-only
static deletions/position edits, finite scales/rotations and refusal to promote a
failed merge. Source hashes remain unchanged. Ten viewer tests, source checks
and Compose validation pass. Browser inspection passes all five runs at five clock positions, both shared
views at the middle instant, additional refined motion/end states, playback/pause,
orbit and reset. Camera changes preserve time/model; no uncaught exceptions or
invalid run manifests. Captures wait eight rendered frames. Software rendering
is not a GPU performance benchmark. See browser checks (historical reference: `docs/browser-check.json`).

Actual browser captures of raw, consolidated and refined at1.5015s show two
separated people in both shared views and little visible difference between
stages. The side-by-side sheet is retained at
`working/splat-fusion-prototype/comparison.jpg`; no overall visual improvement
is promoted.
