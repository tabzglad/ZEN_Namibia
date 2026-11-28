from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData


class ManualPlantLocations(Dataset[pd.DataFrame]):
    """Node of each existing NamPower plant (the plant lists of renewable IPPs
    and committed projects carry their own node column)."""

    name = "manual_plant_locations"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Location of NamPower's power stations",
            author=["ZEN Namibia"],
            publication="ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv",
            publication_year=2026,
        )

    def _set_path(self) -> Path:
        return self.source_path / "01-energy_system" / "manual_nodes" / "plant_locations.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        if not {"plant", "node"}.issubset(data.columns) or data["plant"].duplicated().any():
            raise ValueError("plant_locations.csv needs unique plants with a node")
        return data.set_index("plant")

    def node(self, plant: str) -> str:
        if plant not in self.data.index:
            raise KeyError(f"{plant} is not in plant_locations.csv")
        return str(self.data.loc[plant, "node"])
