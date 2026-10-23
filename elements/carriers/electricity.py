from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier

from zen_namibia.datasets.datasets.electricity_demand import ElectricityDemand

# MOCK DATA: up to 1 MW can be imported at every hour of the year.
# TODO: replace with the real grid import limit once available.
AVAILABILITY_IMPORT = 1.0


class Electricity(Carrier):
    """All data and assumptions for the electricity carrier."""

    name: str = "electricity"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """Set the electricity demand, loaded from source_data/demand_electricity.csv."""
        return ElectricityDemand(self.source_path).get_demand(self)

    def _set_availability_import(self) -> Attribute:
        """Set the maximum electricity import (same value for every time step)."""
        return Attribute(
            "availability_import",
            default_value=AVAILABILITY_IMPORT,
            unit=self.power_unit,
            element=self,
        )
