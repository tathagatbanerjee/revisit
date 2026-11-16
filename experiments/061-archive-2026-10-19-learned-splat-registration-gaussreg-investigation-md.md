> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/gaussreg/investigation.md`.
> Original SHA-256: `2fa212abc9a5020368b6f5f93ef8e9b21ec5cf1dca9f5073a0ad24ea6abfacd8`. Private media/logs are not included.

# GaussReg implementation investigation

Use official main85df227f and its released coarse checkpoint, with the fixed
procedure in shared investigation (historical reference: `../investigation.md`). The demo supports
source/reference PLY and saves `estimated_transform.npz` in native coordinates.
Its fixed opacity/percentile selection is part of this method; record retained
counts separately from the all-point diagnostic union.

Pad the DC-only exports with45 zero higher-order SH floats. Verify exact
preservation of XYZ, covariance parameters, opacity and DC before transfer.
Use a deterministic row shuffle in the exact-copy control and never expose
known-copy correspondences/transform to inference. No random weight substitute.

The author checkpoint link is OneDrive; verify a real tensor checkpoint instead
of an HTML login page. Availability failure is recorded before spending paid
GPU time on an unusable setup. Separate optional fine branch from coarse result.
Cost and cutoff are the shared one-Pod US$2/two-hour bounds, not a second budget.
