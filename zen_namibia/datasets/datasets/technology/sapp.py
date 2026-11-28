from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

LIMIT_COLUMNS = [
    "interconnector",
    "node_from",
    "node_to",
    "voltage_kv",
    "number_of_lines",
    "applicable_transfer_limit_mw",
    "model_limit_mw",
]


def edge_name(node_from: str, node_to: str) -> str:
    """ZEN-garden names a directed edge `<node_from>-<node_to>`."""
    return f"{node_from}-{node_to}"


class SAPPTransferLimits(Dataset[pd.DataFrame]):
    """SAPP transfer limits of the cross-border lines in the model (MW)."""

    name = "sapp_transfer_limits"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="SAPP interconnector transfer limits",
            author=["Southern African Power Pool"],
            publication="SAPP Transfer Limits table (sapp.co.zw/transfer-limits)",
            publication_year=2023,
            url="https://www.sapp.co.zw/transfer-limits",
            note="Table is undated; applicable limit = lowest of thermal, voltage and stability limits",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "sapp" / "interconnectors.csv"

    def _set_data(self) -> pd.DataFrame:
        """Return the interconnectors in the model (`in_model` = yes).

        Rows with `in_model` = no (planned or distribution-level links) are
        documented in the file but create no nodes or lines.
        """
        raw = pd.read_csv(self.path)
        missing = set(LIMIT_COLUMNS + ["in_model"]).difference(raw.columns)
        if missing:
            raise ValueError(
                "interconnectors.csv is missing columns: " + ", ".join(sorted(missing))
            )
        if raw["interconnector"].duplicated().any():
            raise ValueError("interconnectors.csv has duplicate interconnectors")
        flags = raw["in_model"].str.strip().str.lower()
        if not flags.isin(["yes", "no"]).all():
            raise ValueError("interconnectors.csv in_model must be yes or no")
        data = raw.loc[flags == "yes"].copy()
        for column in ["applicable_transfer_limit_mw", "model_limit_mw"]:
            data[column] = pd.to_numeric(data[column], errors="raise")
        if data[LIMIT_COLUMNS].isna().any().any():
            raise ValueError("interconnectors.csv has blank values in a modeled interconnector")
        if (data[["applicable_transfer_limit_mw", "model_limit_mw"]] <= 0).any().any():
            raise ValueError("interconnectors.csv has non-positive transfer limits")
        if (data["node_from"] == data["node_to"]).any():
            raise ValueError("interconnectors.csv has a line starting and ending at the same node")
        return data

    def edge_capacities(self) -> pd.Series:
        """Model transfer limit per directed edge in MW, summing parallel lines.

        Uses `model_limit_mw`, which equals the SAPP applicable limit unless
        the source column documents a reason to differ.

        SAPP lists each line in one direction only (into Namibia, and Zambia to
        Zimbabwe for Kariba). The same limit is assumed for the reverse
        direction unless that direction is listed.
        """
        listed = self.data.groupby(["node_from", "node_to"])[
            "model_limit_mw"
        ].sum()
        capacities = {
            edge_name(node_from, node_to): limit
            for (node_from, node_to), limit in listed.items()
        }
        for (node_from, node_to), limit in listed.items():
            capacities.setdefault(edge_name(node_to, node_from), limit)
        return pd.Series(capacities, name="capacity_mw").rename_axis("edge").sort_index()

    def nodes(self) -> list[str]:
        """All nodes joined by an interconnector."""
        return sorted(set(self.data["node_from"]) | set(self.data["node_to"]))

