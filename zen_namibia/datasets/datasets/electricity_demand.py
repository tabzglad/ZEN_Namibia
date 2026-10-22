from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData, SourceInformation


class ElectricityDemand(Dataset[pd.DataFrame]):
    """Reads electricity demand from source_data/demand_electricity.csv.

    The raw CSV has one demand value (in MW) per node:

        node,demand_mw
        NAM,1.0

    get_demand() turns that into the "demand" Attribute that ZEN-garden expects:
    a value for every time step (here, there is only one time step per year).
    """

    name = "electricity_demand"

    def __init__(self, source_path: Path | str | None = None):
        super().__init__(source_path=source_path)

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Mock electricity demand for Namibia",
            author=["ZEN Namibia"],
            publication="ZEN Namibia",
            publication_year=2026,
        )

    def _set_path(self) -> Path:
        return self.source_path / "demand_electricity.csv"

    def _set_data(self) -> pd.DataFrame:
        return pd.read_csv(self.path, index_col="node")

    def get_demand(self, element: Element) -> Attribute:
        """Build the "demand" attribute of a carrier (e.g. electricity)."""
        demand_per_node = self.data["demand_mw"]

        # one row (time step 0), one column per node
        demand_time_series = demand_per_node.to_frame().T
        demand_time_series.index = pd.Index([0], name="time")

        attr = Attribute("demand", element=element)
        attr.set_data(
            default_value=0.0,
            unit=element.power_unit,
            df=demand_time_series,
            source=SourceInformation(
                description="Mock demand values, to be replaced with real data.",
                metadata=self.metadata,
            ),
        )
        return attr
