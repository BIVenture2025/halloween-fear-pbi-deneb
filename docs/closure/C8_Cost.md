# P28 — C8 Cost analysis and the ledger row

Source: `capture_session_cost.py --merge _cost/` (tool sha1 f0c4aff298, the windows-aware dedupe fixed this closure — §162j). Run 2026-10-17 ~01:10 MYT.

| S | Phase | Turns | Active h | Cache read | cr / turn | Output | Caveat |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Brainstorm (Cowork, Fable) | — | — | — | — | — | **missing** — no transcript tool in that session |
| 2 | Contract, mockups A/B, package | 174 | 0.49 | 62,674,876 | 360,200 | 317,976 | complete |
| 3 | Build Version A | 242 | 0.73 | 93,658,060 | 387,017 | 404,675 | complete (window 14 Oct 11:33–14:13Z) |
| 4 | B rev 3, C brainstorm + build, cleanup, submit, closure | 340 | 1.9 | 137,025,397 | 403,016 | — | **partial**: window starts at the compaction boundary 14 Oct 16:04Z; the B brainstorm, B build and revs 1–2 (14 Oct ~14:15–16:04Z) are **not on disk** |
| | **Total (floor)** | **≥ 756** | **≥ 3.1** | **≥ 293,358,333** | **388,040** | **≥ 1,293,412** | 428 tool calls · browser 0 % · 0 subagent transcripts |

**Ledger row** (appended to `_ENGINE/reference/PROJECT_COST_LEDGER.md`, tool-marked): `INCOMPLETE, missing sessions [1] · PARTIAL (compaction) in sessions [4]`.

**cache_read_per_turn by session: 360 k → 387 k → 403 k.** Rising, which is the signal the split-session hypothesis says should not appear — but S4 is one 2.5-day conversation holding three phases plus closure, not a split session, so it does not test the hypothesis; it is the expected shape of a long single context. Basis: the S4 snapshot's window and turn count.

**What the tool fix changed:** before §162j, the merge dropped S4 entirely as a "compaction fragment superseded by S3" and reported 416 turns / 1.2 h. The real floor is 756 turns / 3.1 h — the old figure under-reported this project by **45 % of turns and 61 % of active time**.

**Tool mix:** 0 % browser; the work ran through the device shell (generation, validation, rendering), the device bridge (staging renders to view them), and the local modeling MCP (two live DAX read-backs).
