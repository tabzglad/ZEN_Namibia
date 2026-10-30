from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData, SourceInformation


class ElectricityDemand(Dataset[pd.DataFrame]):
    """Read annual electricity demand from source_data/demands.csv.

    Expected columns are year,node,demand_mw. One row is required for each
    year and node. The first year's values form the default profile; the
    remaining annual profiles are written as ZEN-garden year overrides.
    """

    name = "electricity_demand"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Electricity demand for Namibia",
            author=["ZEN Namibia"],
            publication="ZEN Namibia",
            publication_year=2026,
        )

    def _set_path(self) -> Path:
        return self.source_path / "demands.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        required = {"year", "average_demand_mw"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError(
                "demands.csv must include year and average_demand_mw; "
                f"missing: {', '.join(sorted(missing))}"
            )

        data = data[["year", "average_demand_mw"]].copy()
        data["node"] = "NAM"
        data = data.rename(columns={"average_demand_mw": "demand_mw"})
        data["year"] = pd.to_numeric(data["year"], errors="raise").astype(int)
        data["demand_mw"] = pd.to_numeric(data["demand_mw"], errors="raise")
        if data[["year", "node", "demand_mw"]].isna().any().any():
            raise ValueError("demands.csv contains blank values")
        if data.duplicated(["year", "node"]).any():
            raise ValueError("demands.csv has duplicate year,node rows")
        if (data["demand_mw"] < 0).any():
            raise ValueError("demand_mw values must be non-negative")

        by_year = data.pivot(index="year", columns="node", values="demand_mw")
        if by_year.isna().any().any():
            raise ValueError("Each year must have a demand value for every node")
        return data

    def _demand_by_year(self) -> pd.DataFrame:
        return self.data.pivot(index="year", columns="node", values="demand_mw")

    def get_demand(self, element: Element) -> Attribute:
        """Build the default demand profile from the first input year."""
        demand_by_year = self._demand_by_year()
        first_year = demand_by_year.index.min()
        demand_time_series = demand_by_year.loc[[first_year]].copy()
        demand_time_series.index = pd.Index([0], name="time")

        attr = Attribute("demand", element=element)
        attr.set_data(
            default_value=0.0,
            unit=element.power_unit,
            df=demand_time_series,
            source=SourceInformation(
                description=f"Demand profile for base year {first_year}.",
                metadata=self.metadata,
            ),
        )
        return attr

    def get_year_specific_demand(self) -> dict[int, pd.DataFrame]:
        """Return one time-step demand table for each input year."""
        demand_by_year = self._demand_by_year()
        result = {}
        for year, values in demand_by_year.iterrows():
            table = values.to_frame().T
            table.index = pd.Index([0], name="time")
            result[int(year)] = table
        return result
