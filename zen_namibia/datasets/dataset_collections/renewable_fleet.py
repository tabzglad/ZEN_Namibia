from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.energy_system.manual_plant_locations import (
    ManualPlantLocations,
)
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
from zen_namibia.utils import capacity_existing_df, capacity_limit_df, capacity_lower_limit_df

# Technology in renewable_plants.csv of each element.
TECHNOLOGY = {"photovoltaics": "solar", "onshore_wind_turbine": "wind"}


class RenewableFleet(DatasetCollection):
    """Wind and solar per node: existing plants with capacity-weighted hourly
    profiles, committed projects, and unlimited new capacity after 2023 at the
    nodes that have a profile.

    Combines the hand-compiled plant list (with each plant's node), the
    Renewables.ninja profile of each plant, NamPower's separate Omburu PV unit
    (not in the plant list), NamPower's wind yield, and the committed projects.
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
            "manual_plant_locations": ManualPlantLocations(self.source_path),
        }

    def _plants(self, technology: str, year: int) -> pd.DataFrame:
        """Plants of a technology with node, capacity and profile file, including
        NamPower's Omburu PV unit for solar."""
        plants = self.data["manual_renewable_plants"].plants(technology)[
            ["plant", "node", "capacity_mw", "profile_file"]].copy()
        if technology == "solar":
            omburu = self.data["nampower_capacities"].capacities_in(year)
            if float(omburu["omburu_pv_mw"]) > 0:
                plants.loc[len(plants)] = [
                    "Omburu PV (NamPower)", self.data["manual_plant_locations"].node("omburu_pv"),
                    float(omburu["omburu_pv_mw"]), omburu["omburu_pv_profile_file"]]
        plants["capacity_mw"] = plants["capacity_mw"].astype(float)
        return plants

    def existing_by_node(self, technology: str, year: int) -> dict[str, float]:
        """Existing capacity per node in a year."""
        return self._plants(technology, year).groupby("node", sort=False)["capacity_mw"].sum().to_dict()

    def _existing(self, element: Element) -> tuple[str, dict[str, float]]:
        technology = TECHNOLOGY[element.name]
        return technology, self.existing_by_node(technology, element.config.system.reference_year)

    def profiles(self, element: Element) -> pd.DataFrame:
        """Hourly capacity factor per node: the capacity-weighted mean of the
        node's plant profiles. Wind at the node of NamPower's Rosh Pinah wind
        farm is scaled to its P50 yield (capped at 1), because the
        Renewables.ninja Ombepo profile gives about 51%."""
        technology = TECHNOLOGY[element.name]
        ninja = self.data["renewables_ninja"]
        plants = self._plants(technology, element.config.system.reference_year)
        if plants.empty or (plants["capacity_mw"] <= 0).any():
            raise ValueError(f"{technology} plants must be listed with positive capacities")
        columns = {}
        for node, rows in plants.groupby("node", sort=False):
            weighted = sum(row.capacity_mw * ninja.capacity_factor(row.profile_file)
                           for row in rows.itertuples()) / rows["capacity_mw"].sum()
            columns[node] = weighted
        if technology == "wind":
            node = self.data["manual_plant_locations"].node("rosh_pinah_wind")
            target = self.data["nampower_capacities"].performance("wind_capacity_factor")
            columns[node] = (columns[node] * target / float(columns[node].mean())).clip(upper=1.0)
        profiles = pd.DataFrame({n: p.to_numpy() for n, p in columns.items()},
                                index=pd.RangeIndex(STEPS_PER_YEAR, name="time"))
        if len(profiles) != STEPS_PER_YEAR:
            raise ValueError(f"{technology} profiles must contain 8,760 hourly values")
        return profiles

    def expandable_nodes(self, element: Element) -> list[str]:
        """New capacity only where an existing plant gives an hourly profile."""
        return list(self._existing(element)[1])

    def get_capacity_existing(self, element: Element) -> Attribute:
        """The listed renewable portfolio as existing capacity in the reference year."""
        technology, existing = self._existing(element)
        year = element.config.system.reference_year
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_existing_df(existing, year),
            source=cite(self, f"Existing {year} {technology} fleet per node: plants in "
                              "renewable_plants.csv at their node"
                              + (", plus NamPower's Omburu PV unit (capacities.csv)."
                                 if technology == "solar" else "."),
                        "manual_renewable_plants", "nampower_capacities", "manual_plant_locations"),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """The existing fleet in the reference year; unlimited later at the
        nodes with a profile."""
        technology, existing = self._existing(element)
        nodes = self.expandable_nodes(element)
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_limit_df(element, existing, expandable_nodes=nodes),
            source=cite(self, f"Existing {technology} fleet per node in the reference year "
                              "(calibrated 2023 run); unlimited in later years (assumption) at "
                              f"the nodes with an existing plant, and so an hourly profile: "
                              f"{', '.join(nodes)}; zero elsewhere.",
                        "manual_renewable_plants", "nampower_capacities", "manual_plant_locations"),
        )

    def get_capacity_lower_limit(self, element: Element) -> Attribute:
        """The existing fleet plus committed projects online by each later year."""
        _, existing = self._existing(element)
        projects = self.data["nampower_committed_projects"]
        outside = set(projects.nodes(element.name)).difference(self.expandable_nodes(element))
        if outside:
            raise ValueError(f"Committed {element.name} projects at nodes without a profile: {outside}")
        return element.capacity_lower_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_lower_limit_df(
                element, existing,
                lambda node, year: projects.committed_by(element.name, year, node=node),
                projects.nodes(element.name)),
            source=cite(self, "Existing fleet per node plus committed projects online by each "
                              f"year: {projects.describe(element.name)}."),
        )

    def get_max_load(self, element: Element) -> Attribute:
        technology = TECHNOLOGY[element.name]
        profiles = self.profiles(element)
        description = (f"Hourly 2023 Renewables.ninja power profiles of the {technology} plants "
                       "at each node, normalized by each profile's simulated capacity and "
                       "weighted by installed capacity")
        if technology == "wind":
            node = self.data["manual_plant_locations"].node("rosh_pinah_wind")
            target = self.data["nampower_capacities"].performance("wind_capacity_factor")
            description += (f"; at {node} scaled to a {target:.1%} annual capacity factor "
                            "(NamPower P50 yield of the Rosh Pinah wind farm)")
        return element.max_load.set_data(
            default_value=float(profiles.to_numpy().mean()), unit="1", df=profiles,
            source=cite(self, description + ".", "manual_renewable_plants", "renewables_ninja",
                        "nampower_capacities", "manual_plant_locations"),
        )
