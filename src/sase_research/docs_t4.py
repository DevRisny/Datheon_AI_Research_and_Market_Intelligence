"""Task 4: capstone report (A4, ~18 pages) and executive deck (16:9)."""

from __future__ import annotations

import pandas as pd

from . import DATA
from .docs_t1_t3 import b, m, pct
from .market import Triangulation
from .refs import Cite
from .render import AUTHOR, DATE, PROGRAM, fig, img, page, to_pdf
from .sizing import SizingResult
from .swot import ENTRANT

TITLE = "Edge Shift"
SUBTITLE = "The SASE market and the Sri Lankan SME opportunity"


def _plan_numbers(s: SizingResult) -> dict:
    price_client = 120.0   # $7 platform + $3 managed service per user per month
    platform = 84.0
    som_seats = s.som_p50 / platform
    return {
        "price_client": price_client,
        "platform": platform,
        "gm": (price_client - platform) / price_client,
        "y1_seats": 3000, "y3_seats": 20000, "y5_seats": round(som_seats, -3),
        "y1_arr": 3000 * price_client, "y3_arr": 20000 * price_client, "y5_arr": round(som_seats, -3) * price_client,
        "share_y5": round(som_seats, -3) / s.seats_mode,
    }


def capstone(t: Triangulation, s: SizingResult, r: dict, comp: pd.DataFrame, sc: pd.DataFrame, est: pd.DataFrame):
    c = Cite()
    sn = t.scenarios
    p = _plan_numbers(s)
    reg = pd.read_csv(DATA / "regulation.csv")
    swot_cell = lambda k, cls, name: f"<div class='{cls}'><h4>{name}</h4><ul>{''.join(f'<li>{x}</li>' for x in ENTRANT[k])}</ul></div>"  # noqa: E731
    score_rows = "".join(
        f"<tr><td><b>{v}</b></td>" + "".join(f"<td class=r>{row[k]:.1f}</td>" for k in sc.columns[:-1]) +
        f"<td class=r><b>{row['weighted']:.2f}</b></td></tr>" for v, row in sc.iterrows()
    )
    comp_rows = "".join(
        f"<tr><td><b>{x.vendor}</b></td><td>{x.gartner_sase_mq_2026.split(' (')[0]}</td><td class=r>+{x.growth_pct:.0f}%</td>"
        f"<td>{x.published_entry_price}</td><td class=r>${x.price_low_usd_user_yr:.0f}-{x.price_high_usd_user_yr:.0f}</td>"
        f"<td class=r>{x.g2_rating}</td><td>{x.south_asia_presence}</td></tr>" for x in comp.itertuples()
    )
    reg_rows = "".join(
        f"<tr><td>{x.jurisdiction}</td><td>{x.milestone}</td><td class=r>{pd.Timestamp(x.date):%d %b %Y}</td>"
        f"<td>{x.obligation_relevant_to_sase}</td></tr>" for x in reg.itertuples()
    )

    body = f"""
<div class='cover full'>
  <div><div class='kicker'>Capstone report · Datheon AI Research &amp; Market Intelligence</div>
  <h1>{TITLE}</h1>
  <p class='lead' style='font-size:15pt;font-family:Lora,serif;color:#0f2a44'>{SUBTITLE}</p>
  <p class='lead' style='max-width:150mm'>Cloud-delivered security is replacing the office VPN and firewall. This report sizes that shift,
  studies its leader's annual report, tears down five competing platforms, and recommends how a local provider can serve the buyers
  the global leaders overlook: Sri Lanka's small and medium firms, ahead of the country's data-protection law taking effect on
  1 January 2027.</p></div>
  <div class='tiles'>
    <div class='tile'><b>{b(t.base_2025)}</b><span>Global SASE market, 2025 (triangulated)</span></div>
    <div class='tile'><b>{b(sn.base.iloc[-1])}</b><span>Base-case market by 2030 ({pct(t.cagr_base)} CAGR)</span></div>
    <div class='tile'><b>{m(s.sam_p50 / 1e6)}</b><span>Sri Lankan SME serviceable market per year (P50)</span></div>
    <div class='tile'><b>{m(s.som_p50 / 1e6, 1)}</b><span>Year-5 ARR one focused provider can win (P50)</span></div>
  </div>
  <div><p class='meta' style='font-size:10pt'><b>{AUTHOR}</b><br>{PROGRAM}<br>{DATE}</p>
  <p class='small'>All figures are reproducible: data in <code>data/</code>, models in <code>src/sase_research/</code>,
  rebuilt with <code>python -m sase_research.build</code>.</p></div>
</div>

<h2 style='border-top:none;margin-top:0'>Contents</h2>
<div class='toc'>
<div>1 Executive summary</div><div>2 What SASE is and why it matters now</div><div>3 Market size and growth</div>
<div>4 Demand drivers and restraints</div><div>5 Competitive landscape</div><div>6 Case study: Zscaler's financial health</div>
<div>7 Regulation: the compliance clock</div><div>8 The Sri Lankan SME opportunity</div><div>9 Strategic recommendations</div>
<div>10 Implementation roadmap and KPIs</div><div>11 Risks and mitigations</div><div>12 Methodology and limitations</div>
<div>Appendix A: Data tables</div><div>References</div></div>

<h2><span class='n'>1</span>Executive summary</h2>
<p class='lead'>SASE is one of the fastest-growing parts of enterprise security, but its growth is concentrated in large enterprises
served by five global platforms. Small and medium firms in South Asia are the least-served buyers, and two privacy laws are about to
make security a legal duty for them.</p>
<h3>Five findings</h3>
<ol>
<li><b>The market is about {b(t.base_2025)} and growing about a fifth a year.</b> Eleven published 2025 estimates range from {b(t.all_low)}
to {b(t.all_high)}; the four most transparent sources give a median of {b(t.base_2025)}. Vendor revenue grew 17%-22% year over year
through 2025{c('delloro_1q25', 'delloro_2q25', 'delloro_3q25')}. Base case: {b(sn.base.iloc[-1])} by 2030.</li>
<li><b>Consolidation is the dominant buying pattern.</b> Single-vendor SASE grew 21% against 3% for multi-vendor in 1Q 2025{c('delloro_1q25')},
and Gartner expects half of new deployments to be single-vendor by 2028{c('netskope_mq')}.</li>
<li><b>The leader is healthy but slowing.</b> Zscaler grew revenue {pct(r['revenue_growth'])} to {m(r['revenue_m'])} with a {pct(r['fcf_margin'])}
free-cash-flow margin, but guides to {pct(r['fy27_rev_growth_mid'])} growth, still posts GAAP operating losses, and pays more in stock
than it generates in free cash flow{c('zs_10k', 'zs_pr')}.</li>
<li><b>Price, not satisfaction, separates vendors.</b> G2 ratings span 4.3-4.6; prices span $0-$300 per user per year. Only Cloudflare
publishes a price, and it scores highest ({sc.loc['Cloudflare', 'weighted']:.2f}/5) on fit for small firms.</li>
<li><b>Sri Lanka's SME segment is small, unserved and about to become urgent.</b> A bottom-up model puts serviceable spend at
{m(s.sam_p50 / 1e6)} a year (80% interval {m(s.sam_p10 / 1e6)}-{m(s.sam_p90 / 1e6)}). Core duties of the Personal Data Protection Act
apply from 1 January 2027{c('lk_pdpa')}.</li></ol>
<h3>Three recommendations</h3>
<div class='callout green'><ol style='margin:0'>
<li><b>Launch a compliance-ready managed SASE service</b> for Sri Lankan firms of 11-200 staff on a free-to-start platform, priced at about
${p['price_client'] / 12:.0f} per user per month.</li>
<li><b>Sell through partners SMEs already trust</b>: internet providers, accounting and audit firms, and chambers of commerce, with PDPA
readiness as the opening offer.</li>
<li><b>Earn the right to expand to India</b> before its DPDP security duties take effect on 13 May 2027{c('in_dpdp')}, gated on clear year-one
milestones.</li></ol></div>
<p>Executed well, the plan targets about {p['y5_seats']:,.0f} seats and {m(p['y5_arr'] / 1e6, 1)} of client ARR by year five, roughly
{pct(p['share_y5'], 0)} of the seats that need SASE at modal inputs.</p>

<h2 class='pb'><span class='n'>2</span>What SASE is and why it matters now</h2>
<p>For two decades, companies protected staff by routing traffic back to an office network guarded by a firewall and a VPN. Cloud
applications and remote work broke that model: traffic now goes straight to the internet, and the office perimeter protects little.
<b>Secure Access Service Edge (SASE)</b> moves the security checks into a cloud service that sits between every user, device or branch and
every application. It combines two halves:</p>
<table><tr><th style='width:26%'>Component</th><th>What it does</th><th style='width:30%'>What it replaces</th></tr>
<tr><td><b>SD-WAN</b> (networking)</td><td>Routes branch traffic over any internet link to the nearest cloud point of presence</td><td>MPLS circuits, branch routers</td></tr>
<tr><td><b>Secure web gateway (SWG)</b></td><td>Filters web traffic and blocks malware</td><td>On-premises proxies</td></tr>
<tr><td><b>Zero-trust network access (ZTNA)</b></td><td>Grants each user access to one application at a time after checking identity and device</td><td>VPNs</td></tr>
<tr><td><b>Cloud access security broker (CASB)</b> and DLP</td><td>Controls use of SaaS apps and stops sensitive data leaving</td><td>Separate data-loss tools</td></tr>
<tr><td><b>Firewall as a service (FWaaS)</b></td><td>Inspects non-web traffic in the cloud</td><td>Branch firewalls</td></tr></table>
<p>The security half alone is called <b>Security Service Edge (SSE)</b>. Vendors that supply both halves are "single-vendor SASE".
Three forces make 2026-2027 a turning point: branch routers are being retired at speed (access-router revenue fell 25% year over year in
3Q 2025{c('delloro_3q25')}), AI agents are creating new traffic that must be inspected, and privacy laws in South Asia are switching on.</p>

<h2><span class='n'>3</span>Market size and growth</h2>
<p>There is no agreed size. The eleven estimates I collected differ by {t.spread_ratio:.1f}x, mainly because publishers define the market
differently: manufacturer revenue (Dell'Oro{c('delloro_2030')}), buyer spending (Gartner{c('gartner_15b')}), or broader bundles that include
services and hardware{c('kings', 'mm')}. I therefore triangulated from four anchor sources rather than averaging all eleven.</p>
{fig('t1_estimate_dispersion', 'Figure 1. 2025 estimates by publisher. Anchors in blue; median of anchors = triangulated base.')}
<div class='two'><div>
<table><tr><th>Scenario</th><th class=r>CAGR</th><th class=r>2030</th></tr>
<tr><td>Conservative (Dell'Oro)</td><td class=r>{pct(t.cagr_conservative)}</td><td class=r>{b(sn.conservative.iloc[-1])}</td></tr>
<tr><td><b>Base</b> (median of 11)</td><td class=r><b>{pct(t.cagr_base)}</b></td><td class=r><b>{b(sn.base.iloc[-1])}</b></td></tr>
<tr><td>Aggressive (MarketsandMarkets)</td><td class=r>{pct(t.cagr_aggressive)}</td><td class=r>{b(sn.aggressive.iloc[-1])}</td></tr></table>
<p class='small'>Gartner's May 2026 forecast is reported at 23% a year for 2025-2030{c('gartner_forecast')}, between the base and aggressive cases.</p>
</div><div>{fig('t1_delloro_quarters', 'Figure 2. Quarterly SASE vendor revenue, 2025.')}</div></div>
{fig('t1_scenarios', 'Figure 3. Global SASE spend by scenario, 2025-2030.')}

<h2 class='pb'><span class='n'>4</span>Demand drivers and restraints</h2>
<div class='two'><div><h3>Drivers</h3><ul>
<li><b>Branch modernisation.</b> SASE grew 21% while router spending fell 25% (3Q 2025){c('delloro_3q25')}.</li>
<li><b>Platform consolidation.</b> Vendors with both SD-WAN and SSE earn 84% of SASE revenue{c('delloro_2q25')}.</li>
<li><b>AI traffic.</b> Agentic traffic on Palo Alto's SASE platform rose 9x in nine months{c('panw_call')}; Prisma AIRS reached $100M ARR within
four quarters{c('panw_pr')}.</li>
<li><b>Data sovereignty.</b> Gartner added a Sovereign SASE use case in 2026{c('ntsk_cc')}.</li>
<li><b>Privacy law.</b> Sri Lanka's PDPA and India's DPDP Rules impose security and breach-notification duties (section 7).</li></ul></div>
<div><h3>Restraints</h3><ul>
<li><b>Two-vendor inertia.</b> Dual-vendor is still the dominant model, though the inquiry ratio narrowed from 4:1 to 2:1{c('gartner_dual')}.</li>
<li><b>Opaque pricing.</b> Four of the five leading platforms are quote-only.</li>
<li><b>Skills.</b> Small firms rarely employ a security specialist to configure policies.</li>
<li><b>Budget pressure.</b> Zscaler's own 10-K warns that a broad cut in IT security spending would hurt it materially{c('zs_10k')}.</li>
<li><b>Lock-in.</b> Users depend on one vendor's points of presence and policy model.</li></ul></div></div>
<div class='callout'><b>Where growth concentrates.</b> Publishers consistently name small and medium enterprises as the fastest-growing buyer
segment and Asia-Pacific as the fastest region{c('sme_fast', 'meticulous')}. India alone is a $528M SASE market growing 22.1% a year{c('coherent_india')}.</div>

<h2><span class='n'>5</span>Competitive landscape</h2>
<p>Five platforms define the market. Four are Leaders in Gartner's 2026 Magic Quadrant for SASE Platforms; Cloudflare is the only vendor
named a Visionary in both the SASE and SSE reports{c('gartner_mq', 'net_mq')}.</p>
<table><tr><th>Vendor</th><th>Gartner 2026</th><th class=r>Growth</th><th>Published price</th><th class=r>$/user/yr</th><th class=r>G2</th><th>South Asia presence</th></tr>{comp_rows}</table>
{fig('t3_price_vs_rating', 'Figure 4. Estimated price against G2 rating. Satisfaction is bunched; price is not.')}
<h3>Fit for small and medium buyers</h3>
<p>I scored each vendor on six criteria weighted for a Sri Lankan firm of 20-200 users. Five scores are formulas over published data; small-firm
fit is a judgement from cited evidence (free tiers, minimum deal sizes, per-site charges).</p>
<table><tr><th>Vendor</th>{''.join(f'<th class=r>{k}</th>' for k in sc.columns[:-1])}<th class=r>Weighted</th></tr>{score_rows}</table>
<p>Cloudflare leads on every weighting I tested except one that puts about half of the weight on Gartner position, where Netskope moves
ahead. That makes Cloudflare One the natural <b>entry platform</b> and Netskope the <b>upgrade path</b> for data-heavy clients.</p>

<h2 class='pb'><span class='n'>6</span>Case study: Zscaler's financial health</h2>
<p>Zscaler's FY2026 Form 10-K is the best public window into the economics of cloud-delivered security{c('zs_10k')}.</p>
<div class='tiles'>
<div class='tile'><b>{m(r['revenue_m'])}</b><span>Revenue, +{pct(r['revenue_growth'])}</span></div>
<div class='tile'><b>{pct(r['gross_margin'])}</b><span>Gross margin</span></div>
<div class='tile'><b>{pct(r['fcf_margin'])}</b><span>Free cash flow margin (FY2025: {pct(r['fcf_margin_prev'])})</span></div>
<div class='tile'><b>{m(r['net_cash_m'])}</b><span>Net cash after the 2028 notes</span></div></div>
{fig('t2_revenue_dollar', 'Figure 5. FY2026 cost per revenue dollar. Sales and marketing is the largest cost.')}
<div class='two'><div>{fig('t2_cash_vs_sbc', 'Figure 6. Free cash flow versus stock-based pay.')}</div>
<div><h3>What it teaches an entrant</h3><ul>
<li><b>Selling security is expensive.</b> Sales and marketing took {pct(r['sm_pct'])} of revenue, the largest single cost and well
above R&amp;D ({pct(r['rd_pct'])}). A local provider must keep acquisition cheap, which argues for partners.</li>
<li><b>Partners carry the market.</b> {pct(r['channel_share'], 0)} of Zscaler's revenue came through channel partners.</li>
<li><b>Recurring revenue compounds.</b> Net revenue retention of {pct(r['nrr'], 0)}{c('zs_call2')} means existing customers grow every year.</li>
<li><b>Growth is maturing.</b> FY2027 guidance of {pct(r['fy27_rev_growth_mid'])} shows the enterprise core slowing; new segments matter more.</li>
<li><b>Asia-Pacific is under-weighted:</b> {pct(r['apac_share'])} of revenue, growing {pct(r['apac_growth'], 0)}.</li></ul></div></div>

<h2><span class='n'>7</span>Regulation: the compliance clock</h2>
<p>Two privacy regimes change the buying conversation for South Asian firms from "nice to have" to "legal duty".</p>
{fig('t4_regulation_timeline', 'Figure 7. Privacy-law milestones in Sri Lanka and India.')}
<table><tr><th>Jurisdiction</th><th>Milestone</th><th class=r>Date</th><th>Relevance to SASE</th></tr>{reg_rows}</table>
<ul><li><b>Sri Lanka.</b> Extraordinary Gazette 2498/16 made 1 January 2027 the effective date for the Act's processing rules and its
controller and processor duties{c('lk_pdpa')}. The government plans to begin enforcement within a year of that date{c('lk_enf')}, and
administrative penalties can reach LKR 10 million per breach{c('lk_penalty')}.</li>
<li><b>India.</b> The DPDP Rules 2025 bring security-safeguard and 72-hour breach-reporting duties into force on 13 May 2027, with
penalties up to INR 250 crore for failing to protect data{c('in_dpdp', 'in_dpdp2')}.</li></ul>
<p>SASE does not make a firm compliant on its own, but it delivers the controls these laws expect: who accessed what, from which device,
with logs and data-loss rules. That is a concrete reason for an owner-managed firm to buy now.</p>

<h2 class='pb'><span class='n'>8</span>The Sri Lankan SME opportunity</h2>
{fig('t4_srilanka_signals', 'Figure 8. Why Sri Lanka, why now.')}
<p>Sri Lanka has about 1.1 million micro, small and medium enterprises, which generate about 52% of GDP and 45% of
employment{c('lk_msme', 'lk_sme')}. Internet use reached 13.9 million people (59.7%) by late 2025{c('lk_digital', 'lk_pen')}, and Sri Lanka CERT
received more than 12,650 cyber complaints in 2025, after 21,743 in 2024{c('lk_cert', 'lk_cert24')}. Micro firms (mostly sole
proprietors) are excluded from the target; the focus is the roughly 81,500 small and medium enterprises counted in the last economic
census listing{c('lk_census')}.</p>
<h3>Bottom-up sizing</h3>
{fig('t1_tam_sam_som', 'Figure 9. TAM, SAM and SOM.')}
<div class='two'><div>{fig('t1_monte_carlo', 'Figure 10. SAM distribution, 20,000 draws.')}</div>
<div><table><tr><th>Output</th><th class=r>P10</th><th class=r>P50</th><th class=r>P90</th></tr>
<tr><td>SAM ($M / yr)</td><td class=r>{s.sam_p10 / 1e6:.0f}</td><td class=r><b>{s.sam_p50 / 1e6:.0f}</b></td><td class=r>{s.sam_p90 / 1e6:.0f}</td></tr>
<tr><td>Year-5 SOM ($M ARR)</td><td class=r>{s.som_p10 / 1e6:.1f}</td><td class=r><b>{s.som_p50 / 1e6:.1f}</b></td><td class=r>{s.som_p90 / 1e6:.1f}</td></tr></table>
<p class='small'>SAM = firms x growth since census x share needing SASE x users per firm x price per user. Price mode = Cloudflare's published
$7 per user per month{c('net_price')}. Full input table in the Task 1 memo and workbook.</p>
<p class='small'>At every input's modal value the result is {m(s.sam_mode / 1e6, 1)}: low, because the seat ranges skew upward. I treat the P50 as
the central estimate.</p></div></div>
{fig('t1_tornado', 'Figure 11. What moves the year-5 SOM most.')}
<h3>SWOT for the proposed entrant</h3>
<div class='swot'>{swot_cell('S', 's', 'Strengths')}{swot_cell('W', 'w', 'Weaknesses')}{swot_cell('O', 'o', 'Opportunities')}{swot_cell('T', 't', 'Threats')}</div>

<h2 class='pb'><span class='n'>9</span>Strategic recommendations</h2>
<div class='rec'><span class='num'>1</span><h3>Launch a compliance-ready managed SASE service before PDPA enforcement begins</h3>
<p><span class='tag'>Why</span>The scorecard's top platform is free to 50 users and has a Colombo point of presence{c('net_colombo')}, but
reviewers report a steep learning curve when combining its products{c('g2_cf')}. Small firms need someone to set it up and run it.</p>
<p><span class='tag'>What</span>Three packages, priced in US dollars per user per month and billed in rupees:</p>
<table><tr><th>Package</th><th>For</th><th>Platform</th><th class=r>Client price</th><th>Includes</th></tr>
<tr><td><b>Starter</b></td><td>11-50 staff</td><td>Cloudflare One free tier</td><td class=r>Flat monthly fee</td><td>VPN replacement, web filtering, PDPA readiness checklist</td></tr>
<tr><td><b>Growth</b></td><td>51-200 staff</td><td>Cloudflare One ($7)</td><td class=r>${p['price_client'] / 12:.0f}</td><td>Above + DLP rules, monthly access report, breach-response runbook</td></tr>
<tr><td><b>Regulated</b></td><td>Finance, health, BPO</td><td>Netskope (quoted)</td><td class=r>Quoted</td><td>Data-centric controls, audit evidence pack</td></tr></table>
<p><span class='tag'>Economics</span>On the Growth package the provider keeps ${(p['price_client'] - p['platform']) / 12:.0f} of every
${p['price_client'] / 12:.0f} ({pct(p['gm'], 0)} gross margin on recurring revenue) before one-off setup fees.</p></div>

<div class='rec'><span class='num'>2</span><h3>Sell through partners SMEs already trust</h3>
<p><span class='tag'>Why</span>Selling security directly is costly: Zscaler spends {pct(r['sm_pct'])} of revenue on sales and marketing and
earns {pct(r['channel_share'], 0)} of revenue through partners{c('zs_10k')}. A start-up cannot afford a direct sales force.</p>
<p><span class='tag'>What</span>Three channels: (1) internet providers, which already bill SMEs monthly and run local data centres;
(2) accounting and audit firms, which will be asked about PDPA readiness; (3) chambers of commerce and industry associations, for
workshops that lead with a free readiness check. Offer partners a recurring revenue share rather than a one-off fee.</p></div>

<div class='rec'><span class='num'>3</span><h3>Earn the right to expand to India</h3>
<p><span class='tag'>Why</span>India's SASE market is about $528M and growing 22.1% a year{c('coherent_india')}, and its DPDP security
duties apply from 13 May 2027{c('in_dpdp')}.</p>
<p><span class='tag'>What</span>Use Sri Lanka as the playbook, then enter South India through one partner. <b>Gate:</b> proceed only if, by
mid-2027, the Sri Lankan business has 40+ paying firms, net revenue retention above 100% and a referenceable PDPA case study.</p></div>

<h2><span class='n'>10</span>Implementation roadmap and KPIs</h2>
<table><tr><th style='width:18%'>Phase</th><th>Actions</th><th style='width:30%'>Exit criteria</th></tr>
<tr><td><b>Days 0-30</b><br><span class='small'>Validate</span></td><td>Survey 50 Colombo SMEs on headcount, remote work and current security; register as a platform partner; draft the PDPA readiness checklist</td><td>Survey confirms the two most sensitive inputs (users per firm, need share)</td></tr>
<tr><td><b>Days 31-60</b><br><span class='small'>Pilot</span></td><td>Deploy for 5 pilot firms free of charge; build the onboarding runbook; sign one internet-provider or audit-firm partner</td><td>Pilot setup under 5 working days per firm; 4 of 5 willing to pay</td></tr>
<tr><td><b>Days 61-90</b><br><span class='small'>Launch</span></td><td>Launch three packages; run two chamber workshops; publish one case study</td><td>15 paying firms by day 90</td></tr></table>
<table><tr><th>KPI</th><th class=r>Year 1</th><th class=r>Year 3</th><th class=r>Year 5</th></tr>
<tr><td>Managed seats</td><td class=r>{p['y1_seats']:,}</td><td class=r>{p['y3_seats']:,}</td><td class=r>{p['y5_seats']:,.0f}</td></tr>
<tr><td>Client ARR at ${p['price_client'] / 12:.0f}/user/month</td><td class=r>{m(p['y1_arr'] / 1e6, 2)}</td><td class=r>{m(p['y3_arr'] / 1e6, 1)}</td><td class=r>{m(p['y5_arr'] / 1e6, 1)}</td></tr>
<tr><td>Share of modal seats needing SASE</td><td class=r>{pct(p['y1_seats'] / s.seats_mode)}</td><td class=r>{pct(p['y3_seats'] / s.seats_mode)}</td><td class=r>{pct(p['share_y5'])}</td></tr>
<tr><td>Net revenue retention</td><td class=r>&gt; 100%</td><td class=r>&gt; 110%</td><td class=r>&gt; 115%</td></tr>
<tr><td>Recurring gross margin</td><td class=r>&ge; {pct(p['gm'], 0)}</td><td class=r>&ge; {pct(p['gm'], 0)}</td><td class=r>&ge; {pct(p['gm'], 0)}</td></tr></table>
<p class='small'>Year-5 seats equal the P50 SOM ({m(s.som_p50 / 1e6, 1)}) divided by the $84 platform price per user per year.</p>

<h2><span class='n'>11</span>Risks and mitigations</h2>
<table><tr><th style='width:26%'>Risk</th><th style='width:11%'>Likelihood</th><th>Mitigation</th></tr>
<tr><td>PDPA enforcement slips, weakening urgency</td><td>Medium</td><td>Lead with breach and fraud losses (CERT data) as well as compliance; keep the offer valuable without a deadline</td></tr>
<tr><td>Platform changes its free tier or price</td><td>Low-Med</td><td>Keep a second platform (Netskope) qualified; price in services so margin survives</td></tr>
<tr><td>Global vendor sells direct to SMEs or via a telco</td><td>Medium</td><td>Compete on local onboarding and Sinhala/Tamil support; sign the telco as a partner first</td></tr>
<tr><td>SME budgets squeezed</td><td>Medium</td><td>Starter package on the free tier; monthly billing; no hardware</td></tr>
<tr><td>Currency risk (USD costs, LKR revenue)</td><td>Medium</td><td>Index rupee prices to USD quarterly; keep a three-month cost buffer</td></tr>
<tr><td>Inputs in the model are wrong</td><td>Medium</td><td>Days 0-30 survey targets the two most sensitive inputs before money is spent</td></tr></table>

<h2 class='pb'><span class='n'>12</span>Methodology and limitations</h2>
<ul><li><b>Sources.</b> Company filings on SEC EDGAR (Zscaler 10-K, results releases), analyst-firm releases (Dell'Oro, Gartner abstracts),
syndicated market reports, G2 and Gartner Peer Insights pages, and Sri Lankan and Indian government and press sources. All were accessed
between 1 and 15 November 2026 and are listed with links.</li>
<li><b>Computation.</b> Every number in this report is computed in Python from CSV files in the repository; Excel workbooks repeat the key
calculations with live formulas. Unit tests check the arithmetic.</li>
<li><b>Tools.</b> Desk research and drafting were AI-assisted; every figure was checked against its source and recomputed in code. The
NotebookLM step suggested in the brief was replaced by direct reading of the filing and code-based ratio analysis.</li>
<li><b>Limitations.</b> (1) Market estimates use different scopes. (2) Gartner's 2026 forecast figures are reported second-hand. (3) Firm counts
come from the 2013/14 census listing, adjusted by an assumed growth factor. (4) Prices for quote-only vendors are third-party purchase data.
(5) Review ratings are snapshots. (6) No primary research was done; the 30-day survey in section 10 is designed to close that gap.</li></ul>

<h2><span class='n'>A</span>Appendix: data tables</h2>
<table><tr><th>Publisher</th><th class=r>2025 ($bn)</th><th class=r>Forecast year</th><th class=r>Forecast ($bn)</th><th class=r>CAGR</th></tr>
{''.join(f"<tr><td>{x.publisher}{' <span class=tag>anchor</span>' if x.anchor else ''}</td><td class=r>{x.base_usd_b:.2f}</td><td class=r>{int(x.forecast_year)}</td><td class=r>{x.forecast_usd_b:.2f}</td><td class=r>{x.cagr_pct:.1f}%</td></tr>" for x in est.sort_values('base_usd_b', ascending=False).itertuples())}</table>
<table><tr><th>Zscaler FY2026 ratio</th><th class=r>Value</th><th>Zscaler FY2026 ratio</th><th class=r>Value</th></tr>
<tr><td>Revenue growth</td><td class=r>{pct(r['revenue_growth'])}</td><td>Rule of 40</td><td class=r>{r['rule_of_40']:.1f}</td></tr>
<tr><td>Gross margin</td><td class=r>{pct(r['gross_margin'])}</td><td>Stock comp / revenue</td><td class=r>{pct(r['sbc_pct'])}</td></tr>
<tr><td>GAAP operating margin</td><td class=r>{pct(r['op_margin'])}</td><td>RPO / revenue</td><td class=r>{r['rpo_to_revenue']:.2f}x</td></tr>
<tr><td>Free cash flow margin</td><td class=r>{pct(r['fcf_margin'])}</td><td>Goodwill / assets</td><td class=r>{pct(r['goodwill_to_assets'])}</td></tr>
<tr><td>Liabilities / assets</td><td class=r>{pct(r['liabilities_to_assets'])}</td><td>Revenue per employee</td><td class=r>${r['revenue_per_employee_k']:.0f}K</td></tr></table>
<h2><span class='n'>R</span>References</h2>{c.html()}
"""
    return to_pdf(page("Edge Shift - capstone report", body), "Task4_Capstone_Report_Edge_Shift", "Edge Shift · SASE market and the Sri Lankan SME opportunity")


# ===================================================================== Deck
DECK_CSS = """
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: 'Inter', sans-serif; color: #1d2430; }
.sl { width: 1280px; height: 720px; padding: 52px 64px 40px; position: relative; page-break-after: always; overflow: hidden;
      background: #fcfcfb; }
.sl.dark { background: linear-gradient(135deg, #0f2a44 0%, #16406a 100%); color: #fff; }
.sl.dark h1, .sl.dark h2 { color: #fff; }
.k { font-size: 13px; letter-spacing: 2px; text-transform: uppercase; color: #2a78d6; font-weight: 700; margin-bottom: 10px; }
.dark .k { color: #8cc0ff; }
h1 { font-family: 'Lora', serif; font-size: 64px; margin: 0 0 14px; line-height: 1.05; color: #0f2a44; font-weight: 600; }
h2 { font-family: 'Lora', serif; font-size: 34px; margin: 0 0 18px; line-height: 1.15; color: #0f2a44; font-weight: 600; max-width: 1100px; }
p, li { font-size: 20px; line-height: 1.45; }
ul { padding-left: 24px; margin: 0; } li { margin-bottom: 10px; }
.foot { position: absolute; bottom: 20px; left: 64px; right: 64px; display: flex; justify-content: space-between;
        font-size: 12px; color: #8a93a1; }
.dark .foot { color: #a9bdd4; }
.g2 { display: grid; grid-template-columns: 1.75fr 1fr; gap: 36px; align-items: center; }
.g2e { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: start; }
.g3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.g4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.tile { background: #fff; border: 1px solid #e1e6ee; border-radius: 12px; padding: 20px 20px; }
.dark .tile { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.18); }
.tile b { display: block; font-family: 'Lora', serif; font-size: 40px; color: #0f2a44; line-height: 1.05; }
.dark .tile b { color: #fff; }
.tile span { font-size: 15px; color: #5b6676; display: block; margin-top: 6px; line-height: 1.35; }
.dark .tile span { color: #c9d8ea; }
img { width: 100%; border-radius: 6px; }
.card { background: #fff; border: 1px solid #e1e6ee; border-radius: 12px; padding: 22px 24px; }
.card h3 { font-family: 'Lora', serif; font-size: 22px; margin: 0 0 8px; color: #0f2a44; }
.card p { font-size: 16px; margin: 0; color: #3d4756; }
.num { display: inline-block; width: 34px; height: 34px; border-radius: 50%; background: #2a78d6; color: #fff; font-weight: 700;
       text-align: center; line-height: 34px; font-size: 17px; margin-bottom: 10px; }
table { border-collapse: collapse; width: 100%; font-size: 16px; }
th { background: #0f2a44; color: #fff; text-align: left; padding: 9px 12px; }
td { padding: 9px 12px; border-bottom: 1px solid #e3e7ee; }
td.r, th.r { text-align: right; }
.note { font-size: 13px; color: #6b7482; margin-top: 8px; }
"""


def deck(t: Triangulation, s: SizingResult, r: dict, comp: pd.DataFrame, sc: pd.DataFrame):
    sn = t.scenarios
    p = _plan_numbers(s)
    n = [0]

    def slide(inner: str, cls: str = "") -> str:
        n[0] += 1
        return (f"<section class='sl {cls}'>{inner}<div class='foot'><span>Edge Shift · {AUTHOR} · Datheon DT-2026-P5IEX</span>"
                f"<span>{n[0]}</span></div></section>")

    def im(name: str, h: int | None = None) -> str:
        style = f" style='max-height:{h}px;object-fit:contain'" if h else ""
        return f"<img src='{img(name)}'{style}>"

    slides = [
        slide(f"""<div style='margin-top:90px'><div class='k'>Capstone · AI Research &amp; Market Intelligence</div>
<h1>{TITLE}</h1><p style='font-size:28px;font-family:Lora,serif;color:#dbe8f7;margin:0 0 40px'>{SUBTITLE}</p>
<div class='g4'><div class='tile'><b>{b(t.base_2025)}</b><span>Global SASE market, 2025</span></div>
<div class='tile'><b>{b(sn.base.iloc[-1], 0)}</b><span>Base case by 2030</span></div>
<div class='tile'><b>{m(s.sam_p50 / 1e6)}</b><span>Sri Lankan SME market / yr</span></div>
<div class='tile'><b>1 Jan 2027</b><span>Sri Lanka PDPA core duties start</span></div></div>
<p style='margin-top:40px;color:#c9d8ea;font-size:17px'>{AUTHOR} · {DATE}</p></div>""", "dark"),
        slide(f"""<div class='k'>The answer</div><h2>SASE is a {b(t.base_2025)} market growing ~20% a year. Its least-served buyers are small firms, and in Sri Lanka they are about to need it by law.</h2>
<div class='g3' style='margin-top:26px'>
<div class='card'><span class='num'>1</span><h3>Market</h3><p>{b(t.base_2025)} in 2025 (11 estimates, {t.spread_ratio:.1f}x spread); {b(sn.conservative.iloc[-1], 0)}-{b(sn.aggressive.iloc[-1], 0)} by 2030. Consolidating onto single-vendor platforms.</p></div>
<div class='card'><span class='num'>2</span><h3>Competition</h3><p>Four Gartner Leaders price for enterprises. G2 ratings are 4.3-4.6 for all; prices run $0-$300 per user per year. Cloudflare best fits SMEs ({sc.loc['Cloudflare', 'weighted']:.2f}/5).</p></div>
<div class='card'><span class='num'>3</span><h3>Opportunity</h3><p>Sri Lankan SMEs: {m(s.sam_p50 / 1e6)} a year (P50). A local managed-SASE provider can reach {m(s.som_p50 / 1e6, 1)} ARR in five years.</p></div></div>"""),
        slide(f"""<div class='k'>Market size</div><h2>Eleven estimates disagree by {t.spread_ratio:.1f}x, so I anchored on the four most transparent</h2>
<div class='g2'><div>{im('t1_estimate_dispersion', 530)}</div><div><ul><li>Gaps are about <b>scope</b>: vendor revenue vs buyer spend vs bundles with services.</li>
<li>Median of Dell'Oro, Gartner, MarketsandMarkets and Mordor: <b>{b(t.base_2025)}</b>.</li><li>Range of anchors: {b(t.anchor_low)}-{b(t.anchor_high)}.</li></ul></div></div>"""),
        slide(f"""<div class='k'>Growth</div><h2>Revenue is growing 17%-22% a year; base case reaches {b(sn.base.iloc[-1])} by 2030</h2>
<div class='g2'><div>{im('t1_scenarios', 530)}</div><div><ul><li>Dell'Oro: SASE +21% while branch routers fell 25% (3Q 2025).</li>
<li>Single-vendor SASE grew 21% vs 3% for multi-vendor.</li><li>Fastest segments: <b>SMEs</b> and <b>Asia-Pacific</b>.</li></ul></div></div>"""),
        slide(f"""<div class='k'>Competition</div><h2>Users rate all five platforms alike. Price is what separates them.</h2>
<div class='g2'><div>{im('t3_price_vs_rating', 530)}</div><div><ul><li>Only Cloudflare publishes a price: free to 50 users, then $7/user/month.</li>
<li>Zscaler ~$150-$300 and Prisma Access ~$168-$264 per user per year (third-party data).</li><li>Challengers grow fastest: Cato +42%, Netskope +31%.</li></ul></div></div>"""),
        slide(f"""<div class='k'>SME fit</div><h2>Weighted for a 20-200 person Sri Lankan firm, Cloudflare leads and Netskope follows</h2>
{im('t3_scorecard', 470)}<p class='note'>Cloudflare stays first unless Gartner position carries about half of all weight. Weights are editable in Task3_Competitor_Matrix.xlsx.</p>"""),
        slide(f"""<div class='k'>Case study · Zscaler FY2026 10-K</div><h2>The leader is financially sound but strategically pressured</h2>
<div class='g4' style='margin-bottom:22px'><div class='tile'><b>{m(r['revenue_m'])}</b><span>Revenue, +{pct(r['revenue_growth'])}</span></div>
<div class='tile'><b>{pct(r['fcf_margin'])}</b><span>Free cash flow margin</span></div>
<div class='tile'><b>{m(r['fcf_minus_sbc_m'])}</b><span>Free cash flow minus stock pay</span></div>
<div class='tile'><b>{pct(r['fy27_rev_growth_mid'])}</b><span>FY2027 guided growth</span></div></div>
<div class='g2e'><div>{im('t2_revenue_dollar', 340)}</div><div><ul><li>Sales &amp; marketing = {pct(r['sm_pct'], 0)} of revenue; {pct(r['channel_share'], 0)} sold through partners.</li>
<li>Interest income ({m(r['interest_income_m'])}) offsets the operating loss.</li><li>Asia-Pacific only {pct(r['apac_share'], 0)} of revenue.</li></ul></div></div>"""),
        slide(f"""<div class='k'>Why now</div><h2>Two privacy laws switch on within 18 months</h2>{im('t4_regulation_timeline', 330)}
<div class='g3' style='margin-top:14px'><div class='card'><h3>Sri Lanka PDPA</h3><p>Core duties from 1 Jan 2027; penalties up to LKR 10M per breach.</p></div>
<div class='card'><h3>India DPDP</h3><p>Security and 72-hour breach duties from 13 May 2027; up to INR 250 crore.</p></div>
<div class='card'><h3>Threat level</h3><p>12,650 cyber complaints to Sri Lanka CERT in 2025.</p></div></div>"""),
        slide(f"""<div class='k'>Opportunity</div><h2>Bottom-up: Sri Lankan SMEs are a {m(s.sam_p50 / 1e6)}-a-year market the global leaders do not price for</h2>
<div class='g2e'><div>{im('t1_tam_sam_som', 400)}</div><div>{im('t1_monte_carlo', 400)}</div></div>
<p class='note'>20,000-draw Monte Carlo over firm counts, seats, need share and price. 80% interval for SAM: {m(s.sam_p10 / 1e6)}-{m(s.sam_p90 / 1e6)}; SOM P50 {m(s.som_p50 / 1e6, 1)}.</p>"""),
        slide(f"""<div class='k'>Recommendations</div><h2>Three moves</h2><div class='g3'>
<div class='card'><span class='num'>1</span><h3>Launch compliance-ready managed SASE</h3><p>For firms of 11-200 staff, on Cloudflare One (free to 50 users, local PoP) with Netskope for regulated clients. ~${p['price_client'] / 12:.0f}/user/month; {pct(p['gm'], 0)} recurring gross margin.</p></div>
<div class='card'><span class='num'>2</span><h3>Sell through trusted partners</h3><p>Internet providers, accounting and audit firms, chambers of commerce. Lead with a free PDPA readiness check; share recurring revenue.</p></div>
<div class='card'><span class='num'>3</span><h3>Earn the India expansion</h3><p>India SASE: $528M, +22.1% a year; DPDP duties from 13 May 2027. Gate: 40+ firms, NRR &gt; 100% by mid-2027.</p></div></div>"""),
        slide(f"""<div class='k'>Roadmap</div><h2>90 days to first revenue; five years to {m(p['y5_arr'] / 1e6, 1)} ARR</h2>
<div class='g2e'><table><tr><th>Phase</th><th>Milestone</th></tr><tr><td>Days 0-30</td><td>Survey 50 SMEs; platform partnership; readiness checklist</td></tr>
<tr><td>Days 31-60</td><td>5 free pilots; sign first channel partner</td></tr><tr><td>Days 61-90</td><td>Launch 3 packages; 15 paying firms</td></tr></table>
<table><tr><th>KPI</th><th class=r>Y1</th><th class=r>Y3</th><th class=r>Y5</th></tr>
<tr><td>Seats</td><td class=r>{p['y1_seats']:,}</td><td class=r>{p['y3_seats']:,}</td><td class=r>{p['y5_seats']:,.0f}</td></tr>
<tr><td>Client ARR</td><td class=r>{m(p['y1_arr'] / 1e6, 2)}</td><td class=r>{m(p['y3_arr'] / 1e6, 1)}</td><td class=r>{m(p['y5_arr'] / 1e6, 1)}</td></tr>
<tr><td>NRR</td><td class=r>&gt;100%</td><td class=r>&gt;110%</td><td class=r>&gt;115%</td></tr></table></div>"""),
        slide("""<div class='k'>Risks</div><h2>What could go wrong, and the hedge for each</h2>
<table><tr><th>Risk</th><th>Mitigation</th></tr><tr><td>PDPA enforcement slips</td><td>Lead with fraud and breach losses, not only compliance</td></tr>
<tr><td>Platform changes price or free tier</td><td>Keep Netskope qualified; earn margin on services</td></tr>
<tr><td>Global vendor goes direct via telcos</td><td>Sign the telco first; win on local onboarding and language</td></tr>
<tr><td>Currency (USD costs, LKR revenue)</td><td>Index prices quarterly; three-month buffer</td></tr>
<tr><td>Model inputs wrong</td><td>30-day survey targets the two most sensitive inputs</td></tr></table>"""),
        slide(f"""<div style='margin-top:120px'><div class='k'>Thank you</div><h1 style='font-size:52px'>Reproducible, cited, and ready to test</h1>
<p style='color:#c9d8ea;max-width:900px'>Every figure comes from code and CSV files in the repository, with links to its source. Full report,
10-K briefing, competitor matrix and models: github.com/DevRisny/Datheon_AI_Research_and_Market_Intelligence</p>
<p style='color:#c9d8ea'>{AUTHOR} · {PROGRAM}</p></div>""", "dark"),
    ]
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{DECK_CSS}</style></head><body>{''.join(slides)}</body></html>"
    return to_pdf(html, "Task4_Executive_Deck_Edge_Shift", "", landscape_deck=True)
