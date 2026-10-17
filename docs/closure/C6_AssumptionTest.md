# P28 — C6 Test one assumption

**The assumption:** *"An offline Deneb render is a sufficient pre-Desktop check"* (S3 F5: "it caught label overlap and edge clipping before Desktop did"). Every placement in S3–S4 relied on it.

**Test.** Classify every defect the owner found in Desktop (screenshots, S3–S4) by whether an offline render could have shown it.

| Desktop defect | Round | SVG render (S3 harness) | Canvas render (S4 harness) | Why |
|---|---|---|---|---|
| Table/cards scroll or paint tiles (A) | A r1–2 | n/a (native visuals) | n/a | not Deneb |
| Text too small (A, B ×2) | A r1, B r1, B r2 | **no** | **no** by overlap test; **yes** by font-floor assertion at page scale | a scale question, not a render question |
| Flip tooltip on its line (B) | B r2 | yes, if hovered state rendered and looked at | **yes** (hover states) | rendering was available; the hover state was not in the check |
| Stray "as a child → now" (B) | B r2 | **no** — SVG hides group children | **yes** in the image; overlap test would NOT flag (nothing overlapped) | renderer semantics |
| Header icons over "66" / "BORN" (C) | C | **no** | **no** | host chrome — exists only in Desktop |

**Result.** 6 Deneb-relevant defect reports: SVG render could show **1** (with the hover state); canvas render + font floor + hover states could show **4**; **1 cannot be shown offline at all** (host chrome). And one of the canvas "yes" answers needs a human to *look* — the automated overlap rule would have passed it.

**Conclusion.** The assumption was **false as stated**. An offline render is *necessary* (it caught 7 defects in C before Desktop) but *not sufficient*: it must be canvas, it must include hover states and a page-scale font floor, and a Desktop look remains mandatory for host chrome. Confound: the canvas harness was written *after* these defects were known, so its "yes" column is partly hindsight — the column records what it **can** show, not what it would have been pointed at.

Secondary (not tested, recorded): *"splitting sessions keeps cache-read per turn flat"* — S2 360 k, S3 387 k, S4 ≥ 305 k (fragment, after compaction). The S4 figure is post-compaction and partial; the data does not settle it.
