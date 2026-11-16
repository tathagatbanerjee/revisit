# Runpod: credential checks and current limits

This preview supports **read-only account verification**, not public paid-job
allocation. The app's create route fails closed and creates no resources. Do not
interpret migrated historical worker code as a qualified paid service.

## Configure your own account key locally

Create an API key in your personal Runpod account using its
[official authentication documentation](https://docs.runpod.io/get-started/api-keys).
Keep it in the local server environment. For example, enter it without echoing
into shell history, then start the app from the same shell:

```bash
read -rs -p 'Runpod API key: ' RUNPOD_API_KEY
export RUNPOD_API_KEY
docker compose up --build -d
unset RUNPOD_API_KEY
```

Avoid shell tracing. Docker environment values are accessible to local Docker
administrators. Do not put the key into tracked files, uploaded footage, browser
storage or a model manifest. Native startup uses the same environment variable.
To remove a Compose credential, recreate the service from a shell without the
variable set. Revoke unused keys through Runpod.

**Test Runpod credentials** calls `GET /account` on RESTv2; it returns only a
success/scope message to the browser, not your account email or the key. It does
not allocate a worker. The API adapter uses `https://api.runpod.io/v2` and the
v2 GPU catalog for advisory offers. Current quotes are not historical prices.

## Why paid allocation remains disabled

The [official migration guide](https://docs.runpod.io/api-reference-v2/migrate-from-v1)
announced RESTv1 retirement for15 November2026. The old research GraphQL/transport
code was intentionally not migrated as the public control path.

Current official Pod APIs do not document a provider-enforced termination TTL.
The [official Runpod CLI guidance](https://github.com/runpod/runpod-plugins-official/blob/main/plugins/runpod/skills/runpodctl/SKILL.md)
warns that old `--stop-after`/`--terminate-after` flags were not enforced.
A worker-side stop timer is different from full deletion; stopped storage can
still bill. We have not established that a Pod-scoped injected key can safely
perform complete termination. The account control key must not be sent to workers.

Before enabling allocation, implement/qualify independent deadline cleanup (or
an independent trusted scheduler), persist ownership before uncertain allocation
responses, test cancel/disconnect/download failure, verify resource absence,
qualify the public worker image/source setup, and perform the independent
new-user static reconstruction rehearsal. Each live validation needs an explicit
budget/runtime. No historical allowance is reused.

The read-only client and owned-termination helper have fake-provider tests;
that is not evidence of live cleanup. A provider timeout means UNKNOWN resource
state, never proof that a worker is off. Use the provider console to reconcile
any advanced manually allocated resources.
