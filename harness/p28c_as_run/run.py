import json, os, sys, subprocess
sys.path.insert(0, os.path.expanduser("~/w/build")); import importlib, p28c_deneb as d; importlib.reload(d)
D = os.path.expanduser("~/w/vc"); td = json.load(open(f"{D}/testdata.json"))
def put(spec, vals):
    for x in spec["data"]:
        if x["name"] == "dataset": x["values"] = vals
    return spec
specs = {"V1": d.title_band(), "V2": d.graveyard(), "V3": d.flip(), "V4": d.nightmare()}
for k, sp in specs.items(): json.dump(put(sp, td[k]), open(f"{D}/c_{k}.json", "w"), ensure_ascii=False)
L = lambda f: f
jobs = [{"id": "V1", "spec": f"{D}/c_V1.json", "states": [{"name": "idle"}]},
        {"id": "V2", "spec": f"{D}/c_V2.json", "states": [{"name": "idle"}] + [
            {"name": f"hov_{n.split()[0].lower()}", "pick": {"signal": "hov", "data": "pos", "field": "label", "value": n}}
            for n in ["Demons", "War", "Financial insecurity", "Conflict", "Spiders", "Losing a limb", "Getting lost", "The unknown"]]},
        {"id": "V3", "spec": f"{D}/c_V3.json", "states": [{"name": "idle"}] + [
            {"name": f"hov_{n.split()[0].lower()}", "pick": {"signal": "hovD", "data": "rows", "field": "label", "value": n}}
            for n in ["Death", "The dark", "Financial insecurity", "Being laughed at"]]},
        {"id": "V4", "spec": f"{D}/c_V4.json", "states": [{"name": "idle"}] + [
            {"name": f"hov_{i}", "pick": {"signal": "hovN", "data": "rows", "field": "r", "value": i}} for i in (1, 5, 8)]}]
json.dump({"out": f"{D}/out", "minFont": 15, "jobs": jobs}, open(f"{D}/cfg.json", "w"))
os.makedirs(f"{D}/out", exist_ok=True)
r = subprocess.run(["node", os.path.expanduser("~/w/vega/c_check.mjs"), f"{D}/cfg.json"], capture_output=True, text=True, cwd=os.path.expanduser("~/w/vega"), env={**os.environ, "FONTCONFIG_FILE": os.path.expanduser("~/w/vega/fc/fonts.conf")})
print(r.stdout[-6000:], r.stderr[-3000:])
