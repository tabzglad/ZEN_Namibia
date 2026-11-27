from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class NamPowerOtjikoto(ItemValues, Dataset[pd.DataFrame]):
    """Otjikoto biomass plant: efficiency, wood-chip energy content and price."""

    name = "nampower_otjikoto"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Otjikoto Biomass Power Station project fact sheet",
            author=["NamPower"],
            publication="NamPower",
            publication_year=2024,
            note="May 2024; 40 MW plant fuelled with encroacher-bush wood chips",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "nampower_otjikoto" / "fact_sheet.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)

    def wood_chip_mwh_per_tonne(self) -> float:
        return self.value("biomass_energy_content") / 3.6

    def get_conversion_factor(self, element: Element) -> Attribute:
        efficiency = self.value("biomass_efficiency")
        unit = f"{element.power_unit}h/{element.power_unit}h"
        return element.conversion_factor.set_data(
            default_value=[{"biomass": {"default_value": 1.0 / efficiency, "unit": unit}}],
            source=SourceInformation(
                description=f"Fuel per MWh of electricity: 1 / {efficiency:.0%} efficiency "
                            "(300,000 MWh per year from 245,000 t of wood chips at 14.7 GJ/t).",
                metadata=self.metadata,
            ),
        )
