"""Bottom-up sizing of the Sri Lankan SME SASE opportunity (SAM and SOM).

No published estimate exists for Sri Lanka, so the market is built from firm
counts, seats per firm, the share of firms that need SASE and a per-user price.
Each input is a triangular distribution (low, mode, high) from
``data/srilanka_sme_parameters.csv``. A Monte Carlo run turns those ranges into
P10 / P50 / P90 outcomes, and a one-at-a-time sweep shows which input matters most.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import DATA

SEED = 2026
DRAWS = 20_000


def load_parameters() -> pd.DataFrame:
    return pd.read_csv(DATA / "srilanka_sme_parameters.csv").set_index("parameter")


def sam_usd(p: dict) -> float | np.ndarray:
    """Serviceable market (USD/yr): firms x need x users x price, small + medium."""
    small = p["small_firms"] * p["firm_growth_factor"] * p["need_share"] * p["small_avg_users"]
    medium = p["medium_firms"] * p["firm_growth_factor"] * p["need_share"] * p["medium_avg_users"]
    return (small + medium) * p["price_user_year"]


def som_usd(p: dict) -> float | np.ndarray:
    return sam_usd(p) * p["som_share_y5"]


def seats(p: dict) -> float | np.ndarray:
    return p["firm_growth_factor"] * p["need_share"] * (
        p["small_firms"] * p["small_avg_users"] + p["medium_firms"] * p["medium_avg_users"]
    )


def point(params: pd.DataFrame, col: str = "mode") -> dict:
    return params[col].astype(float).to_dict()


def _draw(params: pd.DataFrame, rng: np.random.Generator, n: int) -> dict:
    out = {}
    for name, row in params.iterrows():
        lo, mo, hi = float(row.low), float(row["mode"]), float(row.high)
        out[name] = np.full(n, mo) if lo == hi else rng.triangular(lo, mo, hi, n)
    return out


@dataclass(frozen=True)
class SizingResult:
    sam_mode: float
    som_mode: float
    seats_mode: float
    sam_p10: float
    sam_p50: float
    sam_p90: float
    som_p10: float
    som_p50: float
    som_p90: float
    sam_draws: np.ndarray
    som_draws: np.ndarray
    tornado: pd.DataFrame  # SOM swing per input, sorted by impact


def run(params: pd.DataFrame | None = None, n: int = DRAWS, seed: int = SEED) -> SizingResult:
    params = load_parameters() if params is None else params
    rng = np.random.default_rng(seed)
    draws = _draw(params, rng, n)
    sam = sam_usd(draws)
    som = som_usd(draws)

    base = point(params)
    rows = []
    for name, row in params.iterrows():
        if row.low == row.high:
            continue
        lo = dict(base, **{name: float(row.low)})
        hi = dict(base, **{name: float(row.high)})
        rows.append({"parameter": name, "som_low": som_usd(lo), "som_high": som_usd(hi)})
    tornado = pd.DataFrame(rows)
    tornado["swing"] = (tornado.som_high - tornado.som_low).abs()
    tornado = tornado.sort_values("swing", ascending=False).reset_index(drop=True)

    q = lambda a, p: float(np.percentile(a, p))  # noqa: E731
    return SizingResult(
        sam_mode=float(sam_usd(base)),
        som_mode=float(som_usd(base)),
        seats_mode=float(seats(base)),
        sam_p10=q(sam, 10), sam_p50=q(sam, 50), sam_p90=q(sam, 90),
        som_p10=q(som, 10), som_p50=q(som, 50), som_p90=q(som, 90),
        sam_draws=sam, som_draws=som, tornado=tornado,
    )
