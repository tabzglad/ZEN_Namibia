from __future__ import annotations

from pathlib import Path

from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022


class ThermalAvailability(DatasetCollection):
    """Share of nameplate capacity the existing thermal plants can deliver."""

    name = "thermal_availability"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "nampower_capacities": NamPowerCapacities(self.source_path),
            "nirp_2022": NIRP2022(self.source_path),
        }

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
                              f"installed capacity ({nameplate:g} MW)."),
        )
