# Contributing

- Every pull request, including each layer of a stacked pull request, runs CI.
- Review a stack layer by layer. When it is ready, retarget the top layer to
  `main` so that it contains the whole stack; the lower pull requests then show
  as merged.
- Merge with "Merge when ready" (or `gh pr merge --merge --auto`). The pull
  request enters the merge queue, CI runs on the merge result, and on success
  it lands on `main` as a merge commit.
- A branch does not need to be up to date with `main`; merge `main` into it
  only to resolve conflicts.

Add yourself and your contribution to [CONTRIBUTIONS.md](../CONTRIBUTIONS.md).
