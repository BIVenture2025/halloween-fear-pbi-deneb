"""P28 Version B - Deneb (Vega) specs: V1 title band, V2 cemetery, V3 leaderboard flip.
Geometry = 01_Mockups/versionB/mockup_b.py (approved 2026-10-14 23:05 MYT), shifted into each visual box.
Motion = Vega timer signals: t runs 0 -> 1 over 4.5 s from first render, `loop` keeps running for the
ambient flicker/bob. The END STATE (t = 1) is the poster, so exports and thumbnails are complete.
Every number is a bound measure; the only static data is the short-label lookup (presentation)."""

BG, PANEL, INK, MUTED = "#0B0B0F", "#16161E", "#FFFFFF", "#B8B8C8"
ACID, CORAL, VIOLET, GREY, LILAC = "#D4FF3A", "#FF6B4A", "#9D4EFF", "#8A8A9A", "#C9A6FF"
FONT, DISPLAY = "Segoe UI", "Arial Black"
LABELS = {"Demons/the devil": "Demons", "Basements / Attics": "Basements", "Dolls/mannequins": "Dolls",
          "Doctors/hospitals": "Doctors", "Open/empty spaces": "Open spaces", "Thunderstorms/lightning": "Thunderstorms",
          "Death (your own or a loved one’s)": "Death", "Cancer or another serious diagnosis": "Serious diagnosis",
          "Financial insecurity/poverty": "Financial insecurity", "Uncertainty about the future": "Uncertain future",
          "Wasting one’s life/potential": "Wasting potential", "Being trapped / small spaces": "Being trapped",
          "Insects/bugs in general": "Insects", "Radioactivity/nuclear disaster": "Nuclear disaster",
          "Losing a limb or developing a disability": "Losing a limb", "Separation from friends or family": "Separation",
          "Not being good enough": "Not good enough", "The unknown/unfamiliar": "The unknown", "Monsters under the bed": "Monsters",
          "Natural disasters generally": "Natural disasters", "Getting sick/illness": "Getting sick", "Germs/contamination": "Germs",
          "Being alone / Loneliness": "Loneliness", "Conflict/confrontation": "Conflict", "Rats/mice": "Rats",
          "Bees/wasps": "Bees", "Needles/shots": "Needles", "Failing at work/school": "Failing at work",
          "Deep/open water": "Deep water", "Intruders/home invasion": "Intruders", "Divorce/breakup": "Divorce",
          "Something else: War": "War (written in)", "Abandoned buildings": "Abandoned places"}


def motion(duration_ms=4500):
    return [
        {"name": "t0", "init": "now()"},
        {"name": "clock", "init": "0", "on": [{"events": {"type": "timer", "throttle": 40}, "update": "now() - t0"}]},
        {"name": "t", "update": f"min(1, clock / {duration_ms})"},
        {"name": "loop", "update": "clock / 1000"},
    ]


def ease(x):
    return f"(1 - pow(1 - clamp({x}, 0, 1), 3))"


SCALE = 1.5  # S3 rev 3: owner asked again for larger text inside the charts


def T(x, y, text, size, fill, weight=400, align="left", font=FONT, extra=None, from_=None, upd=None, scale=True):
    """Text mark. Marks drawn from 'rows' get unique names lbl0, lbl1, ... for the flip's hover events."""
    enc = {"x": x, "y": y, "fontSize": {"value": round(size * SCALE, 1) if scale else size}, "fill": {"value": fill}, "fontWeight": {"value": weight},
           "align": {"value": align}, "font": {"value": font}}
    if text is not None:
        enc["text"] = text
    if extra:
        enc.update(extra)
    m = {"type": "text", "encode": {"update": enc}}
    if from_ == "rows":
        m["name"] = "lbl" + str(T.n)
        T.n += 1
    if from_:
        m["from"] = {"data": from_}
    return m


def v(x):
    return {"value": x}


def s(x):
    return {"signal": x}


T.n = 0


# ============================================================== V1 title band (1920 x 220)
def title_band(w=1920, h=220):
    nums = [("buried", "Childhood-Only Fear Selections", ACID, "childhood picks nobody kept"),
            ("survived", "Responses Where Fears Remained", CORAL, "picks still held as an adult"),
            ("born", "Adult-Only Fear Selections", LILAC, "adult picks new since childhood")]
    marks = [T(v(70), v(62), v("WHAT KEEPS YOU UP AT NIGHT?  ·  105 PEOPLE, THEN AND NOW"), 15, ACID, 700),
             T(v(66), v(150), v("Fear has a lifespan"), 80, INK, 900, font=DISPLAY, scale=False),
             T(v(70), v(196), v("Every fear here is a real answer: what scared you as a child, and what scares you now."), 22, MUTED, scale=False)]
    x = 1110
    for key, field, col, sub in nums:
        marks += [
            {"type": "text", "from": {"data": "base"}, "encode": {"update": {
                "x": v(x), "y": v(132), "font": v(DISPLAY), "fontSize": v(82), "fontWeight": v(900), "fill": v(col),
                "text": s(f"format(round((datum['{field}'] || 0) * {ease('t * 1.6')}), ',')"),
                "tooltip": s(f"{{'{key.capitalize()}': datum['{field}'], 'What it counts': '{sub}'}}")}}},
            T(v(x), v(170), v(key.upper()), 14, INK, 800),
            T(v(x), v(198), v(sub), 17, MUTED, scale=False)]
        x += 270
    return {"$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "P28 B / V1 title band: three pair totals count up on open.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "background": BG,
            "signals": motion(), "data": [{"name": "dataset"}, {"name": "base", "source": "dataset"}], "marks": marks}


# ============================================================== V2 cemetery (1920 x 703)
def cemetery(w=1920, h=703):
    gy = 553  # ground line inside the box (page 785)
    unit = 14
    labels = [{"Fear": k, "label": vv} for k, vv in LABELS.items()]
    tip_dead = "{'Fear': datum.label, 'Category': datum.Category, 'People as a child': datum.c, 'People now': 0, 'Status': 'buried: nobody holds it now'}"
    tip_alive = ("{'Fear': datum.label, 'People as a child': datum.c, 'People now': datum.a, 'Kept since childhood': datum.k, "
                 "'Status': datum.k > 0 ? 'still burning' : 'relit: feared now by different people'}")
    tip_born = "{'Fear': datum.label, 'Category': datum.Category, 'People now': datum.a, 'Status': 'born: nobody had it as a child'}"
    data = [
        {"name": "dataset"},
        {"name": "labels", "values": labels},
        {"name": "rows", "source": "dataset", "transform": [
            {"type": "filter", "expr": "datum.Category !== 'Other Responses'"},
            {"type": "formula", "as": "c", "expr": "datum['People Childhood'] || 0"},
            {"type": "formula", "as": "a", "expr": "datum['People Adult'] || 0"},
            {"type": "formula", "as": "k", "expr": "datum['People Kept'] || 0"},
            {"type": "filter", "expr": "datum.c > 0 || datum.a > 0"},
            {"type": "lookup", "from": "labels", "key": "Fear", "fields": ["Fear"], "values": ["label"], "as": ["lab0"]},
            {"type": "formula", "as": "label", "expr": "datum.lab0 || datum.FearShort || datum.Fear"},
            {"type": "formula", "as": "kind", "expr": "datum.a === 0 ? 'dead' : datum.c === 0 ? 'born' : 'alive'"},
            {"type": "formula", "as": "size", "expr": "datum.kind === 'dead' ? datum.c : datum.a"},
            {"type": "formula", "as": "tier", "expr":
                "datum.kind === 'dead' ? (datum.c >= 3 ? 0 : 1) : datum.kind === 'born' ? (datum.a >= 3 ? 0 : 1) : (datum.a >= 6 ? 0 : datum.a >= 3 ? 1 : 2)"},
            {"type": "window", "groupby": ["kind", "tier"], "sort": {"field": ["size", "label"], "order": ["descending", "ascending"]},
             "ops": ["row_number"], "as": ["rn"]}]},
        {"name": "deadT0", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'dead' && datum.tier === 0"}]},
        {"name": "deadT1", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'dead' && datum.tier === 1"}]},
        {"name": "aliveT0", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'alive' && datum.tier === 0"}]},
        {"name": "aliveT1", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'alive' && datum.tier === 1"}]},
        {"name": "aliveT2", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'alive' && datum.tier === 2"}]},
        {"name": "bornAll", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'born'"}]},
        {"name": "bornT0", "source": "rows", "transform": [{"type": "filter", "expr": "datum.kind === 'born' && datum.tier === 0"}]},
        {"name": "pos", "source": "rows", "transform": [
            {"type": "formula", "as": "idx", "expr":
                "datum.kind === 'dead' ? (datum.tier === 0 ? datum.rn - 1 : nD0 + datum.rn - 1) : "
                "datum.kind === 'born' ? (datum.tier === 0 ? datum.rn - 1 : nB0 + datum.rn - 1) : "
                "(datum.tier === 0 ? datum.rn - 1 : datum.tier === 1 ? nA0 + datum.rn - 1 : nA0 + nA1 + datum.rn - 1)"},
            {"type": "formula", "as": "x", "expr":
                "datum.kind === 'dead' ? (datum.tier === 0 ? 96 + (datum.rn - 1) * 48 : 96 + nD0 * 48 + 14 + (datum.rn - 1) * 16) : "
                "datum.kind === 'born' ? (datum.tier === 0 ? 1646 + (datum.rn - 1) * 46 : 1646 + nB0 * 46 + (datum.rn - 1) * 28) : "
                "(datum.tier === 0 ? 690 + (datum.rn - 1) * 36 : datum.tier === 1 ? 690 + nA0 * 36 + 10 + (datum.rn - 1) * 14 : "
                "690 + nA0 * 36 + 10 + nA1 * 14 + 10 + (datum.rn - 1) * 7)"},
            # headstone
            {"type": "formula", "as": "hw", "expr": "datum.c >= 3 ? 40 : 12"},
            {"type": "formula", "as": "hfull", "expr": f"24 + datum.c * {unit}"},
            # candle
            {"type": "formula", "as": "cw", "expr": "datum.a >= 6 ? 16 : datum.a >= 3 ? 8 : 4"},
            {"type": "formula", "as": "cfull", "expr": f"14 + datum.a * {unit}"},
            {"type": "formula", "as": "fr", "expr": "5 + datum.k * 2.2"},
            # ghost
            {"type": "formula", "as": "gh", "expr": "22 + datum.a * 9"},
            {"type": "formula", "as": "gw", "expr": "18 + datum.a * 1.6"}]},
    ]
    signals = motion() + [
        {"name": "nD0", "update": "length(data('deadT0'))"}, {"name": "nD1", "update": "length(data('deadT1'))"},
        {"name": "nA0", "update": "length(data('aliveT0'))"}, {"name": "nA1", "update": "length(data('aliveT1'))"},
        {"name": "nA2", "update": "length(data('aliveT2'))"}, {"name": "nB0", "update": "length(data('bornT0'))"},
        {"name": "nB", "update": "length(data('bornAll'))"}]
    grow = lambda step: ease(f"t * 1.3 - datum.idx * {step}")
    hs = f"datum.hfull * {grow(0.03)}"
    cs = f"datum.cfull * {grow(0.015)}"
    gp = ease("t * 1.4 - 0.25 - datum.idx * 0.05")
    marks = [
        # scenery
        {"type": "symbol", "encode": {"update": {"x": v(1500), "y": v(120), "shape": v("circle"), "size": v(9160), "fill": v(INK), "opacity": v(0.92)}}},
        {"type": "symbol", "encode": {"update": {"x": v(1518), "y": v(108), "shape": v("circle"), "size": v(6650), "fill": v(BG)}}},
        {"type": "rect", "encode": {"update": {"x": v(0), "y": v(gy), "width": v(w), "height": v(h - gy), "fill": v(PANEL)}}},
        {"type": "rule", "encode": {"update": {"x": v(0), "x2": v(w), "y": v(gy), "stroke": v(GREY), "strokeWidth": v(1.5), "opacity": v(0.7)}}},
    ]
    for i in range(3):
        marks.append({"type": "path", "encode": {"update": {
            "path": s(f"'M' + ({300 + i * 640 - 420} + 40 * sin(loop * 0.6 + {i})) + ' {gy - 8} a420 26 0 1 0 840 0 a420 26 0 1 0 -840 0 Z'"),
            "fill": v(INK), "opacity": s("t > 0.2 ? 0.035 : 0")}}})
    # zone captions (counts are data-driven)
    marks += [
        T(v(70), v(40), v("BURIED"), 16, ACID, 800),
        T(v(70), v(62), s("(nD0 + nD1) + ' fears nobody holds any more'"), 13, MUTED),
        T(v(690), v(40), v("STILL BURNING"), 16, CORAL, 800),
        T(v(690), v(62), s("(nA0 + nA1 + nA2) + ' fears alive · flame = kept since childhood · no flame = feared by different people now'"), 13, MUTED),
        T(v(1625), v(40), v("BORN"), 16, LILAC, 800),
        T(v(1625), v(62), s("nB + ' fears new since childhood'"), 13, MUTED),
    ]
    dead = "pos_dead"
    data += [{"name": "pos_dead", "source": "pos", "transform": [{"type": "filter", "expr": "datum.kind === 'dead'"}]},
             {"name": "pos_alive", "source": "pos", "transform": [{"type": "filter", "expr": "datum.kind === 'alive'"}]},
             {"name": "pos_born", "source": "pos", "transform": [{"type": "filter", "expr": "datum.kind === 'born'"}]}]
    # headstones
    marks += [
        {"type": "path", "from": {"data": dead}, "encode": {"update": {
            "path": s(f"'M' + (datum.x - datum.hw / 2) + ' {gy} V' + ({gy} - {hs} + datum.hw / 2) + ' A' + (datum.hw / 2) + ' ' + (datum.hw / 2) + ' 0 0 1 ' + (datum.x + datum.hw / 2) + ' ' + ({gy} - {hs} + datum.hw / 2) + ' V{gy} Z'"),
            "fill": v(PANEL), "stroke": v(GREY), "strokeWidth": v(1.6), "opacity": s(f"{hs} > 1 ? 1 : 0")}}},
        {"type": "rule", "from": {"data": dead}, "encode": {"update": {
            "x": s("datum.x - 9"), "x2": s("datum.x + 9"), "y": s(f"{gy} - {hs} + 20"), "stroke": v(GREY), "strokeWidth": v(1.2),
            "opacity": s(f"datum.c >= 3 && {hs} > 30 ? 1 : 0")}}},
        T(s("datum.x"), s(f"datum.c >= 3 ? {gy} - {hs} + 42 : {gy} - {hs} - 6"), s("datum.c"), 15, INK, 800, "center", from_=dead,
          extra={"fontSize": s("datum.c >= 3 ? 23 : 17"), "fill": s(f"datum.c >= 3 ? '{INK}' : '{MUTED}'"), "opacity": s(f"{hs} > 10 ? 1 : 0")}),
        T(s("datum.x"), v(gy + 22), s("datum.c >= 3 ? datum.label : ''"), 11.5, MUTED, align="right", from_=dead, extra={"angle": v(-38)}),
        T(s("96 + (nD0 * 48 + nD1 * 16) / 2"), v(gy + 136), s("nD1 > 0 ? '+ ' + nD1 + ' fears held by 1–2 people as children' : ''"), 11.5, MUTED, align="center"),
    ]
    alive = "pos_alive"
    ctop = f"({gy} - {cs})"
    marks += [
        {"type": "rect", "from": {"data": alive}, "encode": {"update": {
            "x": s("datum.x - datum.cw / 2"), "width": s("datum.cw"), "y": s(ctop), "y2": v(gy), "cornerRadius": v(2),
            "fill": v("#2A2A36"), "stroke": v(GREY), "strokeWidth": v(1)}}},
        {"type": "rule", "from": {"data": alive}, "encode": {"update": {
            "x": s("datum.x"), "x2": s("datum.x"), "y": s(ctop), "y2": s(f"{ctop} - 6"), "stroke": v(GREY), "strokeWidth": v(1.5),
            "opacity": s(f"{cs} > 2 ? 1 : 0")}}},
        # flame (outer teardrop + core) for kept > 0
        {"type": "path", "from": {"data": alive}, "encode": {"update": {
            "path": s(
                f"datum.k > 0 ? 'M' + datum.x + ' ' + ({ctop} - 8 - 2 * datum.fr * (1 + 0.12 * sin(loop * 18.84 + datum.idx))) + "
                f"' C' + (datum.x + datum.fr) + ' ' + ({ctop} - 8 - 1.2 * datum.fr) + ' ' + (datum.x + datum.fr * 0.9) + ' ' + ({ctop} - 8 - 0.3 * datum.fr) + ' ' + datum.x + ' ' + ({ctop} - 8) + "
                f"' C' + (datum.x - datum.fr * 0.9) + ' ' + ({ctop} - 8 - 0.3 * datum.fr) + ' ' + (datum.x - datum.fr) + ' ' + ({ctop} - 8 - 1.2 * datum.fr) + ' ' + datum.x + ' ' + ({ctop} - 8 - 2 * datum.fr * (1 + 0.12 * sin(loop * 18.84 + datum.idx))) + ' Z' : ''"),
            "fill": v(CORAL), "opacity": s(f"0.95 * {grow(0.015)}")}}},
        {"type": "symbol", "from": {"data": alive}, "encode": {"update": {
            "x": s("datum.x"), "y": s(f"{ctop} - 8 - 0.55 * datum.fr"), "shape": v("circle"),
            "size": s(f"datum.k > 0 ? pow(datum.fr * 0.7, 2) * {grow(0.015)} : 0"), "fill": v(ACID), "opacity": v(0.9)}}},
        # smoke wisp when nobody kept it
        {"type": "path", "from": {"data": alive}, "encode": {"update": {
            "path": s(f"datum.k === 0 && {cs} > 4 ? 'M' + datum.x + ' ' + ({ctop} - 8) + ' q6 -10 0 -20 q-6 -10 0 -20' : ''"),
            "stroke": v(GREY), "strokeWidth": v(1.2), "opacity": s("0.4 + 0.2 * sin(loop * 2 + datum.idx)")}}},
        T(s("datum.x"), s(f"{ctop} - (datum.k > 0 ? 18 + 2 * datum.fr : 58)"), s("datum.a >= 3 ? datum.a : ''"), 14, INK, 800, "center", from_=alive,
          extra={"fontSize": s("datum.a >= 6 ? 23 : 17"), "fill": s(f"datum.a >= 6 ? '{INK}' : '{MUTED}'"), "opacity": s(f"{grow(0.015)}")}),
        T(s("datum.x + 4"), v(gy + 22), s("datum.a >= 6 ? datum.label : ''"), 11.5, MUTED, align="right", from_=alive, extra={"angle": v(-38)}),
        T(v(1150), v(gy + 136), s("(nA1 + nA2) > 0 ? '+ ' + (nA1 + nA2) + ' fears held by 1–5 people now' : ''"), 11.5, MUTED, align="center"),
    ]
    marks.append({"type": "rect", "name": "hit", "from": {"data": "pos"}, "encode": {"update": {
        "x": s("datum.x - max(datum.kind === 'dead' ? datum.hw : datum.kind === 'born' ? datum.gw : datum.cw, 7) / 2 - 2"),
        "width": s("max(datum.kind === 'dead' ? datum.hw : datum.kind === 'born' ? datum.gw : datum.cw, 7) + 4"),
        "y": v(120), "y2": v(gy + 20), "fill": v("#000000"), "fillOpacity": v(0.001), "cursor": v("pointer")}}})
    born = "pos_born"
    gy0 = f"({gy} - 10 - {gp} * (datum.gh + 40) + 6 * sin(loop * 6.28 * 0.4 + datum.idx))"
    marks += [
        {"type": "path", "from": {"data": born}, "encode": {"update": {
            "path": s(f"'M' + (datum.x - datum.gw / 2) + ' ' + ({gy0} + datum.gh) + ' V' + ({gy0} + datum.gw / 2) + "
                      f"' A' + (datum.gw / 2) + ' ' + (datum.gw / 2) + ' 0 0 1 ' + (datum.x + datum.gw / 2) + ' ' + ({gy0} + datum.gw / 2) + "
                      f"' V' + ({gy0} + datum.gh) + ' q' + (-datum.gw / 8) + ' -9 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' 9 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' -9 ' + (-datum.gw / 4) + ' 0 q' + (-datum.gw / 8) + ' 9 ' + (-datum.gw / 4) + ' 0 Z'"),
            "fill": v(VIOLET), "fillOpacity": s(f"0.28 * {gp}"), "stroke": v(ACID), "strokeWidth": v(1.4),
            "strokeOpacity": s(f"0.85 * {gp}")}}},
        T(s("datum.x"), s(f"{gy0} + datum.gh * 0.55"), s("datum.a"), 14, INK, 800, "center", from_=born,
          extra={"fontSize": s("datum.a >= 3 ? 23 : 17"), "opacity": s(gp)}),
        T(s("datum.x + 4"), v(gy + 22), s("datum.a >= 3 ? datum.label : ''"), 11.5, MUTED, align="right", from_=born, extra={"angle": v(-38)}),
        T(v(1760), v(gy + 136), s("(nB - nB0) > 0 ? '+ ' + (nB - nB0) + ' fears held by 1–2 people' : ''"), 11.5, MUTED, align="center"),
    ]
    marks += hover_card(w, gy)
    signals.append({"name": "hov", "value": None, "on": [
        {"events": "@hit:mouseover", "update": "datum"}, {"events": "@hit:mouseout", "update": "null"}]})
    return {"$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "P28 B / V2 cemetery: every fear as a headstone (nobody holds it now), a candle (still held; flame = kept since childhood) or a ghost (new since childhood).",
            "width": w, "height": h, "padding": 0, "autosize": "none", "background": BG,
            "signals": signals, "data": data, "marks": marks}


# ============================================================== V3 leaderboard flip (1110 x 335)
def flip(w=1110, h=372, n=12):
    T.n = 0
    xl, xr, top, rowh = 268, w - 268, 64, 23.5
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
            {"type": "formula", "as": "col", "expr": f"datum.rr < datum.lr ? '{ACID}' : datum.rr > datum.lr ? '{CORAL}' : '{GREY}'"}]},
        {"name": "stay", "source": "rows", "transform": [{"type": "filter", "expr": "datum.both"}]}]
    tip = "{'Fear': datum.label, 'Rank as a child': datum.lr, 'Rank now': datum.rr, 'People as a child': datum.c, 'People now': datum.a}"
    mid = (xl + xr) / 2
    marks = [
        T(v(0), v(18), v("THE LEADERBOARD FLIP"), 16, INK, 800),
        T(v(345), v(18), s(f"'top {n} fears by people, as a child → now  ·  only ' + length(data('stay')) + ' fears stay on the list'"), 13, MUTED),
        T(v(xl - 10), v(top - 5), v("AS A CHILD"), 11, ACID, 800, "right"),
        T(v(xr + 10), v(top - 5), v("NOW"), 11, ACID, 800),
        {"type": "path", "name": "line", "from": {"data": "rows"}, "encode": {"update": {
            "path": s(f"datum.both ? 'M{xl} ' + datum.y1 + ' C{mid} ' + datum.y1 + ' {mid} ' + datum.y2 + ' {xr} ' + datum.y2 : "
                      f"datum.lr <= {n} ? 'M{xl} ' + datum.y1 + ' h' + ({(xr - xl) * 0.22} * {prog}) : 'M{xr} ' + datum.y2 + ' h' + (-{(xr - xl) * 0.22} * {prog})"),
            "stroke": s("datum.both ? datum.col : (datum.lr <= " + str(n) + f" ? '{CORAL}' : '{ACID}')"),
            "strokeDash": s(f"datum.both ? [{w}, {w}] : [4, 4]"), "strokeDashOffset": s(f"datum.both ? {w} * (1 - {prog}) : 0"),
            "opacity": s("hovF ? (hovF === datum.label ? 1 : 0.12) : (datum.both ? 0.9 : 0.45)"),
            "strokeWidth": s("hovF === datum.label ? 4 : datum.both ? 2.5 : 1.4")}}},
        T(v(xl - 12), s("datum.y1 + 4"), s(f"datum.lr <= {n} ? datum.label + '  ' + datum.c : ''"), 12.5, INK, align="right", from_="rows",
          extra={"opacity": s("hovF && hovF !== datum.label ? 0.3 : 1"), "fontWeight": s("hovF === datum.label ? 800 : 400")}),
        T(v(xr + 12), s("datum.y2 + 4"), s(f"datum.rr <= {n} ? datum.a + '  ' + datum.label : ''"), 12.5, INK, from_="rows",
          extra={"opacity": s("hovF && hovF !== datum.label ? 0.3 : 1"), "fontWeight": s("hovF === datum.label ? 800 : 400")}),
        T(v(mid), v(top + (n + 0.5) * rowh + 4), v("dashed = drops out of, or enters, the top 12"), 11, MUTED, align="center",
          extra={"fontStyle": v("italic")}),
    ] + flip_card(n, w)
    return {"$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "P28 B / V3 leaderboard flip: top-12 fears by people as a child vs now; lines draw on open; hover spotlights one fear.",
            "width": w, "height": h, "padding": 0, "autosize": "none", "background": BG,
            "signals": motion() + [{"name": "hovD", "value": None, "on": [
                {"events": "@lbl0:mouseover, @lbl1:mouseover, @line:mouseover", "update": "datum"},
                {"events": "@lbl0:mouseout, @lbl1:mouseout, @line:mouseout", "update": "null"}]},
                {"name": "hovF", "update": "hovD ? hovD.label : null"}],
            "data": data, "marks": marks}



def _hide(marks, on):
    """Deneb draws on canvas, where a group's opacity does NOT reach its children (S3 rev 3: the card's fixed
    labels 'as a child -> now' showed on the idle page). Every child carries its own opacity and ignores the mouse."""
    for m in marks:
        m["interactive"] = False
        m["encode"]["update"]["opacity"] = {"signal": on}
    return marks


def hover_card(w, gy, cw=530, ch=206):
    """In-chart epitaph card, drawn in the empty sky above the hovered object."""
    on = "hov ? 1 : 0"
    kcol = f"hov && hov.kind === 'dead' ? '{ACID}' : hov && hov.kind === 'born' ? '{LILAC}' : '{CORAL}'"
    cx = f"clamp(hov ? hov.x - {cw / 2} : 0, 12, {w - cw - 12})"
    top = 84
    kicker = "hov ? (hov.kind === 'dead' ? 'HERE LIES' : hov.kind === 'born' ? 'BORN IN ADULTHOOD' : 'STILL BURNING') : ''"
    line = ("hov ? (hov.kind === 'dead' ? 'Outgrown by everyone who had it.' : "
            "hov.kind === 'born' ? 'Nobody had it as a child.' : "
            "hov.k > 0 ? (hov.k === hov.c ? 'All ' + hov.k + ' never let it go.' : hov.k + ' of ' + hov.c + ' never let it go.') : "
            "'Nobody kept it. Others fear it now.') : ''")
    big = lambda key: f"hov ? (hov.kind === 'born' && '{key}' === 'c' ? '—' : format(hov.{key}, ',')) : ''"
    lbl = lambda t: f"hov ? '{t}' : ''"
    tx = lambda x, y, text, size, fill, **k: {"type": "text", "encode": {"update": {
        "x": v(x), "y": y if isinstance(y, dict) else v(y), "align": v(k.get("align", "center")), "text": s(text),
        "font": v(k.get("font", FONT)), "fontSize": v(size), "fontWeight": v(k.get("weight", 400)),
        "fill": fill if isinstance(fill, dict) else v(fill), **k.get("extra", {})}}}
    kids = [
        tx(cw / 2, s("hov && hov.kind === 'dead' ? 50 : 36"), kicker, 17, s(kcol), weight=800),
        tx(cw / 2, s("hov && hov.kind === 'dead' ? 86 : 76"), "hov ? hov.label : ''", 31, INK, weight=800, extra={"limit": v(cw - 28)}),
        tx(cw / 2 - 86, 140, big("c"), 44, MUTED, font=DISPLAY),
        tx(cw / 2, 132, "hov ? '→' : ''", 30, MUTED),
        tx(cw / 2 + 86, 140, big("a"), 44, s(kcol), font=DISPLAY),
        tx(cw / 2 - 86, 162, lbl("as a child"), 16, MUTED),
        tx(cw / 2 + 86, 162, lbl("now"), 16, MUTED),
        tx(cw / 2, 192, line, 19, INK, extra={"fontStyle": v("italic"), "limit": v(cw - 24)}),
    ]
    return [
        {"type": "rule", "interactive": False, "encode": {"update": {
            "x": s("hov ? hov.x : 0"), "x2": s("hov ? hov.x : 0"), "y": v(top + ch),
            "y2": s(f"hov ? {gy} - (hov.kind === 'dead' ? hov.hfull : hov.kind === 'born' ? hov.gh + 50 : hov.cfull + 20) : {top + ch}"),
            "stroke": s(kcol), "strokeDash": v([3, 4]), "strokeWidth": v(1.5), "opacity": s(on)}}},
        {"type": "group", "interactive": False, "encode": {"update": {
            "x": s(cx), "y": v(top), "width": v(cw), "height": v(ch), "fill": v(PANEL), "stroke": s(kcol), "strokeWidth": v(1.8),
            "fillOpacity": s(on), "strokeOpacity": s(on), "opacity": s(on),
            "cornerRadiusTopLeft": s("hov && hov.kind === 'dead' ? 150 : 16"), "cornerRadiusTopRight": s("hov && hov.kind === 'dead' ? 150 : 16"),
            "cornerRadiusBottomLeft": v(16), "cornerRadiusBottomRight": v(16)}},
         "marks": _hide(kids, on)}]


def flip_card(n, w=1110, bh=46):
    """Hover banner for the leaderboard flip. It covers the title row only, so it can never sit on a line (S3 rev 3)."""
    on = "hovD ? 1 : 0"
    verdict = (f"hovD ? (hovD.lr > {n} ? 'NEW TO THE TOP {n}' : hovD.rr > {n} ? 'DROPPED OUT OF THE TOP {n}' : "
               "hovD.rr < hovD.lr ? 'CLIMBED ' + (hovD.lr - hovD.rr) + (hovD.lr - hovD.rr === 1 ? ' PLACE' : ' PLACES') : "
               "hovD.rr > hovD.lr ? 'FELL ' + (hovD.rr - hovD.lr) + (hovD.rr - hovD.lr === 1 ? ' PLACE' : ' PLACES') : 'HELD ITS PLACE') : ''")
    col = f"hovD && hovD.rr < hovD.lr ? '{ACID}' : hovD && hovD.rr > hovD.lr ? '{CORAL}' : '{MUTED}'"
    rank = lambda k: f"hovD ? (hovD.{k} > {n} ? 'outside' : '#' + hovD.{k}) : ''"
    tx = lambda x, y, text, size, fill, **k: {"type": "text", "encode": {"update": {
        "x": v(x), "y": v(y), "align": v(k.get("align", "left")), "text": s(text), "font": v(k.get("font", FONT)),
        "fontSize": size if isinstance(size, dict) else v(size), "fontWeight": v(k.get("weight", 400)),
        "fill": fill if isinstance(fill, dict) else v(fill), **k.get("extra", {})}}}
    kids = [
        tx(16, 18, verdict, 14, s(col), weight=800),
        tx(16, 39, "hovD ? hovD.label : ''", 21, INK, weight=800, extra={"limit": v(390)}),
        tx(500, 34, rank("lr"), s(f"hovD && hovD.lr > {n} ? 19 : 28"), MUTED, align="right", font=DISPLAY),
        tx(530, 32, "hovD ? '→' : ''", 24, MUTED, align="center"),
        tx(560, 34, rank("rr"), s(f"hovD && hovD.rr > {n} ? 19 : 28"), s(col), font=DISPLAY),
        tx(w - 16, 31, "hovD ? hovD.c + (hovD.c === 1 ? ' person' : ' people') + ' as a child  →  ' + hovD.a + ' now' : ''",
           19, INK, align="right"),
    ]
    return [{"type": "group", "interactive": False, "encode": {"update": {
        "x": v(0), "y": v(0), "width": v(w), "height": v(bh), "fill": v(PANEL), "stroke": s(col), "strokeWidth": v(1.8),
        "cornerRadius": v(12), "fillOpacity": s(on), "strokeOpacity": s(on), "opacity": s(on)}},
        "marks": _hide(kids, on)}]


def nightmare_card(w=530, h=260):
    """Report-page tooltip for V4 (page TT_NightmareB), in the same card language as the graveyard and the flip."""
    col = f"d && d['Nightmare Rank'] === 1 ? '{CORAL}' : '{LILAC}'"
    full = "(d ? d.dataNightmare : '')"
    cut = f"indexof({full}, ' (')"
    quote = f"{cut} > 0 ? '“' + substring({full}, 0, {cut}) + '”' : {full}"
    detail = f"{cut} > 0 ? substring({full}, {cut} + 2, length({full}) - 1) : ''"
    tools = ("d && indexof(d['TT Nightmare Sentence'], 'tools: ') >= 0 ? "
             "replace(split(d['TT Nightmare Sentence'], 'tools: ')[1], /\\.$/, '') : ''")
    tx = lambda x, y, text, size, fill, **k: {"type": "text", "encode": {"update": {
        "x": v(x), "y": v(y), "align": v(k.get("align", "left")), "text": s(text), "font": v(k.get("font", FONT)),
        "fontSize": v(size), "fontWeight": v(k.get("weight", 400)), "fill": fill if isinstance(fill, dict) else v(fill),
        "limit": v(w - 44), **k.get("extra", {})}}}
    return {"$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "P28 B / V4 tooltip card: the hovered data nightmare (report-page tooltip TT_NightmareB).",
            "width": w, "height": h, "padding": 0, "autosize": "none", "background": BG,
            "signals": [{"name": "d", "update": "length(data('base')) ? data('base')[0] : null"}],
            "data": [{"name": "dataset"}, {"name": "base", "source": "dataset"}],
            "marks": [
                {"type": "rect", "encode": {"update": {"x": v(1), "y": v(1), "width": v(w - 2), "height": v(h - 2), "cornerRadius": v(16),
                    "fill": v(PANEL), "stroke": s(col), "strokeWidth": v(2)}}},
                tx(22, 36, "d ? 'THE DATA NIGHTMARE  ·  #' + d['Nightmare Rank'] + ' OF 8' : ''", 15, s(col), weight=800),
                tx(22, 72, quote, 24, INK, weight=800),
                tx(22, 98, detail, 16, MUTED, extra={"fontStyle": v("italic")}),
                tx(22, 160, "d ? format(d['Nightmare Respondents'], ',') : ''", 48, s(col), font=DISPLAY),
                tx(22, 160, "d ? 'of ' + d.Respondents + ' people' : ''", 18, INK,
                   extra={"dx": s("d ? 34 * length(format(d['Nightmare Respondents'], ',')) + 10 : 0")}),
                tx(w - 22, 160, "d ? format(d['Nightmare Share'], '.0%') : ''", 34, INK, align="right", font=DISPLAY),
                {"type": "rule", "encode": {"update": {"x": v(22), "x2": v(w - 22), "y": v(184), "stroke": v(GREY), "opacity": v(0.4)}}},
                tx(22, 212, "d ? 'THEIR MOST-USED FABRIC TOOLS' : ''", 13, MUTED, weight=800),
                tx(22, 238, tools, 17, INK),
            ]}

