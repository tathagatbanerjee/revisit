# Current state — 16 November 2026

Revisit is an independent checkout under `opensource/revisit`, with remote
https://github.com/tathagatbanerjee/revisit . The containing experiments repo
locally excludes `opensource/` to avoid double-staging; that does not affect
tracking or pushing files inside Revisit.

## Implemented local preview

The Node/Three.js/Spark app on localhost:4320 leads with our Guildhall full-interior
fixed-world experiment: source video first, then an interactive viewer. A pinned
release supplies all 305 full-density observed states on demand, with SHA-256
verification and local caching (about 31 MiB initially, 5 MiB per additional state; 1.7 GB total download). The source and
derived reconstruction retain CC BY-SA 4.0 attribution. Ghosted people, turn blur
and failed motion coverage remain visible limitations. Houseplant by Marcel Padilla
(CC BY 4.0) and a labelled synthetic sequence are secondary checks. It supports static PLY/splat
import, timestamped imported run bundles, recorded camera reset, orbit/pan,
translation and playback with camera pose preserved across time changes.

Video uploads remain local. Users choose a continuous 1–30s interval from a readable
16:9 source of at most 10minutes / 1 GiB; the app extracts 640×360 observations at 12 Hz
using actual source PTS and records hashes. Users review source previews before
optional CPU camera recovery. Passing maps can be packaged into isolated native
worker inputs. Failed/interrupted attempts are retained; reviews are explicit.
Docker includes pinned CPU mapping dependencies. Native startup requires ffmpeg,
ffprobe and Python; advanced mapping additionally needs its preparation environment.

Runpod credentials come only from the server environment. The app can test account
access without allocating compute and has a RESTv2 read-only offer adapter. The
account key is never sent to the browser or GPU worker. File routes are confined,
mutation endpoints require a local session token and cross-origin requests are
rejected. This is a single-user localhost application, not an internet service.

## Easier onboarding and hosted preview

The README leads with a browser-only Guildhall viewer and a 30-second walkthrough.
The public viewer reuses the same full-density renderer and keeps model assembly,
hash verification and sample caching in the browser. Its Worker streams only pinned
public files; it accepts no uploads, cloud keys or paid compute requests.
Service-worker caching supports offline reloads and previously visited states.
A full offline pack downloads about 1.7 GB without storing 305 expanded models.
Browser storage limits/eviction apply; keeping the tab open and resuming interrupted
downloads is required. Local Node caching can expand to about 11.5 GB.

Both interfaces show cache usage, remaining bytes and transfer progress, and offer
explicit offline download, cancellation/resume, sample-only clearing and a setup
check. The optional host script checks Docker/Compose, disk and port availability.
An alternative local port is configurable with REVISIT_PORT.

Portable contracts/cache/build checks run on Linux, Windows and macOS. A separate
clean Docker workflow rehearses the first public download on fresh Linux. These
are automated checks; an independent human's Windows/macOS Desktop walkthrough
remains outstanding, with a checklist and installation issue form provided.

## Incomplete: paid upload-to-reconstruction workflow

Paid allocation is disabled. The historical project-owned native stage code and
recipes have been migrated for inspection and advanced development, with a public
source acquisition/setup recipe. They have not completed a fresh Revisit GPU run.
The setup still needs dependency/image qualification; some dependencies are
research-restricted and are not covered by Revisit's MIT license.

Official Runpod v2 documentation does not establish an independent provider-side
termination TTL. A stopped process is not a terminated Pod; stopping can leave
storage billing. Independent deadline cleanup, live lifecycle/failure tests, and
an independent new-user rehearsal remain required before enabling paid jobs.
No user budget or historical session allowance is silently reused. No workers
were created during implementation.

## Evidence and assets

There are 143 migrated project-authored research/result records plus a 103-export
inventory. These include rejected results, controls and overlapping reports,
not 143 unique trials or 103 successful fits. Their private media/logs remain
unavailable. Historical plans and resource instructions are not current runbooks.
The selected Guildhall source excerpt and reconstruction are separate public
release assets. No pretrained weights, SDK, training checkpoints or credentials
were migrated. The real community sample downloads into ignored local storage;
it is separately attributed and is not a Revisit-trained model.

See [verification](../testing/verification.md) for checks actually performed.
