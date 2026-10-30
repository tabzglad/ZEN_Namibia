from __future__ import annotations

from pathlib import Path

import pandas as pd


class NamibiaBaseline:
    """Load the split annual Namibia baseline source tables."""

    def __init__(self, source_path: Path | str):
        source = Path(source_path)
        tables = [
            pd.read_csv(source / "capacities.csv"),
            pd.read_csv(source / "imports.csv"),
            pd.read_csv(source / "demands.csv"),
        ]
        self.data = tables[0].merge(tables[1], on="year", validate="one_to_one").merge(
            tables[2], on="year", validate="one_to_one"
        )
        self.data["year"] = pd.to_numeric(self.data["year"], errors="raise").astype(int)

    def capacity_existing(self, column: str) -> float:
        base_year = self.data["year"].min()
        return float(self.data.loc[self.data.year == base_year, column].iloc[0])
