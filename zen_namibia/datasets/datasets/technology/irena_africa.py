from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class IRENAAfricaPlanning2021(ItemValues, Dataset[pd.DataFrame]):
    """Onshore wind fixed O&M for Africa (USD/kW/year, 2020 USD)."""

    name = "irena_africa_planning_2021"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Planning and Prospects for Renewable Power: Africa",
            author=["IRENA"],
            publication="International Renewable Energy Agency, Abu Dhabi",
            publication_year=2021,
            url="https://www.irena.org/publications/2021/March/Planning-and-prospects-for-renewable-power-Africa",
            note="As used in the TMP (2023) least-cost study for Namibia, Table 2",
        )

    def _set_path(self) -> Path:
        return (self.source_path / "03-technology" / "irena"
                / "planning_and_prospects_africa_2021.csv")

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)
