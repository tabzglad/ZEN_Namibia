from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class HyphenHydrogen(ItemValues, Dataset[pd.DataFrame]):
    """Hyphen Hydrogen Energy Phase 1: annual hydrogen output and first year."""

    name = "hyphen_hydrogen"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Hyphen Hydrogen Energy project updates (Tsau Khaeb, near Luderitz)",
            author=["Engineering News", "Windhoek Express"],
            publication="Engineering News (Sep 2026); Windhoek Express (Dec 2025)",
            publication_year=2026,
        )

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "hyphen" / "hydrogen_project.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path)

    def demand_tonnes(self) -> float:
        return self.value("hydrogen_demand")

    def first_year(self) -> int:
        return int(self.value("hydrogen_first_year"))
