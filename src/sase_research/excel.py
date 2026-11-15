"""Build the two Excel deliverables with live formulas (no hard-coded results).

* outputs/Task1_SASE_Market_Model.xlsx  - estimates, triangulation, scenarios, Sri Lanka SAM/SOM
* outputs/Task3_Competitor_Matrix.xlsx  - matrix, editable weights, scorecard, SWOT, sources
"""

from __future__ import annotations

import pandas as pd
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from . import DATA, OUT
from .scorecard import WEIGHTS
from .swot import ENTRANT, SWOT

F = "Arial"
BLUE = Font(name=F, size=10, color="0000FF")
BLACK = Font(name=F, size=10, color="000000")
GREEN = Font(name=F, size=10, color="008000")
BOLD = Font(name=F, size=10, bold=True)
HEAD = Font(name=F, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=F, size=14, bold=True, color="0F2A44")
NOTE = Font(name=F, size=9, italic=True, color="52514E")
HEAD_FILL = PatternFill("solid", fgColor="0F2A44")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
BAND = PatternFill("solid", fgColor="F3F6FA")
THIN = Side(style="thin", color="D9DDE3")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def _header(ws, row: int, labels: list[str], widths: list[int] | None = None) -> None:
    for j, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=lab)
        c.font, c.fill, c.alignment, c.border = HEAD, HEAD_FILL, CENTER, BOX
        if widths:
            ws.column_dimensions[get_column_letter(j)].width = widths[j - 1]
    ws.row_dimensions[row].height = 32


def _title(ws, text: str, sub: str) -> None:
    ws["A1"] = text
    ws["A1"].font = TITLE
    ws["A2"] = sub
    ws["A2"].font = NOTE


def _legend(ws, row: int) -> None:
    ws.cell(row=row, column=1, value="Legend:").font = BOLD
    ws.cell(row=row, column=2, value="Blue text = sourced input").font = BLUE
    ws.cell(row=row, column=3, value="Black = formula").font = BLACK
    c = ws.cell(row=row, column=4, value="Yellow fill = assumption you may edit")
    c.font, c.fill = BLACK, INPUT_FILL
    ws.cell(row=row, column=5, value="Green = link to another sheet").font = GREEN


# ---------------------------------------------------------------- Task 1
def market_model() -> str:
    est = pd.read_csv(DATA / "sase_market_estimates.csv")
    par = pd.read_csv(DATA / "srilanka_sme_parameters.csv")
    wb = Workbook()

    ws = wb.active
    ws.title = "Estimates"
    _title(ws, "Task 1 - Global SASE market: published estimates",
           "Edge Shift research, Risny Suha, Datheon AI Research & Market Intelligence (DT-2026-P5IEX), November 2026")
    _legend(ws, 3)
    cols = ["ID", "Publisher", "Tier", "Anchor? (1 = yes)", "2025 size ($bn)", "Forecast year", "Forecast ($bn)",
            "Stated CAGR", "Implied CAGR (check)", "Basis", "Source", "Anchor value ($bn)"]
    _header(ws, 5, cols, [6, 30, 12, 11, 12, 10, 12, 11, 13, 46, 60, 12])
    anchors = {"DO", "GA", "MM", "MO"}
    for i, r in est.iterrows():
        row = 6 + i
        vals = [r.id, r.publisher, r.tier, 1 if r.id in anchors else 0, r.base_usd_b, int(r.forecast_year),
                r.forecast_usd_b, r.cagr_pct / 100]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = BLUE if j >= 4 else BLACK
            c.border = BOX
        ws.cell(row=row, column=4).fill = INPUT_FILL
        base_year = 2025
        c = ws.cell(row=row, column=9, value=f"=(G{row}/E{row})^(1/(F{row}-{base_year}))-1")
        c.font, c.border, c.number_format = BLACK, BOX, "0.0%"
        ws.cell(row=row, column=8).number_format = "0.0%"
        for j in (5, 7):
            ws.cell(row=row, column=j).number_format = '$#,##0.00'
        ws.cell(row=row, column=10, value=r.basis).alignment = WRAP
        ws.cell(row=row, column=11, value=r.source_url).font = NOTE
        for j in (10, 11):
            ws.cell(row=row, column=j).border = BOX
        c = ws.cell(row=row, column=12, value=f'=IF(D{row}=1,E{row},"")')
        c.font, c.border, c.number_format = BLACK, BOX, '$#,##0.00'
    last = 5 + len(est)
    n = last + 2
    ws.cell(row=n, column=9, value="Note: implied CAGR uses 2025 as base; publishers whose CAGR window starts in 2026 differ slightly.").font = NOTE

    ws2 = wb.create_sheet("Triangulation")
    _title(ws2, "Triangulated base year and 2030 scenarios", "All cells below are formulas over the Estimates sheet.")
    ws2.column_dimensions["A"].width = 46
    for col in "BCDEFG":
        ws2.column_dimensions[col].width = 14
    rng = f"Estimates!$E$6:$E${last}"
    anc = f"Estimates!$L$6:$L${last}"
    rows = [
        ("Anchor median, 2025 ($bn)", f"=MEDIAN({anc})", '$#,##0.00', False),
        ("Anchor low ($bn)", f"=MIN({anc})", '$#,##0.00', False),
        ("Anchor high ($bn)", f"=MAX({anc})", '$#,##0.00', False),
        ("All-estimate median ($bn)", f"=MEDIAN({rng})", '$#,##0.00', False),
        ("Spread: highest / lowest", f"=MAX({rng})/MIN({rng})", '0.0"x"', False),
        ("Conservative CAGR (Dell'Oro implied)", "=Estimates!I6", "0.0%", False),
        ("Base CAGR (median of stated CAGRs)", f"=MEDIAN(Estimates!$H$6:$H${last})", "0.0%", False),
        ("Aggressive CAGR (MarketsandMarkets)", "=Estimates!H8", "0.0%", False),
    ]
    for i, (lab, f, fmt, arr) in enumerate(rows):
        r = 4 + i
        ws2.cell(row=r, column=1, value=lab).font = BOLD
        c = ws2.cell(row=r, column=2, value=f)
        c.font = GREEN if f.startswith("=Estimates!") else BLACK
        c.number_format = fmt
        c.border = BOX
    _header(ws2, 14, ["Scenario ($bn)", "2025", "2026", "2027", "2028", "2029", "2030"])
    for k, (lab, ref) in enumerate([("Conservative", "$B$9"), ("Base", "$B$10"), ("Aggressive", "$B$11")]):
        r = 15 + k
        ws2.cell(row=r, column=1, value=lab).font = BOLD
        for j in range(6):
            c = ws2.cell(row=r, column=2 + j, value=f"=$B$4*(1+{ref})^{j}")
            c.number_format, c.border, c.font = '$#,##0.0', BOX, BLACK
    ws2["A19"] = "Base year = anchor median. Each scenario compounds that base at its CAGR."
    ws2["A19"].font = NOTE

    ws3 = wb.create_sheet("Sri Lanka SAM-SOM")
    _title(ws3, "Bottom-up: Sri Lankan SME SASE market (modal case)",
           "Edit the yellow cells. The Python model (src/sase_research/sizing.py) runs 20,000 Monte Carlo draws over the low-high ranges.")
    _legend(ws3, 3)
    _header(ws3, 5, ["Parameter", "Low", "Mode (used)", "High", "Unit", "Kind", "Rationale", "Source"],
            [26, 11, 13, 11, 10, 12, 60, 60])
    for i, r in par.iterrows():
        row = 6 + i
        vals = [r.parameter, r.low, r["mode"], r.high, r.unit, r.kind, r.rationale, r.source]
        for j, v in enumerate(vals, 1):
            c = ws3.cell(row=row, column=j, value=v)
            c.border = BOX
            c.font = BLUE if j in (2, 3, 4) else BLACK
            if j in (7, 8):
                c.alignment = WRAP
        if r.kind != "sourced":
            ws3.cell(row=row, column=3).fill = INPUT_FILL
        for j in (2, 3, 4):
            ws3.cell(row=row, column=j).number_format = "0.0%" if r.unit == "share" else "#,##0.00" if r.unit == "multiplier" else "#,##0"
    m = {p: f"$C${6 + i}" for i, p in enumerate(par.parameter)}
    out = [
        ("Seats that need SASE", f"={m['firm_growth_factor']}*{m['need_share']}*({m['small_firms']}*{m['small_avg_users']}+{m['medium_firms']}*{m['medium_avg_users']})", "#,##0"),
        ("SAM, USD per year", f"=C16*{m['price_user_year']}", "$#,##0"),
        ("SOM, year-5 ARR (USD)", f"=C17*{m['som_share_y5']}", "$#,##0"),
    ]
    for i, (lab, f, fmt) in enumerate(out):
        r = 16 + i
        ws3.cell(row=r, column=1, value=lab).font = BOLD
        c = ws3.cell(row=r, column=3, value=f)
        c.number_format, c.font, c.border = fmt, BLACK, BOX
    ws3["A20"] = ("Monte Carlo (Python, 20,000 draws): see outputs/model_results.json for P10/P50/P90. "
                  "The modal case sits low because the seat ranges skew upward.")
    ws3["A20"].font = NOTE
    path = OUT / "Task1_SASE_Market_Model.xlsx"
    wb.save(path)
    return str(path)


# ---------------------------------------------------------------- Task 3
MATRIX_COLS = [
    ("vendor", "Vendor", 18), ("product", "Product", 26), ("hq", "HQ", 16), ("ownership", "Ownership", 22),
    ("gartner_sase_mq_2026", "Gartner SASE MQ 2026", 24), ("scale_metric", "Scale metric", 20),
    ("scale_usd_m", "Scale ($m)", 11), ("growth_pct", "Growth Y/Y (%)", 10), ("scale_note", "Scale period / note", 26),
    ("customers_note", "Customers", 22), ("pricing_model", "Pricing model", 30), ("published_entry_price", "Published entry price", 22),
    ("price_low_usd_user_yr", "Price low ($/user/yr)", 11), ("price_mid_usd_user_yr", "Price mid ($/user/yr)", 11),
    ("price_high_usd_user_yr", "Price high ($/user/yr)", 11), ("pricing_note", "Pricing evidence", 40),
    ("g2_rating", "G2 rating", 9), ("g2_reviews", "G2 reviews", 9), ("gartner_pi_rating", "Gartner Peer Insights", 10),
    ("gartner_pi_ratings", "Peer Insights ratings", 10), ("architecture", "Architecture", 30), ("differentiator", "Key differentiator", 36),
    ("review_praise", "What reviewers praise", 28), ("review_complaints", "What reviewers dislike", 30),
    ("vulnerability", "Vulnerability", 40), ("south_asia_presence", "South Asia / Sri Lanka presence", 26),
    ("sme_fit_score", "Small-firm fit (1-5, judgement)", 11), ("sme_fit_reason", "Small-firm fit rationale", 40),
]
NUMERIC = {"scale_usd_m", "growth_pct", "price_low_usd_user_yr", "price_mid_usd_user_yr", "price_high_usd_user_yr",
           "g2_rating", "g2_reviews", "gartner_pi_rating", "gartner_pi_ratings", "sme_fit_score"}


def competitor_matrix() -> str:
    comp = pd.read_csv(DATA / "competitors.csv")
    wb = Workbook()
    ws = wb.active
    ws.title = "Matrix"
    _title(ws, "Task 3 - SASE competitive matrix: five vendors",
           "Data as of 15 November 2026. Prices for quote-only vendors are third-party estimates, not list prices.")
    _legend(ws, 3)
    _header(ws, 5, [c[1] for c in MATRIX_COLS], [c[2] for c in MATRIX_COLS])
    col_of = {k: get_column_letter(j) for j, (k, _, _) in enumerate(MATRIX_COLS, 1)}
    for i, r in comp.iterrows():
        row = 6 + i
        for j, (key, _, _) in enumerate(MATRIX_COLS, 1):
            v = r[key]
            v = None if pd.isna(v) else v
            c = ws.cell(row=row, column=j, value=v)
            c.border = BOX
            c.alignment = WRAP
            c.font = BLUE if key in NUMERIC else BLACK
            if key == "sme_fit_score":
                c.fill = INPUT_FILL
            if i % 2 and key != "sme_fit_score":
                c.fill = BAND
        ws.row_dimensions[row].height = 78
    ws.cell(row=6, column=1).comment = Comment("Zscaler: Form 10-K FY2026 and Q4 FY2026 results (Sep 2026).", "Risny Suha")
    ws.freeze_panes = "B6"
    ws.cell(row=12, column=1, value="Notes").font = BOLD
    notes = [
        "Scale figures differ in kind: Zscaler, Netskope and Cato report ARR; Palo Alto reports company-wide Next-Gen Security ARR; "
        "Cloudflare is company revenue (Q3 2026 x4). Compare growth, not size.",
        "Palo Alto Prisma Access has no Gartner Peer Insights figure here because none was verified.",
        "G2 and Gartner Peer Insights ratings captured November 2026; counts change daily.",
        "Full source list: data/sources.md in the repository.",
    ]
    for k, t in enumerate(notes):
        ws.cell(row=13 + k, column=1, value=t).font = NOTE

    wsw = wb.create_sheet("Weights")
    _title(wsw, "Scoring weights (edit the yellow cells)", "Weights must total 100%. The Scorecard recalculates automatically.")
    _header(wsw, 4, ["Criterion", "Weight", "How it is scored"], [24, 10, 90])
    how = {
        "Affordability": "Formula: MAX(1,MIN(5,5-4*price_mid/300)): 5 at $0, 1 at $300 per user per year",
        "Small-firm fit": "Judgement score from evidence in the Matrix (minimum deal size, free tier, per-site costs)",
        "User satisfaction": "Formula: MAX(1,MIN(5,1+(G2-4)/0.7*4)): G2 4.0 maps to 1, 4.7 maps to 5",
        "Market validation": "Gartner SASE MQ 2026: Leader 5, Visionary 3.5, Challenger 3, Niche 2",
        "Price transparency": "Published self-serve price = 5, quote-only = 1",
        "Momentum": "Formula: MAX(1,MIN(5,1+growth/50*4)): latest reported Y/Y growth",
    }
    for i, (k, w) in enumerate(WEIGHTS.items()):
        r = 5 + i
        wsw.cell(row=r, column=1, value=k).font = BOLD
        c = wsw.cell(row=r, column=2, value=w)
        c.font, c.fill, c.number_format, c.border = BLUE, INPUT_FILL, "0%", BOX
        wsw.cell(row=r, column=3, value=how[k]).font = BLACK
    wsw.cell(row=11, column=1, value="Total (must be 100%)").font = BOLD
    c = wsw.cell(row=11, column=2, value="=SUM(B5:B10)")
    c.number_format, c.font = "0%", BOLD
    wsw.cell(row=11, column=3, value='=IF(ROUND(B11,4)=1,"OK","Weights do not sum to 100%")').font = BOLD

    wss = wb.create_sheet("Scorecard")
    _title(wss, "SME-fit scorecard (1-5)", "Every score is a formula over the Matrix and Weights sheets.")
    crit = list(WEIGHTS)
    _header(wss, 4, ["Vendor"] + crit + ["Weighted score", "Rank"], [20, 13, 13, 13, 13, 13, 13, 14, 8])
    for i in range(len(comp)):
        mr = 6 + i
        r = 5 + i
        wss.cell(row=r, column=1, value=f"=Matrix!A{mr}").font = GREEN
        pm, g2, gr, mqc = (f"Matrix!{col_of[k]}{mr}" for k in ("price_mid_usd_user_yr", "g2_rating", "growth_pct", "gartner_sase_mq_2026"))
        f = [
            f"=MAX(1,MIN(5,5-4*{pm}/300))",
            f"=Matrix!{col_of['sme_fit_score']}{mr}",
            f"=MAX(1,MIN(5,1+({g2}-4)/0.7*4))",
            f'=IF(LEFT({mqc},6)="Leader",5,IF(LEFT({mqc},9)="Visionary",3.5,IF(LEFT({mqc},10)="Challenger",3,2)))',
            f'=IF(OR(Matrix!{col_of["published_entry_price"]}{mr}="None published",Matrix!{col_of["published_entry_price"]}{mr}="Contact for pricing"),1,5)',
            f"=MAX(1,MIN(5,1+{gr}/50*4))",
        ]
        for j, formula in enumerate(f):
            c = wss.cell(row=r, column=2 + j, value=formula)
            c.number_format, c.border, c.alignment = "0.00", BOX, CENTER
            c.font = GREEN if formula.startswith("=Matrix") else BLACK
        c = wss.cell(row=r, column=8, value=f"=B{r}*Weights!$B$5+C{r}*Weights!$B$6+D{r}*Weights!$B$7+E{r}*Weights!$B$8+F{r}*Weights!$B$9+G{r}*Weights!$B$10")
        c.number_format, c.font, c.border, c.alignment = "0.00", BOLD, BOX, CENTER
        c = wss.cell(row=r, column=9, value=f"=RANK(H{r},$H$5:$H${4 + len(comp)})")
        c.font, c.border, c.alignment = BOLD, BOX, CENTER
    end = 4 + len(comp)
    wss.conditional_formatting.add(f"B5:H{end}", ColorScaleRule(start_type="num", start_value=1, start_color="EEF4FC",
                                                                  end_type="num", end_value=5, end_color="2A78D6"))
    wss.cell(row=end + 2, column=1, value="Reading the scorecard: it ranks fit for a Sri Lankan firm of 20-200 users, "
                                           "not overall product quality. Enterprise buyers would weight scale and depth higher.").font = NOTE

    wsx = wb.create_sheet("SWOT")
    _title(wsx, "SWOT by vendor", "Each point traces to a figure in the Matrix or a cited source.")
    _header(wsx, 4, ["Vendor", "Strengths", "Weaknesses", "Opportunities", "Threats"], [20, 48, 48, 48, 48])
    for i, (v, d) in enumerate(list(SWOT.items()) + [(ENTRANT["title"], ENTRANT)]):
        r = 5 + i
        wsx.cell(row=r, column=1, value=v).font = BOLD
        for j, k in enumerate("SWOT", 2):
            c = wsx.cell(row=r, column=j, value="\n".join(f"• {x}" for x in d[k]))
            c.alignment, c.border, c.font = WRAP, BOX, BLACK
        wsx.cell(row=r, column=1).alignment = WRAP
        wsx.row_dimensions[r].height = 120

    path = OUT / "Task3_Competitor_Matrix.xlsx"
    wb.save(path)
    return str(path)
