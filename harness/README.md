# The offline layout check

Deneb draws its visuals with Vega. These scripts render each spec the way Deneb does in Power BI, on
**canvas**, using node-canvas. They then measure every visible text item:

- the font is at least `minFont` px **at page scale** (15 px for this page);
- the item sits inside its visual;
- it keeps at least 3 px from other text and at least 2 px from shapes. Marks named `bg_*`, `hit`, `line`,
  `card_link` and `card` are decoration and are skipped. Text named `in_*` may sit inside a shape;
- in a hover state (`states[].pick`) only the hover card's children are checked, against each other and
  against the card frame.

It **throws if it reads zero text items.** A checker that reads nothing must not report "0 issues".

## Two copies, on purpose

| File | What it is |
|---|---|
| `deneb_layout_check.mjs` + `deneb_fonts.conf` | The general tool, cleaned up after this project. Use this one. |
| `p28c_as_run/` | The exact scripts that checked the submitted page, kept as the record. Their paths point at the working folder they ran in (`~/w/...`), and `gen_data.py` also reads the survey CSV, which is not in this repository. They will not run unchanged. |

## Running the general tool

```bash
mkdir -p ~/vega/v6 && cd ~/vega/v6 && npm i vega@6.4.0 canvas@3.1.0
FONTCONFIG_FILE=/path/to/deneb_fonts.conf VEGA_NM=~/vega/v6/node_modules \
  node deneb_layout_check.mjs cfg.json
```

`cfg.json` lists the specs and the states to render:

```json
{"out": "out", "minFont": 15, "jobs": [
  {"id": "V2", "spec": "V2.json", "states": [
    {"name": "idle"},
    {"name": "hov", "pick": {"signal": "hov", "data": "pos", "field": "label", "value": "War"}}]}]}
```

Each spec must carry its test data in `data[name=dataset].values`. To get the four specs, import
`build/p28c_deneb.py` and call `title_band()`, `graveyard()`, `flip()` and `nightmare()`, or copy them
out of the `visual.json` files under `pbip/`.

## Fonts

`deneb_fonts.conf` maps **Segoe UI → DejaVu Sans** and **Arial Black → DejaVu Sans Bold** through
fontconfig. DejaVu is about 10 % wider than Segoe UI, so the check errs on the cautious side.

One trap from building this check: registering the fonts with node-canvas's `registerFont` while an
italic variant was also registered **silently dropped the bold face**. Bold then measured as regular,
about 10 % too narrow. The fontconfig alias does not have that problem.
