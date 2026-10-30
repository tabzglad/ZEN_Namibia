from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier


class Diesel(Carrier):
    """Diesel fuel carrier (fuel availability is an uncalibrated placeholder)."""

    name: str = "diesel"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        return Attribute("availability_import", default_value=1.0e6, unit=self.power_unit, element=self)

    def _set_availability_import_yearly(self) -> Attribute:
        """Use a deliberately high annual cap until fuel-supply data is sourced."""
        return Attribute(
            "availability_import_yearly", default_value=1.0e12,
            unit=f"{self.power_unit}*h", element=self,
        )
