# P28 — C5 What to do better next project

## Diagnosis first
- **"Text too small" ×3** looked like a taste problem. It was a scale problem: every spec was sized in canvas pixels on a 1920-wide (or 1357-wide) page that Desktop shows at Fit-to-page, ~0.47×. Evidence: C fixed a 15 px floor *at page scale* before drawing and set Fit to width; no size note followed.
- **Three versions** looked like churn. It was preference discovery: A was correct, validated and saved (S3 HO). The owner's final choice combined A's palette/orientation with B's motion/cleanliness — information that did not exist until both had been seen in Desktop.

## What I did wrong
1. Shipped B rev 2 hover cards whose fixed labels showed on the idle page — I trusted an SVG render for a canvas host (§162a).
2. Placed the flip card where a line always crosses it (rev 2) — placement chosen without a collision rule (§162e).
3. Sized text in canvas pixels without a page-scale floor, three rounds running (A, B, B).
4. First harness read 0 texts and reported 0 issues; the bold face measured as regular — caught only because the checker printed what it read (§162b).
5. Wrote "2,221 turns" into three documents before running the merge that disproved it (C1 count 12) — corrected the same session.

## What the owner did that cost time
1. **Asked for B after A was built and saved**, and for C after B — two unplanned versions. Worth it (C is the better entry) but it was the biggest cost line; a *moving* side-by-side at mockup stage might have surfaced the preference a session earlier.
2. **Feedback arrived as screenshots of the whole page, in rounds** ("small", "boring", "overlap") — each round a full regenerate-validate-place cycle. A size target stated once ("nothing under X pt at Fit to width") would have closed two rounds.
3. **Hover states for C were never screenshotted in Desktop** — only idle. They are verified offline on canvas, not in the host. Low risk (same construction as B rev 3, which was seen), but unverified.

## What the owner did right that I did not
1. Asked for **"no overlap" and "big enough"** as hard requirements — that is what produced the measured harness instead of eyeballing.
2. **Closed Desktop with Don't save every time** — eight placements, the hash guard never once found an owner edit to collide with.
3. **Saved A and B as .pbix backups before the cleanup** and asked for the cleanup in one instruction.
4. Submitted **five days early**.

## Changes, ranked by expected value
| Rank | Change | Evidence | Cost to adopt | Done? |
|---|---|---|---|---|
| 1 | **Page-scale type floor + display option decided in the mockup step** | 3 size rounds; 0 after C | one line in Skill 0's mockup checklist | **done** — `SKILL_Brainstorm_Mockup.md` amended |
| 2 | **Canvas layout proof before every Deneb placement** (`deneb_layout_check.mjs`) | caught 7 defects pre-Desktop in C; would have shown B's stray labels | ~2 min per run | **done** — promoted to `_ENGINE/tools/`, Skill 4 amended |
| 3 | `DENEB_HOVER_CHILD_NO_OPACITY` lint | the shipped defect | zero (runs in the linter) | **done** |
| 4 | Cost merge windows (§162j) | an hour of P28 and 50 turns of engine history dropped | zero | **done** |
| 5 | **Moving side-by-side for competing directions** (two short GIF/MP4 storyboards) before any build | B and C were decided only after builds | ~20 min per direction | Skill 0 amended (recommendation, not gate) |
