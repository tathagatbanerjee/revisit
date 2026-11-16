# Current state — 16 November 2026

Revisit is an independent checkout under `opensource/revisit`, with remote
https://github.com/tathagatbanerjee/revisit . The containing experiments repo
locally excludes `opensource/` to avoid double-staging; that does not affect
tracking or pushing files inside Revisit.

## Implemented local preview

The Node/Three.js/Spark app on localhost:4320 downloads a pinned, hash-verified real
Houseplant reconstruction by Marcel Padilla (CC BY 4.0), and offers a separate
labelled synthetic sequence for interaction tests. It supports static PLY/splat
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
No original footage, pretrained weights, SDK, local checkpoints or credentials
were migrated. The real community sample downloads into ignored local storage;
it is separately attributed and is not a Revisit-trained model.

See [verification](../testing/verification.md) for checks actually performed.
