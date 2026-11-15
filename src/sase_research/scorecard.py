"""Task 3: SME-fit scorecard. The same formulas are written into the Excel matrix."""

from __future__ import annotations

import pandas as pd

from . import DATA

WEIGHTS = {
    "Affordability": 0.25,
    "Small-firm fit": 0.20,
    "User satisfaction": 0.20,
    "Market validation": 0.15,
    "Price transparency": 0.10,
    "Momentum": 0.10,
}

MQ_SCORE = {"Leader": 5.0, "Visionary": 3.5, "Challenger": 3.0, "Niche": 2.0}


def clip(x: float, lo: float = 1.0, hi: float = 5.0) -> float:
    return max(lo, min(hi, x))


def affordability(price_mid: float) -> float:
    """5 at $0, falling 4 points across $300 per user per year."""
    return clip(5 - 4 * price_mid / 300)


def satisfaction(g2: float) -> float:
    """G2 4.0 -> 1, 4.7 -> 5 (the five vendors sit inside that band)."""
    return clip(1 + (g2 - 4.0) / 0.7 * 4)


def momentum(growth_pct: float) -> float:
    return clip(1 + growth_pct / 50 * 4)


def mq(position: str) -> float:
    return next((v for k, v in MQ_SCORE.items() if position.startswith(k)), 2.0)


def transparency(published: str) -> float:
    return 5.0 if published.strip().lower() not in ("none published", "contact for pricing", "") else 1.0


def compute(comp: pd.DataFrame | None = None) -> pd.DataFrame:
    comp = pd.read_csv(DATA / "competitors.csv") if comp is None else comp
    rows = {}
    for _, r in comp.iterrows():
        rows[r.vendor] = {
            "Affordability": affordability(r.price_mid_usd_user_yr),
            "Small-firm fit": float(r.sme_fit_score),
            "User satisfaction": satisfaction(r.g2_rating),
            "Market validation": mq(r.gartner_sase_mq_2026),
            "Price transparency": transparency(r.published_entry_price),
            "Momentum": momentum(r.growth_pct),
        }
    s = pd.DataFrame(rows).T
    s["weighted"] = sum(s[c] * w for c, w in WEIGHTS.items())
    return s.sort_values("weighted", ascending=False)
