from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, DatasetCollection

from zen_namibia.datasets.datasets.financial.bank_of_namibia import BankOfNamibia
from zen_namibia.datasets.datasets.financial.ecb import ECBExchangeRates

# All costs in the model are in euros of this year.
PRICE_YEAR = 2023


class MonetaryConversion(DatasetCollection):
    """Converts N$ and USD to euros of the price year, and scales N$ prices
    between years with the Namibian CPI."""

    name = "monetary_conversion"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset]:
        return {
            "bank_of_namibia": BankOfNamibia(self.source_path),
            "ecb": ECBExchangeRates(self.source_path),
        }

    def nad_per_eur(self, year: int = PRICE_YEAR) -> float:
        return self.data["bank_of_namibia"].nad_per_eur(year)

    def nad_to_euro(self, nad: float, year: int = PRICE_YEAR) -> float:
        """N$ to euros at the year's average N$/EUR rate."""
        return nad / self.nad_per_eur(year)

    def usd_to_euro(self, usd: float, year: int = PRICE_YEAR) -> float:
        """USD to euros at the year's average ECB USD/EUR rate."""
        return usd / self.data["ecb"].usd_per_eur(year)

    def cpi_factor(self, from_year: int, to_year: int = PRICE_YEAR) -> float:
        """Namibian CPI ratio, to scale N$ prices from one year to another."""
        bank = self.data["bank_of_namibia"]
        return bank.cpi(to_year) / bank.cpi(from_year)

    def monthly_usd_per_eur(self, year: int) -> pd.Series:
        return self.data["ecb"].monthly_usd_per_eur(year)
