from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_namibia.elements.carriers._fuel import ImportedFuel


class Biomass(ImportedFuel):
    """Encroacher-bush wood chips, bought in Namibia without a volume limit."""

    name: str = "biomass"

    availability_note = (
        "Assumption: no volume limit; ample resource: NamPower estimates that only 13% of the harvestable bush near Otjikoto would be used over 25 years."
    )

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)
