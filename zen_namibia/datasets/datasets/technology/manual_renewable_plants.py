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
]


class ManualRenewablePlants(Dataset[pd.DataFrame]):
    """Hand-compiled list of Namibia's 2023 wind and solar plants.

    Each row gives a plant's installed capacity and the name of its
    Renewables.ninja profile. The capacity factors are calculated from those
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
            note="source of the plant capacities still to be documented",
        )

    def _set_path(self) -> Path:
        return (
            self.source_path / "03-technology" / "manual_renewable_plants"
            / "renewable_plants.csv"
        )

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        missing = set(PLANT_COLUMNS).difference(data.columns)
        if missing:
            raise ValueError(
                f"renewable_plants.csv is missing columns: {', '.join(sorted(missing))}"
            )
        data = data[PLANT_COLUMNS].copy()
        data["capacity_mw"] = pd.to_numeric(
            data["capacity_mw"], errors="raise"
        )
        data["capacity_factor_2023_percent"] = pd.to_numeric(
            data["capacity_factor_2023_percent"], errors="raise"
        )
        if data.isna().any().any() or data["plant"].duplicated().any():
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
