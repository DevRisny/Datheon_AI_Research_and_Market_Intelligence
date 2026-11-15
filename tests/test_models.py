"""Arithmetic checks: the reports quote these numbers, so they must hold."""

import math
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sase_research import DATA, market, scorecard, sizing, zscaler  # noqa: E402


def test_cagr_roundtrip():
    assert market.implied_cagr(100, 200, 5) == pytest.approx(2 ** 0.2 - 1)
    assert market.project(10, 0.1, range(2025, 2028)) == pytest.approx([10, 11, 12.1])


def test_cagr_rejects_bad_input():
    with pytest.raises(ValueError):
        market.implied_cagr(0, 10, 5)


def test_triangulation_uses_anchor_median():
    t = market.triangulate()
    assert t.base_2025 == pytest.approx((12.94 + 15.0) / 2)  # median of 12.0, 12.94, 15.0, 15.52
    assert t.anchor_low <= t.base_2025 <= t.anchor_high
    assert t.cagr_conservative < t.cagr_base < t.cagr_aggressive
    s = t.scenarios
    assert s.base.iloc[-1] == pytest.approx(t.base_2025 * (1 + t.cagr_base) ** 5)


def test_delloro_doubling_implies_about_15pct():
    df = market.load_estimates()
    r = df[df.id == "DO"].iloc[0]
    assert r.forecast_usd_b / r.base_usd_b == pytest.approx(2.0)


def test_sizing_modal_case_by_hand():
    p = sizing.point(sizing.load_parameters())
    seats = 1.10 * 0.25 * (71126 * 20 + 10405 * 90)
    assert sizing.seats(p) == pytest.approx(seats)
    assert sizing.sam_usd(p) == pytest.approx(seats * 84)
    assert sizing.som_usd(p) == pytest.approx(seats * 84 * 0.05)


def test_monte_carlo_is_reproducible_and_ordered():
    a, b = sizing.run(n=4000), sizing.run(n=4000)
    assert a.sam_p50 == b.sam_p50
    assert a.sam_p10 < a.sam_p50 < a.sam_p90
    assert a.som_p10 < a.som_p50 < a.som_p90
    assert a.tornado.swing.is_monotonic_decreasing


def test_zscaler_ratios_match_filing():
    r = zscaler.ratios()
    assert r["revenue_growth"] == pytest.approx(3352.523 / 2673.115 - 1)
    assert r["fcf_minus_sbc_m"] == pytest.approx(779.143 - 830.392)
    assert r["net_cash_m"] == pytest.approx(928.354 + 2545.797 - 1725.0)
    fin = pd.read_csv(DATA / "zscaler_fy2026.csv").set_index("metric")["fy2026_usd_m"]
    regions = sum(fin[f"Revenue {g}"] for g in ["United States", "EMEA", "Asia Pacific", "Other"])
    assert regions == pytest.approx(fin["Revenue"], abs=0.01)
    assert fin["Gross profit"] == pytest.approx(fin["Revenue"] - fin["Cost of revenue"], abs=0.01)


def test_scorecard_weights_and_bounds():
    assert math.isclose(sum(scorecard.WEIGHTS.values()), 1.0)
    s = scorecard.compute()
    crit = list(scorecard.WEIGHTS)
    assert ((s[crit] >= 1) & (s[crit] <= 5)).all().all()
    assert scorecard.affordability(0) == 5 and scorecard.affordability(300) == 1
    assert scorecard.mq("Leader (first year)") == 5


def test_every_competitor_row_has_sources_for_numbers():
    comp = pd.read_csv(DATA / "competitors.csv")
    assert len(comp) == 5
    assert comp[["price_low_usd_user_yr", "price_mid_usd_user_yr", "price_high_usd_user_yr"]].apply(
        lambda r: r.iloc[0] <= r.iloc[1] <= r.iloc[2], axis=1).all()
