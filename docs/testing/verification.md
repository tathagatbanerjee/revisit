# Verification and limits — 16 November 2026

## Completed checks

- JavaScript syntax and22 Node tests: run timestamp/path contracts, manifest import
  without unrelated files, byte ranges, file confinement/symlink rejection,
  localhost origin/session checks, interrupted-state recovery, read-only credential
  verification, owned termination semantics and actual short/full360-state video extraction.
- Chromium software-WebGL smoke:113,648-Gaussian real Houseplant sample, camera
  translation,650-Gaussian synthetic sequence, seeking with exactly unchanged camera
  position, playback and390px mobile layout. See [receipt](browser-smoke.json).
- Guildhall main example: source video before viewer, full-density first/middle/final
  states (475,357 Gaussians), translation with event time unchanged and seeking
  with camera unchanged. See [Guildhall receipt](guildhall-smoke.json). Shared static
  bytes are identical across all 305 states; each assembled PLY is checked against
  its original export hash. Downloader tests cover deduplication, offline cache,
  corrupted data and lossless assembly. MP4 range requests pass.
- Docker image builds on Linux amd64; pinned CPU mapping dependencies install.
  Docker Compose config validates; app/doctor starts without a Runpod key.
- Five CPU camera/stage contract tests pass, including ordered identities,
  world scale, camera validity and review gates. The depth-validity patch preimage
  matches the pinned public MoSca file and its patched syntax parses.
- A real locally retained 30s sculpture clip completed local preparation, all 360
  camera recoveries and isolated worker handoff packaging in 160.323s, retaining
  at least 171 observed anchors/frame. See [receipt](local-preparation.json).
  This is CPU pipeline evidence, not a new fitted3D result or independent user test.
- Python source parses and bootstrap shell syntax validates. This does not prove
  migrated native/CUDA dependencies or GPU math work in Revisit.
- Intended public files and all reachable historical Git blobs are scanned for
  credential patterns and excluded file classes; no values are printed. This
  complements manual review and cannot detect every possible secret encoding.
- Public relative links and JSON syntax are checked.

The real-video extraction test uses generated ffmpeg test imagery as a technical
fixture, not reconstruction evidence. The browser uses actual downloaded CC BY
captured geometry and a separately labelled synthetic playback fixture.

## Onboarding update

The hosted viewer has passed first/middle/final full-density states and a normal
page reload with network disabled, loading the cached first state again. See
[hosted receipt](hosted-smoke.json). Tests also cover corrupted downloads,
cancellation/resume, exact browser assembly, sample-only cache deletion and the
hosted proxy's public allowlist/read-only boundary.

The [30-second tour](readme-tour.json) uses the actual source clip and four captured
viewer states, with explanatory captions. It is not a loading-performance benchmark.
[Portable CI passed on all three systems](portable-platforms.json). A
[fresh GitHub Linux Docker rehearsal](clean-linux-rehearsal.json) built the image
in 76 seconds, then downloaded and verified the source/first state in 1.38 seconds.
Those are runner-specific timings, excluding browser graphics startup. These supplement the
[independent walkthrough checklist](fresh-install.md). Automated OS tests do not
qualify Windows/macOS Docker Desktop or an independent person's first run.

## Still required

A fresh native GPU setup/fit and export in this repository, real-provider deadline
termination/cancel/disconnect/download-failure qualification, cleared reference
training input acquisition, a different person's fresh-install walkthrough,
Windows/macOS Docker Desktop verification and real new-video fitting outcomes.
No paid worker was allocated by this implementation. Public allocation remains
disabled; historical successful experiments do not replace these release gates.

## Local environment note

This host had exhausted Docker's automatic network address pools. A local ignored
Compose override selected an unused subnet without pruning or changing unrelated
networks. The standard Compose file is unchanged. This is a host configuration
issue, not a requirement to reuse the developer's Docker environment.
