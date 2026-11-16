# Revisit implementation plan

Prepared 16 November 2026. Owner: Tathagat Banerjee.
Status: proposed implementation; this initial publication is documentation only.
Project-owned code and documentation use the [MIT License](../LICENSE).

## Outcome

A new user can understand the idea, run a local demonstration, and then submit a
video from that same app using their own Runpod account. The result or a useful
failure report returns to the app, and owned cloud resources are cleaned up.

The defining interaction is independent event time and camera viewpoint. The
first supported reconstruction mode is static scene reconstruction, because that
is the tested engineering baseline. Short dynamic example playback is useful
immediately; reliable reconstruction of arbitrary moving people is not a promise.
New-video dynamic fitting is an experimental, separately gated capability.

## User journey and timing goals

| Step | User sees/does | Release target and evidence |
| --- | --- | --- |
| Understand | README with one demonstration, capabilities, limitations and two starting paths | Understand purpose in 2–3 minutes; validate with a new reader |
| Try locally | Follow one documented startup command, open app, pause/move/replay an example | 5–10 minutes after prerequisites; target, not yet measured |
| Test local installation | Run a local diagnostic that validates files and exercises a small example without a cloud key | No paid allocation; actionable error messages |
| Prepare video | Choose/upload file to localhost, select continuous interval, inspect suitability report | Local checks complete or fail before a paid worker is allocated |
| Connect compute | Supply personal API key, verify access, configure a scoped SSH identity | 5–15 minutes after account/billing readiness; target only |
| Run | Review current quote/allowance/deadline, start job, follow stages | GPU availability/network/cold setup affect elapsed time |
| Inspect | Open downloaded scene or read exact failure; see cleanup status | All files verified before success; independent termination verification |

Historical required GPU stages for three tested 30-second static cases took
about 25–30 minutes; upload, cold setup, review and retrieval were additional.
Allow roughly 1–2 hours for an initial attempt as a planning estimate, not an SLA
or a success guarantee. Measure fresh public-user setup before advertising those
targets as achieved. Do not reuse historical GPU prices as current quotes.

## Scope of the first usable release

Include static Gaussian scene viewing, timestamped sequence playback, recorded
camera reset, orbit/pan/translation, local imports, guided sample exploration,
video preparation, bounded Runpod jobs, stage diagnostics, artifact download and
verified worker termination. Include research history, failed results and clear
experimental labels.

Defer general multi-phone synchronization/merging, generative hidden-surface
completion, arbitrary native dynamic checkpoints, long-duration scaling, hosted
accounts, shared cloud credentials and a broad cloud orchestration platform.
Playback of exported observations holds the nearest preceding state; do not
silently invent continuous deformation or interpolate capture clocks.

## Proposed architecture

The local app runs a browser UI plus a loopback-only backend. Use a pinned Node
LTS release for the web service and a pinned Python environment for preparation
and job execution. The existing Three.js/Spark viewer is a starting point, not a
reason to carry over all historical panels. Check dependency terms before reuse.

The backend owns local video uploads, project storage, credential access and job
control. The browser never calls Runpod directly or stores provider keys. Run CPU
preparation and remote transport in worker processes so uploads/status pages
remain responsive. Persist job metadata, stage receipts and artifact hashes on
local disk, separate from tracked source.

A provider adapter encapsulates account checks, current offers, worker creation,
SSH readiness, transfer, termination and absence verification. A pinned worker
image/setup receipt encapsulates GPU dependencies, source patches and preflight.
Treat it as a replaceable backend with explicit upstream licensing boundaries.

Conceptual flow:

```text
browser -> localhost API -> local preparation and persisted job controller
                                |
                       Runpod provider adapter
                                |
                 one owned worker + shutdown watchdog
                                |
                  verified artifacts -> local viewer
```

Proposed layout, to be created during implementation:

```text
README.md / LICENSE / THIRD_PARTY_NOTICES.md
app/                   local web service and browser viewer
runner/                preparation, job state machine and provider adapter
worker/                pinned setup/image recipe and inference adapters
schemas/               video project, job, experiment and result contracts
examples/              generator, manifests and cleared sample acquisition
experiments/            portable result cards and reviewed evidence
scripts/               doctor, sample acquisition and release checks
site-docs/             optional later rendered documentation; not needed for MVP
docs/                  quick start, capture guide, Runpod, results, troubleshooting
tests/                 local integration, failure and lifecycle tests
.github/workflows/     credential-free CI
```

Local data/credentials/caches are ignored and kept outside distribution artifacts.
Use a distinct local port, proposed 4320, and Compose project `revisit` so existing
research viewers remain undisturbed. Docker is the primary reproducible startup
route; native development instructions are secondary. Bind to127.0.0.1 by default.
The GPU worker is separate; no CUDA requirement for basic local viewing.

## Phase 0 — documentation, provenance and a clean boundary

Deliver README, this plan, experiment history, MIT license and asset policy. Build
an allowlisted migration manifest for later code extraction; never push the old
monorepo/history or ignored working trees wholesale. Retain original notices on
adapted components and identify patches. Audit backend source/weight/renderer
terms before distributing an image or derivative asset.

Migrate the history into durable experiment cards. Each has an ID, question,
status, parent/control IDs, source interval, capture/frame clocks, settings,
measurements, failed gates, visual defects, conclusion and evidence references.
Separate family/attempt/export IDs so counts are meaningful. Include plans marked
NOT RUN. Make every public link resolve within Revisit or to an accessible source;
private/local evidence is explicitly unavailable rather than a broken link.

Acceptance:

- Fresh visitor can find the purpose, current implementation status and limitations.
- No credentials, machine paths, cloud session state, SDK, media or checkpoints
  enter the public tree/history.
- Every imported component has provenance; unavailable/restricted items are listed.
- The experiment ledger retains failure and stops, including stale status correction.

The initial docs publication completes only part of phase 0. Code/image/asset
provenance review remains before their migration.

## Phase 1 — portable local viewer and zero-cost test

Extract the useful viewer into an independent project. Support static PLY and a
versioned timestamped sequence manifest, preserving all source observations.
Validate relative paths, hashes, finite/increasing timestamps, camera intrinsics,
poses, coordinate conventions, duration and file availability.

Provide a small procedural splat sequence labelled SYNTHETIC / INTERACTION TEST.
Prepare a separate real sample pack only after permission review. Sample manifests
include origin, allowed uses, hashes, download size, point counts, observed times
and known defects. Do not claim that the real-pack experience is complete until
users can actually acquire it.

Add pause/play/seek, keyboard and touch/button camera movement, orbit/pan, recorded
view selection, source reset and format/import errors. Keep viewport position
fixed while time changes. Handle slow loads and stale asynchronous requests;
dispose previous GPU resources. Native full-SH images and DC browser appearance
need distinct labels if comparison media is later added.

Acceptance:

- A fresh clone on documented supported hosts starts with one documented command.
- No Runpod key or local historical folder is required to render the synthetic test.
- A browser test freezes time, moves camera, changes time and verifies pose retention.
- Missing models, failed downloads and lack of WebGL2 produce useful messages.
- Sequence changes do not leak GPU memory or flash a stale frame after reselection.
- Linux and one supported desktop Docker environment are exercised and recorded;
  don't advertise untested OS support. Measure first-install and repeat-start time.

## Phase 2 — upload and local video preparation

Implement project creation, streamed upload to backend-controlled storage,
continuous-interval selection, thumbnails and a preparation report. Validate size,
container/codec, decode completeness, duration and sampling. Detect likely edits
as warnings for explicit interval review, not proof of scene continuity.

Preserve original bytes and actual frame presentation timestamps; store source
hash, selected interval, image transforms, sample identities and effective config.
Use a pinned CPU preparation image/environment for ffmpeg, COLMAP/pycolmap,
NumPy/OpenCV and optional person masking. Eliminate archived virtual-environment
paths. Avoid distorting non-16:9 inputs: specify and test a documented crop/resize
policy and its effect on intrinsics.

Start with tested static baseline settings: at most 30s,640×360,12Hz and the fixed
camera/scale-only recipe. Not every shorter/aspect-ratio input has been validated;
unsupported cases must fail clearly until qualified. Keep source, priors and map
review receipts; do not replace mandatory reviews with synthetic success markers.

Acceptance:

- A user can prepare their own suitable video entirely through the UI.
- A bad/cut/undecodable/insufficient-coverage clip stops before GPU allocation.
- Original timestamps and camera conventions survive extraction and reload.
- Mapping failure returns a report and useful capture advice; reruns get new IDs.
- Upload paths, filenames and invoked commands cannot escape the project directory.
- Cancelling preparation stops owned processes and retains an intelligible status.

## Phase 3 — portable reconstruction worker

Extract only the validated static stages and project-owned fixes. Resolve source
and weights from declared, pinned origins with hashes and license information;
no unpublished source tarball or archived cache may be required by a fresh user.
Preserve depth validity, observed-anchor coverage and exact camera locks.

Build a documented pinned GPU setup/image recipe, with platform/driver
requirements and native forward/backward/rasterization preflight. Download
weights lawfully on demand or use user-supplied locations where needed. Avoid
shipping upstream material without redistribution permission. Cold installation
and model downloads must have visible progress and bounded setup failure.

Standardize stage inputs/outputs, logs, checkpoints and receipts. Keep the
historical 30k static schedule initially; optimizations need separate measured
trials. Export exact source clocks, Gaussian counts and display colour convention.

Acceptance:

- Setup is reproducible from public/project-owned inputs plus documented external
  prerequisites, without access to the old workspace.
- Source pins, patches and native math checks are recorded before fitting.
- A failed geometry gate cannot launch appearance, even after restart.
- All selected observations/model tensors are finite and camera locks survive loads.
- Failure reports distinguish dependency, prior, geometry, fitting and export errors.

## Phase 4 — Runpod connection and durable job lifecycle

Add a local setup flow that checks API access without creating a worker. Use
server-side environment variables or an OS-backed secret store; do not persist
keys in browser storage, logs, tracked config, examples or result manifests.
Generate a dedicated SSH identity or accept a user-selected identity through the
backend. Mount secrets read-only when needed; remote workers receive only what
the job needs, not the user's provider control key.

Use supported Runpod APIs verified against current documentation at implementation
time. Replace historical data-center lists, GPU rates, shared SSH paths, budget IDs
and session assumptions with explicit per-user configuration and per-job state.
Select a compatible worker only after showing current availability/rate and the
user's chosen allowance/runtime. Provider billing/account charges are not an
application-enforced guaranteed currency cap; termination and estimates have limits.

Use one owned worker per initial job. Persist resource ID and ownership metadata
before further setup, reconcile uncertain creation before retrying, and never
terminate unrelated account resources. Use bounded checksummed transfer,
readiness retries and an exclusive GPU-stage lock. No silent expensive fallback.

Implement a job state machine: NEW -> PREPARING -> READY -> ALLOCATING -> SETUP
-> PRIORS -> GEOMETRY -> REVIEW -> FITTING -> EXPORTING -> RETRIEVING -> CLEANUP
-> SUCCEEDED; failures/cancellation enter CLEANUP and finish FAILED/CANCELLED only
with explicit resource status. Extra priors/source reviews occur at their required
stages. A REVIEW_REQUIRED state survives app restart; deadlines still apply.

Use a worker-side deadline plus an independent external termination mechanism.
A local watchdog alone is insufficient if the laptop closes. Verify which
provider-side or independently hosted mechanism is feasible and test it. Until
independent cleanup is qualified, block unattended execution and label that limit.
A worker's process shutdown is not proof that billable resources disappeared.

Acceptance with a fake provider:

- Authentication checks allocate nothing; keys are redacted throughout.
- Timeouts and uncertain responses cannot create duplicate untracked workers.
- Cancellation, worker loss, app crash/restart, failed setup, stalled upload,
  failed fit and failed download enter appropriate recovery/cleanup paths.
- Termination is idempotent; provider absence is checked independently and failed
  checks remain visible/retried. Completion never hides a live resource.
- User can list/reconcile owned jobs and explicitly retry cleanup after restart.

A paid real-provider validation requires a separately declared budget/runtime.
Publishing this plan does not launch or authorize any billed trial.

## Phase 5 — complete static upload-to-result journey

Connect the UI, preparation runner and provider lifecycle. Show stage names,
progress/last activity, elapsed time, estimated spend, log excerpts and explicit
review actions for source/priors/geometry. Precomputed numeric gates can stop a
job; passing numbers do not silently count as visual approval.

Retrieve required artifacts before normal termination, verify all hashes and only
then publish a local result card. Emergency deadlines/cancellation still terminate
a worker even if some artifacts remain unavailable; report partial retrieval.
A result card links source/native comparisons where available, recorded cameras,
known defects and failed checks. Rejected outputs cannot replace accepted sources.

Record separate outcomes: reconstruction result, retrieval completeness and cloud
cleanup. A model can be viewable while cleanup is unresolved, but the job cannot
claim clean completion in that state. Provide resume/recovery instructions without
claiming exact training resume from a model-only checkpoint.

Acceptance:

- From a fresh clone and personal credentials, a new user can submit a suitable
  video, perform required reviews, retrieve it and navigate the result.
- One reference static run and one genuinely new-video static run complete under
  explicit bounded validation allocations; capture full cold-start timings.
- At least one intentionally unsuitable input fails before rental.
- One exercised remote failure/cancel path demonstrably terminates the owned worker.
- Documentation matches actual UI/commands; there are no hidden manual environment
  repairs, local paths, credentials, source archives or pre-existing checkpoints.

This is the first release that can advertise the intended personal-video journey.

## Phase 6 — experimental motion and release polish

Expose existing short dynamic example playback from phase 1 separately from
new-video dynamic reconstruction. Add motion/foreground stages only after the
static path is qualified. Declare motion-support intervals before fitting and
retain failed coverage, including the historical 87-frame and116/120-frame failures.
Never relabel a static fit or camera animation as reconstructed motion.

Keep failed gates strict. An exploratory override, if offered later, must be an
explicit new candidate retaining the failure and its scope. It is not a default
fallback. Do not promise general dynamic fitting based on the old single-scene
exploratory result. Qualify any new dynamic recipe through its own funded trial.

Finish accessible/responsive UI, empty/error states, capture guidance, demo media,
troubleshooting, contributor/result-card templates, issue templates and tagged
releases. Add a license/notice inventory for exactly the code and assets shipped.

Acceptance:

- Experimental labels remain visible in mode selection, job and result screens.
- Motion failure prevents normal appearance launch; no empty-success export.
- Published demo/claims identify source interval, sampling and actual limitations.
- A novice can follow both starting paths without reading the historical archive.

## Testing and CI

Use fixture-driven contract tests for timestamps/coordinate conversions and
manifest validation. Exercise realistic upload/preparation failure cases and
provider lifecycle races with a fake service. Browser-test actual splat loading,
pose retention while seeking, stale-load handling, imports and errors.

CI needs no Runpod credentials and creates no paid resources. Keep an opt-in,
separately budgeted live-provider procedure outside automatic pull-request CI.
Use public-safe synthetic fixtures in tests; historical camera20 remains sealed.
Check dependency/image pins, public links, release file allowlists and secret
exclusion. Run a fresh-checkout/container rehearsal, not just tests inside the
original developer environment. Record what was actually tested.

## Delivery order and completion definition

Use small reviewable changes: documentation/license/history; local viewer/sample;
video preparation; portable worker; provider lifecycle; integrated static run;
experimental motion and polish. Preparation and provider work can proceed once
their contracts are frozen; live integration follows both. Do not publish quick
start commands or success claims until they work from the public repository.

The core release is complete when a fresh user can understand the idea, try a
real cleared example, submit a suitable personal video with their own credentials,
inspect the result or useful failure, and verify that compute is gone. The targets
must be measured. If the backend or real assets cannot be cleared, publish the
viewer/docs honestly but do not claim the complete reconstruction journey.
