from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class IEAFutureOfHydrogen2019(ItemValues, Dataset[pd.DataFrame]):
    """2030 electrolyser efficiency (LHV) and fixed O&M share."""

    name = "iea_future_of_hydrogen_2019"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="The Future of Hydrogen: Seizing today's opportunities",
            author=["IEA"],
            publication="International Energy Agency, Paris",
            publication_year=2019,
            url="https://www.iea.org/reports/the-future-of-hydrogen",
            note="Assumptions annex",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "iea" / "future_of_hydrogen_2019.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)

    def get_conversion_factor(self, element: Element) -> Attribute:
        """Hydrogen out (LHV) per MWh of electricity in."""
        efficiency = self.value("electrolyser_efficiency")
        unit = f"{element.power_unit}h/{element.power_unit}h"
        return element.conversion_factor.set_data(
            default_value=[{"hydrogen": {"default_value": efficiency, "unit": unit}}],
            source=SourceInformation(
                description=f"2030 electrolyser efficiency of {efficiency:.0%} (LHV).",
                metadata=self.metadata,
            ),
        )
