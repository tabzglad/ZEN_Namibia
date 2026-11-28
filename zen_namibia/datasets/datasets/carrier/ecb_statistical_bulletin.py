from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData


class ECBDistributionSales(Dataset[pd.DataFrame]):
    """End-user electricity sales of each distribution licensee in 2022 (GWh),
    with the model node of its supply area."""

    name = "ecb_distribution_sales"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Electricity Supply Industry Statistical Bulletin 2022",
            author=["Electricity Control Board"],
            publication="Electricity Control Board, Namibia",
            publication_year=2024,
            url="https://www.ecb.org.na/wp-content/uploads/2024/02/ECB-Statistical-Bulletin-2022-draft-3.pdf",
            note=("Appendix Tables 6-8, pp. 42-43: domestic, commercial and large power user "
                  "sales per licensee; rows matched to licensees with Tables 3-5 and 9-11"),
        )

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "ecb" / "distribution_sales_2022.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path, keep_default_na=False)
        if not {"licensee", "node", "sales_gwh"}.issubset(data.columns):
            raise ValueError("distribution_sales_2022.csv needs licensee, node and sales_gwh")
        data["sales_gwh"] = pd.to_numeric(data["sales_gwh"], errors="raise")
        return data.set_index("licensee")
