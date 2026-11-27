from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class IEAGlobalHydrogenReview2024(ItemValues, Dataset[pd.DataFrame]):
    """2030 installed cost of electrolysers (USD/kW)."""

    name = "iea_global_hydrogen_review_2024"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Global Hydrogen Review 2024",
            author=["IEA"],
            publication="International Energy Agency, Paris",
            publication_year=2024,
            url="https://www.iea.org/reports/global-hydrogen-review-2024",
            note="Stated Policies 2030 installed cost of non-Chinese electrolysers, as reported by Argus Media (Oct 2024)",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "iea" / "global_hydrogen_review_2024.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)
