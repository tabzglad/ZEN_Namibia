from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

PLANT_COLUMNS = [
    "technology",
    "plant",
    "capacity_mw",
    "capacity_factor_2023_percent",
    "profile_file",
    "node",
]


class ManualRenewablePlants(Dataset[pd.DataFrame]):
    """Hand-compiled list of Namibia's 2023 wind and solar plants.

    Each row gives a plant's installed capacity, its model node (from its
    coordinates and administrative region) and the name of its Renewables.ninja profile. The capacity factors are calculated from those
    profiles.
    """

    name = "manual_renewable_plants"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Namibia wind and solar plants in operation in 2023",
            author=["ZEN Namibia"],
            publication="ZEN Namibia",
            publication_year=2026,
            note=(
                "2023 operating-plant roster compiled from the project list; "
                "profile files are from Renewables.ninja"
            ),
        )

    def _set_path(self) -> Path:
        return (
            self.source_path / "03-technology" / "manual_renewable_plants"
            / "renewable_plants.csv"
        )

    def _set_data(self) -> pd.DataFrame:
        raw = pd.read_csv(self.path)
        missing = set(PLANT_COLUMNS).difference(raw.columns)
        if missing:
            raise ValueError(
                f"renewable_plants.csv is missing columns: {', '.join(sorted(missing))}"
            )
        data = raw[PLANT_COLUMNS].copy()
        if "project_category" in raw.columns:
            data["project_category"] = raw["project_category"].fillna("")
        data["capacity_mw"] = pd.to_numeric(
            data["capacity_mw"], errors="raise"
        )
        data["capacity_factor_2023_percent"] = pd.to_numeric(
            data["capacity_factor_2023_percent"], errors="raise"
        )
        if data[PLANT_COLUMNS].isna().any().any() or data["plant"].duplicated().any():
            raise ValueError(
                "renewable_plants.csv has blank values or duplicate plant names"
            )
        if (data["capacity_mw"] < 0).any() or not data[
            "capacity_factor_2023_percent"
        ].between(0, 100).all():
            raise ValueError(
                "Plant capacities must be non-negative and capacity factors "
                "must be percentages from 0 to 100"
            )
        if not set(data["technology"]).issubset({"wind", "solar"}):
            raise ValueError("technology must be wind or solar")
        return data

    def plants(self, technology: str) -> pd.DataFrame:
        """Return the plants listed for ``wind`` or ``solar``."""
        return self.data.loc[self.data.technology == technology]

    def capacity_mw(self, technology: str) -> float:
        """Sum the plant capacities listed for ``wind`` or ``solar``."""
        return float(self.plants(technology)["capacity_mw"].sum())
