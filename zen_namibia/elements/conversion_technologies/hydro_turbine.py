from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.renewables_ninja import RenewablesNinja
from zen_namibia.utils import capacity_existing_df

# MOCK DATA: assumed lifetime of 25 years.
# TODO: replace with a real lifetime assumption once available.
LIFETIME = 25
RUACANA_ANNUAL_ENERGY_PROXY_GWH = 1323.0
HOURS_PER_YEAR = 8760


class HydroTurbine(ConversionTechnology):
    """Class containing all data and assumptions for hydro turbine."""

    name: str = "hydro_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """Set the reference carrier of hydro turbine to electricity."""
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """
        Hydro turbine has no input carrier, since it converts hydro energy
        directly into electricity.
        """
        return Attribute(name="input_carrier", default_value=[], element=self)

    def _set_output_carrier(self) -> Attribute:
        """Set the output carrier of hydro turbine to electricity."""
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            "lifetime", default_value=LIFETIME, unit="1", element=self
        )

    def _set_conversion_factor(self) -> Attribute:
        """Hydro turbine has no input carrier, so no conversion factor is needed."""
        attr = self.conversion_factor  # default value: []
        return attr

    # ---------- Optional method for overriding a default attribute ----------

    def _set_capacity_existing(self) -> Attribute:
        """Set the preinstalled (already existing) hydro turbine capacity."""
        reference_year = self.config.system.reference_year
        capacity = NamPowerCapacities(self.source_path).capacity_existing(
            "ruacana_hydro_mw", reference_year
        )
        return Attribute(
            "capacity_existing",
            default_value=capacity,
            unit=self.power_unit,
            element=self,
            df=capacity_existing_df(capacity, reference_year),
        )

    def _set_capacity_limit(self) -> Attribute:
        """Prevent the 2023 snapshot from expanding the existing hydro fleet."""
        capacity = NamPowerCapacities(self.source_path).capacity_existing(
            "ruacana_hydro_mw", self.config.system.reference_year
        )
        return Attribute(
            "capacity_limit", default_value=capacity,
            unit=self.power_unit, element=self,
        )

    def _set_max_load(self) -> Attribute:
        """Set monthly hydro availability from smoothed local rainfall.

        Rainfall is only a seasonal proxy for river flow. The profile is scaled
        so its annual upper-bound energy equals the reported 1,323 GWh Ruacana
        generation benchmark; that benchmark is NamPower FY2023, not calendar
        2023, and is therefore an explicit modeling assumption.
        """
        weather = RenewablesNinja(self.source_path).hydro_precipitation()
        rainfall = weather["prectotland"]

        monthly_rainfall = rainfall.groupby(weather["time"].dt.month).sum().reindex(
            range(1, 13), fill_value=0.0
        )
        # A centered three-month mean represents runoff lag and basin storage;
        # it avoids treating a rain-free month at the weather point as a dry
        # river-flow month. This remains an assumption, not a hydrologic model.
        runoff_index = monthly_rainfall.rolling(window=3, center=True, min_periods=1).mean()
        if float(runoff_index.sum()) <= 0:
            raise ValueError("Hydro weather contains no precipitation to form availability")
        # Retain a small year-round base-flow component because local point
        # rainfall can be zero while the Kunene still carries upstream flow.
        runoff_index = runoff_index + 0.10 * float(monthly_rainfall.mean())

        month_hours = weather["time"].dt.month.value_counts().reindex(range(1, 13), fill_value=0).sort_index()
        target_gwh = RUACANA_ANNUAL_ENERGY_PROXY_GWH
        capacity_mw = NamPowerCapacities(self.source_path).capacity_existing(
            "ruacana_hydro_mw", self.config.system.reference_year
        )

        def annual_energy(scale: float) -> float:
            fractions = np.minimum(1.0, runoff_index.to_numpy() * scale)
            return float(
                (fractions * month_hours.to_numpy() * capacity_mw).sum() / 1000.0
            )

        if target_gwh > annual_energy(1e12):
            raise ValueError(
                f"Annual hydro energy proxy exceeds the {capacity_mw:g} MW plant's physical limit"
            )
        low, high = 0.0, 1.0
        while annual_energy(high) < target_gwh:
            high *= 2.0
        for _ in range(80):
            middle = (low + high) / 2.0
            if annual_energy(middle) < target_gwh:
                low = middle
            else:
                high = middle
        monthly_max_load = np.minimum(1.0, runoff_index.to_numpy() * high)
        profile = pd.DataFrame(
            {"NAM": monthly_max_load[weather["time"].dt.month.to_numpy() - 1]},
            index=pd.RangeIndex(HOURS_PER_YEAR, name="time"),
        )
        return Attribute(
            "max_load", default_value=1.0, unit="1", element=self, df=profile
        )

