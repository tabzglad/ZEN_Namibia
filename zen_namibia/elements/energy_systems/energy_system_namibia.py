from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, EnergySystem

from zen_namibia.datasets.dataset_collections.interconnectors import Interconnectors
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes


class EnergySystemNamibia(EnergySystem):
    """Namibia with its South African, Zambian and Zimbabwean neighbours.

    Namibia holds the demand and the domestic fleet; the neighbours only supply
    imports and take exports at the boundary prices, via the cross-border lines.
    """

    name: str = "energy_system_namibia"

    def __init__(self, model: Model):
        super().__init__(model=model)

    def _set_discount_rate(self) -> Attribute:
        """8% real; NamPower does not disclose its WACC."""
        return ZENNamibiaAssumptions(self.source_path).get_attribute(
            self, "discount_rate", "discount_rate", unit="1")

    def _set_set_nodes(self) -> Attribute:
        return ManualNodes(self.source_path).get_set_nodes(self)

    def _set_set_edges(self) -> Attribute:
        return Interconnectors(self.source_path).get_set_edges(self)
