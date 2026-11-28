from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.carrier.hyphen import HyphenHydrogen
from zen_namibia.datasets.datasets.carrier.pypsa import STEPS_PER_YEAR
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes
from zen_namibia.utils import model_years


class HydrogenDemand(DatasetCollection):
    """Green hydrogen demand: Hyphen Phase 1 output, flat over the year, in MW (LHV),
    at the node of Hyphen's plant."""

    name = "hydrogen_demand"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "hyphen": HyphenHydrogen(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "manual_nodes": ManualNodes(self.source_path),
        }

    def first_year(self) -> int:
        return self.data["hyphen"].first_year()

    def demand_mw(self) -> float:
        """Flat hydrogen demand in MW (LHV) from the annual tonnes."""
        lhv = self.data["assumptions"].value("hydrogen_lhv")  # kWh/kg = MWh/t
        return self.data["hyphen"].demand_tonnes() * lhv / 8760.0

    def get_demand(self, element: Element) -> Attribute:
        years = model_years(element)
        first_year = self.first_year()
        hyphen = self.data["hyphen"]
        node = self.data["manual_nodes"].hydrogen_node()
        return element.demand.set_data(
            default_value=0.0,
            unit=element.power_unit,
            df=pd.DataFrame(
                {node: np.full(STEPS_PER_YEAR, self.demand_mw())},
                index=pd.RangeIndex(STEPS_PER_YEAR, name="time"),
            ),
            yearly_variations_df=pd.DataFrame(
                {node: [1.0 if year >= first_year else 0.0 for year in years]},
                index=pd.Index(years, name="year"),
            ),
            source=cite(
                self,
                f"Hyphen Phase 1 green hydrogen output ({hyphen.demand_tonnes():,.0f} t/yr) "
                f"times the lower heating value, flat over the year at {node} (Hyphen's plant), "
                f"from {first_year}.",
            ),
        )
