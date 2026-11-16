# Fresh-install rehearsal

The hosted viewer is the quickest way to inspect Guildhall. Docker is the path
for preparing your own recording. A release is easier to trust when someone
unfamiliar with the project follows the README without help.

## Independent desktop walkthrough

Use a clean Windows, macOS or Linux account/machine. Record the actual OS, browser,
Docker/Compose versions, connection speed and free disk space. Do not copy the
maintainer's data, environment or credentials. No Runpod key is needed.

1. Start a timer. Read only the public README. Explain in one sentence what the
   experiment attempts and one limitation; note how long that took.
2. Open the hosted viewer. Watch the source, enter Guildhall, freeze time, move
   right, scrub to the middle and reset a recorded camera. Record download wait
   time and whether the controls were obvious.
3. Reload. Confirm cached states do not redownload. Turn off the network, reload
   again and inspect a previously visited state. Reconnect afterwards.
4. Check the displayed cache usage. Start the explicitly labelled offline pack,
   cancel, then resume. Record interruptions and whether the messages help.
5. Clear the Guildhall cache. Confirm the app still opens and offers downloads.
6. Follow the three Docker commands from the README. Record build time separately
   from first-source/first-model download time. Use “Check my setup”.
7. Upload a suitable short recording to localhost and preview it. The current app
   prepares observations/cameras; paid reconstruction remains disabled.
8. Stop with `docker compose down`, restart, and verify local cached data remains.
   Do not use `down --volumes` unless intentionally deleting that test installation.
9. File an installation issue with every intervention, unclear instruction and
   platform-specific difference. Report versions/stages, not keys or private video.

Record each path as **pass**, **fail**, or **not run**, with timings. An automated
Linux test does not substitute for this independent desktop walkthrough.

## Automated coverage

`Portable import and cache checks` runs Node contracts, imports, byte verification,
cache operations and the hosted build on Linux, Windows and macOS. This checks
portable code, not each operating system's Docker Desktop or browser graphics.

The manually triggered `Clean Docker rehearsal` workflow builds from a fresh
checkout on a GitHub-hosted Linux runner, uses an empty cache, downloads the public
source and first original state and verifies hashes. It creates no GPU workers
and uses no cloud key. Its receipt is available as a workflow artifact. Build
cache/image pull time is separate from the receipt's first-download timing.

For a local isolated rehearsal, use a different Compose project, port and empty
volume, then run `node scripts/rehearse.mjs http://127.0.0.1:YOUR_PORT`.
The script refuses a nonempty cache and never clears existing data.

## Recorded automated run — 16 November 2026

[Linux, Windows and macOS portable checks passed](portable-platforms.json).
The [fresh Linux Docker run](clean-linux-rehearsal.json) passed with an empty data
volume and no cloud key: 76s image build, then 1.38s for public video/model download
and hash verification. These runner-specific timings exclude browser initialization.
The independent human/Desktop walkthrough above remains open.
