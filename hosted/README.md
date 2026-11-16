# Browser-only Guildhall viewer

The public viewer reuses the local app's rendering and navigation. It has no
upload endpoint, account credentials, Runpod access or training process. A small
Worker streams only the public release assets named in the pinned descriptor;
it cannot proxy arbitrary URLs. Browser code verifies and losslessly assembles
original model bytes, caching static/motion parts rather than every expanded PLY.

Build from the repository root:

```bash
npm --prefix app ci
node hosted/build.mjs
node hosted/preview.mjs
```

Open http://localhost:4323 . The build embeds only allowlisted public HTML/JS/CSS,
required pinned viewer modules, notices, sample metadata and read-only endpoints
in `hosted/dist/server/index.js`. It reads no environment values or data folders.
The Worker has a standard `export default { fetch }` entrypoint. Its streaming
proxy avoids GitHub Releases' browser CORS restriction without copying the full
sample into the deployment. All data remains available from GitHub Releases.

A service worker caches the interface and verified visited parts. The full offline
pack is explicit; keep the tab open and resume after interruptions. Browser quota
and eviction apply. Clear-cache removes public sample parts and preserves the
interface. No user recordings enter the public hosting service.

The deployment's identity is in `.openai/hosting.json`. Maintainers publish through
the Sites source/packaging workflow; publishing from a fork requires its own
hosting identity/access. `node hosted/build.mjs --site-root` writes `dist/` at the
repository root for that packaging workflow. Generated build output stays ignored.

Required third-party notices are served at `/THIRD_PARTY_NOTICES.md`; code is MIT,
and the separately downloaded Guildhall media retains its attribution/license.
The build includes Three.js's OrbitControls and Pass modules and Spark's embedded
worker/WASM code, preserving their notices.
