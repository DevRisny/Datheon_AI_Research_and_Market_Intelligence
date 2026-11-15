"""Edge Shift: research toolkit for the SASE market and the Sri Lankan SME opportunity.

Every number the reports use is computed here from the CSVs in ``data/``,
so the PDFs, the Excel matrix and the charts can be rebuilt with one command.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"

__all__ = ["ROOT", "DATA", "OUT", "CHARTS"]
