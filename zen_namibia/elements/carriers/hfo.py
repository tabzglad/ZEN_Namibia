from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_namibia.elements.carriers._fuel import ImportedFuel


class HFO(ImportedFuel):
    """Heavy fuel oil for Anixas I and new engines (estimated 2023 delivered price)."""

    name: str = "hfo"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)
