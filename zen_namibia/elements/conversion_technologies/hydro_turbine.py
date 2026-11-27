from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.hydro_availability import HydroAvailability
from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities


class HydroTurbine(ConversionTechnology):
    """Ruacana hydro power station on the Kunene. Not expandable."""

    name: str = "hydro_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        """No input carrier: the river flow is represented by max_load."""
        return Attribute(name="input_carrier", default_value=[], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "existing_plant_lifetime")

    def _set_conversion_factor(self) -> Attribute:
        """No input carrier, so no conversion factor."""
        return self.conversion_factor

    # ---------- Optional methods for overriding default attributes ----------

    def _set_capacity_existing(self) -> Attribute:
        return NamPowerCapacities(self.source_path).get_capacity_existing(self)

    def _set_capacity_limit(self) -> Attribute:
        return NamPowerCapacities(self.source_path).get_capacity_limit(self)

    def _set_max_load(self) -> Attribute:
        """Monthly availability from smoothed rainfall, scaled to Ruacana's generation."""
        return HydroAvailability(self.source_path).get_max_load(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """NIRP 2022 Table 5 fixed cost; variable O&M is not applied."""
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)
