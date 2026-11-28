from __future__ import annotations

from pathlib import Path

from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.energy_system.manual_plant_locations import (
    ManualPlantLocations,
)
from zen_namibia.datasets.datasets.technology.nampower import (
    PLANT_COLUMNS,
    PLANTS,
    NamPowerCapacities,
)
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022
from zen_namibia.utils import capacity_existing_df, capacity_limit_df


class ThermalFleet(DatasetCollection):
    """NamPower's existing non-expandable plants (Van Eck, Anixas I, Ruacana):
    installed capacity at their node and the share of it they can deliver."""

    name = "thermal_fleet"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "nampower_capacities": NamPowerCapacities(self.source_path),
            "nirp_2022": NIRP2022(self.source_path),
            "manual_plant_locations": ManualPlantLocations(self.source_path),
        }

    def _capacity_by_node(self, element: Element) -> dict[str, float]:
        node = self.data["manual_plant_locations"].node(PLANTS[element.name])
        return {node: self.data["nampower_capacities"].plant_capacity(element)}

    def get_capacity_existing(self, element: Element) -> Attribute:
        year = element.config.system.reference_year
        (node, mw), = self._capacity_by_node(element).items()
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_existing_df({node: mw}, year),
            source=cite(self, f"Installed capacity in {year} ({PLANT_COLUMNS[element.name]} in "
                              f"capacities.csv, {mw:g} MW) at {node}, as one vintage built in "
                              f"{year}.", "nampower_capacities", "manual_plant_locations"),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """No new capacity: capped at the existing plant at its node, zero elsewhere."""
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=capacity_limit_df(element, self._capacity_by_node(element)),
            source=cite(self, "Capped at the installed capacity in every year (not "
                              "expandable); zero at all other nodes.",
                        "nampower_capacities", "manual_plant_locations"),
        )

    def get_max_load(self, element: Element) -> Attribute:
        capacities = self.data["nampower_capacities"]
        if element.name == "coal_steam_turbine":
            return capacities.get_max_load_van_eck(element)
        if element.name != "anixas_i":
            raise KeyError(f"No availability for {element.name}")
        nameplate = capacities.plant_capacity(element)
        net = self.data["nirp_2022"].value("anixas_net_capacity")
        if nameplate <= 0 or net > nameplate:
            raise ValueError("Anixas I net capacity must be positive and no greater than nameplate")
        return element.max_load.set_data(
            default_value=net / nameplate, unit="1",
            source=cite(self, f"Anixas I net output in the NIRP 2022 ({net:g} MW) / NamPower "
                              f"installed capacity ({nameplate:g} MW).",
                        "nampower_capacities", "nirp_2022"),
        )
