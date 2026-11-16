from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.utils import capacity_existing_df

# MOCK DATA: assumed lifetime of 25 years.
# TODO: replace with a real lifetime assumption once available.
LIFETIME = 25
# Van Eck full-load heat rate from Namibia's 2022 NIRP: 15.81 GJ/MWh_e (580 kg coal/MWh).
FULL_LOAD_HEAT_RATE_GJ_PER_MWH_E = 15.81
# MWh of fuel per MWh of electricity: heat rate divided by 3.6 GJ/MWh.
FUEL_INPUT_PER_ELECTRIC_OUTPUT = FULL_LOAD_HEAT_RATE_GJ_PER_MWH_E / 3.6


class CoalSteamTurbine(ConversionTechnology):
    """Class containing all data and assumptions for coal steam turbine."""

    name: str = "coal_steam_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """Set the reference carrier of coal steam turbine to electricity."""
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """Use coal as the plant's fuel input carrier."""
        return Attribute(name="input_carrier", default_value=["coal"], element=self)

    def _set_output_carrier(self) -> Attribute:
        """Set the output carrier of coal steam turbine to electricity."""
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            "lifetime", default_value=LIFETIME, unit="1", element=self
        )

    def _set_conversion_factor(self) -> Attribute:
        """Use Van Eck's reported full-load heat rate (about 22% efficiency).

        The NIRP also reports a lower efficiency at minimum load; this scalar
        assumption represents full-load operation only.

        Source: Namibia NIRP Review and Update (2022), Van Eck parameters.
        """
        return Attribute(
            name="conversion_factor",
            default_value=[{"coal": {"default_value": FUEL_INPUT_PER_ELECTRIC_OUTPUT, "unit": f"{self.power_unit}h/{self.power_unit}h"}}],
            element=self,
        )

    # ---------- Optional method for overriding a default attribute ----------

    def _set_capacity_existing(self) -> Attribute:
        """Set the preinstalled (already existing) coal steam turbine  capacity."""
        reference_year = self.config.system.reference_year
        capacity = NamPowerCapacities(self.source_path).capacity_existing(
            "van_eck_thermal_mw", reference_year
        )
        return Attribute(
            "capacity_existing",
            default_value=capacity,
            unit=self.power_unit,
            element=self,
            df=capacity_existing_df(capacity, reference_year),
        )
