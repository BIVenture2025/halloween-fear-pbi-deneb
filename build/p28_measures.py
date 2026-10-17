"""P28 Session 3 - guide sec 5 measures, display folder P28, appended to _Measures as TMDL text.
Multi-line DAX at 3 tabs, properties at 2 tabs (non-negotiable 4). CRLF. Refuses to run twice."""
import os, sys, uuid

D = sys.argv[1]
p = os.path.join(D, "tables", "_Measures.tmdl")
s = open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
if "displayFolder: P28" in s:
    sys.exit("P28 measures already present - refusing to run twice")

M = []  # (name, dax, formatString or None, dataCategory or None, description)


def m(name, dax, fmt=None, cat=None, desc=None):
    M.append((name, dax.strip("\n"), fmt, cat, desc))


INT = "#,##0"
DEATH = "Death (your own or a loved one’s)"
# ---- stage-scoped base
m("Picks Childhood", 'CALCULATE ( [Number of Fear Selections], KEEPFILTERS ( FactFearSelection[LifeStage] = "Childhood" ) )', INT,
  desc="Fear selections in the childhood list (285 overall).")
m("Picks Adult", 'CALCULATE ( [Number of Fear Selections], KEEPFILTERS ( FactFearSelection[LifeStage] = "Adult" ) )', INT,
  desc="Fear selections in the adult list (264 overall).")
m("People Childhood", 'CALCULATE ( [Number of Respondents], KEEPFILTERS ( FactFearSelection[LifeStage] = "Childhood" ) )', INT)
m("People Adult", 'CALCULATE ( [Number of Respondents], KEEPFILTERS ( FactFearSelection[LifeStage] = "Adult" ) )', INT)
m("Change People", "[People Adult] - [People Childhood]", "+#,##0;-#,##0;0")
m("People Kept", """
CALCULATE (
    [Number of Respondents],
    KEEPFILTERS ( FactFearSelection[LifeStage] = "Childhood" ),
    KEEPFILTERS ( FactFearSelection[IsRetained] = TRUE () )
)""", INT, desc="People who picked the fear as a child AND as an adult.")
m("Retention Rate", "DIVIDE ( [Responses Where Fears Remained], [Picks Childhood] )", "0.0%")
m("Fear Retention %", "DIVIDE ( [People Kept], [People Childhood] )", "0%")
m("New Since Childhood", "[People Adult] - [People Kept]", INT)
m("Respondents", "CALCULATE ( DISTINCTCOUNT ( DataNightmare[ResponseKey] ), REMOVEFILTERS ( DataNightmare ) )", INT,
  desc="Every response in the file (105), whether or not fears were picked.")
m("Share of Respondents", "DIVIDE ( [People Adult], [Respondents] )", "0%")
# ---- hero numbers (text)
m("Beat1 Hero", """
FORMAT ( CALCULATE ( [People Childhood], DimFear[Beat] = 1 ) + 0, "0" ) & " → "
    & FORMAT ( CALCULATE ( [People Adult], DimFear[Beat] = 1 ) + 0, "0" )""", desc="48 -> 14")
m("Beat2 Hero", f"""
VAR f = "{DEATH}"
RETURN
    FORMAT ( CALCULATE ( [People Childhood], DimFear[Fear] = f ) + 0, "0" ) & " → "
        & FORMAT ( CALCULATE ( [People Adult], DimFear[Fear] = f ) + 0, "0" )""", desc="9 -> 12")
m("Beat3 Hero", """
FORMAT ( CALCULATE ( [People Childhood], DimFear[Category] = "Performance & Future" ) + 0, "0" ) & " → "
    & FORMAT ( CALCULATE ( [People Adult], DimFear[Category] = "Performance & Future" ) + 0, "0" )""", desc="11 -> 42")
m("War Kept", 'CALCULATE ( [People Kept], DimFear[Fear] = "War" )', INT)
m("War Childhood", 'CALCULATE ( [People Childhood], DimFear[Fear] = "War" )', INT)
m("Financial Child", 'CALCULATE ( [People Childhood], DimFear[Fear] = "Financial insecurity/poverty" ) + 0', INT)
m("Financial Adult", 'CALCULATE ( [People Adult], DimFear[Fear] = "Financial insecurity/poverty" )', INT)
m("Beat3 Note", """
VAR k = [War Kept] + 0
VAR c = [War Childhood] + 0
RETURN
    IF ( k = c && c > 0, "All " & k, k & " of " & c ) & " who feared war as children still do. "
        & "The Hungry Ghost Festival burns paper money for the dead. Financial insecurity: "
        & FORMAT ( [Financial Child], "0" ) & " → " & FORMAT ( [Financial Adult] + 0, "0" ) & "." """)
m("Beat3 Note 1", """
VAR k = [War Kept] + 0
VAR c = [War Childhood] + 0
RETURN
    IF ( k = c && c > 0, "All " & k, k & " of " & c ) & " who feared war as children still do." """)
m("Beat3 Note 2", '"The Hungry Ghost Festival burns paper money"')
m("Beat3 Note 3", '"for the dead. Financial insecurity: " & FORMAT ( [Financial Child], "0" ) & " \u2192 " & FORMAT ( [Financial Adult] + 0, "0" ) & "."')
# ---- in-cell SVG (Image URL)
m("Dumbbell Body", """
VAR c = [People Childhood] + 0
VAR a = [People Adult] + 0
VAR maxV = 20 -- one fixed scale shared by the three beat tables
VAR x0 = 14
VAR x1 = 150
VAR xc = ROUND ( x0 + MIN ( c, maxV ) / maxV * ( x1 - x0 ), 1 )
VAR xa = ROUND ( x0 + MIN ( a, maxV ) / maxV * ( x1 - x0 ), 1 )
VAR col = SWITCH ( SELECTEDVALUE ( DimFear[Beat] ), 1, "%233DE0D0", 2, "%23FF3D9A", 3, "%23FFB400", "%23A99BD6" )
VAR up = a >= c
RETURN
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 175 22' width='175' height='22'>"
        & "<line x1='" & x0 & "' y1='11' x2='" & x1 & "' y2='11' stroke='%23A99BD6' stroke-opacity='.35'/>"
        & "<line x1='" & xc & "' y1='11' x2='" & xa & "' y2='11' stroke='" & col & "' stroke-width='3'/>"
        & "<circle cx='" & xc & "' cy='11' r='5.5' fill='%231E0F4A' stroke='%23FFF3DC' stroke-width='2'/>"
        & "<circle cx='" & xa & "' cy='11' r='6.5' fill='" & col & "'/>"
        & "<text x='" & IF ( up, xa + 10, xa - 10 ) & "' y='15' font-family='Segoe UI' font-size='12' font-weight='700' fill='%23FFF3DC' text-anchor='" & IF ( up, "start", "end" ) & "'>" & a & "</text>"
        & "<text x='" & IF ( up, xc - 9, xc + 9 ) & "' y='15' font-family='Segoe UI' font-size='11' fill='%23A99BD6' text-anchor='" & IF ( up, "end", "start" ) & "'>" & c & "</text>"
        & "</svg>" """, desc="SVG markup (no data-URI prefix) for one dumbbell row: hollow ring = people as a child, filled dot = people now; scale 0-20 shared by beats I-III.")
m("Dumbbell SVG", '"data:image/svg+xml;utf8," & [Dumbbell Body]', cat="ImageUrl")
m("Kept Units Body", """
VAR n = [People Childhood] + 0
VAR k = [People Kept] + 0
VAR dots =
    CONCATENATEX (
        GENERATESERIES ( 1, n ),
        VAR x = 7 + ( [Value] - 1 ) * 14.5
        RETURN
            IF (
                [Value] <= k,
                "<circle cx='" & x & "' cy='11' r='5.5' fill='%23FF3D9A'/>",
                "<circle cx='" & x & "' cy='11' r='5' fill='none' stroke='%23A99BD6' stroke-width='1.5'/>"
            ),
        "",
        [Value]
    )
RETURN
    IF ( n > 0, "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 205 22' width='205' height='22'>" & dots & "</svg>" )""",
  desc="SVG markup (no prefix): one circle per person who held the fear as a child; filled = still holds it.")
m("Kept Units SVG", 'IF ( NOT ISBLANK ( [Kept Units Body] ), "data:image/svg+xml;utf8," & [Kept Units Body] )', cat="ImageUrl")
# ---- row selection for the three beat tables (blank = row hidden)
m("B1 Order", """
VAR score = [Change People] * 100 - [People Childhood]
VAR r =
    RANKX (
        FILTER ( ALL ( DimFear ), DimFear[Beat] = 1 ),
        CALCULATE ( [Change People] * 100 - [People Childhood] ),
        score,
        ASC,
        SKIP
    )
RETURN
    IF ( HASONEVALUE ( DimFear[Fear] ) && SELECTEDVALUE ( DimFear[Beat] ) = 1 && r <= 5, r )""", "0",
  desc="Top 5 beat-I fears by change in people (largest drop first; ties on people as a child).")
m("B1 Dumbbell", 'IF ( NOT ISBLANK ( [B1 Order] ), "data:image/svg+xml;utf8," & [Dumbbell Body] )', cat="ImageUrl")
m("B2 Order", f"""
SWITCH ( SELECTEDVALUE ( DimFear[Fear] ), "{DEATH}", 1, "Cancer or another serious diagnosis", 2 )""", "0")
m("B2 Dumbbell", 'IF ( NOT ISBLANK ( [B2 Order] ), "data:image/svg+xml;utf8," & [Dumbbell Body] )', cat="ImageUrl")
m("Sticky Order", """
VAR r =
    RANKX ( FILTER ( ALL ( DimFear ), [People Childhood] >= 10 ), [People Kept] + 0, [People Kept] + 0, DESC, SKIP )
RETURN
    IF ( HASONEVALUE ( DimFear[Fear] ) && [People Childhood] >= 10 && r <= 3, r )""", "0",
  desc="Top 3 by people kept among fears held by at least 10 people as children.")
m("Sticky Count", 'IF ( NOT ISBLANK ( [Sticky Order] ), FORMAT ( [People Kept] + 0, "0" ) & " of " & FORMAT ( [People Childhood], "0" ) )')
m("Sticky Units", 'IF ( NOT ISBLANK ( [Sticky Order] ), "data:image/svg+xml;utf8," & [Kept Units Body] )', cat="ImageUrl")
m("B3 Order", """
VAR score = -( [Change People] * 100 + [People Childhood] )
VAR r =
    RANKX (
        FILTER ( ALL ( DimFear ), DimFear[Beat] = 3 ),
        CALCULATE ( -( [Change People] * 100 + [People Childhood] ) ),
        score,
        ASC,
        SKIP
    )
RETURN
    IF ( HASONEVALUE ( DimFear[Fear] ) && SELECTEDVALUE ( DimFear[Beat] ) = 3 && r <= 5, r )""", "0",
  desc="Top 5 beat-III fears by change in people (largest rise first).")
m("B3 Dumbbell", 'IF ( NOT ISBLANK ( [B3 Order] ), "data:image/svg+xml;utf8," & [Dumbbell Body] )', cat="ImageUrl")
# ---- nightmares
m("Nightmare Respondents", "DISTINCTCOUNT ( DataNightmare[ResponseKey] )", INT)
m("Nightmare Share", "DIVIDE ( [Nightmare Respondents], CALCULATE ( [Nightmare Respondents], REMOVEFILTERS ( DataNightmare ) ) )", "0%")
m("Nightmare Rank", """
RANKX (
    ALL ( DataNightmare[Nightmare], DataNightmare[NightmareOrder] ),
    [Nightmare Respondents],
    ,
    DESC,
    DENSE
)""", "0", desc="ALL names the sort-by column too, or every bar ranks 1.")
m("Nightmare Bar Color", 'IF ( [Nightmare Rank] = 1, "#C8006E", "#5B2DBF" )')
m("Ritual Caption", "SELECTEDVALUE ( DataNightmare[RitualCaption] )")
# ---- who answered
m("Tool Users", "DISTINCTCOUNT ( FabricTool[ResponseKey] )", INT)
m("Fabric Users", 'CALCULATE ( DISTINCTCOUNT ( FabricTool[ResponseKey] ), KEEPFILTERS ( FabricTool[Tool] <> "None yet" ) )', INT,
  desc="Respondents who named at least one Fabric tool (97).")
m("Europe Childhood", 'CALCULATE ( [People Childhood], DimCountry[Continent] = "Europe" )', INT)
m("Europe Now", 'CALCULATE ( [People Adult], DimCountry[Continent] = "Europe" )', INT)
m("Honesty 1", 'FORMAT ( [Respondents], "0" ) & " people, self-reported: it reflects who took part, not everyone."')
m("Honesty 2", """
VAR mn = CALCULATE ( [Number of Respondents], DimGender[Gender] = "Male" ) + 0
VAR wm = CALCULATE ( [Number of Respondents], DimGender[Gender] = "Female" ) + 0
RETURN
    mn & " men · " & wm & " women · " & ( [Respondents] - mn - wm ) & " another gender or preferred not to say." """)
m("Honesty 3", """
VAR a = CALCULATE ( [Number of Respondents], DimAgeGroup[AgeGroup] IN { "25" & UNICHAR ( 8211 ) & "34", "35" & UNICHAR ( 8211 ) & "44" } ) + 0
RETURN
    a & " of " & [Respondents] & " aged 25–44 · about two-thirds in Europe (" & [Europe Childhood] & " as children, " & [Europe Now] & " now)." """)
m("Honesty 4", '"Up to 3 fears per life stage; counts are people unless marked picks."')
m("Honesty 5", """
VAR t1 = CALCULATE ( [Tool Users], FabricTool[Tool] = "Power BI reports" )
VAR t2 = CALCULATE ( [Tool Users], FabricTool[Tool] = "Power BI semantic models" )
VAR t3 = CALCULATE ( [Tool Users], FabricTool[Tool] = "Lakehouses" )
RETURN
    [Fabric Users] & " of " & [Respondents] & " use Fabric: Power BI reports " & t1 & ", semantic models " & t2 & ", Lakehouses " & t3 & "." """)
# ---- tooltip sentences
m("TT Outgrow Sentence", """
VAR f = LOWER ( SELECTEDVALUE ( DimFear[FearShort] ) )
VAR c = [People Childhood] + 0
VAR a = [People Adult] + 0
VAR k = [People Kept] + 0
RETURN
    IF (
        HASONEVALUE ( DimFear[Fear] ),
        c & IF ( c = 1, " person", " people" ) & " feared " & f & " as children; " & a & " do now. "
            & IF ( k = 0, "None kept it.", k & " kept it." )
    )""")
m("TT Keep Sentence", """
VAR f = LOWER ( SELECTEDVALUE ( DimFear[FearShort] ) )
VAR c = [People Childhood] + 0
VAR k = [People Kept] + 0
RETURN
    IF ( HASONEVALUE ( DimFear[Fear] ) && c > 0,
        k & " of " & c & " still fear " & f & " (" & FORMAT ( DIVIDE ( k, c ), "0%" ) & ")." )""")
m("TT GrowInto Sentence", """
VAR f = LOWER ( SELECTEDVALUE ( DimFear[FearShort] ) )
VAR a = [People Adult] + 0
VAR k = [People Kept] + 0
RETURN
    IF ( HASONEVALUE ( DimFear[Fear] ),
        a & IF ( a = 1, " person fears ", " people fear " ) & f & " now; " & ( a - k ) & " of them did not as children." )""")
m("TT Nightmare Sentence", """
VAR n = [Nightmare Respondents]
VAR full = SELECTEDVALUE ( DataNightmare[dataNightmare] )
VAR tools =
    TOPN (
        3,
        FILTER ( VALUES ( FabricTool[Tool] ), FabricTool[Tool] <> "None yet" ),
        [Tool Users], DESC,
        FabricTool[Tool], ASC
    )
VAR toolList =
    CONCATENATEX ( tools, FabricTool[Tool] & " (" & [Tool Users] & ")", ", ", [Tool Users], DESC, FabricTool[Tool], ASC )
RETURN
    IF ( HASONEVALUE ( DataNightmare[Nightmare] ),
        n & " of " & [Respondents] & " chose: " & full & ". Their most-used Fabric tools: " & toolList & "." )""")


def emit(name, dax, fmt, cat, desc):
    out = []
    if desc:
        out.append(f"\t/// {desc}")
    q = f"'{name}'" if any(ch in name for ch in " %-") else name
    lines = dax.split("\n")
    if len(lines) == 1:
        out.append(f"\tmeasure {q} = {lines[0].strip()}")
    else:
        out.append(f"\tmeasure {q} =")
        out += ["\t\t\t" + l.rstrip() for l in lines if l.strip() != ""]
    if fmt:
        out.append(f"\t\tformatString: {fmt}")
    out.append("\t\tdisplayFolder: P28")
    if cat:
        out.append(f"\t\tdataCategory: {cat}")
    out.append(f"\t\tlineageTag: {uuid.uuid5(uuid.NAMESPACE_URL, 'p28-measure-' + name)}")
    return "\n".join(out) + "\n\n"


block = "".join(emit(*x) for x in M)
anchor = "\tcolumn Column1"
assert s.count(anchor) == 1
s = s.replace(anchor, block + anchor)
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n"))
print(f"measures: {len(M)} added to _Measures (displayFolder P28); ImageUrl: {sum(1 for x in M if x[3])}")
