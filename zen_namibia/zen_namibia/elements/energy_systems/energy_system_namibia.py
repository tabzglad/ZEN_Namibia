from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

import pandas as pd
from zen_creator import Attribute, EnergySystem

# The single node of this model: Namibia, identified by its coordinates.
# Note: "NA" is avoided as a node name because pandas reads it as "missing data".
NODES = pd.DataFrame(
    {"lon": [17.0658], "lat": [-22.5609]},
    index=pd.Index(["NAM"], name="node"),
)

# No transport technologies yet, so there are no connections (edges) between nodes.
EDGES = pd.DataFrame(columns=["node_from", "node_to"], index=pd.Index([], name="edge"))


class EnergySystemNamibia(EnergySystem):
    """Energy system for Namibia, currently modeled with a single node."""

    name: str = "energy_system_namibia"

    def __init__(self, model: Model):
        super().__init__(model=model)

    def _set_set_nodes(self) -> Attribute:
        return Attribute("set_nodes", default_value=None, df=NODES, element=self)

    def _set_set_edges(self) -> Attribute:
        return Attribute("set_edges", default_value=None, df=EDGES, element=self)
