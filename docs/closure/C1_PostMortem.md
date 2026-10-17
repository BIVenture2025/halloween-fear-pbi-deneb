# P28 — C1 Stage-by-stage post-mortem

Basis legend: **[snap]** = `_cost/session-NN.json` · **[HO]** = the session's handover · **[disk]** = read from the files on 2026-10-17 · **[DAX]** = live query on the open model · **[chat]** = this conversation (S4 only; S1–S3 are reconstructed from artefacts).

| # | Phase (session, date MYT) | Planned | Actual | Hiccup | Learning | Pivot | Cost |
|---|---|---|---|---|---|---|---|
| S1 | Brainstorm — Skill 0 Step 1 (Cowork, Fable, 14 Oct) | Story + design decisions | `P28_BRAINSTORM_DECISIONS.md`: 4-beat "Thinning Veil", portrait, palette A primary, Deneb + HTML allowed [disk] | One prose claim false ("childhood country = current country") — not caught until S2 | §162f | — | **not captured** (Cowork session, no transcript tool) [HO S2] |
| S2 | Data contract, cross-check, mockups A/B, guide, package (Opus/Sonnet, 14 Oct 18:52–19:21) | Package for approval | `P28_DataContract.md`, `P28_Package.html`; **approved 19:30** [HO S2]; every §2 aggregate matched CSV replay AND live DAX except the one sentence (24 of 105 moved) | Mockup caption contradicted guide route (dumbbells) | §162f | Owner: *correct and continue* | 174 turns · 0.49 h · 62.7 M cache read [snap] |
| S3 | Build Version A (Opus, 14 Oct 19:33–22:13) | Model + theme + E02–E22 | TMDL model (+3 columns, 2 tables, **53 measures**), theme, page with **26 visuals** (8 Deneb), TT_Nightmare; **3 render rounds**; owner saved 22:10; live DAX 285/264/56/48→14/9→12/11→42/23…2/97/105 all matched [HO S3] | Native table scrolled ×2; cardVisual tiles; CLI + linter false positives; screenshot tool produced no PNG | §162g–i | Tables/cards → Deneb panels | 242 turns · 0.73 h · 93.7 M [snap] |
| S4a | Version B brainstorm + package (Fable, 14 Oct ~22:15) | **unplanned** | "Fear has a lifespan" cemetery + leaderboard flip, landscape, Acid Ghost; `P28_VersionB_Package.html` [disk] | — | — | Owner: new version, max 5 visuals, motion | **lost** — before the compaction boundary (16:04Z) [snap S4 window] |
| S4b | Build B + rev 1 + rev 2 (Opus, 14–15 Oct) | unplanned | Page `P28B_Lifespan` 5 visuals; rev 1 hover cards + text ×1.3; rev 2 flip spotlight [HO S4 §2] | "Text too small" (twice), "tooltip boring" | — | — | **lost** (same) |
| S4c | B rev 3 (Opus, 15 Oct) | unplanned | Text ×1.5, canvas group-opacity fix, flip banner, TT_NightmareB [chat] | Stray "as a child → now" on the idle page — canvas renderer; flip card on its line | **§162a**, §162e | — | in S4 fragment |
| S4d | Version C brainstorm + package (Fable, 16 Oct 23:31) | unplanned | Blend A (portrait, palette, night→day) + B (graveyard, flip, motion, 5 visuals); claim 48→14 · 105→96 · 28→66; scorecard; `P28_VersionC_Package.html` [disk] | B's ambient loop fails WCAG 2.2.2 | §162c | **Owner picks C direction** | in S4 fragment |
| S4e | Build C (Opus, 16–17 Oct 23:48–00:14) | unplanned | 2 measures, background PNG, page `P28C_Costume` 5 visuals; canvas harness 19 states / 961 texts / 0 issues; placed with hash guard [chat] | Harness read 0 texts (walker), bold measured as regular, "10 10" touching | **§162b** | — | in S4 fragment |
| S4f | Pick, cleanup, check, submit (17 Oct 00:14–00:47) | Session 4 of the original plan | Owner picked C; 7 pages + 5 images moved to `_removed_after_C_pick/`; live DAX 105→96, 48→14, 28→66, 16/47/8, nightmares, War 19, Financial 11 all matched [DAX]; header icons off; owner saved `Fear changes costume.pbix` (16:26Z) and **submitted** 00:47 [chat] | Header icons over "66" and "BORN" (host chrome — only visible in Desktop) | §162d | — | in S4 fragment |
| S4g | Closure (this) | Skill 10 | Two tool defects found and fixed (§162j cost merge; lint rule §162a) | The cost merge itself dropped S4 | **§162j** | — | in S4 fragment |

S4 fragment total (window 14 Oct 16:04Z → 17 Oct): **≥ 199 turns, ≥ 1.0 h, ≥ 60.7 M cache read** at the 00:16 capture [snap]; recaptured at the end of closure (C8).

## Cross-phase patterns
1. **Every defect the owner reported was one an offline render could not show at the size it would be read.** "Text too small" ×3 (A round 1, B twice) was page-scale legibility: specs sized at canvas pixels, read at Fit-to-page (~0.47×). C set a 15 px floor at page scale before drawing and got no size complaint.
2. **Two of four renderer/host defects were invisible to the checking medium, not to the checker.** Canvas vs SVG group opacity (stray labels) and host chrome (visual header) — see C6.
3. **The work tripled by choice, not by rework.** A was built, validated and saved before B was asked for; C was a synthesis of A and B. None of A's or B's build was wrong; both were superseded by preference. See C2's split.
4. **Each harness lied once before it told the truth** — the overlap checker read 0 texts; the font registration measured bold as regular; the cost merge dropped a session. All three were caught by using them, and each now refuses to run blind (§162b, §162j).

## Every count this project asserted, enumerated
| # | Count as asserted | Where | Reconciled | Basis |
|---|---|---|---|---|
| 1 | "E02–E22" (21 element ids) vs "**26 visuals**" for Version A | S3 HO §2 vs summary | 21 ids + E07b/E10b/E14b legends + E12a + E16 ×3 note lines = 26; folder count **26** | [disk] `_removed_after_C_pick/pages/a602…/visuals` |
| 2 | "53 measures" (S3) | S3 HO | now **55** = 53 + 2 (Version C); `_Measures` holds 61 incl. 6 starter | [disk] grep `displayFolder: P28` = 55 |
| 3 | S2 snapshot "165 turns, 0.46 h, 57.9 M" | S2 HO | file now reads **174 / 0.49 h / 62.7 M** — recaptured after the handover (close ritual ran on) | [snap] |
| 4 | Contrast pairs: A 20, B 20 (S2); "15 pairs" (B package); 27 (C mockup); 19 (C final) | 4 places | different scopes: S2 = drawn pairs per mockup; B pkg = B poster only; C mockup = every drawn pair; C final = **text pairs only**, min 4.54 : 1 | [disk] contrast JSONs + final check |
| 5 | Born fears "8" (page) vs **11** (model) | page vs DAX | 3 "Other Responses" (None of these, Prefer not, Something else) excluded by the graveyard filter | [DAX] |
| 6 | "Desktop rewrote **40 of 80** generated files" | S3 HO TL;DR | **no list behind it survives**; the pre-save scratch copy was not kept. Unverifiable — recorded as such | — |
| 7 | "3 render rounds" (A); B rev 1–3; C 1 build + 1 fix | HOs | A 3 · B 3 (+ build) · C 1 + header fix = 8 placements of report files | [HO] + [chat] |
| 8 | Harness "19 states, 961 text items, 0 issues" | S4 | re-run on the **shipped bytes** (specs pulled out of visual.json) — same 19 / 961 / 0 | [disk] `out_shipped/report.json` |
| 9 | Removed "7 pages + 5 images" | S4 | 7 page folders + 5 resource files = **12 moves**, 58 files | [disk] |
| 10 | CLI warnings 8 → 7 | S4 | 8 before cleanup; the cleanup removed one schema-unreachable file class; all `PBIR_SCHEMA_UNREACHABLE` | [disk] CLI JSON |
| 11 | Estate sweep "349 visual.json, 0 instances" | closure | 79 + 149 + 79 + 42 = 349 across P07/P15/P16/P22 | [disk] `[scan]` lines |
| 12 | engine-expansion merge "2,221" | my first §162j draft | **wrong** — today's merge over 12 snapshots reads **2,654**; corrected in 4 places same session | [snap] merge |
