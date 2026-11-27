from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData


class ECBExchangeRates(Dataset[dict[str, pd.Series]]):
    """ECB euro reference rates, USD per EUR: annual (2020, 2023) and monthly 2023."""

    name = "ecb_exchange_rates"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Euro foreign exchange reference rates, US dollar",
            author=["European Central Bank"],
            publication="ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A",
            publication_year=2024,
            url="https://data.ecb.europa.eu/data/datasets/EXR",
        )

    def _set_path(self) -> Path:
        return self.source_path / "04-monetary" / "ecb"

    def _set_data(self) -> dict[str, pd.Series]:
        annual = pd.read_csv(self.path / "usd_per_eur_annual.csv")
        monthly = pd.read_csv(self.path / "usd_per_eur_monthly.csv")
        annual = pd.to_numeric(annual.set_index("year")["usd_per_eur"], errors="raise")
        monthly = pd.to_numeric(monthly.set_index("month")["usd_per_eur"], errors="raise")
        monthly.index = pd.PeriodIndex(monthly.index, freq="M")
        for name, series in (("annual", annual), ("monthly", monthly)):
            if series.isna().any() or (series <= 0).any():
                raise ValueError(f"usd_per_eur_{name}.csv has blank or non-positive rates")
        return {"annual": annual, "monthly": monthly.sort_index()}

    def usd_per_eur(self, year: int) -> float:
        return float(self.data["annual"].loc[year])

    def monthly_usd_per_eur(self, year: int) -> pd.Series:
        monthly = self.data["monthly"]
        monthly = monthly.loc[monthly.index.year == year]
        if len(monthly) != 12:
            raise ValueError(f"usd_per_eur_monthly.csv needs 12 months for {year}")
        return monthly
