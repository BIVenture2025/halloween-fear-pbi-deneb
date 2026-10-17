# P28 — C7 Folder disposition (owner-approved 2026-10-17 01:2x MYT: "Keep A/B material in place")

| Path | Class | Reason |
|---|---|---|
| `Fear changes costume.pbix` | Keep–deliverable | the submitted file (read: 1 page, 5 visuals, Deneb embedded) |
| `Fear changes costume.mp4`, `Pic.png` | Keep–deliverable | owner's demo video and post image |
| `Version1.pbix`, `Version 2.pbix` | Keep–deliverable | owner's backups of A and B |
| `Halloween Contest 2026 - Starter File.{Report,SemanticModel,pbip}` | Keep–deliverable | the PBIP working copy of C |
| `P28_VersionC_Package.html`, `HANDOVER.md`, `09_Closure/` | Keep–deliverable | approved package, handover, closure |
| `P28_DataContract.md`, `survey_responses.csv` | Keep–evidence | number source and the provided dataset |
| `00_Plan/` (decisions, handovers S2/S3, kickoffs, `build/` generators + harness) | Keep–evidence | the record; `build/p28b_deneb_r2.py` is the frozen positive control for the lint rule |
| `_cost/` | Keep–evidence | snapshots |
| `01_Mockups/versionC/` | Keep–evidence | C mockup sources and the offline QA renders |
| `P28_Package.html`, `P28_VersionB_Package.html`, `01_Mockups/` A/B material, `00_Plan/_s3_preview/`, `_removed_after_C_pick/`, `00_Plan/SESSION05_KICKOFF.md` | **Kept in place (owner)** — proposed Archive | superseded by C; owner chose to keep them where they are. `versionC/mockup_c.py` imports `versionB/mockup_b.py`, so `versionB/` must stay anyway |
| `01_Mockups/qaA.png`, `01_Mockups/versionB/qa/` | Delete → moved to `_to_delete/` | my scratch renders |
| engine root `_to_delete/P28_S3_retired_visuals/`, `_to_delete/P28_S3_rev2/` | Delete — **already gone** (`ls` 2026-10-17 finds no P28 folder there) | retired S3 visual folders and 3 tooltip pages; removed by the owner earlier |

**Post-move checks:** see C8 / HANDOVER — `validate_pbip.py` and `scrub_check.py` re-run after the move.
