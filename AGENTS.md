# Revisit workspace guidance

- This is an independent MIT-licensed repository; remote is
  https://github.com/tathagatbanerjee/revisit .
- Read README.md, docs/README.md and docs/architecture/current-state.md first.
- Keep the local application in app/, reconstruction code in core-pipeline/,
  durable evidence in docs/ and temporary work in ignored working/.
- Record completed changes in docs/changelog/YYYY.MM.DD/YYYY.MM.DD.N.md.
- Preserve experiment failures, timestamps, camera conventions and provenance.
- Never commit credentials, .secrets/, .env files, user video, cached downloads,
  models, checkpoints or private execution state. Use environment variables for
  credentials; the browser and remote worker never receive the Runpod API key.
- Run relevant checks and the publication audit before committing or pushing.
- Provider authentication tests must allocate nothing. A paid validation needs
  an explicit budget/runtime. Plans and code changes do not authorize GPU spend.
- Do not advertise the paid reconstruction flow as qualified until independent
  deadline cleanup and fresh-user end-to-end validation have actually passed.
- Retain upstream notices. Real sample assets retain their individual licenses.
