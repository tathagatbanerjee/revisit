# Licensing and assets

The owner selected the **MIT License** on 16 November 2026. It covers Revisit's
project-owned code and accompanying documentation, under the copyright notice
`Copyright (c) 2026 Tathagat Banerjee`. MIT allows commercial use, modification,
distribution and sublicensing, with preservation of its copyright and permission
notice in copies or substantial portions. The software is provided without
warranty. See the complete [license](../LICENSE) and the
[Open Source Initiative's MIT text](https://opensource.org/license/mit).

MIT is highly permissive but is not a public-domain dedication: its notice
condition remains. Zero-Clause BSD removes that notice condition, but MIT is the
owner's chosen license for this project.

## What this grant covers

The initial publication contains newly prepared project documentation and the
license. Future project-owned app code, tests and adapters should use the same
license unless explicitly identified otherwise. Do not assume that every file in
the old research workspace can be copied and relicensed.

## Third-party boundaries

External code, pretrained weights, datasets, source footage, SDKs and exported
reconstructions require their own provenance and permission review. Revisit's MIT
license does not override upstream terms or make those assets MIT-licensed.
Historical notes specifically identify separate terms for MoSca author code,
its priors and its native renderer. No current clearance for all derived model
outputs is established by this documentation publication.

Before shipping a backend or real sample pack:

1. Inventory exact source revisions, packages, weights, footage and renderers.
2. Record origin, license/terms, required notices, hashes and redistribution
   decision for each item; preserve existing notices on copied/adapted code.
3. Include required third-party notices and distinguish project-owned patches
   from upstream material.
4. Distribute only cleared assets, with per-asset attribution and allowed uses.
   Provide documented user-supplied acquisition when redistribution is unavailable
   and those terms permit it. Do not bypass upstream acceptance requirements.
5. Explain any research-only or other restrictions on an optional reconstruction
   backend. A permissive local viewer is not a promise that every pipeline
   dependency is cleared for unrestricted commercial use.

A procedural sample can be authored for Revisit without copying historical media.
It must be labelled synthetic and must not be used as reconstruction evidence.
A useful real reconstruction pack remains a separate release requirement.

No footage, fitted models, pretrained weights, proprietary SDK or credentials are
included in this initial publication.

## Local preview update — 16 November 2026

Project-owned app, tests, preparation tools and selected native research helpers
are now included under MIT. Required dependency and adapted-recipe notices are in
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). The pinned community Houseplant
sample downloads locally under CC BY4.0 with explicit attribution; it is not
relicensed under MIT. Historical model/media assets remain excluded.
