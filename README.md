<div align="center">

# Edge Shift
### The SASE market and the Sri Lankan SME opportunity

**Datheon AI Research & Market Intelligence Internship · DT-2026-P5IEX**
Risny Suha · November 2026

[**Project site**](https://devrisny.github.io/Datheon_AI_Research_and_Market_Intelligence/) ·
[Capstone report](outputs/Task4_Capstone_Report_Edge_Shift.pdf) ·
[Executive deck](outputs/Task4_Executive_Deck_Edge_Shift.pdf)

![tests](https://github.com/DevRisny/Datheon_AI_Research_and_Market_Intelligence/actions/workflows/tests.yml/badge.svg)

</div>

Cloud-delivered security (**SASE**: Secure Access Service Edge) is replacing the office VPN and firewall.
This project sizes that market, reads its leader's annual report, tears down five competing platforms,
and builds a bottom-up case for the buyers the leaders overlook: **Sri Lanka's small and medium firms**,
just before the country's Personal Data Protection Act takes effect on **1 January 2027**.

| | |
|---|---|
| **$14.0B** | Global SASE market, 2025 (median of four anchor sources; 11 estimates span $2.7B-$23.2B) |
| **$36.8B** | Base-case market by 2030 (21.4% CAGR; range $27.9B-$40.3B) |
| **$85M / yr** | Sri Lankan SME serviceable market, Monte Carlo P50 (80% interval $53M-$134M) |
| **$4.6M** | Year-5 ARR one focused managed-SASE provider can win (P50) |

## Deliverables

| Task | Brief | Output |
|---|---|---|
| **1. Market landscape** | Size a market with TAM/SAM/SOM, CAGR and drivers, all cited | [Memo (PDF)](outputs/Task1_SASE_Market_Landscape_Memo.pdf) · [Live-formula model (Excel)](outputs/Task1_SASE_Market_Model.xlsx) |
| **2. 10-K synthesis** | Executive briefing on a company's financial health and strategic risks | [Zscaler FY2026 briefing (PDF)](outputs/Task2_Zscaler_10K_Executive_Briefing.pdf) |
| **3. Competitive teardown** | Five players: pricing, differentiators, G2/Capterra sentiment, vulnerabilities; matrix + SWOT | [Teardown (PDF)](outputs/Task3_Competitive_Teardown.pdf) · [Matrix, scorecard & SWOT (Excel)](outputs/Task3_Competitor_Matrix.xlsx) |
| **4. Capstone** | 15-20 page report with recommendations, plus an executive deck | [Report, 16 pages (PDF)](outputs/Task4_Capstone_Report_Edge_Shift.pdf) · [Deck, 13 slides (PDF)](outputs/Task4_Executive_Deck_Edge_Shift.pdf) |

## Key findings

1. **No agreed market size.** Eleven 2025 estimates differ by 8.5x because publishers define SASE differently. I anchored on Dell'Oro, Gartner, MarketsandMarkets and Mordor rather than averaging incompatible scopes.
2. **Growth is real and consolidating.** Vendor revenue grew 17%-22% a year through 2025 while branch-router spending fell 25%; single-vendor platforms are taking share.
3. **The leader is sound but slowing.** Zscaler grew revenue 25.4% with a 23.2% free-cash-flow margin, but stock pay ($830M) now exceeds free cash flow ($779M) and FY2027 growth is guided to ~17%.
4. **Price, not satisfaction, separates vendors.** G2 ratings span 4.3-4.6; prices span $0-$300 per user per year. Cloudflare scores highest for SME fit (4.29/5), Netskope second.
5. **An overlooked beachhead.** Sri Lankan SMEs (11-200 staff) are worth about $85M a year, and privacy-law duties start on 1 January 2027 (India's follow on 13 May 2027).

**Recommendations:** launch a compliance-ready managed SASE service on a free-to-start platform; sell through internet providers, audit firms and chambers; expand to India only after clear year-one milestones.

## How it is built

Every number in the PDFs, workbooks and charts is computed from the CSV files in [`data/`](data/), each row with its source URL.

```
data/                      sourced inputs (CSV) + sources.md (62 references)
src/sase_research/
  market.py                Task 1: triangulation and 2030 scenarios
  sizing.py                Task 1: bottom-up Sri Lankan SAM/SOM, 20,000-draw Monte Carlo, tornado sensitivity
  zscaler.py               Task 2: 40+ ratios from the FY2026 10-K
  scorecard.py, swot.py    Task 3: weighted SME-fit scorecard and SWOT
  charts.py                15 figures in one validated, colour-blind-safe light palette
  excel.py                 workbooks with live formulas (recalculate when you edit an input)
  docs_t1_t3.py, docs_t4.py  the reports and deck (HTML -> PDF)
tests/                     arithmetic checks (pytest)
outputs/                   generated deliverables
docs/                      GitHub Pages site
```

```bash
pip install -r requirements.txt
python -m playwright install chromium
PYTHONPATH=src python -m sase_research.build   # rebuilds every chart, workbook and PDF
pytest
```

## Method notes and limitations

- **Sources:** SEC filings (Zscaler 10-K and results), Dell'Oro and Gartner releases, syndicated market reports, G2 and Gartner Peer Insights, and Sri Lankan/Indian government and press sources, accessed 1-15 Nov 2026.
- **Tools:** the brief suggested NotebookLM; I read the 10-K on SEC EDGAR directly and recomputed every ratio in Python so each figure traces to a line of the filing. Desk research and drafting were AI-assisted; every figure was checked against its source and recomputed in code.
- **Limits:** market estimates use different scopes; Gartner's 2026 forecast is reported second-hand; Sri Lankan firm counts come from the 2013/14 census listing with an assumed growth factor; prices for quote-only vendors are third-party purchase data; ratings are snapshots; no primary research yet (the capstone proposes a 50-firm survey to test the two most sensitive inputs).

---
© 2026 Risny Suha. Code under the MIT License; third-party data belongs to its publishers.
