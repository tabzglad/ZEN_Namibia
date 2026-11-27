"""Shared attribute setters of the imported fuels (coal, HFO, wood chips)."""
from __future__ import annotations

from math import inf
from typing import ClassVar

from zen_creator import Attribute, Carrier
from zen_creator.datasets.datasets.metadata import AssumptionInformation

from zen_namibia.datasets.dataset_collections.fuel_prices import FuelPrices


class ImportedFuel(Carrier):
    """A fuel bought at a fixed price without a volume limit."""

    name: str = "imported_fuel"
    # zen-creator adds the subpath of every class in the MRO to the output
    # folder; empty here so the fuels stay in set_carriers/<name>.
    subpath: ClassVar[str] = ""
    availability_note: str = "Assumption: the fuel can be bought without a volume limit."

    def _set_availability_import(self) -> Attribute:
        return self.availability_import.set_data(
            default_value=inf, unit=self.power_unit,
            source=AssumptionInformation(description=self.availability_note),
        )

    def _set_price_import(self) -> Attribute:
        return FuelPrices(self.source_path).get_price_import(self)
