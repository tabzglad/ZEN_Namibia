from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table

GJ_PER_MWH = 3.6


class NIRP2022(ItemValues, Dataset[pd.DataFrame]):
    """Plant parameters and costs from Namibia's NIRP Review and Update (2022).

    Van Eck and Anixas heat rates, Anixas net capacity, fixed and variable
    O&M of Van Eck, Anixas and Ruacana (N$, 2020-2021 data), and the 2020
    delivered HFO price.
    """

    name = "nirp_2022"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="National Integrated Resource Plan (NIRP) Review and Update 2022 for the Electricity Supply Industry",
            author=["Ministry of Mines and Energy, Namibia"],
            publication="Ministry of Mines and Energy, Namibia",
            publication_year=2022,
            url="https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf",
            note="Costs based on 2020-2021 data, in N$",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "nirp" / "nirp_2022.csv"

    def _set_data(self) -> pd.DataFrame:
        data = read_item_table(self.path)
        if (data["value"] <= 0).any():
            raise ValueError("nirp_2022.csv has non-positive values")
        return data

    def fuel_per_electricity(self, plant: str) -> float:
        """MWh of fuel per MWh of electricity: full-load heat rate / 3.6 GJ/MWh."""
        return self.value(f"{plant}_heat_rate") / GJ_PER_MWH

    def coal_mwh_per_tonne(self) -> float:
        """Energy content of Van Eck's coal: heat rate / coal use per MWh."""
        return self.fuel_per_electricity("van_eck") / (self.value("van_eck_coal_use") / 1000.0)

    def get_conversion_factor(self, element: Element, plant: str, fuel: str,
                              description: str = "") -> Attribute:
        """Fuel per MWh of electricity from a plant's full-load heat rate."""
        heat_rate = self.value(f"{plant}_heat_rate")
        unit = f"{element.power_unit}h/{element.power_unit}h"
        return element.conversion_factor.set_data(
            default_value=[{fuel: {"default_value": self.fuel_per_electricity(plant), "unit": unit}}],
            source=SourceInformation(
                description=(
                    f"Full-load heat rate of {plant.replace('_', ' ').title()} "
                    f"({heat_rate:g} GJ/MWh) / 3.6 GJ/MWh{description}."
                ),
                metadata=self.metadata,
            ),
        )
