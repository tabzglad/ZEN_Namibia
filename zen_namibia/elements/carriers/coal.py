from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_namibia.elements.carriers._fuel import ImportedFuel


class Coal(ImportedFuel):
    """Coal for Van Eck, bought without a volume limit."""

    name: str = "coal"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)
