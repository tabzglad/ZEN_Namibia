from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes
from zen_namibia.datasets.datasets.technology.sapp import SAPPTransferLimits


class Interconnectors(DatasetCollection):
    """Cross-border edges (SAPP interconnectors) between the model's nodes."""

    name = "interconnectors"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)
        unknown = set(self.data["sapp_transfer_limits"].nodes()).difference(
            self.data["manual_nodes"].nodes())
        if unknown:
            raise ValueError(f"interconnectors.csv uses nodes not in nodes.csv: {sorted(unknown)}")

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "sapp_transfer_limits": SAPPTransferLimits(self.source_path),
            "manual_nodes": ManualNodes(self.source_path),
        }

    def _edges(self) -> pd.Index:
        return self.data["sapp_transfer_limits"].edge_capacities().index

    def get_set_edges(self, element: Element) -> Attribute:
        """One directed edge per interconnector direction."""
        edges = self._edges()
        return element.set_edges.set_data(
            df=pd.DataFrame([edge.split("-") for edge in edges],
                            columns=["node_from", "node_to"], index=edges),
            source=cite(self, "One directed edge per direction of each SAPP interconnector "
                              "in the model.", "sapp_transfer_limits"),
        )

    def get_distance(self, element: Element) -> Attribute:
        """Straight-line distance between the node coordinates. Only informative:
        transport losses and line costs are zero."""
        edges = self._edges()
        nodes = self.data["manual_nodes"]
        return element.distance.set_data(
            default_value=0.0, unit="km",
            df=pd.DataFrame({"distance": [nodes.distance_km(*e.split("-")) for e in edges]},
                            index=edges),
            source=cite(self, "Great-circle distance between the capital cities of the two "
                              "nodes (informative only: no line losses or costs)."),
        )
