"""Reader for the small ``item,value,unit,source`` tables in the raw data."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_item_table(path: Path, note_column: str = "source") -> pd.DataFrame:
    """Read a table of named values, indexed by item, with numeric values."""
    data = pd.read_csv(path)
    required = {"item", "value", "unit", note_column}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {', '.join(sorted(missing))}")
    if data["item"].duplicated().any():
        raise ValueError(f"{path.name} has duplicate items")
    data["value"] = pd.to_numeric(data["value"], errors="raise")
    if data["value"].isna().any():
        raise ValueError(f"{path.name} has blank values")
    return data.set_index("item")


class ItemValues:
    """Mixin for datasets whose data is an item table (see read_item_table)."""

    data: pd.DataFrame
    path: Path

    def value(self, item: str) -> float:
        if item not in self.data.index:
            raise KeyError(f"{item} is not in {self.path.name}")
        return float(self.data.loc[item, "value"])
