from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.dataset_collections.thermal_availability import ThermalAvailability
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.nampower import NamPowerCapacities
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022


class AnixasI(ConversionTechnology):
    """Anixas I, the existing HFO plant at Walvis Bay. Not expandable: new
    engines are engine_power_plant."""

    name: str = "anixas_i"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["hfo"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "existing_plant_lifetime")

    def _set_conversion_factor(self) -> Attribute:
        """NIRP full-load heat rate (about 44.8% efficiency)."""
        return NIRP2022(self.source_path).get_conversion_factor(self, "anixas", "hfo")

    # ---------- Optional methods for overriding default attributes ----------

    def _set_capacity_existing(self) -> Attribute:
        return NamPowerCapacities(self.source_path).get_capacity_existing(self)

    def _set_capacity_limit(self) -> Attribute:
        return NamPowerCapacities(self.source_path).get_capacity_limit(self)

    def _set_max_load(self) -> Attribute:
        """Net output limited to the NIRP's 21.5 MW."""
        return ThermalAvailability(self.source_path).get_max_load(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """The NIRP lists "3 x N$1.55/kWh", applied as N$4.65/kWh; it excludes fuel."""
        return TechnologyCosts(self.source_path).get_opex_specific_variable(self)
