"""P28 Version C - "Fear changes costume". Deneb (Vega) specs for the portrait page 1357 x 1920.
V1 title band (0,0 1357x380) · V2 graveyard (0,390 1357x690) · V3 the morning after (60,1160 1237x440)
· V4 the data nightmare + sign-off (60,1612 1237x240). Palette A Marigold & Indigo; night half above
y 1080, cream daylight below y 1150 (page background image). Specs set NO background: the page shows through.
Motion: one timer, 4.5 s, then the clock freezes (no ambient loop: WCAG 2.2.2). Every child of a hover
group carries its own opacity (canvas does not inherit group opacity - S3 rev 3).
Typographic floor: no text below 15 px at page scale (MINF), asserted at build time."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p28b_deneb import LABELS

NIGHT, NIGHT2, GROUND, CANDLE = "#1E0F4A", "#120933", "#2A1A5E", "#3A2878"
CREAM, MARI, TURQ, MAG, DIM = "#FFF3DC", "#FFB400", "#3DE0D0", "#FF3D9A", "#B9AEDC"
DAY, INK, HOTMAG, VIOLET, MUTED, CARD = "#FFF3DC", "#1A1528", "#C8006E", "#5B2DBF", "#5A5470", "#FFF9EC"
FONT, DISPLAY = "Segoe UI", "Arial Black"
DARK = "Dark, Unknown & Supernatural"
MINF = 15
SCHEMA = "https://vega.github.io/schema/vega/v5.json"


def v(x):
    return {"value": x}


def s(x):
    return {"signal": x}


def ease(x):
    return f"(1 - pow(1 - clamp({x}, 0, 1), 3))"


def motion(ms=4500):
    # clock stops changing at ms + 100, so the dataflow goes quiet once the intro has played
    return [{"name": "t0", "init": "now()"},
            {"name": "clock", "init": "0", "on": [{"events": {"type": "timer", "throttle": 40}, "update": f"min(now() - t0, {ms + 100})"}]},
            {"name": "t", "update": f"min(1, clock / {ms})"}]


def tx(x, y, text, size, fill, weight=400, align="left", font=FONT, name=None, frm=None, **extra):
    if isinstance(size, (int, float)):
        assert size >= MINF, (size, text)
    enc = {"x": x if isinstance(x, dict) else v(x), "y": y if isinstance(y, dict) else v(y),
           "text": text if isinstance(text, dict) else v(text),
           "fontSize": size if isinstance(size, dict) else v(size), "fill": fill if isinstance(fill, dict) else v(fill),
           "fontWeight": v(weight), "align": v(align), "font": v(font), "baseline": v("alphabetic")}
    enc.update(extra)
    m = {"type": "text", "encode": {"update": enc}}
    if name:
        m["name"] = name
    if frm:
        m["from"] = {"data": frm}
    return m


def uniq(spec):
    """Vega mark names must be unique; decor marks share a prefix, so number the repeats."""
    seen = {}
    def go(ms):
        for m in ms:
            nm = m.get("name")
            if nm:
                seen[nm] = seen.get(nm, 0) + 1
                if seen[nm] > 1:
                    m["name"] = f"{nm}_{seen[nm]}"
            go(m.get("marks", []))
    go(spec["marks"])
    return spec


def _hide(marks, on):
    for m in marks:
        m["interactive"] = False
        m["encode"]["update"]["opacity"] = s(on)
    return marks


def lantern(x, y, col, sz=8, frm=None, op=None, name="bg_lantern"):
    """Original glyph: round paper lantern with cap and handle. x, y are signal strings (centre of the body)."""
    p = (f"'M' + ({x} - {sz * .45}) + ' ' + ({y} - {sz * 1.55}) + ' q{sz * .45} -{sz * .6} {sz * .9} 0' + "
         f"' M' + ({x} - {sz * .5}) + ' ' + ({y} - {sz * 1.5}) + ' h{sz}' + "
         f"' M' + ({x} - {sz * .7}) + ' ' + ({y}) + ' a{sz * .7} {sz * .78} 0 1 0 {sz * 1.4} 0 a{sz * .7} {sz * .78} 0 1 0 -{sz * 1.4} 0' + "
         f"' M' + ({x}) + ' ' + ({y} - {sz * .78}) + ' v{sz * 1.56}' + ' M' + ({x} - {sz * .5}) + ' ' + ({y} + {sz * .95}) + ' h{sz}'")
    m = {"type": "path", "name": name, "interactive": False, "encode": {"update": {
        "path": s(p), "stroke": v(col), "strokeWidth": v(1.6), "fill": v(None) if False else {"value": "transparent"}}}}
    if op:
        m["encode"]["update"]["opacity"] = s(op)
    if frm:
        m["from"] = {"data": frm}
    return m


# ===================================================================== V1 title band
def title_band(w=1357, h=380):
    cols = [(60, "HALLOWEEN'S OWN FEARS", "hc", "ha", TURQ, "people afraid of the dark & the supernatural"),
            (486, "FEAR ITSELF", "fc", "fa", CREAM, "people naming at least one fear"),
            (912, "THE NEW FEARS", "nc", "na", MARI, "people afraid of loss, money, the future")]
    first = lambda ds, f: f"length(data('{ds}')) ? (data('{ds}')[0]['{f}'] || 0) : 0"
    sig = motion() + [
        {"name": "hc", "update": first("b1", "People Childhood")}, {"name": "ha", "update": first("b1", "People Adult")},
        {"name": "nc", "update": first("b3", "People Childhood")}, {"name": "na", "update": first("b3", "People Adult")},
        {"name": "fc", "update": first("dataset", "People Naming A Fear Childhood")},
        {"name": "fa", "update": first("dataset", "People Naming A Fear Adult")}]
    data = [{"name": "dataset"},
            {"name": "b1", "source": "dataset", "transform": [{"type": "filter", "expr": "datum.Beat === 1"}]},
            {"name": "b3", "source": "dataset", "transform": [{"type": "filter", "expr": "datum.Beat === 3"}]}]
    marks = []
    for i, (sx, sy) in enumerate([(1190, 40), (1250, 96), (1318, 30), (1300, 168), (1214, 214), (1336, 236)]):
        marks.append({"type": "symbol", "name": "bg_star", "interactive": False, "encode": {"update": {
            "x": v(sx), "y": v(sy), "shape": v("circle"), "size": v(9 if i % 2 else 16), "fill": v(CREAM),
            "opacity": s(f"0.7 - 0.35 * {ease('t')}")}}})
    marks += [
        tx(60, 52, "WHAT KEEPS YOU UP AT NIGHT?  ·  105 PEOPLE, THEN AND NOW", 16, MARI, 700),
        tx(56, 142, "Fear changes costume", 84, CREAM, 900, font=DISPLAY),
        tx(60, 192, "We outgrew the fears Halloween is made of.", 22, DIM),
        tx(60, 222, "We did not outgrow fear — it moved to things nobody carves a lantern for.", 22, DIM)]
    for i, (x, head, a, b, col, sub) in enumerate(cols):
        e = ease(f"t * 1.6 - {i * 0.12}")
        marks += [
            tx(x, 270, head, 15, col, 700),
            tx(x + 122, 336, s(f"format(round({a} * {e}), ',')"), 56, DIM, 900, "right", DISPLAY),
            tx(x + 154, 326, "→", 30, DIM, 400, "center"),
            tx(x + 186, 336, s(f"format(round({b} * {e}), ',')"), 56, col, 900, "left", DISPLAY),
            tx(x, 366, sub, 16, DIM)]
    return uniq({"$schema": SCHEMA, "description": "P28 C / V1 title band: three before-and-after counts count up on open.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "signals": sig, "data": data, "marks": marks})


# ===================================================================== V2 graveyard
GEO = dict(X0=40, SD=32, HW=28, SDS=12, HWS=10, G=20, SC=29, CW=14, SCM=9, CWM=6, SCS=6, CWS=4, GAP=8, UNIT=13)


def graveyard(w=1357, h=690):
    gy = 545
    g = GEO
    labels = [{"Fear": k, "label": vv} for k, vv in LABELS.items()]
    data = [
        {"name": "dataset"}, {"name": "labels", "values": labels},
        {"name": "rows", "source": "dataset", "transform": [
            {"type": "filter", "expr": "datum.Category !== 'Other Responses'"},
            {"type": "formula", "as": "c", "expr": "datum['People Childhood'] || 0"},
            {"type": "formula", "as": "a", "expr": "datum['People Adult'] || 0"},
            {"type": "formula", "as": "k", "expr": "datum['People Kept'] || 0"},
            {"type": "filter", "expr": "datum.c > 0 || datum.a > 0"},
            {"type": "lookup", "from": "labels", "key": "Fear", "fields": ["Fear"], "values": ["label"], "as": ["lab0"]},
            {"type": "formula", "as": "label", "expr": "datum.lab0 || datum.FearShort || datum.Fear"},
            {"type": "formula", "as": "hal", "expr": f"datum.Category === '{DARK}'"},
            {"type": "formula", "as": "kind", "expr": "datum.a === 0 ? 'dead' : datum.c === 0 ? 'born' : 'alive'"},
            {"type": "formula", "as": "size", "expr": "datum.kind === 'dead' ? datum.c : datum.a"},
            {"type": "formula", "as": "tier", "expr":
                "datum.kind === 'dead' ? (datum.c >= 3 ? 0 : 1) : datum.kind === 'born' ? 0 : (datum.a >= 6 ? 0 : datum.a >= 3 ? 1 : 2)"},
            {"type": "formula", "as": "gw", "expr": "16 + datum.a * 1.5"},
            {"type": "formula", "as": "gstep", "expr": "datum.kind === 'born' ? (datum.a >= 3 ? max(datum.gw + 4, 30) : datum.gw + 4) : 0"},
            {"type": "window", "groupby": ["kind", "tier"], "sort": {"field": ["size", "label"], "order": ["descending", "ascending"]},
             "ops": ["row_number", "sum"], "fields": [None, "gstep"], "as": ["rn", "gcum"], "frame": [None, 0]}]}]
    for nm, ex in [("deadT0", "datum.kind === 'dead' && datum.tier === 0"), ("deadT1", "datum.kind === 'dead' && datum.tier === 1"),
                   ("aliveT0", "datum.kind === 'alive' && datum.tier === 0"), ("aliveT1", "datum.kind === 'alive' && datum.tier === 1"),
                   ("aliveT2", "datum.kind === 'alive' && datum.tier === 2"), ("bornAll", "datum.kind === 'born'"),
                   ("halBig", "datum.kind === 'dead' && datum.tier === 0 && datum.hal"), ("aliveAll", "datum.kind === 'alive'"),
                   ("deadAll", "datum.kind === 'dead'")]:
        data.append({"name": nm, "source": "rows", "transform": [{"type": "filter", "expr": ex}]})
    n = lambda ds: f"length(data('{ds}'))"
    sig = motion() + [
        {"name": "nD0", "update": n("deadT0")}, {"name": "nD1", "update": n("deadT1")}, {"name": "nD", "update": n("deadAll")},
        {"name": "nA0", "update": n("aliveT0")}, {"name": "nA1", "update": n("aliveT1")}, {"name": "nA2", "update": n("aliveT2")},
        {"name": "nA", "update": n("aliveAll")}, {"name": "nB", "update": n("bornAll")}, {"name": "nHal", "update": n("halBig")},
        {"name": "dEnd0", "update": f"{g['X0']} + nD0 * {g['SD']}"},
        {"name": "dEnd", "update": f"dEnd0 + {g['GAP']} + nD1 * {g['SDS']}"},
        {"name": "C0", "update": f"dEnd + {g['G']}"},
        {"name": "cEnd0", "update": f"C0 + nA0 * {g['SC']}"},
        {"name": "cEnd1", "update": f"cEnd0 + {g['GAP']} + nA1 * {g['SCM']}"},
        {"name": "cEnd", "update": f"cEnd1 + {g['GAP']} + nA2 * {g['SCS']}"},
        {"name": "B0", "update": f"cEnd + {g['G']}"},
        {"name": "hov", "value": None, "on": [{"events": "@hit:mouseover", "update": "datum"}, {"events": "@hit:mouseout", "update": "null"}]}]
    data.append({"name": "pos", "source": "rows", "transform": [
        {"type": "formula", "as": "idx", "expr":
            "datum.kind === 'dead' ? (datum.tier === 0 ? datum.rn - 1 : nD0 + datum.rn - 1) : datum.kind === 'born' ? datum.rn - 1 : "
            "(datum.tier === 0 ? datum.rn - 1 : datum.tier === 1 ? nA0 + datum.rn - 1 : nA0 + nA1 + datum.rn - 1)"},
        {"type": "formula", "as": "x", "expr":
            f"datum.kind === 'dead' ? (datum.tier === 0 ? {g['X0']} + {g['HW'] / 2} + (datum.rn - 1) * {g['SD']} : dEnd0 + {g['GAP']} + {g['HWS'] / 2} + (datum.rn - 1) * {g['SDS']}) : "
            f"datum.kind === 'born' ? B0 + datum.gcum - datum.gstep + datum.gw / 2 : "
            f"(datum.tier === 0 ? C0 + {g['CW'] / 2} + (datum.rn - 1) * {g['SC']} : datum.tier === 1 ? cEnd0 + {g['GAP']} + {g['CWM'] / 2} + (datum.rn - 1) * {g['SCM']} : "
            f"cEnd1 + {g['GAP']} + {g['CWS'] / 2} + (datum.rn - 1) * {g['SCS']})"},
        {"type": "formula", "as": "hw", "expr": f"datum.c >= 3 ? {g['HW']} : {g['HWS']}"},
        {"type": "formula", "as": "hfull", "expr": f"22 + datum.c * {g['UNIT']}"},
        {"type": "formula", "as": "cw", "expr": f"datum.a >= 6 ? {g['CW']} : datum.a >= 3 ? {g['CWM']} : {g['CWS']}"},
        {"type": "formula", "as": "cfull", "expr": f"12 + datum.a * {g['UNIT']}"},
        {"type": "formula", "as": "fr", "expr": "datum.k > 0 ? min(3.5 + 1.8 * datum.k, datum.a >= 6 ? 12 : datum.a >= 3 ? 5 : 2.5) : 0"},
        {"type": "formula", "as": "gh", "expr": "20 + datum.a * 8.5"},
        {"type": "formula", "as": "top", "expr":
            "datum.kind === 'dead' ? datum.hfull + (datum.hal && datum.c >= 3 ? 22 : 0) : datum.kind === 'born' ? datum.gh + 46 : "
            "datum.cfull + 7 + 2 * datum.fr + (datum.a >= 6 ? 26 : 0) + (datum.k === 0 ? 34 : 0)"}]})
    for nm, ex in [("pos_dead", "datum.kind === 'dead'"), ("pos_alive", "datum.kind === 'alive'"), ("pos_born", "datum.kind === 'born'"),
                   ("pos_halbig", "datum.kind === 'dead' && datum.hal && datum.c >= 3")]:
        data.append({"name": nm, "source": "pos", "transform": [{"type": "filter", "expr": ex}]})
    grow = lambda step: ease(f"t * 1.3 - datum.idx * {step}")
    hs = f"datum.hfull * {grow(0.03)}"
    cs = f"datum.cfull * {grow(0.015)}"
    gp = ease("t * 1.4 - 0.25 - datum.idx * 0.05")
    marks = [
        {"type": "symbol", "name": "bg_moon", "interactive": False, "encode": {"update": {
            "x": v(w - 120), "y": v(190), "shape": v("circle"), "size": v(5600), "fill": v(CREAM), "opacity": v(0.95)}}},
        {"type": "symbol", "name": "bg_moon2", "interactive": False, "encode": {"update": {
            "x": v(w - 106), "y": v(180), "shape": v("circle"), "size": v(4300), "fill": v(NIGHT)}}},
        {"type": "rect", "name": "bg_ground", "interactive": False, "encode": {"update": {
            "x": v(0), "y": v(gy), "width": v(w), "height": v(h - gy), "fill": v(GROUND)}}},
        {"type": "rule", "name": "bg_groundline", "interactive": False, "encode": {"update": {
            "x": v(0), "x2": v(w), "y": v(gy), "stroke": v(DIM), "strokeWidth": v(1.5), "opacity": v(0.6)}}}]
    for i in range(3):
        marks.append({"type": "path", "name": "bg_fog", "interactive": False, "encode": {"update": {
            "path": v(f"M{-80 + i * 470} {gy - 6} a300 20 0 1 0 600 0 a300 20 0 1 0 -600 0 Z"),
            "fill": v(CREAM), "opacity": s(f"0.05 * {ease('t * 2')}")}}})
    # zone headers (all prose of the hero lives here)
    marks += [
        tx(g["X0"], 32, "BURIED", 18, TURQ, 700),
        tx(g["X0"], 56, s("nD + ' fears nobody holds now'"), 16, DIM),
        tx(g["X0"] + 18, 80, s("nHal + ' of the ' + nD0 + ' biggest are Halloween\\'s own'"), 16, MARI),
        lantern(f"{g['X0'] + 6}", "75", MARI, 6.5),
        tx(s("C0"), 32, "STILL BURNING", 18, MAG, 700),
        tx(s("C0"), 56, s("nA + ' fears still held · flame = kept since childhood'"), 16, DIM),
        tx(s("C0"), 80, "no flame = feared now by different people", 16, DIM),
        tx(s("B0"), 32, "BORN", 18, MARI, 700),
        tx(s("B0"), 56, s("nB + ' fears new'"), 16, DIM),
        tx(s("B0"), 80, "since childhood", 16, DIM)]
    # headstones
    marks += [
        {"type": "path", "name": "stone", "from": {"data": "pos_dead"}, "encode": {"update": {
            "path": s(f"'M' + (datum.x - datum.hw / 2) + ' {gy} V' + ({gy} - {hs} + datum.hw / 2) + ' A' + (datum.hw / 2) + ' ' + (datum.hw / 2) + ' 0 0 1 ' + (datum.x + datum.hw / 2) + ' ' + ({gy} - {hs} + datum.hw / 2) + ' V{gy} Z'"),
            "fill": v(GROUND), "stroke": v(TURQ), "strokeWidth": v(1.6), "opacity": s(f"{hs} > 1 ? 1 : 0")}}},
        {"type": "rule", "name": "stone_line", "from": {"data": "pos_dead"}, "encode": {"update": {
            "x": s("datum.x - 7"), "x2": s("datum.x + 7"), "y": s(f"{gy} - {hs} + 16"), "stroke": v(TURQ), "strokeWidth": v(1.2),
            "opacity": s(f"datum.c >= 3 && {hs} > 30 ? 1 : 0")}}},
        tx(s("datum.x"), s(f"{gy} - {hs} + 38"), s("datum.c >= 3 ? datum.c : ''"), 19,
           s(f"datum.c >= 3 ? '{CREAM}' : '{DIM}'"), 700, "center", name="in_stone_num", frm="pos_dead", opacity=s(f"{hs} > 10 ? 1 : 0")),
        tx(s("datum.x + 4"), v(gy + 18), s("datum.c >= 3 ? datum.label : ''"), 15, s(f"datum.hal ? '{MARI}' : '{DIM}'"), 400, "right",
           name="lbl_dead", frm="pos_dead", angle=v(-40)),
        lantern("datum.x", f"({gy} - {hs} - 12)", MARI, 7, frm="pos_halbig", op=f"{hs} > 10 ? 1 : 0", name="glyph_lantern")]
    # candles
    ctop = f"({gy} - {cs})"
    fy = f"({ctop} - 7 - datum.fr)"
    marks += [
        {"type": "rect", "name": "candle", "from": {"data": "pos_alive"}, "encode": {"update": {
            "x": s("datum.x - datum.cw / 2"), "width": s("datum.cw"), "y": s(ctop), "y2": v(gy), "cornerRadius": v(2),
            "fill": v(CANDLE), "stroke": v(DIM), "strokeWidth": v(1), "opacity": s(f"{cs} > 1 ? 1 : 0")}}},
        {"type": "rule", "name": "wick", "from": {"data": "pos_alive"}, "encode": {"update": {
            "x": s("datum.x"), "x2": s("datum.x"), "y": s(ctop), "y2": s(f"{ctop} - 5"), "stroke": v(DIM), "strokeWidth": v(1.5),
            "opacity": s(f"{cs} > 2 ? 1 : 0")}}},
        {"type": "path", "name": "flame", "from": {"data": "pos_alive"}, "encode": {"update": {
            "path": s(f"datum.k > 0 ? 'M' + datum.x + ' ' + ({fy} - datum.fr) + ' C' + (datum.x + datum.fr) + ' ' + ({fy} - 0.2 * datum.fr) + ' ' + (datum.x + 0.9 * datum.fr) + ' ' + ({fy} + 0.7 * datum.fr) + ' ' + datum.x + ' ' + ({fy} + datum.fr) + "
                      f"' C' + (datum.x - 0.9 * datum.fr) + ' ' + ({fy} + 0.7 * datum.fr) + ' ' + (datum.x - datum.fr) + ' ' + ({fy} - 0.2 * datum.fr) + ' ' + datum.x + ' ' + ({fy} - datum.fr) + ' Z' : ''"),
            "fill": v(MARI), "opacity": s(f"0.95 * {grow(0.015)}")}}},
        {"type": "symbol", "name": "flame_core", "from": {"data": "pos_alive"}, "encode": {"update": {
            "x": s("datum.x"), "y": s(f"{fy} + 0.35 * datum.fr"), "shape": v("circle"),
            "size": s(f"datum.k > 0 ? pow(datum.fr * 0.75, 2) * {grow(0.015)} : 0"), "fill": v(CREAM), "opacity": v(0.9)}}},
        {"type": "path", "name": "smoke", "from": {"data": "pos_alive"}, "encode": {"update": {
            "path": s(f"datum.k === 0 && {cs} > 4 ? 'M' + datum.x + ' ' + ({ctop} - 7) + ' q4 -7 0 -14 q-4 -7 0 -14' : ''"),
            "stroke": v(DIM), "strokeWidth": v(1.2), "fill": {"value": "transparent"}, "opacity": s(f"0.6 * {grow(0.015)}")}}},
        tx(s("datum.x"), s(f"{ctop} - 7 - (datum.k > 0 ? 2 * datum.fr : 30) - 8"), s("datum.a >= 6 ? datum.a : ''"), 18, CREAM, 700, "center",
           name="candle_num", frm="pos_alive", opacity=s(grow(0.015))),
        tx(s("datum.x + 4"), v(gy + 18), s("datum.a >= 6 ? datum.label : ''"), 15, s(f"datum.hal ? '{MARI}' : '{DIM}'"), 400, "right",
           name="lbl_alive", frm="pos_alive", angle=v(-40))]
    # ghosts (no faces)
    gy0 = f"({gy} - 10 - {gp} * (datum.gh + 36))"
    marks += [
        {"type": "path", "name": "ghost", "from": {"data": "pos_born"}, "encode": {"update": {
            "path": s(f"'M' + (datum.x - datum.gw / 2) + ' ' + ({gy0} + datum.gh) + ' V' + ({gy0} + datum.gw / 2) + "
                      f"' A' + (datum.gw / 2) + ' ' + (datum.gw / 2) + ' 0 0 1 ' + (datum.x + datum.gw / 2) + ' ' + ({gy0} + datum.gw / 2) + "
                      f"' V' + ({gy0} + datum.gh) + ' q' + (-datum.gw / 8) + ' -8 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' 8 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' -8 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' 8 ' + (-datum.gw / 4) + ' 0 Z'"),
            "fill": v(CREAM), "fillOpacity": s(f"0.12 * {gp}"), "stroke": v(MARI), "strokeWidth": v(1.6), "strokeOpacity": s(f"0.95 * {gp}")}}},
        tx(s("datum.x"), s(f"{gy0} + datum.gh * 0.6"), s("datum.a"), s("datum.a >= 3 ? 19 : 15"), CREAM, 700, "center",
           name="in_ghost_num", frm="pos_born", opacity=s(gp)),
        tx(s("datum.x + 4"), v(gy + 18), s("datum.a >= 3 ? datum.label : ''"), 15, DIM, 400, "right",
           name="lbl_born", frm="pos_born", angle=v(-40))]
    marks.append({"type": "rect", "name": "hit", "from": {"data": "pos"}, "encode": {"update": {
        "x": s("datum.x - max(datum.kind === 'dead' ? datum.hw : datum.kind === 'born' ? datum.gw : datum.cw, 6) / 2 - 1"),
        "width": s("max(datum.kind === 'dead' ? datum.hw : datum.kind === 'born' ? datum.gw : datum.cw, 6) + 2"),
        "y": s(f"{gy} - datum.top"), "y2": v(gy + 6), "fill": v("#000000"), "fillOpacity": v(0.001), "cursor": v("pointer")}}})
    marks += graveyard_card(w, gy)
    return uniq({"$schema": SCHEMA, "description": "P28 C / V2 graveyard: every fear as a headstone (nobody holds it now), a candle (still held) or a ghost (new since childhood). Lantern = Halloween's own category.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "signals": sig, "data": data, "marks": marks})


def graveyard_card(w, gy, cw=448, ch=198, top=100):
    on = "hov ? 1 : 0"
    kcol = (f"hov && hov.kind === 'dead' ? '{TURQ}' : hov && hov.kind === 'born' ? '{MARI}' : hov && hov.k === 0 ? '{DIM}' : '{MAG}'")
    cx = f"clamp(hov ? (hov.x < {w * 0.55} ? hov.x + 26 : hov.x - {cw} - 26) : 0, 8, {w - cw - 8})"
    kick = ("hov ? (hov.kind === 'dead' ? 'HERE LIES' : hov.kind === 'born' ? 'BORN IN ADULTHOOD' : hov.k > 0 ? 'STILL BURNING' : 'RELIT BY OTHERS') "
            "+ (hov.hal ? '  ·  HALLOWEEN\\'S OWN' : '') : ''")
    line = ("hov ? (hov.kind === 'dead' ? 'Outgrown by everyone who had it.' : hov.kind === 'born' ? 'Nobody had it as a child.' : "
            "hov.k > 0 ? (hov.k === hov.c ? 'All ' + hov.k + ' never let it go.' : hov.k + ' of ' + hov.c + ' never let it go.') : "
            "'Nobody kept it. Others fear it now.') : ''")
    big = lambda key: f"hov ? (hov.kind === 'born' && '{key}' === 'c' ? '—' : format(hov.{key}, ',')) : ''"
    lab = lambda t: f"hov ? '{t}' : ''"
    C = cw / 2

    def t_(x, y, text, size, fill, weight=400, font=FONT, **extra):
        return tx(x, y, s(text), size, fill if isinstance(fill, dict) else fill, weight, "center", font, **extra)
    kids = [t_(C, s("hov && hov.kind === 'dead' ? 50 : 36"), kick, 16, s(kcol), 700),
            t_(C, s("hov && hov.kind === 'dead' ? 86 : 74"), "hov ? hov.label : ''", 28, CREAM, 700, limit=v(cw - 40)),
            t_(C - 92, 142, big("c"), 40, DIM, 900, DISPLAY),
            t_(C, 134, "hov ? '→' : ''", 28, DIM),
            t_(C + 92, 142, big("a"), 40, s(kcol), 900, DISPLAY),
            t_(C - 92, 169, lab("as a child"), 15, DIM),
            t_(C + 92, 169, lab("now"), 15, DIM),
            t_(C, 191, line, 17, CREAM, 400, fontStyle=v("italic"), limit=v(cw - 30))]
    ey = top + ch / 2
    edge = f"(hov && hov.x < {w * 0.55} ? {cx} : {cx} + {cw})"
    return [
        {"type": "path", "name": "card_link", "interactive": False, "encode": {"update": {
            "path": s(f"hov ? 'M' + {edge} + ' {ey} H' + hov.x + ' V' + ({gy} - hov.top + 4) : ''"),
            "stroke": s(kcol), "strokeDash": v([3, 4]), "strokeWidth": v(1.5), "fill": {"value": "transparent"}, "opacity": s(on)}}},
        {"type": "group", "name": "card", "interactive": False, "encode": {"update": {
            "x": s(cx), "y": v(top), "width": v(cw), "height": v(ch), "fill": v(GROUND), "stroke": s(kcol), "strokeWidth": v(1.8),
            "fillOpacity": s(on), "strokeOpacity": s(on), "opacity": s(on),
            "cornerRadiusTopLeft": s("hov && hov.kind === 'dead' ? 120 : 16"), "cornerRadiusTopRight": s("hov && hov.kind === 'dead' ? 120 : 16"),
            "cornerRadiusBottomLeft": v(16), "cornerRadiusBottomRight": v(16)}},
         "marks": _hide(kids, on)}]


# ===================================================================== V3 the morning after (flip)
def flip(w=1237, h=440, n=12):
    xl, xr, top, rowh = 330, w - 330, 82, 28
    labels = [{"Fear": k, "label": vv} for k, vv in LABELS.items()]
    prog = ease("t * 1.5 - 0.3")
    data = [
        {"name": "dataset"}, {"name": "labels", "values": labels},
        {"name": "rows", "source": "dataset", "transform": [
            {"type": "filter", "expr": "datum.Category !== 'Other Responses'"},
            {"type": "formula", "as": "c", "expr": "datum['People Childhood'] || 0"},
            {"type": "formula", "as": "a", "expr": "datum['People Adult'] || 0"},
            {"type": "lookup", "from": "labels", "key": "Fear", "fields": ["Fear"], "values": ["label"], "as": ["lab0"]},
            {"type": "formula", "as": "label", "expr": "datum.lab0 || datum.FearShort || datum.Fear"},
            {"type": "window", "sort": {"field": ["c", "label"], "order": ["descending", "ascending"]}, "ops": ["row_number"], "as": ["lr"]},
            {"type": "window", "sort": {"field": ["a", "label"], "order": ["descending", "ascending"]}, "ops": ["row_number"], "as": ["rr"]},
            {"type": "filter", "expr": f"datum.lr <= {n} || datum.rr <= {n}"},
            {"type": "formula", "as": "y1", "expr": f"{top} + (min(datum.lr, {n + 1}) - 0.5) * {rowh}"},
            {"type": "formula", "as": "y2", "expr": f"{top} + (min(datum.rr, {n + 1}) - 0.5) * {rowh}"},
            {"type": "formula", "as": "both", "expr": f"datum.lr <= {n} && datum.rr <= {n}"},
            {"type": "formula", "as": "col", "expr": f"datum.rr < datum.lr ? '{VIOLET}' : datum.rr > datum.lr ? '{HOTMAG}' : '{MUTED}'"}]},
        {"name": "stay", "source": "rows", "transform": [{"type": "filter", "expr": "datum.both"}]}]
    mid = (xl + xr) / 2
    spot = "hovF ? (hovF === datum.label ? 1 : 0.14) : (datum.both ? 0.95 : 0.6)"
    marks = [
        tx(0, 28, "THE MORNING AFTER", 22, INK, 700),
        tx(300, 28, s(f"'top {n} fears by people, as a child → now  ·  only ' + length(data('stay')) + ' stay on the list'"), 17, MUTED),
        tx(xl - 12, 70, "AS A CHILD", 15, HOTMAG, 700, "right"),
        tx(xr + 12, 70, "NOW", 15, VIOLET, 700),
        {"type": "path", "name": "line", "from": {"data": "rows"}, "encode": {"update": {
            "path": s(f"datum.both ? 'M{xl} ' + datum.y1 + ' C{mid} ' + datum.y1 + ' {mid} ' + datum.y2 + ' {xr} ' + datum.y2 : "
                      f"datum.lr <= {n} ? 'M{xl} ' + datum.y1 + ' h' + ({(xr - xl) * 0.2} * {prog}) : 'M{xr} ' + datum.y2 + ' h' + (-{(xr - xl) * 0.2} * {prog})"),
            "stroke": s(f"datum.both ? datum.col : (datum.lr <= {n} ? '{HOTMAG}' : '{VIOLET}')"),
            "strokeDash": s(f"datum.both ? [{w}, {w}] : [5, 5]"), "strokeDashOffset": s(f"datum.both ? {w} * (1 - {prog}) : 0"),
            "fill": {"value": "transparent"}, "opacity": s(spot), "strokeWidth": s("hovF === datum.label ? 5 : datum.both ? 3 : 1.8")}}},
        tx(xl - 12, s("datum.y1 + 6"), s(f"datum.lr <= {n} ? datum.label + '  ' + datum.c : ''"), 18, INK, 400, "right", name="lbl0", frm="rows",
           opacity=s("hovF && hovF !== datum.label ? 0.35 : 1"), fontWeight=s("hovF === datum.label ? 700 : 400")),
        tx(xr + 12, s("datum.y2 + 6"), s(f"datum.rr <= {n} ? datum.a + '  ' + datum.label : ''"), 18, INK, 400, "left", name="lbl1", frm="rows",
           opacity=s("hovF && hovF !== datum.label ? 0.35 : 1"), fontWeight=s("hovF === datum.label ? 700 : 400")),
        tx(mid, 434, "violet = climbed  ·  magenta = fell  ·  dashed = drops out of, or enters, the top 12", 15, MUTED, 400, "center",
           fontStyle=v("italic"))] + flip_banner(n, w)
    sig = motion() + [{"name": "hovD", "value": None, "on": [
        {"events": "@lbl0:mouseover, @lbl1:mouseover, @line:mouseover", "update": "datum"},
        {"events": "@lbl0:mouseout, @lbl1:mouseout, @line:mouseout", "update": "null"}]},
        {"name": "hovF", "update": "hovD ? hovD.label : null"}]
    return uniq({"$schema": SCHEMA, "description": "P28 C / V3 the morning after: top-12 fears by people as a child vs now; lines draw on open; hover spotlights one fear.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "signals": sig, "data": data, "marks": marks})


def flip_banner(n, w, bh=48):
    on = "hovD ? 1 : 0"
    verdict = (f"hovD ? (hovD.lr > {n} ? 'NEW TO THE TOP {n}' : hovD.rr > {n} ? 'DROPPED OUT OF THE TOP {n}' : "
               "hovD.rr < hovD.lr ? 'CLIMBED ' + (hovD.lr - hovD.rr) + (hovD.lr - hovD.rr === 1 ? ' PLACE' : ' PLACES') : "
               "hovD.rr > hovD.lr ? 'FELL ' + (hovD.rr - hovD.lr) + (hovD.rr - hovD.lr === 1 ? ' PLACE' : ' PLACES') : 'HELD ITS PLACE') : ''")
    col = f"hovD && hovD.rr < hovD.lr ? '{VIOLET}' : hovD && hovD.rr > hovD.lr ? '{HOTMAG}' : '{MUTED}'"
    rank = lambda k: f"hovD ? (hovD.{k} > {n} ? 'outside' : '#' + hovD.{k}) : ''"
    C = w / 2
    kids = [tx(16, 19, s(verdict), 15, s(col), 700),
            tx(16, 41, s("hovD ? hovD.label : ''"), 20, INK, 700, limit=v(360)),
            tx(C - 26, 36, s(rank("lr")), s(f"hovD && hovD.lr > {n} ? 18 : 26"), MUTED, 900, "right", DISPLAY),
            tx(C, 33, s("hovD ? '→' : ''"), 22, MUTED, 400, "center"),
            tx(C + 26, 36, s(rank("rr")), s(f"hovD && hovD.rr > {n} ? 18 : 26"), s(col), 900, "left", DISPLAY),
            tx(w - 16, 32, s("hovD ? hovD.c + (hovD.c === 1 ? ' person' : ' people') + ' as a child  →  ' + hovD.a + ' now' : ''"), 18, INK, 400, "right")]
    return [{"type": "group", "name": "card", "interactive": False, "encode": {"update": {
        "x": v(0), "y": v(0), "width": v(w), "height": v(bh), "fill": v(CARD), "stroke": s(col), "strokeWidth": v(1.8),
        "cornerRadius": v(12), "fillOpacity": s(on), "strokeOpacity": s(on), "opacity": s(on)}}, "marks": _hide(kids, on)}]


# ===================================================================== V4 the data nightmare + sign-off
def nightmare(w=1237, h=240):
    y0, rowh, lx, bx, bmax = 58, 22.5, 232, 244, 360
    prog = ease("t * 1.5 - 0.3")
    short = {"It arrives a mess (missing values, duplicates, inconsistent formats)": "It arrives a mess",
             "It exists in too many versions (no clear source of truth)": "Too many versions",
             "It doesn’t add up (conflicting numbers and mysterious totals)": "It doesn’t add up",
             "It takes forever (painfully slow processing or queries)": "It takes forever",
             "It falls into the wrong hands (inappropriate access to sensitive data)": "Falls into the wrong hands",
             "The AI confidently gets it wrong (unreliable answers or predictions)": "The AI gets it wrong",
             "It never arrives (broken pipelines and failed refreshes)": "It never arrives",
             "We spot the problem too late (missed events and warnings)": "We spot it too late"}
    data = [{"name": "dataset"},
            {"name": "short", "values": [{"k": k, "s": vv} for k, vv in short.items()]},
            {"name": "rows", "source": "dataset", "transform": [
                {"type": "formula", "as": "n", "expr": "datum['Nightmare Respondents'] || 0"},
                {"type": "lookup", "from": "short", "key": "k", "fields": ["dataNightmare"], "values": ["s"], "as": ["s0"]},
                {"type": "formula", "as": "lab", "expr": "datum.s0 || datum.Nightmare"},
                {"type": "window", "sort": {"field": ["n", "lab"], "order": ["descending", "ascending"]}, "ops": ["row_number"], "as": ["r"]},
                {"type": "formula", "as": "y", "expr": f"{y0} + (datum.r - 0.5) * {rowh}"}]},
            {"name": "mx", "source": "rows", "transform": [{"type": "aggregate", "ops": ["max"], "fields": ["n"], "as": ["m"]}]}]
    sig = motion() + [{"name": "nmax", "update": "length(data('mx')) ? max(1, data('mx')[0].m) : 1"},
                      {"name": "hovN", "value": None, "on": [
                          {"events": "@bar:mouseover, @nlab:mouseover, @nval:mouseover", "update": "datum"},
                          {"events": "@bar:mouseout, @nlab:mouseout, @nval:mouseout", "update": "null"}]}]
    bw = f"datum.n / nmax * {bmax} * {prog}"
    marks = [
        tx(0, 28, "THE DATA NIGHTMARE", 22, INK, 700),
        tx(300, 28, "the data community’s own answer · one each · 105 people", 17, MUTED),
        tx(lx, s("datum.y + 6"), s("datum.lab"), 17, INK, 400, "right", name="nlab", frm="rows",
           opacity=s("hovN && hovN.lab !== datum.lab ? 0.4 : 1")),
        {"type": "rect", "name": "bar", "from": {"data": "rows"}, "encode": {"update": {
            "x": v(bx), "width": s(bw), "y": s("datum.y - 8"), "height": v(16), "cornerRadius": v(2),
            "fill": s(f"datum.r === 1 ? '{HOTMAG}' : '{VIOLET}'"), "opacity": s("hovN && hovN.lab !== datum.lab ? 0.35 : 1")}}},
        tx(s(f"{bx} + 8 + {bw}"), s("datum.y + 6"), s("datum.n"), 17, INK, 700, name="nval", frm="rows",
           opacity=s("hovN && hovN.lab !== datum.lab ? 0.4 : 1")),
        {"type": "rule", "name": "bg_divider", "interactive": False, "encode": {"update": {
            "x": v(692), "x2": v(692), "y": v(52), "y2": v(h - 8), "stroke": v(VIOLET), "strokeWidth": v(2), "opacity": v(0.45)}}}]
    q = "hovN ? 0 : 1"
    for y, line, col in [(86, "We lit lanterns for the dark", INK), (118, "and set a table for the dead.", INK),
                         (170, "The future is still waiting", HOTMAG), (202, "for its festival.", HOTMAG)]:
        marks.append(tx(720, y, line, 25, col, 700, fontStyle=v("italic"), opacity=s(q)))
    marks += nightmare_card(w, h)
    return uniq({"$schema": SCHEMA, "description": "P28 C / V4 the data nightmare (8 answers, one each) and the sign-off; hover a bar for its card.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "signals": sig, "data": data, "marks": marks})


def nightmare_card(w, h, x0=712, y0=46, cw=520, ch=188):
    on = "hovN ? 1 : 0"
    col = f"hovN && hovN.r === 1 ? '{HOTMAG}' : '{VIOLET}'"
    full = "(hovN ? hovN.dataNightmare : '')"
    cut = f"indexof({full}, ' (')"
    quote = f"{cut} > 0 ? '“' + substring({full}, 0, {cut}) + '”' : {full}"
    detail = f"{cut} > 0 ? substring({full}, {cut} + 2, length({full}) - 1) : ''"
    tools = ("hovN && indexof(hovN['TT Nightmare Sentence'] || '', 'tools: ') >= 0 ? "
             "'Top tools: ' + replace(split(hovN['TT Nightmare Sentence'], 'tools: ')[1], /\\.$/, '') : ''")
    kids = [tx(20, 28, s("hovN ? 'THE DATA NIGHTMARE  ·  #' + hovN.r + ' OF ' + length(data('rows')) : ''"), 15, s(col), 700),
            tx(20, 62, s(quote), 23, INK, 700, limit=v(cw - 40)),
            tx(20, 88, s(detail), 16, MUTED, 400, fontStyle=v("italic"), limit=v(cw - 40)),
            tx(20, 138, s("hovN ? format(hovN.n, ',') : ''"), 40, s(col), 900, font=DISPLAY),
            tx(s("20 + (hovN ? length(format(hovN.n, ',')) * 30 : 0) + 12"), 136, s("hovN ? 'of ' + (hovN.Respondents || 105) + ' people' : ''"), 18, INK),
            tx(cw - 20, 138, s("hovN ? format(hovN['Nightmare Share'], '.0%') : ''"), 30, INK, 900, "right", DISPLAY),
            tx(20, 172, s(tools), 16, INK, 400, limit=v(cw - 40))]
    return [{"type": "group", "name": "card", "interactive": False, "encode": {"update": {
        "x": v(x0), "y": v(y0), "width": v(cw), "height": v(ch), "fill": v(CARD), "stroke": s(col), "strokeWidth": v(1.8),
        "cornerRadius": v(14), "fillOpacity": s(on), "strokeOpacity": s(on), "opacity": s(on)}}, "marks": _hide(kids, on)}]
