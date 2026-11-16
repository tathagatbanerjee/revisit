# Licensing and assets

Revisit's project-owned code and documentation use the [MIT License](../LICENSE),
`Copyright (c) 2026 Tathagat Banerjee`. This includes the local app, tests,
preparation tools and project-owned native worker adaptations. Preserve MIT's
copyright and permission notice when distributing the software.

## Examples

**Guildhall is the primary example of our work.** The original interior walkaround
is by Acabashi / Wikimedia Commons, under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
That license permits sharing and adaptation with attribution, an indication of
changes and ShareAlike terms. Our trimmed/resized video and derived reconstruction
retain that notice separately from the app's MIT code. The app displays attribution;
[third-party notices](../THIRD_PARTY_NOTICES.md) record the source and changes.

All 305 full-density observations are available in the `guildhall-fixedworld-v1`
GitHub release through checksummed, on-demand downloads. The fixed room is shared
losslessly across states; assembled model hashes match the original exports.
`examples/guildhall.json` records the exact files, hashes, timestamps and cameras.
Media caches locally outside Git. No training checkpoints or pretrained weights
are included in the sample.

Houseplant is a secondary community example by Marcel Padilla, CC BY 4.0. It is
not a Revisit-trained result. Its pinned provenance is in `examples/houseplant.json`.
The synthetic interaction fixture is project-authored and labelled synthetic.

## Dependencies and optional research backend

Installed packages retain their own licenses; see [third-party notices](../THIRD_PARTY_NOTICES.md).
MoSca's author code is MIT, while its priors, weights and native renderers have
separate terms. Software distribution and generated outputs are separate questions;
a software restriction must not automatically be treated as an output restriction.
The sample release contains reconstruction output, not those upstream packages.

The complete advanced training stack is not advertised as commercially unrestricted.
Keep upstream notices when acquiring or distributing it. Other historical models,
source footage, proprietary SDKs, credentials and cloud execution state are not
part of this release.
