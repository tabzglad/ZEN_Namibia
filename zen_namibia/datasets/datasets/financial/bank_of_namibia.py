from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class BankOfNamibia(ItemValues, Dataset[pd.DataFrame]):
    """N$/EUR exchange rates (2020, 2023) and all-items CPI (2020, 2023)."""

    name = "bank_of_namibia"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Quarterly Bulletin: foreign exchange rates and consumer price index",
            author=["Bank of Namibia"],
            publication="Bank of Namibia Quarterly Bulletin (December 2024, March 2026)",
            publication_year=2026,
            url="https://www.bon.com.na",
            note=(
                "Annual averages computed from the monthly period averages; "
                "2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; "
                "CPI from the March 2026 bulletin"
            ),
        )

    def _set_path(self) -> Path:
        return self.source_path / "04-monetary" / "bank_of_namibia" / "bank_of_namibia.csv"

    def _set_data(self) -> pd.DataFrame:
        data = read_item_table(self.path)
        if (data["value"] <= 0).any():
            raise ValueError("bank_of_namibia.csv has non-positive values")
        return data

    def nad_per_eur(self, year: int) -> float:
        return self.value(f"nad_per_eur_{year}")

    def cpi(self, year: int) -> float:
        return self.value(f"cpi_{year}")
