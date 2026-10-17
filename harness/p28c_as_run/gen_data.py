"""Test data for the Version C specs, replayed from survey_responses.csv + the V2/V3 dataset used for Version B."""
import csv, json, os, sys, re, collections
P = os.path.expanduser("~/mnt/Power BI Automation Engine/Projects/28) Halloween Data Visualization Contest!")
sys.path.insert(0, os.path.expanduser("~/w/build")); import p28c_deneb as d
rows = list(csv.DictReader(open(f"{P}/survey_responses.csv", encoding="utf-8-sig")))
txt = open(f"{P}/P28_DataContract.md", encoding="utf-8").read(); txt = txt[txt.index("### Every fear label"):txt.index("### Unmodelled")]
cat = {}
for ln in txt.split("\n"):
    m = re.match(r"^\| (.+?) \| (.+?) \| (\d+) \| (\d+) \| ([+-]?\d+) \| (\d+) \|$", ln.strip())
    if m and m.group(1) != "Fear": cat[m.group(1)] = m.group(2)
beat = lambda c: 1 if c == d.DARK else 3 if c in ("Separation & Loss", "Performance & Future") else 0 if c == "Other Responses" else 2
pk = lambda s: set(x.strip() for x in json.loads(s))
v1 = []
fc = sum(1 for r in rows if any(beat(cat[f]) > 0 for f in pk(r["childhoodFearsJson"])))
fa = sum(1 for r in rows if any(beat(cat[f]) > 0 for f in pk(r["currentFearsJson"])))
for b in range(4):
    v1.append({"Beat": b, "People Childhood": sum(1 for r in rows if any(beat(cat[f]) == b for f in pk(r["childhoodFearsJson"]))),
               "People Adult": sum(1 for r in rows if any(beat(cat[f]) == b for f in pk(r["currentFearsJson"]))),
               "People Naming A Fear Childhood": fc, "People Naming A Fear Adult": fa})
print("V1", v1)
cnt = collections.Counter(r["dataNightmare"] for r in rows)
v4 = []
for i, (k, n) in enumerate(cnt.most_common()):
    tools = collections.Counter(t for r in rows if r["dataNightmare"] == k for t in pk(r["fabricToolsJson"]) if t != "None yet")
    top = sorted(tools.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    tl = ", ".join(f"{a} ({b})" for a, b in top)
    v4.append({"Nightmare": k.split(" (")[0], "dataNightmare": k, "Nightmare Respondents": n, "Nightmare Rank": i + 1,
               "Nightmare Share": n / 105, "Respondents": 105, "TT Nightmare Sentence": f"{n} of 105 chose: {k}. Their most-used Fabric tools: {tl}."})
print("V4", [(x["Nightmare"], x["Nightmare Respondents"]) for x in v4]); print(v4[0]["TT Nightmare Sentence"])
old = json.load(open(os.path.expanduser("~/w/vega/b_v2.json")))
v23 = [x for x in old["data"] if x["name"] == "dataset"][0]["values"]
json.dump({"V1": v1, "V2": v23, "V3": v23, "V4": v4}, open(os.path.expanduser("~/w/vc/testdata.json"), "w"), ensure_ascii=False)
