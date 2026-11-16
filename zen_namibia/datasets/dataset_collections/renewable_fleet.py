from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element
from zen_creator.utils.attribute import SourceInformation

from zen_namibia.datasets.datasets.technology.manual_renewable_plants import (
    ManualRenewablePlants,
)
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.renewables_ninja import (
    STEPS_PER_YEAR,
    RenewablesNinja,
)
from zen_namibia.utils import capacity_existing_df


class RenewableFleet(DatasetCollection):
    """Existing wind and solar fleet with capacity-weighted hourly profiles.

    Combines the hand-compiled plant list, the Renewables.ninja profile of
    each plant, and the separate Omburu PV unit reported by NamPower (which is
    not duplicated in the plant list).
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
                "Missing plant-level Renewables.ninja profiles: "
                + ", ".join(missing_profiles)
            )

    def _get_data(self) -> dict[str, Dataset[Any] | DatasetCollection]:
        return {
            "manual_renewable_plants": ManualRenewablePlants(self.source_path),
            "renewables_ninja": RenewablesNinja(self.source_path),
            "nampower_capacities": NamPowerCapacities(self.source_path),
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

    def get_capacity_limit(self, element: Element, technology: str) -> Attribute:
        """Cap total renewable capacity at the listed 2023 portfolio size."""
        return Attribute(
            "capacity_limit",
            default_value=self.existing_capacity_mw(
                technology, element.config.system.reference_year
            ),
            unit=element.power_unit,
            element=element,
            sources=[
                SourceInformation(
                    description=(
                        f"Total installed 2023 {technology} capacity from "
                        "renewable_plants.csv plus the Omburu PV unit in "
                        "NamPower's capacities.csv."
                    ),
                    metadata=self.metadata,
                )
            ],
        )

    def get_capacity_existing(self, element: Element, technology: str) -> Attribute:
        """Return the listed renewable portfolio as existing 2023 capacity."""
        reference_year = element.config.system.reference_year
        capacity = self.existing_capacity_mw(technology, reference_year)
        return Attribute(
            "capacity_existing",
            default_value=capacity,
            unit=element.power_unit,
            element=element,
            df=capacity_existing_df(capacity, reference_year),
            sources=[
                SourceInformation(
                    description=(
                        f"Existing 2023 {technology} fleet capacity from "
                        "renewable_plants.csv plus the Omburu PV unit in "
                        "NamPower's capacities.csv."
                    ),
                    metadata=self.metadata,
                )
            ],
        )

    def get_max_load(self, element: Element, technology: str) -> Attribute:
        """Capacity-weight hourly plant profiles into the technology's max_load."""
        ninja = self.data["renewables_ninja"]
        rows = self.data["manual_renewable_plants"].plants(technology)
        if rows.empty:
            raise ValueError(f"No 2023 plants are listed for technology {technology}")

        plant_capacities = rows["capacity_mw"].astype(float).tolist()
        plant_profiles = [
            ninja.capacity_factor(filename) for filename in rows["profile_file"]
        ]

        # Omburu PV's separate 20 MW unit is stored in NamPower's capacities.csv.
        if technology == "solar":
            omburu = self._omburu(element.config.system.reference_year)
            if float(omburu["omburu_pv_mw"]) > 0:
                plant_capacities.append(float(omburu["omburu_pv_mw"]))
                plant_profiles.append(
                    ninja.capacity_factor(omburu["omburu_pv_profile_file"])
                )

        total_capacity = sum(plant_capacities)
        if total_capacity <= 0:
            raise ValueError(f"Installed capacity for {technology} must be positive")
        weighted_profile = (
            sum(
                capacity * profile
                for capacity, profile in zip(
                    plant_capacities, plant_profiles, strict=True
                )
            )
            / total_capacity
        )
        if len(weighted_profile) != STEPS_PER_YEAR:
            raise ValueError(f"{technology} profile must contain 8,760 hourly values")
        profile = pd.DataFrame(
            {"NAM": weighted_profile.to_numpy()},
            index=pd.RangeIndex(STEPS_PER_YEAR, name="time"),
        )
        return Attribute(
            "max_load",
            default_value=float(weighted_profile.mean()),
            unit="1",
            element=element,
            df=profile,
            sources=[
                SourceInformation(
                    description=(
                        f"Hourly 2023 Renewables.ninja power profiles for the "
                        f"{technology} plants, normalized by each profile's "
                        "simulated capacity and weighted by installed capacity."
                    ),
                    metadata=self.metadata,
                )
            ],
        )
