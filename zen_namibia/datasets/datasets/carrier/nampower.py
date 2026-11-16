from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

DEMAND_COLUMNS = [
    "year",
    "average_demand_mw",
    "energy_consumption_gwh",
    "peak_demand_mw",
]


def nampower_metadata(name: str) -> MetaData:
    """Return the citation shared by all NamPower datasets."""
    return MetaData(
        name=name,
        title="NamPower annual reports and statistics 2019-2025",
        author=["NamPower"],
        publication="NamPower Annual Reports",
        publication_year=2025,
        note="compiled in the ZEN Namibia baseline workbook",
    )


class NamPowerDemand(Dataset[pd.DataFrame]):
    """NamPower annual electricity demand 2019-2025.

    The files are in ``02-carrier/nampower/``. ``imports_exports.csv`` is kept
    there as well but is not used by the model at the moment.
    """

    name = "nampower_demand"

    def _set_metadata(self) -> MetaData:
        return nampower_metadata(self.name)

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "nampower" / "demand.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        missing = set(DEMAND_COLUMNS).difference(data.columns)
        if missing:
            raise ValueError(
                "demand.csv must include year, average_demand_mw, "
                "energy_consumption_gwh, and peak_demand_mw; "
                f"missing: {', '.join(sorted(missing))}"
            )
        data = data[DEMAND_COLUMNS].copy()
        data["node"] = "NAM"
        data = data.rename(columns={"average_demand_mw": "demand_mw"})
        data["year"] = pd.to_numeric(data["year"], errors="raise").astype(int)
        for column in ["demand_mw", "energy_consumption_gwh", "peak_demand_mw"]:
            data[column] = pd.to_numeric(data[column], errors="raise")
        if data.isna().any().any():
            raise ValueError("demand.csv contains blank values")
        if data.duplicated(["year", "node"]).any():
            raise ValueError("demand.csv has duplicate year,node rows")
        if (data["demand_mw"] < 0).any():
            raise ValueError("demand_mw values must be non-negative")
        return data

    def demand_in(self, year: int) -> pd.Series:
        """Return the row of demand.csv for one year."""
        rows = self.data.loc[self.data.year == year]
        if rows.empty:
            raise ValueError(f"No demand data for {year} in demand.csv")
        return rows.iloc[0]
