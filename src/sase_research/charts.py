"""All figures for the four tasks, drawn in one light, validated palette.

Palette: categorical slots 1-5 from the dataviz reference instance, validated
with ``validate_palette.js`` (light mode, surface #fcfcfb). Three slots sit
below 3:1 contrast, so every chart carries direct value or name labels.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from . import CHARTS, DATA  # noqa: E402
from .market import Triangulation  # noqa: E402
from .sizing import SizingResult  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8984"
GRID = "#e7e6e1"
NEUTRAL = "#c9c8c1"
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]  # blue, orange, aqua, yellow, magenta
NAVY = "#0f2a44"


def _fonts() -> str:
    for f in font_manager.findSystemFonts():
        if "/inter/" in f.lower():
            font_manager.fontManager.addfont(f)
    names = {f.name for f in font_manager.fontManager.ttflist}
    return "Inter" if "Inter" in names else "DejaVu Sans"


FONT = _fonts()
plt.rcParams.update(
    {
        "font.family": FONT,
        "font.size": 10,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK2,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlecolor": INK,
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "legend.frameon": False,
        "text.parse_math": False,
    }
)


def _save(fig, name: str) -> str:
    CHARTS.mkdir(parents=True, exist_ok=True)
    path = CHARTS / f"{name}.png"
    fig.savefig(path, dpi=220, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    return str(path)


def _source(fig, text: str) -> None:
    fig.text(0.0, -0.02, text, ha="left", va="top", fontsize=7.5, color=MUTED, transform=fig.transFigure)


def _ygrid(ax) -> None:
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)


def _xgrid(ax) -> None:
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)


# ---------------------------------------------------------------- Task 1
def estimate_dispersion(df: pd.DataFrame, t: Triangulation) -> str:
    d = df.sort_values("base_usd_b")
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    colors = [S[0] if a else NEUTRAL for a in d["anchor"]]
    y = np.arange(len(d))
    ax.barh(y, d["base_usd_b"], color=colors, height=0.62, edgecolor=SURFACE, linewidth=2)
    ax.set_yticks(y, d["publisher"])
    for yi, v in zip(y, d["base_usd_b"]):
        ax.text(v + 0.25, yi + (0.32 if abs(v - t.base_2025) < 1.6 else 0), f"${v:.1f}B", va="center", fontsize=8.5, color=INK2)
    ax.axvline(t.base_2025, color=NAVY, linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(t.base_2025 + 0.35, 1.0, f"Triangulated base ${t.base_2025:.1f}B\n(median of 4 anchors)",
            fontsize=8.5, color=NAVY, va="center", fontweight="semibold")
    ax.set_xlabel("2025 market size (USD billion)")
    _xgrid(ax)
    ax.set_xlim(0, d["base_usd_b"].max() * 1.18)
    ax.set_title(f"Eleven estimates, an {t.spread_ratio:.1f}x spread: SASE has no agreed size")
    ax.text(0, 1.02, "Blue = anchor estimates (Dell'Oro, Gartner, MarketsandMarkets, Mordor). Grey = other syndicated reports.",
            transform=ax.transAxes, fontsize=8, color=INK2)
    _source(fig, "Sources: publisher releases listed in data/sase_market_estimates.csv. Dell'Oro 2025 base derived from its $24B-by-2030 'doubling' forecast.")
    return _save(fig, "t1_estimate_dispersion")


def scenarios(t: Triangulation) -> str:
    s = t.scenarios
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    spec = [
        ("aggressive", S[1], f"Aggressive {t.cagr_aggressive:.1%} CAGR (MarketsandMarkets)"),
        ("base", S[0], f"Base {t.cagr_base:.1%} CAGR (median of 11 forecasts)"),
        ("conservative", S[2], f"Conservative {t.cagr_conservative:.1%} CAGR (Dell'Oro)"),
    ]
    ax.fill_between(s.year, s.conservative, s.aggressive, color=S[0], alpha=0.07, linewidth=0)
    for col, c, label in spec:
        ax.plot(s.year, s[col], color=c, linewidth=2.2, marker="o", markersize=6,
                markeredgecolor=SURFACE, markeredgewidth=1.5)
        ax.text(2030.12, s[col].iloc[-1], f"${s[col].iloc[-1]:.1f}B  {label}", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(2024.8, 2030.1)
    ax.set_ylim(0, s.aggressive.max() * 1.12)
    ax.set_ylabel("USD billion")
    _ygrid(ax)
    ax.set_title("Global SASE spend reaches $28B-$40B by 2030")
    _source(fig, "Model: src/sase_research/market.py. Base year $14.0B; growth rates from publishers in data/sase_market_estimates.csv.")
    return _save(fig, "t1_scenarios")


def dell_oro_quarters() -> str:
    q = pd.DataFrame({"q": ["1Q 2025", "2Q 2025", "3Q 2025"], "rev": [2.6, 2.7, 3.0], "yoy": [17, 22, 21]})
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.bar(q.q, q.rev, color=S[0], width=0.55, edgecolor=SURFACE, linewidth=2)
    for i, r in q.iterrows():
        ax.text(i, r.rev + 0.06, f"${r.rev:.1f}B\n+{r.yoy}% Y/Y", ha="center", fontsize=8.5, color=INK)
    ax.set_ylim(0, 3.7)
    _ygrid(ax)
    ax.set_ylabel("USD billion")
    ax.set_title("Quarterly SASE revenue is still accelerating")
    _source(fig, "Source: Dell'Oro Group SASE & SD-WAN quarterly reports (Jun, Sep, Dec 2025). 3Q is 'nearly $3B'.")
    return _save(fig, "t1_delloro_quarters")


def tam_sam_som(t: Triangulation, s: SizingResult, india_m: float) -> str:
    tiers = [
        ("TAM", "Global SASE spend, 2025", f"${t.base_2025:.1f}B", S[0]),
        ("Gateway", "India SASE market, 2025", f"${india_m:.0f}M", S[0]),
        ("SAM", "Sri Lankan SMEs that need SASE (P50)", f"${s.sam_p50/1e6:.0f}M / yr", S[2]),
        ("SOM", "One managed-SASE provider, year-5 ARR", f"${s.som_p50/1e6:.1f}M", S[1]),
    ]
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    widths = [9.8, 8.8, 7.8, 6.8]
    for i, ((tag, desc, val, c), w) in enumerate(zip(tiers, widths)):
        y = 3.4 - i * 1.05
        x = (10 - w) / 2
        ax.add_patch(FancyBboxPatch((x, y), w, 0.86, boxstyle="round,pad=0,rounding_size=0.12",
                                    facecolor=c, alpha=0.12 + 0.05 * i, edgecolor=c, linewidth=1.2))
        ax.text(x + 0.22, y + 0.43, tag, fontsize=11, fontweight="bold", color=INK, va="center")
        ax.text(x + 1.6, y + 0.43, desc.replace("\n", " "), fontsize=8.4, color=INK2, va="center")
        ax.text(x + w - 0.22, y + 0.43, val, fontsize=12, fontweight="bold", color=INK, va="center", ha="right")
    ax.set_title("From a $14B global market to a $4.6M beachhead", loc="left")
    _source(fig, "TAM: triangulated (Task 1). India: Coherent Market Insights. SAM/SOM: 20,000-draw Monte Carlo, src/sase_research/sizing.py.")
    return _save(fig, "t1_tam_sam_som")


def monte_carlo(s: SizingResult) -> str:
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    vals = s.sam_draws / 1e6
    ax.hist(vals, bins=70, color=S[2], alpha=0.85, edgecolor=SURFACE, linewidth=0.6)
    top = ax.get_ylim()[1]
    for v, lab in [(s.sam_p10, "P10"), (s.sam_p50, "P50"), (s.sam_p90, "P90")]:
        ax.axvline(v / 1e6, color=INK, linewidth=1.1, linestyle=(0, (3, 3)))
        ax.text(v / 1e6 + 2, top * 0.93, f"{lab}\n${v/1e6:.0f}M", fontsize=8.5, color=INK, va="top",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=SURFACE, edgecolor="none"))
    ax.set_xlabel("Serviceable market, Sri Lankan SMEs (USD million per year)")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, np.percentile(vals, 99.5))
    ax.set_title("SAM is most likely $53M-$134M a year (80% interval)")
    _source(fig, "20,000 draws from triangular input ranges in data/srilanka_sme_parameters.csv (seed 2026).")
    return _save(fig, "t1_monte_carlo")


LABELS = {
    "som_share_y5": "Year-5 share of SAM (2%-10%)",
    "small_avg_users": "Users per small firm (11-50)",
    "price_user_year": "Price per user per year ($60-$150)",
    "need_share": "Firms that need SASE (15%-40%)",
    "medium_avg_users": "Users per medium firm (51-200)",
    "firm_growth_factor": "Firm-count growth since census (1.0-1.25x)",
}


def tornado(s: SizingResult) -> str:
    d = s.tornado.iloc[::-1]
    base = s.som_mode / 1e6
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    y = np.arange(len(d))
    lo, hi = d.som_low / 1e6, d.som_high / 1e6
    ax.barh(y, lo - base, left=base, color=S[0], height=0.58, edgecolor=SURFACE, linewidth=2)
    ax.barh(y, hi - base, left=base, color=S[1], height=0.58, edgecolor=SURFACE, linewidth=2)
    for yi, l, h in zip(y, lo, hi):
        ax.text(l - 0.08, yi, f"${l:.1f}M", ha="right", va="center", fontsize=8, color=INK2)
        ax.text(h + 0.08, yi, f"${h:.1f}M", ha="left", va="center", fontsize=8, color=INK2)
    ax.axvline(base, color=INK, linewidth=1)
    ax.set_yticks(y, [LABELS[p] for p in d.parameter])
    ax.set_xlim(0, hi.max() * 1.15)
    ax.set_xlabel("Year-5 SOM (USD million). Blue = input at low end, orange = high end")
    _xgrid(ax)
    ax.set_title(f"Win rate and firm size move SOM most (centre = ${base:.1f}M at modal inputs)")
    _source(fig, "One-at-a-time sensitivity: each input swung to its low and high value while the others stay at their mode.")
    return _save(fig, "t1_tornado")


# ---------------------------------------------------------------- Task 2
def zscaler_dollar(r: dict) -> str:
    steps = [
        ("Revenue", 1.0),
        ("Cost of\nrevenue", -(1 - r["gross_margin"])),
        ("Sales &\nmarketing", -r["sm_pct"]),
        ("R&D", -r["rd_pct"]),
        ("G&A", -r["ga_pct"]),
    ]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    run = 0.0
    for i, (name, v) in enumerate(steps):
        bottom = run if v < 0 else 0
        h = v if v > 0 else -v
        start = run + v if v < 0 else 0
        color = S[0] if v > 0 else NEUTRAL
        ax.bar(i, h, bottom=start, color=color, width=0.6, edgecolor=SURFACE, linewidth=2)
        ax.text(i, start + h + 0.02, f"{'' if v > 0 else '-'}{abs(v)*100:.1f}c", ha="center", fontsize=9, color=INK)
        run = run + v if i else v
    op = r["op_margin"]
    ax.bar(len(steps), op, color=S[1], width=0.6, edgecolor=SURFACE, linewidth=2)
    ax.text(len(steps), op - 0.07, f"{op*100:.1f}c", ha="center", fontsize=9, color=INK, fontweight="semibold")
    ax.axhline(0, color=INK2, linewidth=0.8)
    ax.set_xticks(range(len(steps) + 1), [s[0] for s in steps] + ["Operating\nresult"])
    ax.set_ylim(-0.15, 1.15)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title("Where each revenue dollar went in FY2026: sales & marketing takes 45 cents")
    _source(fig, "Source: Zscaler Form 10-K, fiscal year ended 31 Jul 2026 (GAAP). Operating result = loss from operations / revenue.")
    return _save(fig, "t2_revenue_dollar")


def zscaler_cash(r: dict, prev_fcf: float, prev_sbc: float, prev_ocf: float, ocf: float) -> str:
    cats = ["Operating cash flow", "Free cash flow", "Stock-based comp", "FCF minus SBC"]
    fy25 = [prev_ocf, prev_fcf, prev_sbc, prev_fcf - prev_sbc]
    fy26 = [ocf, r["fcf_m"], r["sbc_m"], r["fcf_minus_sbc_m"]]
    x = np.arange(len(cats))
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.bar(x - 0.19, fy25, width=0.36, color=S[0], alpha=0.45, edgecolor=SURFACE, linewidth=2, label="FY2025")
    ax.bar(x + 0.19, fy26, width=0.36, color=S[0], edgecolor=SURFACE, linewidth=2, label="FY2026")
    for xi, a, b in zip(x, fy25, fy26):
        for off, v in [(-0.19, a), (0.19, b)]:
            ax.text(xi + off, v + (25 if v >= 0 else -70), f"{'-' if v < 0 else ''}${abs(v):,.0f}M", ha="center", fontsize=8, color=INK)
    ax.axhline(0, color=INK2, linewidth=0.8)
    ax.set_xticks(x, cats)
    _ygrid(ax)
    ax.set_ylabel("USD million")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("Cash-generative on paper, but stock pay now exceeds free cash flow")
    _source(fig, "Source: Zscaler 10-K FY2026 cash flow and equity statements. FCF = OCF - capex - capitalised software.")
    return _save(fig, "t2_cash_vs_sbc")


def zscaler_geo(fin: pd.DataFrame) -> str:
    regions = ["United States", "EMEA", "Asia Pacific", "Other"]
    f = fin.set_index("metric")
    y25 = [f.loc[f"Revenue {g}", "fy2025_usd_m"] for g in regions]
    y26 = [f.loc[f"Revenue {g}", "fy2026_usd_m"] for g in regions]
    x = np.arange(len(regions))
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    ax.bar(x - 0.19, y25, width=0.36, color=S[0], alpha=0.45, edgecolor=SURFACE, linewidth=2, label="FY2025")
    ax.bar(x + 0.19, y26, width=0.36, color=S[0], edgecolor=SURFACE, linewidth=2, label="FY2026")
    for xi, a, b in zip(x, y25, y26):
        ax.text(xi + 0.19, b + 25, f"${b:,.0f}M\n+{(b/a-1)*100:.0f}%", ha="center", fontsize=8, color=INK)
    ax.set_xticks(x, regions)
    _ygrid(ax)
    ax.set_ylim(0, max(y26) * 1.22)
    ax.set_ylabel("USD million")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("Growth is US-led; Asia Pacific is 15% of revenue and growing 23%")
    _source(fig, "Source: Zscaler 10-K FY2026, revenue by geographic area (based on customer ship-to address).")
    return _save(fig, "t2_geography")


def zscaler_growth_path(kpi_arr: float, r: dict) -> str:
    years = ["FY2024", "FY2025", "FY2026", "FY2027 guide"]
    growth = [2167.8 / 1617.0 - 1, r["revenue_growth"] - 0.0, r["revenue_growth"], r["fy27_rev_growth_mid"]]
    growth[1] = 2673.115 / 2167.8 - 1
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    colors = [S[0], S[0], S[0], S[1]]
    ax.bar(years, [g * 100 for g in growth], color=colors, width=0.56, edgecolor=SURFACE, linewidth=2)
    for i, g in enumerate(growth):
        ax.text(i, g * 100 + 0.8, f"{g*100:.1f}%", ha="center", fontsize=9, color=INK)
    ax.set_ylim(0, 42)
    _ygrid(ax)
    ax.set_ylabel("Revenue growth, %")
    ax.set_title("Guidance implies growth slows to ~17%")
    _source(fig, "FY2024-26 from 10-K revenue; FY2023 revenue $1,617.0M. FY2027 = midpoint of $3,908M-$3,938M guidance.")
    return _save(fig, "t2_growth_path")


# ---------------------------------------------------------------- Task 3
def price_vs_rating(comp: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for _, r in comp.iterrows():
        ax.plot([r.price_low_usd_user_yr, r.price_high_usd_user_yr], [r.g2_rating] * 2, color=S[0], alpha=0.35, linewidth=3,
                solid_capstyle="round")
        ax.scatter(r.price_mid_usd_user_yr, r.g2_rating, s=80, color=S[0], edgecolor=SURFACE, linewidth=2, zorder=3)
        dy = {"Netskope": -0.055, "Zscaler": 0.04, "Cato Networks": 0.04}.get(r.vendor, 0.04)
        ax.text(r.price_mid_usd_user_yr, r.g2_rating + dy, f"{r.vendor}  (${r.price_mid_usd_user_yr:.0f}, {r.g2_rating})",
                ha="center", fontsize=8.5, color=INK)
    ax.set_xlabel("Estimated price, USD per user per year (dot = midpoint, bar = reported range)")
    ax.set_ylabel("G2 star rating")
    ax.set_ylim(4.15, 4.75)
    ax.set_xlim(-10, 300)
    _ygrid(ax)
    ax.axvspan(-10, 100, color=S[2], alpha=0.06, linewidth=0)
    ax.text(2, 4.17, "SME-affordable zone (< $100/user/yr)", fontsize=8, color=INK2)
    ax.set_title("Satisfaction is tightly bunched; price is where vendors really differ")
    _source(fig, "Ratings: G2 product pages (Nov 2026). Prices: published list (Cloudflare) or third-party purchase data; see data/competitors.csv.")
    return _save(fig, "t3_price_vs_rating")


def growth_bars(comp: pd.DataFrame) -> str:
    d = comp.sort_values("growth_pct")
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    y = np.arange(len(d))
    ax.barh(y, d.growth_pct, color=S[0], height=0.58, edgecolor=SURFACE, linewidth=2)
    for yi, (_, r) in zip(y, d.iterrows()):
        ax.text(r.growth_pct + 0.8, yi, f"+{r.growth_pct:.0f}%  ·  ${r.scale_usd_m:,.0f}M {r.scale_metric.split(' (')[0]}",
                va="center", fontsize=8.3, color=INK2)
    ax.set_yticks(y, d.vendor)
    ax.set_xlim(0, 100)
    _xgrid(ax)
    ax.set_xlabel("Year-over-year growth, latest reported period (%)")
    ax.set_title("Challengers grow fastest; Palo Alto's figure is company-wide, not SASE-only")
    _source(fig, "Zscaler, Netskope, Cato: ARR. Palo Alto: Next-Gen Security ARR. Cloudflare: Q3 2026 revenue x4. Periods differ; see matrix.")
    return _save(fig, "t3_growth")


def scorecard(scores: pd.DataFrame, weights: dict) -> str:
    crit = list(weights)
    vendors = scores.index.tolist()
    m = scores[crit].values
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("blue", ["#eef4fc", S[0]])
    ax.imshow(m, cmap=cmap, vmin=1, vmax=5, aspect="auto")
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            ax.text(j, i, f"{m[i, j]:.1f}", ha="center", va="center", fontsize=9,
                    color="white" if m[i, j] >= 3.8 else INK)
    total = scores["weighted"].values
    for i, v in enumerate(total):
        ax.text(len(crit) - 0.3, i, f"{v:.2f}", va="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_xticks(range(len(crit)), [f"{c.replace(' ', chr(10), 1)}\n({weights[c]:.0%})" for c in crit], fontsize=8)
    ax.set_yticks(range(len(vendors)), vendors)
    ax.text(len(crit) - 0.35, -0.62, "Weighted", fontsize=8.5, fontweight="bold", color=INK)
    ax.set_xlim(-0.5, len(crit) + 0.45)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("SME-fit scorecard (1-5): who suits a Sri Lankan mid-sized firm?", pad=22)
    _source(fig, "Scores computed by formulas in outputs/Task3_Competitor_Matrix.xlsx from data/competitors.csv. Weights are editable there.")
    return _save(fig, "t3_scorecard")


# ---------------------------------------------------------------- Task 4
def regulation_timeline() -> str:
    ev = [
        ("2026-07-22", "Sri Lanka gazettes PDPA\nstart date", S[2], 1),
        ("2026-11-13", "India DPDP: consent-\nmanager rules live", S[0], -1),
        ("2027-01-01", "Sri Lanka PDPA core\nduties in force", S[2], 1),
        ("2027-05-13", "India DPDP: security &\n72-hour breach duties", S[0], -1),
        ("2027-12-31", "Sri Lanka targets PDPA\nenforcement by year-end", S[2], 1),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 3.3))
    dates = pd.to_datetime([e[0] for e in ev])
    ax.axhline(0, color=NEUTRAL, linewidth=2)
    align = {"2026-11-13": "right", "2027-01-01": "left", "2026-07-22": "left", "2027-12-31": "right"}
    for (iso, lab, c, side), d in zip(ev, dates):
        ax.plot([d, d], [0, 0.55 * side], color=c, linewidth=1.4)
        ax.scatter(d, 0, s=70, color=c, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.text(d, 0.62 * side, f"{d:%d %b %Y}\n{lab}", ha=align.get(iso, "center"),
                va="bottom" if side > 0 else "top", fontsize=8, color=INK)
    today = pd.Timestamp("2026-11-15")
    ax.scatter(today, 0, s=40, marker="v", color=S[1], zorder=4)
    ax.text(today + pd.Timedelta(days=6), 0.12, "today", color=S[1], fontsize=8, ha="left")
    ax.set_ylim(-1.55, 1.6)
    ax.set_yticks([])
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_visible(False)
    ax.set_xlim(pd.Timestamp("2026-06-01"), pd.Timestamp("2028-02-01"))
    ax.tick_params(axis="x", labelsize=8)
    ax.set_title("The compliance clock: two privacy laws switch on within 18 months", pad=8)
    ax.text(1.0, 0.02, "Green = Sri Lanka   Blue = India", transform=ax.transAxes, fontsize=8, color=INK2, ha="right")
    _source(fig, "Sources: Data Protection Authority of Sri Lanka (Gazette 2498/16); MeitY DPDP Rules 2025; see data/regulation.csv.")
    return _save(fig, "t4_regulation_timeline")


def srilanka_signals(ctx: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 2.6))
    tiles = [
        ("1.1M", "MSMEs = 52% of GDP,\n45% of jobs"),
        ("13.9M", "internet users\n(59.7% penetration)"),
        ("12,650", "cyber complaints to\nSri Lanka CERT in 2025"),
    ]
    for ax, (big, small) in zip(axes, tiles):
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.02, 0.05), 0.96, 0.9, boxstyle="round,pad=0,rounding_size=0.06",
                                    transform=ax.transAxes, facecolor="white", edgecolor=GRID))
        ax.text(0.5, 0.62, big, ha="center", va="center", fontsize=24, fontweight="bold", color=NAVY, transform=ax.transAxes)
        ax.text(0.5, 0.27, small, ha="center", va="center", fontsize=9, color=INK2, transform=ax.transAxes)
    _source(fig, "Sources: National SME Strategy Framework 2026; DataReportal Digital 2026: Sri Lanka; Sri Lanka CERT via The Morning (Jan 2026).")
    return _save(fig, "t4_srilanka_signals")


def build_all(df, t, s, india_m, fin, r, comp, scores, weights) -> dict:
    f = fin.set_index("metric")
    return {
        "dispersion": estimate_dispersion(df, t),
        "scenarios": scenarios(t),
        "quarters": dell_oro_quarters(),
        "funnel": tam_sam_som(t, s, india_m),
        "montecarlo": monte_carlo(s),
        "tornado": tornado(s),
        "dollar": zscaler_dollar(r),
        "cash": zscaler_cash(r, f.loc["Free cash flow", "fy2025_usd_m"], f.loc["Stock-based compensation", "fy2025_usd_m"],
                             f.loc["Operating cash flow", "fy2025_usd_m"], f.loc["Operating cash flow", "fy2026_usd_m"]),
        "geo": zscaler_geo(fin),
        "growthpath": zscaler_growth_path(r["arr_m"], r),
        "pricerating": price_vs_rating(comp),
        "growth": growth_bars(comp),
        "scorecard": scorecard(scores, weights),
        "timeline": regulation_timeline(),
        "signals": srilanka_signals(pd.read_csv(DATA / "srilanka_context.csv")),
    }
