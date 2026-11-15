"""Rebuild every deliverable: python -m sase_research.build (with src/ on PYTHONPATH)."""

from __future__ import annotations

import json

import pandas as pd

from . import DATA, OUT, charts, docs_t1_t3, excel, market, scorecard, sizing, zscaler


def main(only: str | None = None) -> None:
    est = market.load_estimates()
    t = market.triangulate(est)
    s = sizing.run()
    r = zscaler.ratios()
    fin = pd.read_csv(DATA / "zscaler_fy2026.csv")
    comp = pd.read_csv(DATA / "competitors.csv")
    sc = scorecard.compute(comp)
    charts.build_all(est, t, s, 528.1, fin, r, comp, sc, scorecard.WEIGHTS)
    excel.market_model()
    excel.competitor_matrix()
    res = {
        "triangulation": {k: getattr(t, k) for k in ["base_2025", "anchor_low", "anchor_high", "all_median", "all_low",
                                                      "all_high", "spread_ratio", "cagr_conservative", "cagr_base", "cagr_aggressive"]},
        "scenarios": t.scenarios.round(3).to_dict(orient="list"),
        "srilanka": {k: getattr(s, k) for k in ["sam_mode", "som_mode", "seats_mode", "sam_p10", "sam_p50", "sam_p90",
                                                 "som_p10", "som_p50", "som_p90"]},
        "tornado": s.tornado.round(0).to_dict(orient="records"),
        "zscaler": r,
        "scorecard": sc.round(3).reset_index(names="vendor").to_dict(orient="records"),
    }
    (OUT / "model_results.json").write_text(json.dumps(res, indent=2, default=float))
    docs_t1_t3.task1(t, s, est)
    docs_t1_t3.task2(r, fin)
    docs_t1_t3.task3(comp, sc)
    try:
        from . import docs_t4
        docs_t4.capstone(t, s, r, comp, sc, est)
        docs_t4.deck(t, s, r, comp, sc)
    except ImportError:
        pass
    publish_site()


def publish_site() -> None:
    """Copy deliverables and charts into docs/ for GitHub Pages."""
    import shutil

    from . import CHARTS, ROOT

    files = ROOT / "docs" / "files"
    assets = ROOT / "docs" / "assets"
    files.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    for f in list(OUT.glob("*.pdf")) + list(OUT.glob("*.xlsx")):
        shutil.copy2(f, files / f.name)
    for f in CHARTS.glob("*.png"):
        shutil.copy2(f, assets / f.name)
    from . import site

    site.write()


if __name__ == "__main__":
    main()
