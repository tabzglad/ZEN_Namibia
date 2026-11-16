from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier
from math import inf

class Diesel(Carrier):
    """Diesel fuel carrier (fuel is available infinitely)."""

    name: str = "diesel"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_availability_import(self) -> Attribute:
        return Attribute("availability_import", default_value=inf, unit=self.power_unit, element=self)

