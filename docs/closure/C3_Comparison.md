# P28 — C3 Comparison with the previous comparable project

**Which project is comparable.** The last Power BI *report* project (not Fabric Type D) is **Project 22 — Pricing Experimentation Lab**: PBIP, Deneb ×2, a mockup package, last edited 2026-07-28 [disk mtimes]. Its folder says **WIP**; it has **no handover, status or closure document**, so its record cannot be read — only its artefacts. (P21 Chanel is also WIP, last edit 2026-07-23, HTML Content not Deneb.) Comparison is therefore artefact against artefact.

| | P22 PriceLab | P28 Halloween (submitted C) |
|---|---|---|
| Pages / size | 7 pages, 1280 × 720 (+ a 860 × 550 cover) | 1 page, 1357 × 1920 portrait |
| Visuals | 42 (12 textbox, 6 shape, 6 pageNavigator, 4 slicer, 4 card, **2 Deneb**…) | **5** (4 Deneb + 1 textbox) |
| Measures | 66 | 55 in folder P28 (61 in `_Measures`) |
| Interaction | navigation, slicers | none needed; hover cards in-spec; motion 4.5 s |
| Validation | `validate_pbip` 0 DENEB_HOVER findings (42 read) | 1 starter-owned error; CLI 0; canvas harness 961 texts 0 issues; live DAX all matched |

**Reused from earlier projects:** the PBIR generator pattern (scratch copy + hash guard, guide §126), the Deneb container recipe, the theme component, `pack_project_html.py`, the live DAX read-back route.

**What P28 learned that P22's record does not reflect:** (1) canvas group opacity (§162a) — P22's two Deneb visuals have no hover groups, linted clean, so no live defect; (2) a page-scale typographic floor and a canvas layout proof (§162b); (3) motion must end (§162c); (4) poster pages turn the visual header off (§162d).

**Earlier numbers this project corrects:** not P22's (it has none) — the **engine-expansion cost record**: Session 10's "2,221 → 2,171" dedupe dropped 05b's 50 real turns (§162j; correction appended to `HANDOVER_SESSION10.md`).

**Open item for P22's record:** its folder says WIP with no status file; whether it was delivered is unknown from the record. Flagged, not touched.
