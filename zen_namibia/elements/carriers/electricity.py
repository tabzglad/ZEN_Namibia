from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier

from zen_namibia.datasets.dataset_collections.electricity_demand import ElectricityDemand
from zen_namibia.datasets.dataset_collections.electricity_trade import ElectricityTrade
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)


class Electricity(Carrier):
    """Electricity: demand in Namibia, imports and exports at the neighbours."""

    name: str = "electricity"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """Hourly electricity demand (PyPSA shape, NamPower totals, NIRP growth)."""
        return ElectricityDemand(self.source_path).get_demand(self)

    def _set_price_shed_demand(self) -> Attribute:
        """Unmet demand is allowed at the value of lost load, so shortages show
        up in the results instead of making the model infeasible."""
        return ZENNamibiaAssumptions(self.source_path).get_attribute(
            self, "price_shed_demand", "value_of_lost_load", unit=f"Euro/({self.power_unit}*h)")

    def _set_availability_import(self) -> Attribute:
        return ElectricityTrade(self.source_path).get_availability_import(self)

    def _set_availability_export(self) -> Attribute:
        return ElectricityTrade(self.source_path).get_availability_export(self)

    def _set_availability_export_yearly(self) -> Attribute:
        """(The zen-creator default of 0 blocks all exports.)"""
        return ElectricityTrade(self.source_path).get_availability_export_yearly(self)

    def _set_price_import(self) -> Attribute:
        return ElectricityTrade(self.source_path).get_price_import(self)

    def _set_price_export(self) -> Attribute:
        return ElectricityTrade(self.source_path).get_price_export(self)
