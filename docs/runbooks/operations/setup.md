# Setup help

The [hosted Guildhall viewer](https://revisit-guildhall.elephant-str-5431.chatgpt.site)
requires a WebGL2-capable browser and no installation. Start with that if you only
want to inspect the example. Install the local app to prepare your own videos.

## Before Docker startup

Run `docker info` and `docker compose version`. If Docker is unavailable, install
or start Docker Engine/Desktop. Compose must be v2. No Runpod account is needed.
If Node 24+ is already installed, `node scripts/setup-check.mjs` checks Docker,
Compose, disk availability and the port. It never prints credentials. For native
startup, use `node scripts/setup-check.mjs --native` instead.

Allow at least 3 GiB for an initial build/sample, depending on existing images,
and another 12 GB for the complete expanded local sample cache. Docker Desktop
has its own virtual disk; free space on the source-code drive may differ.

If localhost:4320 is occupied, choose an unused port. On bash/zsh:

```bash
REVISIT_PORT=4325 docker compose up --build -d
```

On Windows PowerShell:

```powershell
$env:REVISIT_PORT = "4325"
docker compose up --build -d
```

Then open http://localhost:4325 . Keep using the same port setting for subsequent
Compose commands. If Docker cannot create a network, follow the existing
[address-pool guidance](local-app.md#docker-address-pool-exhaustion); do not prune
unrelated services.

## In the app

**Check my setup** reports WebGL2 availability and storage. If graphics are
unavailable, enable hardware acceleration in your browser settings, restart the
browser and reload. Remote-desktop sessions or virtual machines may lack graphics
support. Local video preparation can still work without the 3D viewer.

The download panel reports sample cache size, remaining offline bytes and active
transfer progress. The first state needs about 31 MiB; each additional state
needs about 5 MiB. A connection or checksum error can be retried without clearing
completed downloads. Downloading the complete offline pack is optional and explicit.

**Cancel download** stops the current transfer and preserves completed files.
Click **Download** again to resume. Keep the hosted tab open; browsers may suspend
background work. Browser storage is subject to quota and eviction. If the browser
cannot hold the full pack, view on demand or use the local app.

**Clear Guildhall cache** removes only the public Guildhall sample cache. It does
not delete local uploads, imported runs, preparation reports or credentials.
Docker stores its cache in the `revisit_revisit-data` volume; native startup uses
`data/showcase/`; the hosted viewer uses this browser's Cache Storage. Static hosted
viewer files remain cached so the page can still open after clearing the sample.
