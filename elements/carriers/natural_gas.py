from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier

# MOCK DATA: up to 1 MW of natural gas can be imported at every hour of the year.
# TODO: replace with the real gas supply limit once available.
AVAILABILITY_IMPORT = 1.0


class NaturalGas(Carrier):
    """All data and assumptions for the natural gas carrier."""

    name: str = "natural_gas"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        """Set the maximum natural gas import (same value for every time step)."""
        return Attribute(
            "availability_import",
            default_value=AVAILABILITY_IMPORT,
            unit=self.power_unit,
            element=self,
        )
