from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class USDOEHydrogenStorage(ItemValues, Dataset[pd.DataFrame]):
    """Capital cost target of stationary compressed hydrogen storage (USD/kg)."""

    name = "us_doe_hydrogen_storage"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Hydrogen Delivery Technical Targets",
            author=["US Department of Energy"],
            publication="DOE Hydrogen and Fuel Cell Technologies Office, Multi-Year Program Plan",
            publication_year=2020,
            url="https://www.energy.gov/eere/fuelcells/doe-technical-targets-hydrogen-delivery",
            note="Stationary gaseous storage, 160 bar, FY2020 purchased capital cost target",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "us_doe" / "hydrogen_storage_targets.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)
