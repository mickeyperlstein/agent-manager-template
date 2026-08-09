# Work a GitHub PR

Usage: `/pr` (all open PRs) or `/pr <number>`

---

Protocol for triaging and closing out GitHub PRs on this repo — checking CI honestly, surfacing every review comment (including ones GitHub hides until submitted), and looping fix → reply → push until the PR is actually done.

## Step 1 — Inventory

`gh pr list --state open --json number,title,headRefName,mergeable,statusCheckRollup` (or just the one PR if a number was given). Note each PR's branch and whether an isolated worktree for it already exists (`git worktree list`) — reuse it rather than creating a new one.

## Step 2 — CI: don't trust a red X at face value

A failing check can be caused by the PR, or it can be pre-existing and unrelated. Before treating a failure as this PR's problem:
- Read the actual failure output (`gh run view <run-id> --log-failed`), not just the pass/fail status.
- Check whether the same failure exists on `main` right now (run the same test/command locally against `main`, or check if `main`'s own CI is also red).
- If it's pre-existing/unrelated: say so plainly, don't block on it, and don't spend the PR's effort "fixing" something the PR didn't break.
- If a real fix for the underlying issue lands on `main` after the PR branch was cut, merge `main` into the PR branch (not the reverse) and push — a rerun of an already-completed workflow run reuses its original merge snapshot, so a stale check needs a fresh push to pick up the fix, not just a rerun.

## Step 3 — Pull every review comment, including hidden drafts

`gh api repos/{owner}/{repo}/pulls/{n}/comments` only returns comments belonging to **submitted** reviews. A reviewer's in-progress draft review (state `PENDING`) has comments that are invisible to that endpoint until they submit it.

- Check `gh api repos/{owner}/{repo}/pulls/{n}/reviews --jq '.[] | {id, state}'`.
- If any review is `PENDING` and it's not yours, its comments exist but you can't see them yet, *and* you can't post any reply while it's open — GitHub allows only one pending review per person per PR, and reply-creation counts against that limit too. Tell the user and ask them to submit (or discard) it; don't submit/discard it yourself, it's their in-progress content.
- Once submitted, re-fetch: `gh api repos/{owner}/{repo}/pulls/{n}/reviews/{review_id}/comments --jq '.[] | {id, path, line, body}'`. If `line` is null, use `original_line` + `diff_hunk` for context instead — it means the diff shifted since the comment was made.

## Step 4 — For each comment, decide: reply or fix

- **Answerable in text alone** (a question about existing design/behavior): reply directly, no code change.
- **Needs a code change**: make the fix, verify it for real (`flutter analyze` / relevant test suite / an actual build — not just "looks right"), commit, push, *then* reply referencing the commit hash and what changed, ending with something like "mark resolved if that covers it."
- **A scope or design decision** (not a correctness question — e.g. "should this support platform X"): don't unilaterally decide. Ask the user. Implement only after they choose.

Reply with the dedicated reply endpoint, not the general one:
`gh api repos/{owner}/{repo}/pulls/{n}/comments/{comment_id}/replies -f body="..."`
(The general `POST .../pulls/{n}/comments` endpoint with `in_reply_to` looks plausible but fails — GitHub's REST docs list `in_reply_to` on that endpoint, but it 422s in practice. Use `/replies`.)

## Step 5 — Push discipline

- If a commit hasn't been pushed yet, `git commit --amend` freely while iterating on the same fix.
- Once a commit is pushed, don't amend it — make a new commit instead (avoids a force-push to a shared branch).
- Never force-push without the user explicitly asking.

## Step 6 — Verify CI after every push

Don't `sleep` and re-check manually. Use a Monitor poll-loop that emits on state changes and exits when nothing is left pending:

```bash
prev=""
while true; do
  s=$(gh pr checks <n> --json name,bucket 2>/dev/null)
  cur=$(jq -r '.[] | select(.bucket!="pending") | "\(.name): \(.bucket)"' <<<"$s" | sort)
  comm -13 <(echo "$prev") <(echo "$cur")
  prev=$cur
  jq -e 'all(.bucket!="pending")' <<<"$s" >/dev/null 2>&1 && break
  sleep 15
done
```

## Step 7 — Don't overreach

Merging, closing, or requesting changes on someone else's behalf is out of scope unless explicitly asked. This protocol ends at "every comment answered or fixed, CI green, everything pushed" — not at "merged."
