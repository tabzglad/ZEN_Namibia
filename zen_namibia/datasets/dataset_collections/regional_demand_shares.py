from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, DatasetCollection

from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.carrier.ecb_statistical_bulletin import ECBDistributionSales
from zen_namibia.datasets.datasets.carrier.manual_large_customers import ManualLargeCustomers
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes


class RegionalDemandShares(DatasetCollection):
    """Share of Namibia's electricity demand at each Namibian node.

    End-user sales of the distributors (ECB 2022) plus the largest direct mine
    customers, by node. NamPower Distribution's sales have no region and are
    split between Central and South by assumption. About 85% of NamPower's
    sales are covered; the rest (distribution losses and direct customers
    without published use, e.g. Rosh Pinah, Namdeb, NamWater) is assumed to
    follow the same split, so the South share is probably a lower bound.
    """

    name = "regional_demand_shares"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "ecb_distribution_sales": ECBDistributionSales(self.source_path),
            "manual_large_customers": ManualLargeCustomers(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "manual_nodes": ManualNodes(self.source_path),
        }

    def energy_by_node(self) -> pd.Series:
        """Covered annual electricity use per Namibian node (GWh)."""
        sales = self.data["ecb_distribution_sales"].data
        customers = self.data["manual_large_customers"].data
        unassigned = sales.loc[sales["node"] == "", "sales_gwh"].sum()
        central = self.data["assumptions"].value("nampower_distribution_central_share")
        energy = (sales.loc[sales["node"] != ""].groupby("node")["sales_gwh"].sum()
                  .add(customers.groupby("node")["electricity_gwh"].sum(), fill_value=0.0))
        energy = energy.add(pd.Series({"NAM_CENTRAL": central * unassigned,
                                       "NAM_SOUTH": (1 - central) * unassigned}), fill_value=0.0)
        nodes = self.data["manual_nodes"].domestic_nodes()
        unknown = set(energy.index).difference(nodes)
        if unknown:
            raise ValueError(f"Demand assigned to nodes that are not Namibian nodes: {unknown}")
        return energy.reindex(nodes, fill_value=0.0)

    def shares(self) -> pd.Series:
        energy = self.energy_by_node()
        return energy / energy.sum()
