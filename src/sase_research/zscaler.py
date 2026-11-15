"""Task 2: financial-health ratios from Zscaler's FY2026 Form 10-K."""

from __future__ import annotations

import pandas as pd

from . import DATA


def load() -> tuple[dict, dict, dict]:
    fin = pd.read_csv(DATA / "zscaler_fy2026.csv").set_index("metric")
    cur = fin["fy2026_usd_m"].to_dict()
    prev = fin["fy2025_usd_m"].to_dict()
    kpi = pd.read_csv(DATA / "zscaler_kpis.csv").set_index("kpi")["value"].to_dict()
    return cur, prev, kpi


def ratios() -> dict:
    c, p, k = load()
    rev, rev0 = c["Revenue"], p["Revenue"]
    r = {}
    r["revenue_m"] = rev
    r["revenue_growth"] = rev / rev0 - 1
    r["gross_margin"] = c["Gross profit"] / rev
    r["gross_margin_prev"] = p["Gross profit"] / rev0
    for key, name in [("sm", "Sales and marketing"), ("rd", "Research and development"), ("ga", "General and administrative")]:
        r[f"{key}_pct"] = c[name] / rev
        r[f"{key}_pct_prev"] = p[name] / rev0
    r["op_margin"] = c["Loss from operations"] / rev
    r["op_margin_prev"] = p["Loss from operations"] / rev0
    r["net_margin"] = c["Net loss"] / rev
    r["sbc_pct"] = c["Stock-based compensation"] / rev
    r["sbc_m"] = c["Stock-based compensation"]
    r["ocf_margin"] = c["Operating cash flow"] / rev
    r["fcf_m"] = c["Free cash flow"]
    r["fcf_margin"] = c["Free cash flow"] / rev
    r["fcf_margin_prev"] = p["Free cash flow"] / rev0
    r["fcf_minus_sbc_m"] = c["Free cash flow"] - c["Stock-based compensation"]
    r["fcf_minus_sbc_prev_m"] = p["Free cash flow"] - p["Stock-based compensation"]
    r["rule_of_40"] = (r["revenue_growth"] + r["fcf_margin"]) * 100
    r["capex_m"] = c["Purchases of property and equipment"]
    r["capex_growth"] = c["Purchases of property and equipment"] / p["Purchases of property and equipment"] - 1
    liquid = c["Cash and cash equivalents"] + c["Short-term investments"]
    liquid0 = p["Cash and cash equivalents"] + p["Short-term investments"]
    r["liquidity_m"] = liquid
    r["liquidity_prev_m"] = liquid0
    r["net_cash_m"] = liquid - c["Convertible notes principal due 2028"]
    r["debt_principal_m"] = c["Convertible notes principal due 2028"]
    r["liabilities_to_assets"] = c["Total liabilities"] / c["Total assets"]
    deferred = c["Deferred revenue current"] + c["Deferred revenue noncurrent"]
    deferred0 = p["Deferred revenue current"] + p["Deferred revenue noncurrent"]
    r["deferred_m"] = deferred
    r["deferred_growth"] = deferred / deferred0 - 1
    r["rpo_m"] = c["Remaining performance obligations"]
    r["rpo_to_revenue"] = c["Remaining performance obligations"] / rev
    r["goodwill_m"] = c["Goodwill"]
    r["goodwill_growth"] = c["Goodwill"] / p["Goodwill"] - 1
    r["goodwill_to_assets"] = c["Goodwill"] / c["Total assets"]
    r["acquisitions_m"] = c["Acquisitions net of cash"]
    r["interest_income_m"] = c["Interest income"]
    r["interest_vs_oploss"] = c["Interest income"] / abs(c["Loss from operations"])
    r["intl_share"] = 1 - c["Revenue United States"] / rev
    r["apac_share"] = c["Revenue Asia Pacific"] / rev
    r["apac_growth"] = c["Revenue Asia Pacific"] / p["Revenue Asia Pacific"] - 1
    r["us_growth"] = c["Revenue United States"] / p["Revenue United States"] - 1
    r["emea_growth"] = c["Revenue EMEA"] / p["Revenue EMEA"] - 1
    r["arr_m"] = k["ARR"]
    r["nrr"] = k["Net revenue retention"] / 100
    r["fy27_rev_mid_m"] = (k["FY2027 revenue guidance low"] + k["FY2027 revenue guidance high"]) / 2
    r["fy27_rev_growth_mid"] = r["fy27_rev_mid_m"] / rev - 1
    r["fy27_arr_mid_m"] = (k["FY2027 ARR guidance low"] + k["FY2027 ARR guidance high"]) / 2
    r["fy27_arr_growth_mid"] = r["fy27_arr_mid_m"] / k["ARR"] - 1
    r["arr_per_customer_k"] = k["ARR"] / k["Customers"] * 1000
    r["revenue_per_employee_k"] = rev / k["Employees"] * 1000
    r["channel_share"] = k["Channel share of revenue"] / 100
    r["top5_channel_share"] = k["Top five channel partners share of revenue"] / 100
    r["tsr_5y"] = k["Five-year TSR ($100 invested 31 Jul 2021)"]
    return r
