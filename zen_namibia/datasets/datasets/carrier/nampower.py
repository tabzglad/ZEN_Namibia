"""NamPower annual reports: demand, trade and prices (02-carrier/nampower/)."""
from __future__ import annotations

from math import inf
from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table
from zen_namibia.utils import model_years

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
        publication="NamPower Integrated Annual Reports",
        publication_year=2025,
        note="compiled in the ZEN Namibia baseline workbook",
    )


class NamPowerPrices(ItemValues, Dataset[pd.DataFrame]):
    """Average electricity import and export prices and the Van Eck coal price (N$)."""

    name = "nampower_prices"

    def _set_metadata(self) -> MetaData:
        return nampower_metadata(self.name)

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "nampower" / "prices.csv"

    def _set_data(self) -> pd.DataFrame:
        data = read_item_table(self.path)
        if (data["value"] <= 0).any():
            raise ValueError("prices.csv has non-positive values")
        return data


class NamPowerTrade(Dataset[pd.DataFrame]):
    """NamPower's annual imports and exports (imports_exports.csv)."""

    name = "nampower_trade"

    def _set_metadata(self) -> MetaData:
        return nampower_metadata(self.name)

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "nampower" / "imports_exports.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        if not {"year", "exports_gwh"}.issubset(data.columns):
            raise ValueError("imports_exports.csv needs year and exports_gwh columns")
        return data.set_index("year")

    def latest_exports_gwh(self) -> tuple[int, float]:
        """Exports in the latest reported year."""
        year = int(self.data.index.max())
        return year, float(self.data.loc[year, "exports_gwh"])

    def get_availability_export_yearly(self, element: Element, node: str) -> Attribute:
        """Annual exports at the export node: unbounded in the reference year
        (calibrated 2023 run); in later years capped at NamPower's latest
        reported exports, so that new capacity is built for Namibia and
        hydrogen, not for sales into SAPP at a fixed price."""
        year_reported, exports_gwh = self.latest_exports_gwh()
        reference_year = element.config.system.reference_year
        years = model_years(element)
        df = pd.DataFrame(
            {"availability_export_yearly": [
                inf if year == reference_year else exports_gwh * 1000.0 for year in years
            ]},
            index=pd.MultiIndex.from_tuples([(node, y) for y in years], names=["node", "year"]),
        )
        return element.availability_export_yearly.set_data(
            default_value=inf, unit=f"{element.power_unit}*h", df=df,
            source=SourceInformation(
                description=(
                    f"Exports at {node} unbounded in {reference_year}; in later years capped at "
                    f"NamPower's {year_reported} exports ({exports_gwh:,.0f} GWh)."
                ),
                metadata=self.metadata,
            ),
        )


class NamPowerDemand(Dataset[pd.DataFrame]):
    """NamPower annual electricity demand 2019-2025."""

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
