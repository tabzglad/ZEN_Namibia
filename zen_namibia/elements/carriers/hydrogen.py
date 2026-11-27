from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier

from zen_namibia.datasets.dataset_collections.hydrogen_demand import HydrogenDemand


class Hydrogen(Carrier):
    """Green hydrogen for export (as ammonia), produced in Namibia.

    Demand is Hyphen Phase 1, flat over the year, from its first production
    year. Hydrogen cannot be imported (zen-creator default), so it must come
    from Namibian electrolysers. Measured in MW of hydrogen (lower heating value).
    """

    name: str = "hydrogen"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        return HydrogenDemand(self.source_path).get_demand(self)
