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
# Anixas full-load heat rate from Namibia's 2022 NIRP: 8.03 MJ/kWh_e,
# numerically equal to 8.03 GJ/MWh_e.
FULL_LOAD_HEAT_RATE_GJ_PER_MWH_E = 8.03
FUEL_INPUT_PER_ELECTRIC_OUTPUT = FULL_LOAD_HEAT_RATE_GJ_PER_MWH_E / 3.6


class DieselGenerator(ConversionTechnology):
    """Class containing all data and assumptions for diesel generator."""

    name: str = "diesel_generator"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """Set the reference carrier of diesel generator  to electricity."""
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """Use diesel as the plant's fuel input carrier."""
        return Attribute(name="input_carrier", default_value=["diesel"], element=self)

    def _set_output_carrier(self) -> Attribute:
        """Set the output carrier of diesel generator to electricity."""
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            "lifetime", default_value=LIFETIME, unit="1", element=self
        )

    def _set_conversion_factor(self) -> Attribute:
        """Use Anixas's reported full-load heat rate (about 44.8% efficiency).

        Source: Namibia NIRP Review and Update (2022), Anixas parameters.
        """
        return Attribute(
            name="conversion_factor",
            default_value=[{"diesel": {"default_value": FUEL_INPUT_PER_ELECTRIC_OUTPUT, "unit": f"{self.power_unit}h/{self.power_unit}h"}}],
            element=self,
        )

    # ---------- Optional method for overriding a default attribute ----------

    def _set_capacity_existing(self) -> Attribute:
        """Set the preinstalled (already existing) diesel generator capacity."""
        reference_year = self.config.system.reference_year
        capacity = NamPowerCapacities(self.source_path).capacity_existing(
            "anixas_diesel_mw", reference_year
        )
        return Attribute(
            "capacity_existing",
            default_value=capacity,
            unit=self.power_unit,
            element=self,
            df=capacity_existing_df(capacity, reference_year),
        )
