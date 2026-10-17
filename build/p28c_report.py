"""P28 Version C - adds page P28C_Costume ("Fear changes costume", portrait 1357 x 1920) to the SAVED report,
two measures to _Measures.tmdl, and one background image. Run on a SCRATCH copy only (guide 126): it refuses to
overwrite anything that exists. Usage: python3 p28c_report.py <project dir containing the .Report and .SemanticModel>"""
import json, os, sys, uuid, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p28c_deneb as DN

ROOT = sys.argv[1]; BG_PNG = sys.argv[2]
REP = os.path.join(ROOT, "Halloween Contest 2026 - Starter File.Report")
SM = os.path.join(ROOT, "Halloween Contest 2026 - Starter File.SemanticModel")
DEF = os.path.join(REP, "definition"); PAGES = os.path.join(DEF, "pages")
PAGE, BGNAME = "P28C_Costume", "P28C_Background.png"
VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json"
PG = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
DENEB = "deneb7E15AEF80B9E4D4F8E12924291ECE89A"
MT = "_Measures"


def lit(x): return {"expr": {"Literal": {"Value": x}}}
def s(x): return lit("'" + str(x).replace("'", "''") + "'")
def n(x): return lit(f"{x}D")
def b(x): return lit("true" if x else "false")
def col(h): return {"solid": {"color": s(h)}}
def mref(m, ent=MT): return {"Measure": {"Expression": {"SourceRef": {"Entity": ent}}, "Property": m}}
def cref(e, c): return {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": c}}


def proj(f):
    k = "Measure" if "Measure" in f else "Column"
    e, p = f[k]["Expression"]["SourceRef"]["Entity"], f[k]["Property"]
    return {"field": f, "queryRef": f"{e}.{p}", "nativeQueryRef": p}


def vco(alt):
    return {"title": [{"properties": {"show": b(False)}}], "background": [{"properties": {"show": b(False)}}],
            "border": [{"properties": {"show": b(False)}}],
            "padding": [{"properties": {"top": n(0), "bottom": n(0), "left": n(0), "right": n(0)}}],
            "general": [{"properties": {"altText": s(alt)}}]}


def deneb(spec, fields, alt):
    return {"visualType": DENEB,
            "query": {"queryState": {"dataset": {"projections": [proj(f) for f in fields]}}, "sortDefinition": {"isDefaultSort": True}},
            "objects": {"display": [{"properties": {}}], "developer": [{"properties": {"version": s("2.0.0.0")}}],
                        "vega": [{"properties": {"provider": s("vega"), "jsonSpec": s(json.dumps(spec, indent=1, ensure_ascii=False)),
                                                 "jsonConfig": s("{}"), "version": s("6.4.0"), "enableTooltips": b(True),
                                                 "enableContextMenu": b(True), "enableHighlight": b(False), "enableSelection": b(False),
                                                 "selectionMaxDataPoints": n(50)}}]},
            "visualContainerObjects": vco(alt)}


ALT = {
    "V1": "Fear changes costume. People who feared the dark and the supernatural fell from 48 to 14; people naming at least one fear fell only from 105 to 96; people fearing loss, money or the future rose from 28 to 66.",
    "V2": "A graveyard of every fear named by 105 people. Sixteen fears nobody holds any more stand as headstones; seven of the nine biggest are Halloween's own: demons, basements, being watched, cemeteries, aliens, clowns, dolls. Forty-seven fears still burn as candles, tallest war (19 people now), uncertainty about the future (14) and death (12); a flame means some kept the fear since childhood. Eight fears rise as ghosts because nobody had them as children, led by financial insecurity (11).",
    "V3": "The morning after: top-12 fears as a child versus now. Only being trapped, snakes and death stay on the list. The dark, heights, demons and dentists drop out; war, uncertainty, financial insecurity and not being good enough enter.",
    "V4": "The data community's own nightmare, one answer each: data arrives a mess (23 of 105), too many versions (19), doesn't add up (17), takes forever (16), wrong hands (14), AI confidently wrong (8), never arrives (6), spotted too late (2). Closing line: we lit lanterns for the dark and set a table for the dead; the future is still waiting for its festival.",
}
FEARCOLS = [cref("DimFear", "Fear"), cref("DimFear", "FearShort"), cref("DimFear", "Category")]
visuals = []


def add(vid, x, y, w, h, visual, tab):
    visuals.append({"$schema": VC, "name": vid,
                    "position": {"x": x, "y": y, "z": 1000 * (len(visuals) + 1), "height": h, "width": w, "tabOrder": tab * 1000},
                    "visual": visual})


add("C1_TitleBand", 0, 0, 1357, 380, deneb(DN.title_band(1357, 380),
    [cref("DimFear", "Beat"), mref("People Childhood"), mref("People Adult"),
     mref("People Naming A Fear Childhood"), mref("People Naming A Fear Adult")], ALT["V1"]), 1)
add("C2_Graveyard", 0, 390, 1357, 690, deneb(DN.graveyard(1357, 690),
    FEARCOLS + [mref("People Childhood"), mref("People Adult"), mref("People Kept")], ALT["V2"]), 2)
add("C3_MorningAfter", 60, 1160, 1237, 440, deneb(DN.flip(1237, 440),
    FEARCOLS + [mref("People Childhood"), mref("People Adult")], ALT["V3"]), 3)
add("C4_DataNightmare", 60, 1612, 1237, 240, deneb(DN.nightmare(1237, 240),
    [cref("DataNightmare", "Nightmare"), cref("DataNightmare", "dataNightmare"), mref("Nightmare Respondents"), mref("Nightmare Rank"),
     mref("Nightmare Share"), mref("Respondents"), mref("TT Nightmare Sentence")], ALT["V4"]), 4)
foot = [("105 people, self-reported · 62 men, 41 women, 2 another or not stated · 75 aged 25–44 · about two-thirds in Europe · up to 3 fears per life stage"),
        ("Counts are people unless marked picks · Data: Microsoft Fabric Community Halloween survey 2026, provided dataset, unmodified")]
add("C5_Footer", 60, 1852, 1237, 56, {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [
    {"textRuns": [{"value": t, "textStyle": {"fontFamily": "Segoe UI", "fontSize": "11.5pt", "color": DN.MUTED}}], "horizontalTextAlignment": "center"}
    for t in foot]}}]},
    "visualContainerObjects": {"background": [{"properties": {"show": b(False)}}], "border": [{"properties": {"show": b(False)}}],
                               "padding": [{"properties": {"top": n(0), "bottom": n(0), "left": n(0), "right": n(0)}}]}}, 5)


def dump(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, indent=2, ensure_ascii=False)
    json.load(open(p, encoding="utf-8"))


# ---- 1 model: two measures (CRLF, tab-indented, before the hidden column)
mt = os.path.join(SM, "definition", "tables", "_Measures.tmdl")
raw = open(mt, "rb").read().decode("utf-8")
assert raw.count("\r\n") > 100 and raw.count("\n") == raw.count("\r\n"), "_Measures.tmdl is not pure CRLF"
NEW = [("People Naming A Fear Childhood", "Childhood"), ("People Naming A Fear Adult", "Adult")]
for nm, _ in NEW:
    if f"measure '{nm}'" in raw:
        sys.exit(f"measure {nm} already exists - refusing")
block = ""
for nm, stage in NEW:
    block += (f"\t/// People who named at least one real fear as {'a child' if stage == 'Childhood' else 'an adult'} (excludes None of these / Prefer not to answer / Something else). Ignores any DimFear[Beat] filter.\r\n"
              f"\tmeasure '{nm}' = CALCULATE ( [People {stage}], DimFear[Beat] IN {{ 1, 2, 3 }} )\r\n"
              f"\t\tformatString: #,##0\r\n\t\tdisplayFolder: P28\r\n"
              f"\t\tlineageTag: {uuid.uuid5(uuid.NAMESPACE_URL, 'p28-measure-' + nm)}\r\n\r\n")
anchor = "\tcolumn Column1\r\n"
assert raw.count(anchor) == 1
raw = raw.replace(anchor, block + anchor)
open(mt, "wb").write(raw.encode("utf-8"))
# ---- 2 background image
rr = os.path.join(REP, "StaticResources", "RegisteredResources", BGNAME)
if os.path.exists(rr):
    sys.exit(f"{BGNAME} already exists - refusing")
shutil.copyfile(BG_PNG, rr)
rj = os.path.join(DEF, "report.json"); rep = json.load(open(rj, encoding="utf-8"))
pk = [p for p in rep["resourcePackages"] if p["type"] == "RegisteredResources"][0]
assert not any(i["name"] == BGNAME for i in pk["items"])
pk["items"].append({"name": BGNAME, "path": BGNAME, "type": "Image"})
dump(rj, rep)
# ---- 3 page
pdir = os.path.join(PAGES, PAGE)
if os.path.exists(pdir):
    sys.exit(f"{PAGE} already exists - refusing")
dump(os.path.join(pdir, "page.json"), {
    "$schema": PG, "name": PAGE, "displayName": "Fear changes costume", "displayOption": "FitToWidth", "height": 1920, "width": 1357,
    "objects": {"background": [{"properties": {"image": {"image": {
        "name": s(BGNAME), "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": BGNAME}}},
        "scaling": s("Fit")}}, "transparency": n(0)}}],
        "outspace": [{"properties": {"color": col("#120933")}}]}})
for vv in visuals:
    dump(os.path.join(pdir, "visuals", vv["name"], "visual.json"), vv)
pj = os.path.join(PAGES, "pages.json"); pages = json.load(open(pj, encoding="utf-8"))
if PAGE not in pages["pageOrder"]:
    pages["pageOrder"].append(PAGE)
pages["activePageName"] = PAGE
dump(pj, pages)
print(f"page {PAGE}: {len(visuals)} visuals · measures +{len(NEW)} · image {BGNAME} · pageOrder {len(pages['pageOrder'])}")
