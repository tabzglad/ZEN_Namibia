from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class IRENARenewableCosts2023(ItemValues, Dataset[pd.DataFrame]):
    """Utility-scale PV O&M cost in 2023 (USD/kW/year)."""

    name = "irena_renewable_costs_2023"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Renewable Power Generation Costs in 2023",
            author=["IRENA"],
            publication="International Renewable Energy Agency, Abu Dhabi",
            publication_year=2024,
            url="https://www.irena.org/Publications/2024/Sep/Renewable-Power-Generation-Costs-in-2023",
            note="Average all-in O&M cost of utility-scale solar PV in 2023 (global survey), 2023 USD",
        )

    def _set_path(self) -> Path:
        return (self.source_path / "03-technology" / "irena"
                / "renewable_power_generation_costs_2023.csv")

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)
