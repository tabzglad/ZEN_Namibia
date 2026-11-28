from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData


class ManualLargeCustomers(Dataset[pd.DataFrame]):
    """Electricity use of NamPower's largest direct customers (mines), compiled
    per customer from their own reports (see the source column)."""

    name = "manual_large_customers"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Electricity use of Namibia's largest mines",
            author=["ZEN Namibia"],
            publication="ZEN Namibia, data/raw_data/02-carrier/manual_large_customers/large_customers.csv",
            publication_year=2026,
            note=("Compiled from Swakop Uranium (2024), Rossing (2023), Dundee Precious Metals "
                  "(2022) and pv magazine (2024); some values derived or estimated (basis column)"),
        )

    def _set_path(self) -> Path:
        return (self.source_path / "02-carrier" / "manual_large_customers"
                / "large_customers.csv")

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        if not {"customer", "node", "electricity_gwh"}.issubset(data.columns):
            raise ValueError("large_customers.csv needs customer, node and electricity_gwh")
        data["electricity_gwh"] = pd.to_numeric(data["electricity_gwh"], errors="raise")
        return data.set_index("customer")
