"""NamPower annual reports: plant capacities and performance (03-technology/nampower/)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.datasets.datasets._item_table import read_item_table
from zen_namibia.datasets.datasets.carrier.nampower import nampower_metadata
from zen_namibia.utils import capacity_existing_df, capacity_limit_df

# Installed-capacity column of capacities.csv for each existing plant.
PLANT_COLUMNS = {
    "coal_steam_turbine": "van_eck_thermal_mw",
    "anixas_i": "anixas_i_mw",
    "hydro_turbine": "ruacana_hydro_mw",
}


class NamPowerCapacities(Dataset[dict[str, pd.DataFrame]]):
    """NamPower installed plant capacities per year, 2019-2025 (MW), and plant
    performance figures (wind yield, Ruacana generation)."""

    name = "nampower_capacities"

    def _set_metadata(self) -> MetaData:
        return nampower_metadata(self.name)

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "nampower"

    def _set_data(self) -> dict[str, pd.DataFrame]:
        capacities = pd.read_csv(self.path / "capacities.csv")
        capacities["year"] = pd.to_numeric(capacities["year"], errors="raise").astype(int)
        if capacities["year"].duplicated().any():
            raise ValueError("capacities.csv has duplicate years")
        return {
            "capacities": capacities,
            "performance": read_item_table(self.path / "plant_performance.csv"),
        }

    def capacities_in(self, year: int) -> pd.Series:
        """Return the row of capacities.csv for one year."""
        data = self.data["capacities"]
        rows = data.loc[data.year == year]
        if rows.empty:
            raise ValueError(f"No capacity data for {year} in capacities.csv")
        return rows.iloc[0]

    def capacity(self, column: str, year: int) -> float:
        """Installed capacity in MW of one capacity column in a year."""
        return float(self.capacities_in(year)[column])

    def plant_capacity(self, element: Element) -> float:
        """Installed capacity of an existing plant in the reference year."""
        return self.capacity(PLANT_COLUMNS[element.name], element.config.system.reference_year)

    def performance(self, item: str) -> float:
        return float(self.data["performance"].loc[item, "value"])

    def get_capacity_existing(self, element: Element) -> Attribute:
        year = element.config.system.reference_year
        column = PLANT_COLUMNS[element.name]
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_existing_df(self.plant_capacity(element), year),
            source=SourceInformation(
                description=f"Installed capacity in {year} ({column} in capacities.csv), "
                            f"as one vintage built in {year}.",
                metadata=self.metadata,
            ),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """No new capacity: capped at the existing plant in Namibia, zero elsewhere."""
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_limit_df(element, self.plant_capacity(element), expandable=False),
            source=SourceInformation(
                description="Capped at the installed capacity in the reference year in every "
                            "year (not expandable); zero at the neighbouring nodes.",
                metadata=self.metadata,
            ),
        )

    def get_max_load_van_eck(self, element: Element) -> Attribute:
        """Limit Van Eck to its available capacity reported for the reference year."""
        year = element.config.system.reference_year
        nameplate = self.capacity("van_eck_thermal_mw", year)
        available = self.capacity("van_eck_available_capacity_mw", year)
        if nameplate <= 0 or available < 0 or available > nameplate:
            raise ValueError("Van Eck available capacity must be between zero and nameplate")
        return element.max_load.set_data(
            default_value=available / nameplate, unit="1",
            source=SourceInformation(
                description=f"Van Eck available capacity / nameplate in {year} "
                            f"({available:g} MW / {nameplate:g} MW).",
                metadata=self.metadata,
            ),
        )
