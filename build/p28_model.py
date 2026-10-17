"""P28 Session 3 - semantic model edits authored as TMDL text (guide sec 4/5, decision sec 6:
never over XMLA). Idempotent: refuses to run twice on the same folder. CRLF on every file written.
Usage: python3 p28_model.py <SemanticModel/definition dir>"""
import os, sys, uuid

D = sys.argv[1]
T = os.path.join(D, "tables")
NL = "\r\n"


def rd(p):
    return open(p, encoding="utf-8", newline="").read()


def wr(p, s):
    s = s.replace("\r\n", "\n").replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(s)


_SEQ = [0]


def lt():
    _SEQ[0] += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"p28-model-{_SEQ[0]}"))


def col(name, dtype, src, hidden=False, sort=None, fmt=None, desc=None):
    out = []
    if desc:
        out.append(f"\t/// {desc}")
    out.append(f"\tcolumn {name}")
    out.append(f"\t\tdataType: {dtype}")
    if hidden:
        out.append("\t\tisHidden")
    if fmt:
        out.append(f"\t\tformatString: {fmt}")
    out.append(f"\t\tlineageTag: {lt()}")
    out.append("\t\tsummarizeBy: none")
    out.append(f"\t\tsourceColumn: {src}")
    if sort:
        out.append(f"\t\tsortByColumn: {sort}")
    out.append("")
    out.append("\t\tannotation SummarizationSetBy = Automatic")
    return "\n".join(out) + "\n\n"


def msrc(lines):
    return "\n".join("\t\t\t\t" + l for l in lines)


# ---------------------------------------------------------------- 1. DimFear: Beat, BeatName, FearShort
p = os.path.join(T, "DimFear.tmdl")
s = rd(p).replace("\r\n", "\n")
if "column Beat\n" in s:
    sys.exit("DimFear already carries Beat - refusing to run twice")
short_pairs = [
    ("Demons/the devil", "Demons / the devil"), ("Basements / Attics", "Basements / attics"),
    ("Death (your own or a loved one’s)", "Death (self or loved one)"),
    ("Cancer or another serious diagnosis", "Serious diagnosis"),
    ("Financial insecurity/poverty", "Financial insecurity"),
    ("Uncertainty about the future", "Uncertain future"),
    ("Wasting one’s life/potential", "Wasting one’s potential"),
    ("Being trapped / small spaces", "Being trapped"),
    ("Insects/bugs in general", "Insects / bugs"),
    ("Radioactivity/nuclear disaster", "Nuclear disaster"),
    ("Losing a limb or developing a disability", "Losing a limb / disability"),
    ("Separation from friends or family", "Separation from loved ones"),
]
pairs_m = ", ".join('{"%s", "%s"}' % (a, b) for a, b in short_pairs)
old_tail = "\n\t\t\t\tin Result"
assert s.count(old_tail) == 1, "DimFear partition tail not found exactly once"
new_tail = (",\n" + msrc([
    ' // P28 S3: beat mapping (guide sec 4) and short display labels; the original Fear text is unchanged.',
    ' WithBeat = Table.AddColumn(Result, "Beat", each',
    '    if [Category] = "Dark, Unknown & Supernatural" then 1',
    '    else if List.Contains({"Separation & Loss", "Performance & Future"}, [Category]) then 3',
    '    else if [Category] = "Other Responses" then 0 else 2, Int64.Type),',
    ' WithBeatName = Table.AddColumn(WithBeat, "BeatName", each',
    '    {"Other answers", "I · Fears we outgrow", "II · Fears we keep", "III · Fears we grow into"}{[Beat]}, type text),',
    ' ShortPairs = {' + pairs_m + '},',
    ' WithShort = Table.AddColumn(WithBeatName, "FearShort", each',
    '    let f = [Fear], m = List.Select(ShortPairs, (p) => p{0} = f) in if List.IsEmpty(m) then f else m{0}{1}, type text)',
]) + "\n\t\t\t\tin WithShort")
s = s.replace(old_tail, new_tail)
anchor = "\tpartition DimFear = m"
assert s.count(anchor) == 1
newcols = (col("Beat", "int64", "Beat", fmt="0",
               desc="P28 story beat: 1 outgrow (Dark, Unknown & Supernatural), 2 keep (five categories), 3 grow into (Separation & Loss, Performance & Future), 0 other answers.")
           + col("BeatName", "string", "BeatName", sort="Beat")
           + col("FearShort", "string", "FearShort",
                 desc="Short display label for the poster; equals Fear except for twelve long labels. Fear keeps the original survey wording."))
s = s.replace(anchor, newcols + anchor)
wr(p, s)

# ---------------------------------------------------------------- 2. DataNightmare
lookup = [
    ("It arrives a mess (missing values, duplicates, inconsistent formats)", "It arrives a mess", "an altar set in a hurry", 1),
    ("It exists in too many versions (no clear source of truth)", "It exists in too many versions", "unclaimed ghosts, wandering", 2),
    ("It doesn’t add up (conflicting numbers and mysterious totals)", "It doesn't add up", "ghosts in the ledger", 3),
    ("It takes forever (painfully slow processing or queries)", "It takes forever", "the long wait at the gate", 4),
    ("It falls into the wrong hands (inappropriate access to sensitive data)", "It falls into the wrong hands", "an uninvited guest at the table", 5),
    ("The AI confidently gets it wrong (unreliable answers or predictions)", "The AI confidently gets it wrong", "a medium who answers anyway", 6),
    ("It never arrives (broken pipelines and failed refreshes)", "It never arrives", "the spirit no lantern guided home", 7),
    ("We spot the problem too late (missed events and warnings)", "We spot the problem too late", "the omen read after the fact", 8),
]
rows = [f'        {{"{a}", "{b}", "{c}", {n}}}' for a, b, c, n in lookup]
m_dn = [
    "let",
    "    Source = raw_survey_responses,",
    '    Kept = Table.SelectColumns(Source, {"ResponseKey", "dataNightmare"}),',
    "    Lookup = #table(type table [Full = text, Nightmare = text, RitualCaption = text, NightmareOrder = Int64.Type], {",
    ] + [r + ("," if i < len(rows) - 1 else "") for i, r in enumerate(rows)] + [
    "    }),",
    '    Joined = Table.NestedJoin(Kept, {"dataNightmare"}, Lookup, {"Full"}, "L", JoinKind.LeftOuter),',
    '    Expanded = Table.ExpandTableColumn(Joined, "L", {"Nightmare", "RitualCaption", "NightmareOrder"}),',
    '    Checked = if List.Contains(Expanded[Nightmare], null) then error "Unmapped dataNightmare label" else Expanded,',
    '    Typed = Table.TransformColumnTypes(Checked, {{"ResponseKey", Int64.Type}, {"dataNightmare", type text}, {"Nightmare", type text}, {"RitualCaption", type text}, {"NightmareOrder", Int64.Type}})',
    "in",
    "    Typed",
]
dn = ("/// P28: one row per response - the data-community nightmare (single choice). Nightmare is a short label and RitualCaption a poster caption, both a lookup on the original wording, which dataNightmare keeps unchanged. An unmapped label fails the refresh.\n"
      f"table DataNightmare\n\tlineageTag: {lt()}\n\n"
      + col("ResponseKey", "int64", "ResponseKey", hidden=True, fmt="0")
      + col("dataNightmare", "string", "dataNightmare")
      + col("Nightmare", "string", "Nightmare", sort="NightmareOrder")
      + col("RitualCaption", "string", "RitualCaption")
      + col("NightmareOrder", "int64", "NightmareOrder", hidden=True, fmt="0")
      + "\tpartition DataNightmare = m\n\t\tmode: import\n\t\tsource =\n" + msrc(m_dn) + "\n\n"
      + "\tannotation PBI_ResultType = Table\n\n")
p = os.path.join(T, "DataNightmare.tmdl")
assert not os.path.exists(p)
wr(p, dn)

# ---------------------------------------------------------------- 3. FabricTool
m_ft = [
    "let",
    '    Source = Table.SelectColumns(raw_survey_responses, {"ResponseKey", "fabricToolsJson"}),',
    '    Lists = Table.AddColumn(Source, "Tool", each if [fabricToolsJson] = null or Text.Trim([fabricToolsJson]) = "" then {} else Json.Document([fabricToolsJson]), type list),',
    '    Expanded = Table.ExpandListColumn(Table.RemoveColumns(Lists, {"fabricToolsJson"}), "Tool"),',
    "    NonNull = Table.SelectRows(Expanded, each [Tool] <> null),",
    '    Typed = Table.TransformColumnTypes(NonNull, {{"ResponseKey", Int64.Type}, {"Tool", type text}})',
    "in",
    "    Typed",
]
ft = ("/// P28: one row per respondent and Fabric tool named (fabricToolsJson expanded). Filtered from DataNightmare through ResponseKey.\n"
      f"table FabricTool\n\tlineageTag: {lt()}\n\n"
      + col("ResponseKey", "int64", "ResponseKey", hidden=True, fmt="0")
      + col("Tool", "string", "Tool")
      + "\tpartition FabricTool = m\n\t\tmode: import\n\t\tsource =\n" + msrc(m_ft) + "\n\n"
      + "\tannotation PBI_ResultType = Table\n\n")
p = os.path.join(T, "FabricTool.tmdl")
assert not os.path.exists(p)
wr(p, ft)

# ---------------------------------------------------------------- 4. relationship + model refs
p = os.path.join(D, "relationships.tmdl")
s = rd(p).replace("\r\n", "\n").rstrip("\n")
s += "\n\nrelationship FabricTool_DataNightmare\n\tfromColumn: FabricTool.ResponseKey\n\ttoColumn: DataNightmare.ResponseKey\n\n"
wr(p, s)
p = os.path.join(D, "model.tmdl")
s = rd(p).replace("\r\n", "\n")
old = '"FactFearSelection","_Measures"]'
assert s.count(old) == 1
s = s.replace(old, '"FactFearSelection","_Measures","DataNightmare","FabricTool"]')
old = "ref table 'View By'\n"
assert s.count(old) == 1
s = s.replace(old, old + "ref table DataNightmare\nref table FabricTool\n")
wr(p, s)
print("model: DimFear +3 columns, DataNightmare, FabricTool, 1 relationship, model refs")
