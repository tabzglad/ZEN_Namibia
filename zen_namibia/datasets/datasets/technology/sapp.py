from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

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

    def get_capacity_existing(self, element: Element) -> Attribute:
        """Existing transfer capacity per directed edge, built in the reference year."""
        reference_year = element.config.system.reference_year
        capacities = self.edge_capacities()
        df = pd.DataFrame(
            {"capacity_existing": capacities.to_numpy()},
            index=pd.MultiIndex.from_tuples(
                [(edge, reference_year) for edge in capacities.index],
                names=["edge", "year_construction"],
            ),
        )
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit, df=df,
            source=SourceInformation(
                description=(
                    "SAPP applicable transfer limit per direction (model_limit_mw in "
                    "interconnectors.csv; parallel lines summed; the listed direction is "
                    "assumed for the reverse direction too)."
                ),
                metadata=self.metadata,
            ),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """No new line capacity: each edge is capped at its existing limit."""
        capacities = self.edge_capacities()
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=pd.DataFrame({"capacity_limit": capacities.to_numpy()}, index=capacities.index),
            source=SourceInformation(
                description="Lines are not expandable: each edge is capped at its transfer limit.",
                metadata=self.metadata,
            ),
        )
