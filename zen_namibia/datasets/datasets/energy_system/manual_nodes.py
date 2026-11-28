from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import AssumptionInformation, SourceInformation

from zen_namibia.utils import capacity_limit_df

EARTH_RADIUS_KM = 6371.0
ROLES = {"domestic", "sapp_market", "contract"}


class ManualNodes(Dataset[pd.DataFrame]):
    """The model's nodes: four Namibian regions and the neighbours Namibia trades with.

    The Namibian nodes hold the demand and the plants; the neighbours only
    supply imports and take exports. ``role`` says how each node trades,
    ``hydrogen`` marks the node of Hyphen's hydrogen plant, and the
    coordinates (a main town of each region) are used only for line distances.
    Note: "NA" is avoided as a node name because pandas reads it as missing data.
    """

    name = "manual_nodes"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="ZEN Namibia nodes",
            author=["ZEN Namibia"],
            publication="ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv",
            publication_year=2026,
            note="Namibian nodes group the administrative regions; coordinates of a main town",
        )

    def _set_path(self) -> Path:
        return self.source_path / "01-energy_system" / "manual_nodes" / "nodes.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path, keep_default_na=False)
        required = {"node", "lon", "lat", "role", "hydrogen"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError(f"nodes.csv is missing columns: {', '.join(sorted(missing))}")
        if data["node"].duplicated().any() or data["node"].str.contains("-").any():
            raise ValueError("nodes.csv needs unique node names without '-'")
        if not set(data["role"]).issubset(ROLES):
            raise ValueError(f"nodes.csv role must be one of {sorted(ROLES)}")
        if (data["role"] == "sapp_market").sum() != 1 or (data["role"] == "domestic").sum() < 1:
            raise ValueError("nodes.csv needs one sapp_market node and at least one domestic node")
        data["hydrogen"] = data["hydrogen"].str.strip().str.lower() == "yes"
        if data["hydrogen"].sum() != 1 or data.loc[data["hydrogen"], "role"].iloc[0] != "domestic":
            raise ValueError("nodes.csv needs exactly one domestic hydrogen node")
        for column in ("lon", "lat"):
            data[column] = pd.to_numeric(data[column], errors="raise")
        return data.set_index("node")

    def nodes(self) -> pd.Index:
        return self.data.index

    def domestic_nodes(self) -> list[str]:
        """The Namibian nodes."""
        return list(self.data.index[self.data["role"] == "domestic"])

    def sapp_market_node(self) -> str:
        """Node where Namibia trades at the SAPP market price (SAPP market and Eskom)."""
        return str(self.data.index[self.data["role"] == "sapp_market"][0])

    def hydrogen_node(self) -> str:
        """Node of Hyphen's hydrogen plant and export port."""
        return str(self.data.index[self.data["hydrogen"]][0])

    def distance_km(self, node_from: str, node_to: str) -> float:
        """Great-circle distance between two node coordinates."""
        lon1, lat1, lon2, lat2 = np.radians([
            self.data.lon[node_from], self.data.lat[node_from],
            self.data.lon[node_to], self.data.lat[node_to],
        ])
        a = (np.sin((lat2 - lat1) / 2) ** 2
             + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
        return float(2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(a)))

    def get_set_nodes(self, element: Element) -> Attribute:
        return element.set_nodes.set_data(
            df=self.data[["lon", "lat"]],
            source=SourceInformation(
                description="Four Namibian regions (North, Central, Coast, South) and the "
                            "neighbours Namibia trades with.",
                metadata=self.metadata,
            ),
        )

    def get_new_technology_capacity_limit(
        self, element: Element, hydrogen_only: bool = False, energy: bool = False,
    ) -> Attribute:
        """Capacity limit of a technology Namibia did not have in the reference
        year: none in that year; unlimited later at every Namibian node, or only
        at the hydrogen node; never at the neighbouring nodes."""
        name = "capacity_limit_energy" if energy else "capacity_limit"
        nodes = [self.hydrogen_node()] if hydrogen_only else self.domestic_nodes()
        where = (f"only at {nodes[0]}, the node of Hyphen's hydrogen plant" if hydrogen_only
                 else "at every Namibian node")
        return getattr(element, name).set_data(
            default_value=0.0,
            unit=f"{element.power_unit}*h" if energy else element.power_unit,
            df=capacity_limit_df(element, {}, expandable_nodes=nodes, name=name),
            source=AssumptionInformation(
                description=(
                    "Assumption: not built in the reference year (the calibrated 2023 fleet); "
                    f"unlimited in later years {where}; not allowed at the neighbouring nodes."
                ),
                metadata=self.metadata,
            ),
        )
