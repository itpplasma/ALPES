# Project state

## CI controller handoff — 2026-10-21

- [CI migration PR #14](https://github.com/itpplasma/ALPES/pull/14) is pushed at a9f5496567fadf87ef8b7153dc9cc9d56167bb73 and submitted to the normal merge queue. It was still open at the controller snapshot; no native success or merge is claimed.
- Required validation uses owned Ubuntu 24.04 hardware. Every PR event skips real validation; merge-group runs remain authoritative. Windows and Intel macOS, where present, are informative and cannot block.
- Existing validation authority is preserved: TeX dependency installation, make, and the PDF artifact. Actionlint and whitespace checks passed; the actual queue result is pending. Shared hygiene workflow and checker use immutable 104634c01aa669d542e8a26a34a50b6471fc19ce.
- Preserve the queued head. The next controller should inspect the actual merge-group jobs and runner identities, collect failures without weakening checks, and verify the main-branch result after normal squash merge.
- The last infrastructure observation was renewed kub3/kub4 connectivity loss. Preserve live jobs; temporary owned dispatch runners and Slurm remain available. ARM macOS is hosted on faepmac1; faepmac2 is not provisioned for CI.
- This documentation branch records the handoff separately so the submitted CI head remains unchanged. No new scientific runs are needed for this workflow-only change.
