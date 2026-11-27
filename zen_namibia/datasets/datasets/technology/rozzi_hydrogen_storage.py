from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class RozziHydrogenStorage(ItemValues, Dataset[pd.DataFrame]):
    """Hydrogen compressor capex per kW of electrical input (EUR2024)."""

    name = "rozzi_hydrogen_storage"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Techno-economic dataset for hydrogen storage-based microgrids",
            author=["Rozzi, E.", "Minuto, F. D.", "Lanzini, A."],
            publication="Data in Brief 56, 110795",
            publication_year=2024,
            doi="10.1016/j.dib.2024.110795",
            note="Reference cost of the compressor cost function, Table 4 (units inferred from Table 3)",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "rozzi_2024" / "compressor_costs.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)
