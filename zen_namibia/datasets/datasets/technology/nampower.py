from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets.carrier.nampower import nampower_metadata


class NamPowerCapacities(Dataset[pd.DataFrame]):
    """NamPower installed plant capacities per year, 2019-2025 (MW)."""

    name = "nampower_capacities"

    def _set_metadata(self) -> MetaData:
        return nampower_metadata(self.name)

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "nampower" / "capacities.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        data["year"] = pd.to_numeric(data["year"], errors="raise").astype(int)
        if data["year"].duplicated().any():
            raise ValueError("capacities.csv has duplicate years")
        return data

    def capacities_in(self, year: int) -> pd.Series:
        """Return the row of capacities.csv for one year."""
        rows = self.data.loc[self.data.year == year]
        if rows.empty:
            raise ValueError(f"No capacity data for {year} in capacities.csv")
        return rows.iloc[0]

    def capacity_existing(self, column: str, year: int) -> float:
        """Return the installed capacity in MW of one capacity column in a year."""
        return float(self.capacities_in(year)[column])
