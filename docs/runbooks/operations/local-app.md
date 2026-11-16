# Run the local app

## Docker: primary setup

From the repository root:

```bash
docker compose up --build -d
```

Open http://localhost:4320 . The service binds to loopback on the host and uses a
separate Compose project, `revisit`. It does not mount the old experiments tree.
The first build downloads CPU dependencies; allow for network/image setup time.
No NVIDIA/CUDA GPU is needed locally to view a sample. A WebGL2-capable browser is
required. Unsupported graphics still leave project preparation available.

Click **Explore Houseplant**. The app downloads3.5MiB once from its pinned public
source, verifies its byte count and SHA256, then opens the real reconstruction.
Inspect leaf boundaries and missing surfaces. Orbit, translate and reset. This
static capture has no event timeline. Choose **Synthetic interaction test** to
test independent time and camera controls; it is expressly not captured evidence.

Persistent Docker data lives in the `revisit_revisit-data` named volume (Compose
may normalize the exact prefix). `docker compose down` stops the app and preserves
that volume. `docker compose down --volumes` removes uploads/results; use it only
when you intentionally want to erase that local data.

## Native development

Requires Node24+, ffmpeg, ffprobe and Python3.11+ for frame extraction.

```bash
cd app
npm ci
npm start
```

Open http://localhost:4320 . The default cache, videos and run assets live in
ignored `data/` at the repository root. Set `REVISIT_DATA` to another private
folder before startup if desired. `npm run doctor` reports prerequisites without
printing credential values. Local viewing requires no cloud key.

Advanced CPU mapping uses Python3.11 with
`core-pipeline/requirements-preparation.txt`. Set `REVISIT_PREP_PYTHON` to that
virtual environment's Python executable. Docker supplies this environment.

## Try your video

1. Follow the [capture guide](capture.md).
2. Upload to localhost, preview it and choose1–30s. Preparation extracts real
   observed frames with exact source timestamps. It does not create a3D model.
3. Review all source previews and explicitly confirm continuity.
4. Recover static cameras on CPU. This may fail for insufficient capture coverage.
   Failed maps remain in local project storage; use a new upload for a fresh trial.
5. Passing camera/anchor gates allow packaging a worker handoff. That bundle
   contains selected images/configuration, not account keys or pretrained weights.

Paid fitting is not enabled in this preview. Camera recovery passing is not a
complete reconstruction, nor a validation of correct moving-person geometry.

## Import a saved experiment

A static file can be opened directly using the viewer's local file picker. For a
complete static/sequence run folder with a `run.json` manifest:

```bash
node scripts/import-run.mjs /path/to/run-folder optional-new-run-id
```

The importer copies only the manifest and referenced model files into
`data/runs/`, computes hashes, preserves every timestamp and rejects overwrite,
absolute/traversal paths and model symlinks escaping the source root. Reload the
app. On Docker, import to an explicit host folder with `REVISIT_DATA` and copy the
reviewed run folder into the app's data volume, or use native startup for local
research assets. No historical asset is auto-imported or publicly redistributed.

## Checks

```bash
cd app
npm run check
npm test
npm run doctor
cd ..
python3 scripts/audit-publication.py
docker compose config --quiet
```

For real Chromium/WebGL checks while the app runs:

```bash
CHROME_PATH=/path/to/chrome node app/test/browser-smoke.mjs
```

Screenshots go to ignored `working/`; a small verification receipt goes to
`docs/testing/`. The browser test downloads the real sample if needed. It does
not allocate compute. Tested platforms/limits are in the verification record;
a Linux rehearsal does not establish universal Docker Desktop compatibility.

## Docker address-pool exhaustion

If Docker reports that all predefined address pools are fully subnetted, do not
prune unrelated services. Ask your local administrator for an unused subnet and
create an ignored `working/compose-network.yaml` override:

```yaml
networks:
  default:
    ipam:
      config:
        - subnet: YOUR_UNUSED_SUBNET
```

Then start with `docker compose -f compose.yaml -f working/compose-network.yaml up
--build -d`. Use that same pair of files for subsequent Compose commands. The
subnet must not overlap existing Docker networks, your LAN or VPN routes.
