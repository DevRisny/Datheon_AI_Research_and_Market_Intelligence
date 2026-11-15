"""Task 1: triangulate the global SASE market and project it to 2030."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import DATA

# The four estimates with the most transparent scope: two analyst houses that
# track vendor revenue or buyer spending every quarter, plus the two most-cited
# syndicated reports. They anchor the base year; the rest show dispersion.
ANCHOR_IDS = ("DO", "GA", "MM", "MO")


def load_estimates() -> pd.DataFrame:
    df = pd.read_csv(DATA / "sase_market_estimates.csv")
    df["anchor"] = df["id"].isin(ANCHOR_IDS)
    return df


def implied_cagr(start: float, end: float, years: int) -> float:
    """Compound annual growth rate between two values."""
    if start <= 0 or years <= 0:
        raise ValueError("start must be positive and years must be > 0")
    return (end / start) ** (1 / years) - 1


def project(base: float, cagr: float, years: range) -> list[float]:
    return [base * (1 + cagr) ** (y - years.start) for y in years]


@dataclass(frozen=True)
class Triangulation:
    base_2025: float          # USD bn, median of anchor set
    anchor_low: float
    anchor_high: float
    all_median: float
    all_low: float
    all_high: float
    spread_ratio: float       # highest / lowest estimate
    cagr_conservative: float  # Dell'Oro implied
    cagr_base: float          # median of all published CAGRs
    cagr_aggressive: float    # MarketsandMarkets
    scenarios: pd.DataFrame   # 2025-2030 by scenario


def triangulate(df: pd.DataFrame | None = None) -> Triangulation:
    df = load_estimates() if df is None else df
    anchors = df[df["anchor"]]
    base = float(np.median(anchors["base_usd_b"]))
    cagrs = df["cagr_pct"].astype(float) / 100

    dello = df.loc[df["id"] == "DO"].iloc[0]
    c_cons = implied_cagr(dello.base_usd_b, dello.forecast_usd_b, int(dello.forecast_year - dello.base_year))
    c_base = float(np.median(cagrs))
    c_aggr = float(df.loc[df["id"] == "MM", "cagr_pct"].iloc[0]) / 100

    years = range(2025, 2031)
    scen = pd.DataFrame(
        {
            "year": list(years),
            "conservative": project(base, c_cons, years),
            "base": project(base, c_base, years),
            "aggressive": project(base, c_aggr, years),
        }
    )
    return Triangulation(
        base_2025=base,
        anchor_low=float(anchors["base_usd_b"].min()),
        anchor_high=float(anchors["base_usd_b"].max()),
        all_median=float(df["base_usd_b"].median()),
        all_low=float(df["base_usd_b"].min()),
        all_high=float(df["base_usd_b"].max()),
        spread_ratio=float(df["base_usd_b"].max() / df["base_usd_b"].min()),
        cagr_conservative=c_cons,
        cagr_base=c_base,
        cagr_aggressive=c_aggr,
        scenarios=scen,
    )
