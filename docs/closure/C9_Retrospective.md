# P28 — C9 Retrospective (accepted by the owner, 2026-10-17 09:49 MYT)

**Scope, stated first.** Only **Session 5** (Skill 9 publishing, 2026-10-17 07:56–09:50 MYT) is observable: it is
this conversation. **Sessions 1–4 are reconstructed from artefacts**: the handovers S2–S4, the closure C1–C8 and
the `_cost/` snapshots. Session 1 has no transcript and no snapshot. Where a number below comes from a
document rather than from something run today, its basis says so.

Basis legend: **[obs]** = observed in this session · **[HO]** = a session handover · **[C1/C2/C8]** = closure file ·
**[snap]** = `_cost/` snapshot · **[tool]** = a command run in this session, output read.

---

## 1. Metrics line (mandated)

| Metric | Value | Basis |
|---|---|---|
| **Validator errors on first pass, build** | **Not recorded.** The handovers quote checks run after the owner's save, not first passes. Earliest recorded: S3 had 2 `validate_pbip` errors, both in the starter's own files and identical on the untouched baseline, so **0 were attributable to P28 generators**. S4 final: 1 (the starter's, left with its page) | [HO S3, S4] |
| Validator false positives met in build | 2: CLI `PBIR_FORMATTING_PROP_NESTED` (F3) and linter `CONTAINER_PROP_IN_OBJECTS` on cardVisual padding (F4). Neither was a defect in the report | [HO S3 §4] |
| **Validator results, publish gates, first pass (S5)** | scrub **0 BLOCK** · `check_rebuild_materials` **ALL PRESENT, but hollow** (0 artefacts recognised: a tool defect, fixed) · `validate_pbip` 1 error (the starter's) · deck `validate.py` **0** · guide structural floors **0** | [obs] |
| **Fix rounds per deliverable** | Version A: **3** render rounds · B: build + **3** revisions · C: 1 build + **1** fix (visual header) · repo: **0** (built once, gated once) · guide: **1** wording round before the first render, 0 after · deck: **2** (self-review: 3 fixes; fresh-eyes QA: 5 should-fix) · card image: **3** crops · P27 redaction: **2** (the `.pbir` catalog name came in the second pass) | [C1], [obs] |
| **Sessions used against planned** | **4 planned to submission, 4 used** (S4 held two unplanned versions). **+1 for publishing** (S5), which the plan did not count; Skill 10 ran inside S4 | [C2], [obs] |
| **Mid-session regressions this session introduced** | **3, all caught in-session, 0 reached the public.** (1) Widening `check_rebuild_materials` produced a false FAIL on P27 (README column alignment read as a path with spaces). (2) `py_compile`, run to verify two edited scripts, wrote 2 `.pyc` files into P27's already-gated mirror; `update_p27_repo.ps1` refused at 160 against 158. (3) Re-committing the handover, kickoff and cost snapshot from unchanged cloud paths landed the **previous** versions on the device while the tool reported `written`, and `session_close.py` still said COMPLETE | [obs] |
| Cost, whole project (floor) | **≥ 4.0 h active · ≥ 1,140 turns · ≥ 664 tool calls · 389,988 cache-read/turn**. S1 missing, S4 partial. S5 alone: 384 turns · 0.9 h · 393,824 cr/turn · browser 14 % | [snap] merge 2026-10-17 ~09:55 MYT |

---

## 2. What the publishing session found, in the tools

| # | Defect | How it showed | Fixed |
|---|---|---|---|
| T1 | `scrub_check.py` returned CLEAN on an empty folder. P27 F-37 had been "settled" since 2026-09-07 with a fix as its reopen condition, and was never built | A control on an empty temp dir | `[scan]` line, exit 4 at zero files |
| T2 | The scrub skipped `.mjs`, `.pbir`, `.pbism`, `.pbip`, `.platform` and `LICENSE` | The new `[scan]` line read 47 of 60 files | Binary skip-list (named in the output) + a UTF-8 read of everything else |
| T3 | `check_rebuild_materials.py` recognised 0 artefacts in a `pbip/ build/ harness/` repo and printed ALL PRESENT | Its own `0 runnable rebuild artefacts` line | Wider vocabulary + a floor at zero + scrub-not-run now fails |
| T4 | Parser: column-aligned README lines read as paths containing spaces | A false FAIL on P27, minutes after T3's fix | 2+ spaces end a path; ALIGNMENT control |
| T5 | `device_commit_files`: an intermittent stale write on re-commit from the same path | Handover first line read back from the device | Commit from a fresh path, then verify by size and hash (SETTLED) |
| T6 | `session_close.py` checks presence and order, not content | It passed the stale handover | It now prints the handover's size and first line |
| **Found by T2** | **P27's PUBLISHED repo carried its workspace name and semantic model id** in a byConnection `.pbir` (plus 8 more files) | The widened scrub re-run over every repo it had already passed | Redacted, pushed `8f2866c`, confirmed by clone (owner: yes). History still holds the old values; that is the owner's call |

## 3. What the session found, in the working method

P24's C9 found that the session's operator frictions had **the same shape** as its tool defects. This one did too.

| # | Friction | Shape | Same as |
|---|---|---|---|
| M1 | I recorded the cloud copy's `written` as done. The device held the older file | Trusting a reply instead of reading the target | T1, T3, T6: a pass reported on something not examined |
| M2 | I ran a compile check *inside* a tree that had already passed its gates | A verification step that mutates what it verifies | T4: widening a check broke an assumption the old input never tested |
| M3 | The kickoff asked for an architecture diagram for the card. The site's own schema (`kind: "powerbi"`, entries 09, 10, 14, 15) needs an image | A kickoff written by analogy with the previous project *type* (Fabric) | Guide §155's "a shape's proof is scoped to its source" |
| M4 | Closure open item 2 (the "Server-equals-tcp miss") was carried into the kickoff as a risk. It was a placeholder classified correctly | A finding filed without reading the classifier for the input used | App C 18, "record what you ran" |
| M5 | The folder-access prompt timed out during the first minutes. The owner was present minutes later | Asking for access before the person was watching | P27, whose card was blocked for the same reason |
| M6 | Every push needed the owner: 3 commands plus 1 re-run. Pushing from the session was refused because the Claude GitHub App is not installed on BIVenture2025 | A standing access gap paid for on every publish | P23–P27 (every publish script exists because of it) |

**What the owner did that worked:** a one-word decision on each fork (CSV out, repo name, light guide, P27 scrub
"Yes"). Pasting the script's full output every time, so each STOP was diagnosed from its own words in one turn.
Saying "continue here" and "do it here" instead of opening new sessions, which kept the card, the publish and the
P27 fix in one context.

---

## 4. Changes, ranked by expected value

| Rank | Change | Evidence | Cost | Status |
|---|---|---|---|---|
| 1 | **Install the Claude GitHub App on BIVenture2025**, at least for new project repos and `BIVenture2025.github.io`, so a session can push and the owner only approves | M6: 4 owner round trips this session; every Type D and contest publish since P23 | One approval screen (owner) | **Owner decision.** Offered, not done |
| 2 | **After any write to the device, read the target back** (size + hash, or first line for docs) before reporting it | M1/T5 | One call | Rule in SETTLED; `session_close` prints the evidence |
| 3 | **Never run a check inside a gated tree.** Use a copy, or `PYTHONDONTWRITEBYTECODE=1` | M2 | Zero | Rule in guide §163g |
| 4 | **Widen a check → re-run it over everything it has passed, and expect the parser to break too** | T2 found the P27 leak; T4 | Minutes | App C 65 |
| 5 | **Name the folders a session needs in its kickoff, and request them in the first tool call** | M5 | Zero | Done in the S6 kickoff format; carry forward |
| 6 | **Derive the card shape from the site's entries for the same kind of project**, not from the last project | M3 | Zero | Skill 9 amendment 2026-10-17 |

## 5. One line

The publishing session was cheap in build work and expensive in trust. Six of its thirteen findings (T1, T2, T3,
T6, M1, M4) were a tool, or me, giving a verdict on something not actually examined. The most valuable thing it did had nothing to do
with Project 28: re-running a widened check over old work and finding a live leak in Project 27.
