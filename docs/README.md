# Revisit documentation

Start with [current state](architecture/current-state.md), then the
[local app runbook](runbooks/operations/local-app.md). The directory conventions
follow the original gaussian-splatting experiment, while this is an independent
Git repository linked to https://github.com/tathagatbanerjee/revisit .

| Folder | Purpose |
| --- | --- |
| architecture/ | Current implementation status and boundaries |
| archive/ | Original research provenance, migration manifest, export inventory |
| changelog/YYYY.MM.DD/ | Dated changes and their actual verification |
| runbooks/operations/ | Local startup, capture and Runpod instructions |
| testing/ | Verification records and limitations |

- [Setup help](runbooks/operations/setup.md)
- [Fresh-install rehearsal](testing/fresh-install.md)
- [Hosted viewer](../hosted/README.md)
- [Experiments and outcomes](experiments.md), with [full records](../experiments/README.md)
- [Implementation plan](implementation-plan.md)
- [Licensing and asset provenance](licensing.md)
- [Historical native worker](../core-pipeline/README.md)
- [Latest change](changelog/2026.11.16/2026.11.16.3.md)
