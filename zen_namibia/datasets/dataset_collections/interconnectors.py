from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes
from zen_namibia.datasets.datasets.technology.manual_transmission import ManualTransmission
from zen_namibia.datasets.datasets.technology.sapp import SAPPTransferLimits, edge_name
from zen_namibia.utils import model_years


class Interconnectors(DatasetCollection):
    """Power lines between the model's nodes, one capacity per direction:

    - cross-border lines: SAPP transfer limits;
    - NamPower's internal corridors between the Namibian nodes: circuits times
      an assumed capacity per circuit by voltage. Lines commissioned after the
      reference year (Auas-Gerus 2024, second Auas-Kokerboom 2028) are added
      from that year on. Lines are not expandable beyond that.
    """

    name = "interconnectors"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)
        nodes = set(self.data["manual_nodes"].nodes())
        used = set(self.data["sapp_transfer_limits"].nodes()) | set(
            self.data["manual_transmission"].data[["node_from", "node_to"]].to_numpy().ravel())
        if used - nodes:
            raise ValueError(f"Lines use nodes not in nodes.csv: {sorted(used - nodes)}")

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "sapp_transfer_limits": SAPPTransferLimits(self.source_path),
            "manual_transmission": ManualTransmission(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "manual_nodes": ManualNodes(self.source_path),
        }

    def internal_capacities(self, year: int) -> pd.Series:
        """Capacity per directed internal edge in MW from the lines in service in a
        year; the same in both directions."""
        lines = self.data["manual_transmission"].lines_online(year)
        assumptions = self.data["assumptions"]
        capacity = {}
        for line in lines.itertuples():
            mw = line.circuits * assumptions.value(f"line_capacity_{line.voltage_kv}kv")
            for a, b in ((line.node_from, line.node_to), (line.node_to, line.node_from)):
                capacity[edge_name(a, b)] = capacity.get(edge_name(a, b), 0.0) + mw
        return pd.Series(capacity, dtype=float)

    def capacities(self, year: int) -> pd.Series:
        """Capacity per directed edge in a year, cross-border and internal."""
        sapp = self.data["sapp_transfer_limits"].edge_capacities()
        return pd.concat([sapp, self.internal_capacities(year)]).rename_axis("edge")

    def _edges(self, element: Element) -> pd.Index:
        """All edges that have capacity in any optimized year."""
        last = max(model_years(element))
        return self.capacities(last).index

    def get_set_edges(self, element: Element) -> Attribute:
        """One directed edge per direction of each line."""
        edges = self._edges(element)
        return element.set_edges.set_data(
            df=pd.DataFrame([edge.split("-") for edge in edges],
                            columns=["node_from", "node_to"], index=edges),
            source=cite(self, "One directed edge per direction of each SAPP interconnector "
                              "and each NamPower corridor between the Namibian nodes.",
                        "sapp_transfer_limits", "manual_transmission"),
        )

    def _per_year(self, element: Element, name: str, years: list[int]) -> pd.DataFrame:
        edges = self._edges(element)
        rows = {(edge, year): self.capacities(year).get(edge, 0.0)
                for edge in edges for year in years}
        return pd.DataFrame(
            {name: list(rows.values())},
            index=pd.MultiIndex.from_tuples(list(rows), names=["edge", "year"]),
        )

    def _description(self, what: str) -> str:
        return (f"{what}: SAPP transfer limit per direction for the cross-border lines; for "
                "NamPower's internal corridors, the circuits in service times an assumed capacity "
                "per circuit by voltage (surge impedance loading).")

    def get_capacity_existing(self, element: Element) -> Attribute:
        reference_year = element.config.system.reference_year
        capacities = self.capacities(reference_year)
        capacities = capacities[capacities > 0]
        df = pd.DataFrame(
            {"capacity_existing": capacities.to_numpy()},
            index=pd.MultiIndex.from_tuples(
                [(edge, reference_year) for edge in capacities.index],
                names=["edge", "year_construction"]),
        )
        return element.capacity_existing.set_data(
            default_value=0.0, unit=element.power_unit, df=df,
            source=cite(self, self._description(f"Lines in service in {reference_year}")),
        )

    def get_capacity_limit(self, element: Element) -> Attribute:
        """Each edge is capped at the lines in service in each year (not expandable)."""
        return element.capacity_limit.set_data(
            default_value=0.0, unit=element.power_unit,
            df=self._per_year(element, "capacity_limit", model_years(element)),
            source=cite(self, self._description(
                "Lines in service in each year, not expandable beyond them")),
        )

    def get_capacity_lower_limit(self, element: Element) -> Attribute:
        """Lines commissioned after the reference year are built by the year they are in service."""
        later = [y for y in model_years(element) if y > element.config.system.reference_year]
        attr = element.capacity_lower_limit
        if not later:
            return attr
        return attr.set_data(
            default_value=0.0, unit=element.power_unit,
            df=self._per_year(element, "capacity_lower_limit", later),
            source=cite(self, self._description(
                "Lines in service in each later year must be built, including those "
                "commissioned after the reference year")),
        )

    def get_distance(self, element: Element) -> Attribute:
        """Straight-line distance between the node coordinates. Only informative:
        transport losses and line costs are zero."""
        edges = self._edges(element)
        nodes = self.data["manual_nodes"]
        return element.distance.set_data(
            default_value=0.0, unit="km",
            df=pd.DataFrame({"distance": [nodes.distance_km(*e.split("-")) for e in edges]},
                            index=edges),
            source=cite(self, "Great-circle distance between the coordinates of the two "
                              "nodes (informative only: no line losses or costs).",
                        "manual_nodes"),
        )
