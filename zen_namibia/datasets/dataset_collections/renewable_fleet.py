from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.technology.manual_renewable_plants import (
    ManualRenewablePlants,
)
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.nampower_projects import (
    NamPowerCommittedProjects,
)
from zen_namibia.datasets.datasets.technology.renewables_ninja import (
    STEPS_PER_YEAR,
    RenewablesNinja,
)
from zen_namibia.utils import (
    DOMESTIC_NODE,
    capacity_existing_df,
    capacity_limit_df,
    capacity_lower_limit_df,
)

# Technology in renewable_plants.csv of each element.
TECHNOLOGY = {"photovoltaics": "solar", "onshore_wind_turbine": "wind"}


class RenewableFleet(DatasetCollection):
    """Wind and solar fleet: existing plants with capacity-weighted hourly
    profiles, committed projects, and unlimited new capacity after 2023.

    Combines the hand-compiled plant list, the Renewables.ninja profile of
    each plant, the separate Omburu PV unit reported by NamPower (not in the
    plant list), NamPower's wind yield, and the committed projects.
    """

    name = "renewable_fleet"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)
        ninja = self.data["renewables_ninja"]
        missing_profiles = [
            filename
            for filename in self.data["manual_renewable_plants"].data["profile_file"]
            if filename not in ninja.data
        ]
        if missing_profiles:
            raise FileNotFoundError(
                "Missing plant-level Renewables.ninja profiles: " + ", ".join(missing_profiles)
            )

    def _get_data(self) -> dict[str, Dataset[Any] | DatasetCollection]:
        return {
            "manual_renewable_plants": ManualRenewablePlants(self.source_path),
            "renewables_ninja": RenewablesNinja(self.source_path),
            "nampower_capacities": NamPowerCapacities(self.source_path),
            "nampower_committed_projects": NamPowerCommittedProjects(self.source_path),
        }

    def _omburu(self, year: int) -> pd.Series:
        """Return NamPower's capacity row with the Omburu PV unit for a year."""
        return self.data["nampower_capacities"].capacities_in(year)

    def existing_capacity_mw(self, technology: str, year: int) -> float:
        """Return the existing wind or solar fleet capacity in a year."""
        capacity = self.data["manual_renewable_plants"].capacity_mw(technology)
        if technology == "solar":
            capacity += float(self._omburu(year)["omburu_pv_mw"])
        return capacity

    def _existing(self, element: Element) -> tuple[str, float]:
        technology = TECHNOLOGY[element.name]
        return technology, self.existing_capacity_mw(
            technology, element.config.system.reference_year)

    def get_capacity_existing(self, element: Element) -> Attribute:
        """The listed renewable portfolio as existing capacity in the reference year."""
        technology, capacity = self._existing(element)
        year = element.config.system.reference_year
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_existing_df(capacity, year),
            source=cite(self, f"Existing {year} {technology} fleet: renewable_plants.csv"
                              + (" plus the Omburu PV unit in NamPower's capacities.csv."
                                 if technology == "solar" else "."),
                        "manual_renewable_plants", "nampower_capacities"),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """The existing fleet in the reference year; unlimited in Namibia later."""
        technology, capacity = self._existing(element)
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_limit_df(element, capacity, expandable=True),
            source=cite(self, f"Existing {technology} fleet in the reference year (calibrated "
                              "2023 run); unlimited in Namibia in later years (assumption); "
                              "zero at the neighbouring nodes.",
                        "manual_renewable_plants", "nampower_capacities"),
        )

    def get_capacity_lower_limit(self, element: Element) -> Attribute:
        """The existing fleet plus committed projects online by each later year."""
        _, capacity = self._existing(element)
        projects = self.data["nampower_committed_projects"]
        return element.capacity_lower_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_lower_limit_df(
                element, capacity, lambda year: projects.committed_by(element.name, year)),
            source=cite(self, "Existing fleet plus committed projects online by each year: "
                              f"{projects.describe(element.name)}."),
        )

    def get_max_load(self, element: Element) -> Attribute:
        """Capacity-weighted hourly plant profiles. Wind is scaled to NamPower's
        P50 yield for the Rosh Pinah wind farm (capped at 1), because the
        Renewables.ninja Ombepo profile gives about 51%."""
        technology = TECHNOLOGY[element.name]
        ninja = self.data["renewables_ninja"]
        rows = self.data["manual_renewable_plants"].plants(technology)
        if rows.empty:
            raise ValueError(f"No 2023 plants are listed for technology {technology}")

        plant_capacities = rows["capacity_mw"].astype(float).tolist()
        plant_profiles = [ninja.capacity_factor(filename) for filename in rows["profile_file"]]

        # Omburu PV's separate 20 MW unit is stored in NamPower's capacities.csv.
        if technology == "solar":
            omburu = self._omburu(element.config.system.reference_year)
            if float(omburu["omburu_pv_mw"]) > 0:
                plant_capacities.append(float(omburu["omburu_pv_mw"]))
                plant_profiles.append(ninja.capacity_factor(omburu["omburu_pv_profile_file"]))

        total_capacity = sum(plant_capacities)
        if total_capacity <= 0:
            raise ValueError(f"Installed capacity for {technology} must be positive")
        weighted_profile = sum(
            capacity * profile
            for capacity, profile in zip(plant_capacities, plant_profiles, strict=True)
        ) / total_capacity
        description = (f"Hourly 2023 Renewables.ninja power profiles of the {technology} plants, "
                       "normalized by each profile's simulated capacity and weighted by "
                       "installed capacity")
        if technology == "wind":
            target = self.data["nampower_capacities"].performance("wind_capacity_factor")
            weighted_profile = (
                weighted_profile * target / float(weighted_profile.mean())).clip(upper=1.0)
            description += (f", scaled to a {target:.1%} annual capacity factor (NamPower P50 "
                            "yield of the Rosh Pinah wind farm)")
        if len(weighted_profile) != STEPS_PER_YEAR:
            raise ValueError(f"{technology} profile must contain 8,760 hourly values")
        return element.max_load.set_data(
            default_value=float(weighted_profile.mean()), unit="1",
            df=pd.DataFrame({DOMESTIC_NODE: weighted_profile.to_numpy()},
                            index=pd.RangeIndex(STEPS_PER_YEAR, name="time")),
            source=cite(self, description + ".", "manual_renewable_plants", "renewables_ninja",
                        "nampower_capacities"),
        )
