from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.renewables_ninja import (
    STEPS_PER_YEAR,
    RenewablesNinja,
)
from zen_namibia.utils import DOMESTIC_NODE


class HydroAvailability(DatasetCollection):
    """Monthly availability of Ruacana from smoothed rainfall near the plant.

    Rainfall is only a seasonal proxy for river flow. The profile is scaled
    so its annual upper-bound energy equals NamPower's reported Ruacana
    generation (FY2022/23, used as a calendar-2023 value).
    """

    name = "hydro_availability"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "renewables_ninja": RenewablesNinja(self.source_path),
            "nampower_capacities": NamPowerCapacities(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
        }

    def monthly_max_load(self, reference_year: int) -> tuple[np.ndarray, pd.Series]:
        """Max load of each month (12 values) and the month of every hour."""
        assumptions = self.data["assumptions"]
        weather = self.data["renewables_ninja"].hydro_precipitation()
        rainfall = weather["prectotland"]
        months = weather["time"].dt.month

        monthly_rainfall = rainfall.groupby(months).sum().reindex(range(1, 13), fill_value=0.0)
        # A centred rolling mean represents runoff lag and basin storage.
        window = int(assumptions.value("hydro_runoff_window"))
        runoff_index = monthly_rainfall.rolling(window=window, center=True, min_periods=1).mean()
        if float(runoff_index.sum()) <= 0:
            raise ValueError("Hydro weather contains no precipitation to form availability")
        # Year-round base flow: the river carries upstream flow when local rainfall is zero.
        runoff_index = runoff_index + assumptions.value("hydro_base_flow_share") * float(
            monthly_rainfall.mean())

        month_hours = months.value_counts().reindex(range(1, 13), fill_value=0).sort_index()
        capacities = self.data["nampower_capacities"]
        target_gwh = capacities.performance("ruacana_generation")
        capacity_mw = capacities.capacity("ruacana_hydro_mw", reference_year)

        def annual_energy(scale: float) -> float:
            fractions = np.minimum(1.0, runoff_index.to_numpy() * scale)
            return float((fractions * month_hours.to_numpy() * capacity_mw).sum() / 1000.0)

        if target_gwh > annual_energy(1e12):
            raise ValueError(
                f"Annual hydro energy exceeds the {capacity_mw:g} MW plant's physical limit")
        # Bisection for the scale that gives the target annual energy.
        low, high = 0.0, 1.0
        while annual_energy(high) < target_gwh:
            high *= 2.0
        for _ in range(80):
            middle = (low + high) / 2.0
            if annual_energy(middle) < target_gwh:
                low = middle
            else:
                high = middle
        return np.minimum(1.0, runoff_index.to_numpy() * high), months

    def get_max_load(self, element: Element) -> Attribute:
        monthly, months = self.monthly_max_load(element.config.system.reference_year)
        profile = pd.DataFrame(
            {DOMESTIC_NODE: monthly[months.to_numpy() - 1]},
            index=pd.RangeIndex(STEPS_PER_YEAR, name="time"),
        )
        target = self.data["nampower_capacities"].performance("ruacana_generation")
        return element.max_load.set_data(
            default_value=1.0, unit="1", df=profile,
            source=cite(
                self,
                "Monthly availability from rainfall near Ruacana (Renewables.ninja MERRA-2), "
                "smoothed with a centred rolling mean plus a base flow (assumptions), scaled so "
                f"that the annual upper bound equals NamPower's Ruacana generation ({target:,.0f} "
                "GWh, FY2022/23, used as a calendar-2023 value). Rainfall is only a seasonal "
                "proxy for river flow.",
            ),
        )
