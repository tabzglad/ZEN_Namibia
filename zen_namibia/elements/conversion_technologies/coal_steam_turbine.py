from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology
from zen_namibia.datasets.datasets.namibia_baseline import NamibiaBaseline

# MOCK DATA: assumed lifetime of 25 years.
# TODO: replace with a real lifetime assumption once available.
LIFETIME = 25


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
        """Placeholder fuel-to-electricity ratio; replace when plant efficiency is sourced."""
        return Attribute(
            name="conversion_factor",
            default_value=[{"coal": {"default_value": 1.0, "unit": f"{self.power_unit}h/{self.power_unit}h"}}],
            element=self,
        )

    # ---------- Optional method for overriding a default attribute ----------

    def _set_capacity_existing(self) -> Attribute:
        """Set the preinstalled (already existing) coal steam turbine  capacity."""
        return Attribute(
            "capacity_existing",
            default_value=NamibiaBaseline(self.source_path).capacity_existing("van_eck_thermal_mw"),
            unit=self.power_unit,
            element=self,
        )

