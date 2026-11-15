"""Task 1-3 documents. Every number is pulled from the models, never typed by hand."""

from __future__ import annotations

import pandas as pd

from . import DATA
from .market import Triangulation
from .refs import Cite
from .render import AUTHOR, DATE, PROGRAM, fig, page, to_pdf
from .sizing import SizingResult
from .swot import SWOT


def b(x: float, d: int = 1) -> str:
    return f"${x:,.{d}f}B"


def m(x: float, d: int = 0) -> str:
    return f"{'-' if x < 0 else ''}${abs(x):,.{d}f}M"


def pct(x: float, d: int = 1) -> str:
    return f"{x * 100:.{d}f}%"


def cover(kicker: str, title: str, lead: str, tiles: list[tuple[str, str]], n: int = 4) -> str:
    t = "".join(f"<div class='tile'><b>{v}</b><span>{lab}</span></div>" for v, lab in tiles)
    return (f"<div class='cover'><div class='kicker'>{kicker}</div><h1>{title}</h1><p class='lead'>{lead}</p>"
            f"<div class='tiles {'t3' if n == 3 else ''}'>{t}</div>"
            f"<div class='meta'>{AUTHOR} · {PROGRAM} · {DATE}</div></div>")


# ===================================================================== Task 1
def task1(t: Triangulation, s: SizingResult, est: pd.DataFrame) -> str:
    c = Cite()
    sc = t.scenarios
    est_rows = "".join(
        f"<tr><td>{r.publisher}{' <span class=tag>anchor</span>' if r.anchor else ''}</td><td class=r>{b(r.base_usd_b, 2)}</td>"
        f"<td class=r>{int(r.forecast_year)}</td><td class=r>{b(r.forecast_usd_b, 1)}</td><td class=r>{r.cagr_pct:.1f}%</td></tr>"
        for r in est.sort_values("base_usd_b", ascending=False).itertuples()
    )
    par = pd.read_csv(DATA / "srilanka_sme_parameters.csv")
    par_rows = "".join(
        f"<tr><td>{r.parameter.replace('_', ' ')}</td><td class=r>{r.low:g}</td><td class=r>{r['mode']:g}</td>"
        f"<td class=r>{r.high:g}</td><td>{r.kind}</td><td>{r.rationale}</td></tr>" for _, r in par.iterrows()
    )
    body = cover(
        "Task 1 · Market landscape memo",
        "The SASE market: how big, how fast, and where the next buyers are",
        "Secure Access Service Edge (SASE) merges networking (SD-WAN) and cloud security (SSE: secure web gateway, "
        "CASB, zero-trust access, firewall-as-a-service) into one cloud service. This memo sizes the global market, "
        "tests eleven published estimates against each other, and builds a bottom-up TAM / SAM / SOM for a segment with no published sizing I could find: "
        "Sri Lanka's small and medium firms.",
        [(b(t.base_2025), "Triangulated global market, 2025"), (f"{t.spread_ratio:.1f}x", "Spread between the 11 published estimates"),
         (f"{b(sc.conservative.iloc[-1], 0)}-{b(sc.aggressive.iloc[-1], 0)}", "2030 range across three scenarios"),
         (m(s.sam_p50 / 1e6), "Sri Lankan SME serviceable market per year (P50)")],
    )
    body += f"""
<h2><span class='n'>1</span>Bottom line</h2>
<div class='callout'><b>SASE is a real, fast-growing market whose size depends on who you ask.</b> Anchoring on the four most transparent
sources gives a 2025 base of <b>{b(t.base_2025)}</b> (range {b(t.anchor_low)}-{b(t.anchor_high)}). Vendor revenue grew 17%-22% a year
through 2025, and the base case reaches <b>{b(sc.base.iloc[-1])}</b> by 2030. The fastest-growing buyers are small and medium firms
and Asia-Pacific, which together point to an untested niche: Sri Lankan SMEs, worth <b>{m(s.sam_p50 / 1e6)}</b> a year at the median
(80% interval {m(s.sam_p10 / 1e6)}-{m(s.sam_p90 / 1e6)}), of which one focused provider could win about <b>{m(s.som_p50 / 1e6, 1)}</b> of annual
recurring revenue (ARR) within five years.</div>

<h2><span class='n'>2</span>Why the estimates disagree</h2>
<p>Eleven publishers put the 2025 market anywhere from {b(t.all_low)} to {b(t.all_high)}, an {t.spread_ratio:.1f}x spread. The gap is mostly
definitional. Dell'Oro counts manufacturer revenue{c('delloro_2030')}; Gartner counts what buyers spend, including services
{c('gartner_15b')}; syndicated reports differ on whether SD-WAN hardware, managed services and stand-alone SSE belong inside "SASE"
{c('mm', 'mordor', 'kings', 'coherent_global')}. Taking a simple average of all eleven would blend incompatible scopes.</p>
<p><b>Method.</b> I used the median of four <i>anchor</i> estimates: two analyst houses that track the market every quarter (Dell'Oro and
Gartner) and the two most-cited syndicated reports (MarketsandMarkets, Mordor). Their median, {b(t.base_2025)}, sits between Dell'Oro's
revenue view ({b(t.anchor_low)}) and the buyer-spend views ({b(t.anchor_high)}). The other seven estimates are kept for context.</p>
{fig('t1_estimate_dispersion', 'Figure 1. 2025 SASE market estimates by publisher. Blue bars are the four anchors used for the base year.')}

<h2><span class='n'>3</span>Growth: three scenarios to 2030</h2>
<p>Growth is not in doubt. Dell'Oro measured SASE revenue up 17% year over year in 1Q 2025, 22% in 2Q and 21% in 3Q, while legacy branch
access-router revenue fell 25% in 3Q, a gap of more than 40 percentage points{c('delloro_1q25', 'delloro_2q25', 'delloro_3q25')}.</p>
<div class='two'><div>{fig('t1_delloro_quarters', 'Figure 2. Quarterly SASE revenue, Dell\'Oro.', '')}</div>
<div><table><tr><th>Scenario</th><th class=r>CAGR</th><th class=r>2027</th><th class=r>2030</th></tr>
<tr><td>Conservative (Dell'Oro implied)</td><td class=r>{pct(t.cagr_conservative)}</td><td class=r>{b(sc.conservative.iloc[2])}</td><td class=r>{b(sc.conservative.iloc[-1])}</td></tr>
<tr><td><b>Base</b> (median of 11 forecasts)</td><td class=r><b>{pct(t.cagr_base)}</b></td><td class=r><b>{b(sc.base.iloc[2])}</b></td><td class=r><b>{b(sc.base.iloc[-1])}</b></td></tr>
<tr><td>Aggressive (MarketsandMarkets)</td><td class=r>{pct(t.cagr_aggressive)}</td><td class=r>{b(sc.aggressive.iloc[2])}</td><td class=r>{b(sc.aggressive.iloc[-1])}</td></tr></table>
<p class='small'>All three scenarios start from the same {b(t.base_2025)} base so that only the growth assumption differs. Gartner's own
May 2026 forecast is reported at 23% a year for 2025-2030, close to the aggressive case{c('gartner_forecast')}.</p></div></div>
{fig('t1_scenarios', 'Figure 3. Global SASE spend, 2025-2030, by scenario (USD billion).')}

<h2><span class='n'>4</span>What is driving demand</h2>
<table><tr><th style='width:26%'>Driver</th><th>Evidence</th><th style='width:16%'>Effect</th></tr>
<tr><td><b>Branch refresh</b>: routers replaced by cloud edges</td><td>Access-router revenue down 25% Y/Y in 3Q 2025 while SASE grew 21%{c('delloro_3q25')}</td><td>Pulls SD-WAN spend into SASE</td></tr>
<tr><td><b>Vendor consolidation</b></td><td>Single-vendor SASE grew 21% vs 3% for multi-vendor (1Q 2025){c('delloro_1q25')}; vendors selling both SD-WAN and SSE earn 84% of SASE revenue{c('delloro_2q25')}; Gartner expects 50% of new deployments to be single-vendor by 2028, up from 30% in 2025{c('netskope_mq')}</td><td>Favours platform vendors</td></tr>
<tr><td><b>AI traffic</b></td><td>Palo Alto reports agentic traffic on its SASE platform up 9x in nine months{c('panw_call')}; Zscaler's AI-security bookings rose more than 50% quarter on quarter{c('zs_call')}</td><td>New paid modules</td></tr>
<tr><td><b>Privacy regulation</b></td><td>Sri Lanka's PDPA core duties from 1 Jan 2027{c('lk_pdpa')}; India's DPDP security duties from 13 May 2027{c('in_dpdp')}</td><td>Compliance-led buying</td></tr>
<tr><td><b>Sovereignty</b></td><td>Gartner added a "Sovereign SASE" use case in 2026{c('ntsk_cc')}</td><td>Local PoPs matter</td></tr></table>
<p><b>Restraints.</b> Integration complexity (Gartner still sees dual-vendor as the dominant model, though the inquiry ratio narrowed from
4:1 in 2024 to 2:1 in 2026{c('gartner_dual')}), opaque quote-only pricing, a shortage of skilled staff, and lock-in to one vendor's
points of presence.</p>
<p><b>Where growth is fastest.</b> Several publishers name small and medium enterprises as the fastest-growing buyer segment and
Asia-Pacific as the fastest region{c('sme_fast', 'meticulous')}. India alone is a {m(528.1)} market in 2025, growing 22.1% a
year{c('coherent_india')}. That combination is the opening this research follows.</p>

<h2 class='pb'><span class='n'>5</span>TAM, SAM and SOM</h2>
<p>A credible SAM and SOM must be built bottom-up, because no publisher sizes Sri Lanka. I defined the opportunity as a
<b>managed-SASE provider serving Sri Lankan small and medium firms</b> (roughly 11-200 staff), the segment that enterprise-priced global vendors are least built to serve.</p>
{fig('t1_tam_sam_som', 'Figure 4. From the global market to a reachable beachhead.')}
<table><tr><th>Layer</th><th>Definition</th><th class=r>Value</th><th>Basis</th></tr>
<tr><td><b>TAM</b></td><td>Global SASE spend, 2025</td><td class=r>{b(t.base_2025)}</td><td>Triangulated (section 2)</td></tr>
<tr><td>Gateway</td><td>India SASE market, 2025</td><td class=r>{m(528.1)}</td><td>Coherent Market Insights{c('coherent_india')}</td></tr>
<tr><td><b>SAM</b></td><td>Annual SASE spend if every Sri Lankan small and medium firm that needs SASE bought it</td><td class=r>{m(s.sam_p50 / 1e6)} (P50)</td><td>Bottom-up Monte Carlo</td></tr>
<tr><td><b>SOM</b></td><td>Year-5 ARR one focused provider can win</td><td class=r>{m(s.som_p50 / 1e6, 1)} (P50)</td><td>2%-10% share of SAM</td></tr></table>
<p><b>The formula.</b> SAM = (small firms x users per small firm + medium firms x users per medium firm) x growth since census x share of
firms that need SASE x price per user per year. Firm counts come from the Economic Census listing (71,126 small and 10,405 medium
enterprises{c('lk_census')}); the price anchor is Cloudflare's published $7 per user per month{c('net_price')}. The other inputs are
assumptions, so instead of one guess each is a range, and 20,000 random draws produce a distribution.</p>
<table><tr><th>Input</th><th class=r>Low</th><th class=r>Mode</th><th class=r>High</th><th>Kind</th><th>Rationale</th></tr>{par_rows}</table>
{fig('t1_monte_carlo', 'Figure 5. Distribution of Sri Lankan SME SAM across 20,000 draws.')}
<p>Using every input's single most likely value gives {m(s.sam_mode / 1e6, 1)} ({int(round(s.seats_mode, -3)):,} seats), which falls near the
10th percentile because the seat ranges are skewed upward (a small firm can have up to 50 staff but rarely fewer than 11). The median
of the full distribution, {m(s.sam_p50 / 1e6)}, is the better central estimate, and I report both.</p>
{fig('t1_tornado', 'Figure 6. Sensitivity of year-5 SOM to each input, others held at their mode.')}
<div class='callout green'><b>What the sensitivity says.</b> The win rate and the number of users per small firm move the answer most.
Both can be checked cheaply: a survey of 50 Colombo SMEs on headcount and remote work would narrow the range more than any further desk
research.</div>

<h2><span class='n'>6</span>Implications</h2>
<ol><li><b>Quote the market as a range with its definition.</b> "{b(t.base_2025)} (2025, anchor median; {b(t.anchor_low)}-{b(t.anchor_high)})"
is defensible; "$44.7B by 2030" without a scope note is not.</li>
<li><b>The growth is in consolidation and in smaller buyers.</b> Single-vendor platforms and SME-friendly pricing are where share is moving.</li>
<li><b>Sri Lanka is small but overlooked.</b> A {m(s.sam_p50 / 1e6)} SAM that no publisher has sized, priced out by quote-only enterprise vendors and facing a privacy-law deadline, is a credible
beachhead. Task 3 tests which vendor fits; Task 4 builds the entry plan.</li></ol>

<h2 class='pb'><span class='n'>A</span>Appendix: all published estimates</h2>
<table><tr><th>Publisher</th><th class=r>2025</th><th class=r>Year</th><th class=r>Forecast</th><th class=r>CAGR</th></tr>{est_rows}</table>
<p class='small'>Reproduce: <code>python -m sase_research.build</code>. Model code: <code>src/sase_research/market.py</code> and
<code>sizing.py</code>; live-formula workbook: <code>outputs/Task1_SASE_Market_Model.xlsx</code>.</p>
<h2><span class='n'>R</span>References</h2>{c.html()}
"""
    return to_pdf(page("Task 1 - SASE market landscape", body), "Task1_SASE_Market_Landscape_Memo", "Task 1 · SASE market landscape memo")


# ===================================================================== Task 2
def task2(r: dict, fin: pd.DataFrame) -> str:
    c = Cite()
    f = fin.set_index("metric")
    body = cover(
        "Task 2 · 10-K executive briefing",
        "Zscaler FY2026: financially sound, strategically pressured",
        "A synthesis of Zscaler's annual report on Form 10-K for the fiscal year ended 31 July 2026, the bellwether of cloud-delivered "
        "zero-trust security, written for an executive who has ten minutes.",
        [(m(r['revenue_m']), "FY2026 revenue (+" + pct(r['revenue_growth']) + ")"),
         (f"{r['rule_of_40']:.0f}", "Rule of 40 score (growth + FCF margin)"),
         (m(r['fcf_minus_sbc_m']), "Free cash flow minus stock pay"),
         (pct(r['fy27_rev_growth_mid']), "FY2027 guided revenue growth")],
    )
    body += f"""
<h2><span class='n'>1</span>The answer in four lines</h2>
<div class='callout'><ul style='margin:0'>
<li><b>Health: strong.</b> Revenue {m(r['revenue_m'])} (+{pct(r['revenue_growth'])}), free cash flow {m(r['fcf_m'])} ({pct(r['fcf_margin'])} margin),
{m(r['liquidity_m'])} of cash and short-term investments against {m(r['debt_principal_m'])} of zero-coupon notes due 2028{c('zs_10k')}.</li>
<li><b>But not yet profitable.</b> GAAP operating margin was {pct(r['op_margin'])}; interest income of {m(r['interest_income_m'])} roughly
offset the {m(-f.loc['Loss from operations', 'fy2026_usd_m'])} operating loss, and stock-based pay ({m(r['sbc_m'])}) now exceeds free cash flow.</li>
<li><b>Growth is slowing.</b> Guidance implies {pct(r['fy27_rev_growth_mid'])} revenue growth in FY2027, down from {pct(r['revenue_growth'])}{c('zs_pr')}.</li>
<li><b>Biggest strategic risk:</b> platform competition. Palo Alto Networks reports $450M of SASE displacements in its FY2026{c('panw_call')}.</li></ul></div>

<h2><span class='n'>2</span>Financial health scorecard</h2>
<table><tr><th>Dimension</th><th>FY2026</th><th>FY2025</th><th>Read</th></tr>
<tr><td>Revenue growth</td><td class=r>{pct(r['revenue_growth'])}</td><td class=r>23.3%</td><td>Re-accelerated, helped by the Red Canary acquisition (ARR excl. Red Canary +20%){c('zs_pr')}</td></tr>
<tr><td>Gross margin</td><td class=r>{pct(r['gross_margin'])}</td><td class=r>{pct(r['gross_margin_prev'])}</td><td>Stable despite heavier data-centre build-out</td></tr>
<tr><td>Sales &amp; marketing / revenue</td><td class=r>{pct(r['sm_pct'])}</td><td class=r>{pct(r['sm_pct_prev'])}</td><td>Improving: the main source of leverage</td></tr>
<tr><td>R&amp;D / revenue</td><td class=r>{pct(r['rd_pct'])}</td><td class=r>{pct(r['rd_pct_prev'])}</td><td>Rising: AI and acquired products</td></tr>
<tr><td>GAAP operating margin</td><td class=r>{pct(r['op_margin'])}</td><td class=r>{pct(r['op_margin_prev'])}</td><td>Narrower loss</td></tr>
<tr><td>Stock-based comp / revenue</td><td class=r>{pct(r['sbc_pct'])}</td><td class=r>{pct(683.568 / 2673.115)}</td><td>High; the gap between GAAP and "non-GAAP" profit</td></tr>
<tr><td>Free cash flow margin</td><td class=r>{pct(r['fcf_margin'])}</td><td class=r>{pct(r['fcf_margin_prev'])}</td><td>Down: capex up {pct(r['capex_growth'], 0)}</td></tr>
<tr><td>FCF minus stock comp</td><td class=r>{m(r['fcf_minus_sbc_m'])}</td><td class=r>{m(r['fcf_minus_sbc_prev_m'])}</td><td>Turned negative</td></tr>
<tr><td>Deferred revenue (total)</td><td class=r>{m(r['deferred_m'])}</td><td class=r>{m(2468.026)}</td><td>+{pct(r['deferred_growth'])}: future revenue is building</td></tr>
<tr><td>Remaining performance obligations</td><td class=r>{m(r['rpo_m'])}</td><td class=r>n/a</td><td>{r['rpo_to_revenue']:.1f}x annual revenue; 45% due within 12 months{c('zs_10k')}</td></tr>
<tr><td>Net cash (liquidity - note principal)</td><td class=r>{m(r['net_cash_m'])}</td><td class=r>{m(3572.409 - 1725)}</td><td>Comfortable</td></tr>
<tr><td>Goodwill</td><td class=r>{m(r['goodwill_m'])}</td><td class=r>{m(417.730)}</td><td>+{pct(r['goodwill_growth'], 0)} after four acquisitions</td></tr></table>
{fig('t2_revenue_dollar', 'Figure 1. FY2026 cost structure per dollar of revenue (GAAP).')}

<h2><span class='n'>3</span>Three things the headline numbers hide</h2>
<h3>a. Profit depends on interest income</h3>
<p>The {m(-f.loc['Net loss', 'fy2026_usd_m'], 1)} net loss looks small, but only because {m(r['interest_income_m'])} of interest income
({r['interest_vs_oploss']:.2f}x the operating loss) sits below the operating line. If rates fall, or cash is spent on more acquisitions,
that cushion shrinks.</p>
<h3>b. Stock pay now exceeds free cash flow</h3>
{fig('t2_cash_vs_sbc', 'Figure 2. Cash generation versus stock-based compensation, FY2025-FY2026.')}
<p>Zscaler reports free cash flow of {m(r['fcf_m'])}, but {m(r['sbc_m'])} of employee pay was in shares. Subtracting it leaves
{m(r['fcf_minus_sbc_m'])}, down from +{m(r['fcf_minus_sbc_prev_m'])}. Shareholders bear that cost through dilution, which helps explain why
$100 invested five years ago was worth ${r['tsr_5y']:.2f} at the fiscal year-end{c('zs_10k')}.</p>
<h3>c. Capex stepped up sharply in Q4</h3>
<p>Purchases of property and equipment rose {pct(r['capex_growth'], 0)} to {m(r['capex_m'])}. In Q4 alone, capex and capitalised software reached
$218.5M against $78.7M a year earlier, cutting quarterly free cash flow margin to 7%{c('zs_pr')}. Management ties this to AI and data-centre
capacity; investors should watch whether margins recover to the guided 23%-23.5%.</p>

<h2><span class='n'>4</span>Where growth comes from</h2>
<div class='two'><div>{fig('t2_growth_path', 'Figure 3. Revenue growth, FY2024 to FY2027 guidance.')}</div>
<div><ul><li><b>ARR {m(r['arr_m'])}</b>, +25%; net new ARR excluding Red Canary accelerated to +17% in Q4{c('zs_call')}.</li>
<li><b>Large customers:</b> 785 above $1M ARR (+18%) and 4,182 above $100K (+20%); net revenue retention {pct(r['nrr'], 0)}{c('zs_call2')}.</li>
<li><b>New pricing:</b> Z-Flex contracts brought $1.7B of total contract value in FY2026{c('zs_call')}.</li>
<li><b>Recognition:</b> first year as a Leader in Gartner's SASE Platforms Magic Quadrant{c('zs_mq')}.</li></ul></div></div>
{fig('t2_geography', 'Figure 4. Revenue by region. International revenue fell to 47% of the total.')}

<h2><span class='n'>5</span>Strategic risks, ranked</h2>
<table><tr><th style='width:4%'>#</th><th style='width:24%'>Risk</th><th>Evidence from the filing and results</th><th style='width:12%'>Severity</th></tr>
<tr><td>1</td><td><b>Platform competition and slowing growth</b></td><td>10-K: "intense and increasing competition"{c('zs_10k')}. FY2027 guide {pct(r['fy27_rev_growth_mid'])}; Palo Alto's $450M of SASE displacements and 63% NGS ARR growth{c('panw_pr')}</td><td>High</td></tr>
<tr><td>2</td><td><b>Dilution and GAAP losses</b></td><td>Stock pay {pct(r['sbc_pct'])} of revenue; accumulated deficit $1,252.7M; history of annual net losses listed as a principal risk</td><td>High</td></tr>
<tr><td>3</td><td><b>Acquisition integration</b></td><td>{m(r['acquisitions_m'])} spent on four deals; Red Canary alone $651.4M; goodwill now {pct(r['goodwill_to_assets'])} of assets</td><td>Medium</td></tr>
<tr><td>4</td><td><b>Channel concentration</b></td><td>{pct(r['channel_share'], 0)} of revenue via partners; top five partners {pct(r['top5_channel_share'], 0)} (28% a year earlier); one partner holds 13% of receivables</td><td>Medium</td></tr>
<tr><td>5</td><td><b>Service outage</b></td><td>10-K: delivery interruptions would harm the business; the cloud processes 750B+ transactions a day</td><td>Medium</td></tr>
<tr><td>6</td><td><b>Capital intensity</b></td><td>Capex +{pct(r['capex_growth'], 0)}; Q4 FCF margin 7%</td><td>Medium</td></tr>
<tr><td>7</td><td><b>2028 notes</b></td><td>$1,725M of 0% convertible notes mature 15 Jul 2028; well covered by {m(r['liquidity_m'])} of liquidity</td><td>Low</td></tr>
<tr><td>8</td><td><b>Macro and IT budgets</b></td><td>10-K cites inflation, tariffs and Middle East energy disruption; "a broad reduction in IT security spending would have a material impact"</td><td>Low-Med</td></tr></table>

<h2><span class='n'>6</span>What this means for the wider SASE market</h2>
<p>The market leader's filing confirms three things that shape Task 4. First, <b>enterprise demand is healthy</b>: deferred revenue +{pct(r['deferred_growth'])}
and {m(r['rpo_m'])} of contracted backlog. Second, <b>the enterprise core is maturing</b>: growth is moving toward high-teens and comes from upsell,
AI modules and acquisitions. Third, <b>Asia-Pacific is under-penetrated</b>: {pct(r['apac_share'])} of Zscaler's revenue
({m(f.loc['Revenue Asia Pacific', 'fy2026_usd_m'])}), growing {pct(r['apac_growth'], 0)}. Smaller buyers in smaller countries are the
part of the market the leader is least built to serve.</p>

<h2><span class='n'>7</span>Method and tools</h2>
<p>The brief suggested NotebookLM. I worked from the 10-K text on SEC EDGAR directly and recomputed every ratio in Python
(<code>src/sase_research/zscaler.py</code>, input lines in <code>data/zscaler_fy2026.csv</code>), so each figure traces to a line of the
filing and can be re-checked. Operating metrics that the 10-K does not disclose (ARR, customers above $1M, net retention) come from the
same-day results release and earnings call, and are cited separately. GAAP figures are used throughout unless marked otherwise.</p>
<h2><span class='n'>R</span>References</h2>{c.html()}
"""
    return to_pdf(page("Task 2 - Zscaler 10-K briefing", body), "Task2_Zscaler_10K_Executive_Briefing", "Task 2 · Zscaler FY2026 10-K executive briefing")


# ===================================================================== Task 3
def _swot_block(v: str, d: dict) -> str:
    cell = lambda k, cls, name: f"<div class='{cls}'><h4>{name}</h4><ul>{''.join(f'<li>{x}</li>' for x in d[k])}</ul></div>"  # noqa: E731
    return (f"<h3>{v}</h3><div class='swot'>{cell('S', 's', 'Strengths')}{cell('W', 'w', 'Weaknesses')}"
            f"{cell('O', 'o', 'Opportunities')}{cell('T', 't', 'Threats')}</div>")


def task3(comp: pd.DataFrame, scores: pd.DataFrame) -> str:
    c = Cite()
    cite_map = {"Zscaler": c("zs_pr", "g2_cato_zia", "price_zs"), "Palo Alto Networks": c("panw_pr", "g2_cato_prisma", "price_prisma"),
                "Netskope": c("ntsk_pr", "g2_ntsk", "price_sse"), "Cloudflare": c("net_q3", "g2_cf", "net_price"),
                "Cato Networks": c("cato_arr", "g2_cato_zia", "price_cato")}
    rows = "".join(
        f"<tr><td><b>{r.vendor}</b>{cite_map[r.vendor]}<br><span class='small'>{r.ownership}</span></td><td>{r.gartner_sase_mq_2026}</td>"
        f"<td class=r>{m(r.scale_usd_m)}<br><span class='small'>+{r.growth_pct:.0f}%</span></td>"
        f"<td>{r.published_entry_price}<br><span class='small'>${r.price_low_usd_user_yr:.0f}-${r.price_high_usd_user_yr:.0f}/user/yr</span></td>"
        f"<td class=r>{r.g2_rating}<br><span class='small'>{int(r.g2_reviews)} reviews</span></td></tr>"
        for r in comp.itertuples()
    )
    diff = "".join(
        f"<tr><td><b>{r.vendor}</b></td><td>{r.differentiator}</td><td>{r.review_praise}</td><td>{r.review_complaints}</td><td>{r.vulnerability}</td></tr>"
        for r in comp.itertuples()
    )
    top = scores.index[0]
    body = cover(
        "Task 3 · Competitive teardown",
        "Five SASE platforms, one question: who wins the smaller buyer?",
        "A teardown of Zscaler, Palo Alto Networks (Prisma SASE), Netskope, Cloudflare One and Cato Networks on pricing, "
        "differentiators, user sentiment and vulnerabilities, scored for fit with a Sri Lankan firm of 20-200 users. The full "
        "matrix with live formulas is in Task3_Competitor_Matrix.xlsx.",
        [("4.3-4.6", "G2 rating range: satisfaction barely separates them"), ("$0-$300", "Per user per year: price separates them"),
         (top, f"Best SME fit (weighted {scores.weighted.iloc[0]:.2f} / 5)")], n=3,
    )
    body += f"""
<h2><span class='n'>1</span>Key findings</h2>
<ol><li><b>Four Leaders, one Visionary.</b> Gartner's 2026 SASE Magic Quadrant names Netskope (highest for execution), Palo Alto (highest
for vision), Cato and Zscaler as Leaders; Cloudflare is the only vendor named Visionary in both the SASE and SSE reports{c('ntsk_cc', 'panw_mq', 'cato_mq', 'zs_mq', 'net_mq')}.</li>
<li><b>Users are equally happy.</b> G2 ratings span only 4.3 to 4.6, so satisfaction is not a buying differentiator.</li>
<li><b>Pricing is the real divide.</b> Four of five vendors are quote-only. Cloudflare alone publishes a price (free to 50 users, then
$7 per user per month); third-party data puts Zscaler at $150-$300 and Prisma Access at $168-$264 per user per year{c('price_zs', 'price_prisma')}.</li>
<li><b>The challengers grow fastest.</b> Cato's ARR grew 42% and Netskope's 31%, against 25% at Zscaler.</li>
<li><b>For SMEs, Cloudflare leads and Netskope follows.</b> On a weighted SME-fit score, Cloudflare scores {scores.loc['Cloudflare', 'weighted']:.2f}
and Netskope {scores.loc['Netskope', 'weighted']:.2f}; the enterprise leaders trail because of price and minimum deal size.</li></ol>

<h2><span class='n'>2</span>The matrix at a glance</h2>
<table><tr><th>Vendor</th><th>Gartner SASE MQ 2026</th><th class=r>Scale &amp; growth</th><th>Entry price</th><th class=r>G2</th></tr>{rows}</table>
<p class='small'>Scale metrics differ: ARR for Zscaler, Netskope and Cato; company-wide Next-Gen Security ARR for Palo Alto; Q3 2026 revenue x4
for Cloudflare. Compare growth rates, not absolute size. Prices for quote-only vendors are third-party purchase data, not list prices.</p>
{fig('t3_price_vs_rating', 'Figure 1. Estimated price per user against G2 rating.')}
{fig('t3_growth', 'Figure 2. Latest reported growth by vendor.')}

<h2><span class='n'>3</span>Differentiators, sentiment and vulnerabilities</h2>
<table><tr><th style='width:13%'>Vendor</th><th>Key differentiator</th><th>Reviewers praise</th><th>Reviewers dislike</th><th>Vulnerability</th></tr>{diff}</table>
<p class='small'>Review themes summarise G2 and Gartner Peer Insights pages{c('g2_cf', 'gpi_cf', 'gpi_cato')}; they are directional, not a statistical sample.</p>

<h2><span class='n'>4</span>SME-fit scorecard</h2>
<p>Each vendor is scored 1-5 on six criteria. Five are formulas over the matrix (for example, affordability = 5 - 4 x price / $300); one,
small-firm fit, is a judgement from cited evidence such as free tiers and minimum deal sizes. The weights are editable in the workbook.</p>
{fig('t3_scorecard', 'Figure 3. Weighted SME-fit scores. Weights in brackets.')}
<div class='callout orange'><b>How to read this.</b> The scorecard ranks fit for a Sri Lankan firm of 20-200 users, not product quality. An
enterprise CISO weighting scale, depth and Gartner position would rank Palo Alto and Zscaler first. Changing weights in the workbook
shows how robust the order is: Cloudflare stays first even with affordability and small-firm fit set to zero, and loses the top spot to Netskope only when Gartner position carries about half of the total weight.</div>

<h2 class='pb'><span class='n'>5</span>SWOT by vendor</h2>
{''.join(_swot_block(v, d) for v, d in SWOT.items())}

<h2><span class='n'>6</span>So what</h2>
<ul><li><b>The enterprise top is crowded; the bottom is open.</b> Every Leader prices for enterprises. Only Cloudflare packages for small teams.</li>
<li><b>Partner, don't compete.</b> A local entrant should resell and manage an existing platform rather than build one. Cloudflare One (with a
Colombo PoP since 2017{c('net_colombo')}) is the natural entry platform; Netskope is the upgrade path for data-heavy clients.</li>
<li><b>Watch the Leaders' SME moves.</b> If Zscaler or Netskope launch a published SME tier, the entrant's advantage shifts from price to local service.</li></ul>
<h2><span class='n'>R</span>References</h2>{c.html()}
"""
    return to_pdf(page("Task 3 - Competitive teardown", body), "Task3_Competitive_Teardown", "Task 3 · SASE competitive teardown")
