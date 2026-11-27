from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.utils import DOMESTIC_NODE

EARTH_RADIUS_KM = 6371.0
ROLES = {"domestic", "sapp_market", "contract"}


class ManualNodes(Dataset[pd.DataFrame]):
    """The model's nodes: Namibia and the neighbours it trades with.

    Namibia holds the demand and the plants; the neighbours only supply imports
    and take exports. The ``role`` column says how each node trades, and the
    coordinates (capital cities) are used only for line distances.
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
            note="Coordinates of the capital cities",
        )

    def _set_path(self) -> Path:
        return self.source_path / "01-energy_system" / "manual_nodes" / "nodes.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path, keep_default_na=False)
        required = {"node", "lon", "lat", "role"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError(f"nodes.csv is missing columns: {', '.join(sorted(missing))}")
        if data["node"].duplicated().any():
            raise ValueError("nodes.csv has duplicate nodes")
        if not set(data["role"]).issubset(ROLES):
            raise ValueError(f"nodes.csv role must be one of {sorted(ROLES)}")
        for role in ("domestic", "sapp_market"):
            if (data["role"] == role).sum() != 1:
                raise ValueError(f"nodes.csv needs exactly one {role} node")
        if data.loc[data["role"] == "domestic", "node"].iloc[0] != DOMESTIC_NODE:
            raise ValueError(f"The domestic node in nodes.csv must be {DOMESTIC_NODE}")
        for column in ("lon", "lat"):
            data[column] = pd.to_numeric(data[column], errors="raise")
        return data.set_index("node")

    def nodes(self) -> pd.Index:
        return self.data.index

    def node_with_role(self, role: str) -> str:
        return str(self.data.index[self.data["role"] == role][0])

    def domestic_node(self) -> str:
        return self.node_with_role("domestic")

    def sapp_market_node(self) -> str:
        """Node where Namibia trades at the SAPP market price (SAPP market and Eskom)."""
        return self.node_with_role("sapp_market")

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
                description="Namibia and the neighbours it trades with, at their capital cities.",
                metadata=self.metadata,
            ),
        )
