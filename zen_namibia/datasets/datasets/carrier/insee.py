from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class INSEEFuelPrices(ItemValues, Dataset[pd.DataFrame]):
    """Heavy fuel oil market price, NW Europe 380 cst FOB (EUR/t), 2020 and 2023."""

    name = "insee_fuel_prices"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Heavy fuel oil, NW Europe, 380 cst 3.5% S, cargo FOB",
            author=["INSEE"],
            publication="INSEE, series 010751333",
            publication_year=2024,
            url="https://www.insee.fr/en/statistiques/serie/010751333",
            note="Annual averages of the 12 monthly values",
        )

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "insee" / "hfo_prices.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)

    def hfo_fob_eur_per_tonne(self, year: int) -> float:
        return self.value(f"hfo_fob_nwe_{year}")
