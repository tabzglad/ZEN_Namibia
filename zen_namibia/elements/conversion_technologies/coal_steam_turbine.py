from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.dataset_collections.thermal_fleet import ThermalFleet
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022


class CoalSteamTurbine(ConversionTechnology):
    """Van Eck, Namibia's coal plant in Windhoek. Not expandable."""

    name: str = "coal_steam_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["coal"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "existing_plant_lifetime")

    def _set_conversion_factor(self) -> Attribute:
        """NIRP full-load heat rate (about 22% efficiency); the lower efficiency
        at minimum load is not represented."""
        return NIRP2022(self.source_path).get_conversion_factor(self, "van_eck", "coal")

    # ---------- Optional methods for overriding default attributes ----------

    def _set_capacity_existing(self) -> Attribute:
        return ThermalFleet(self.source_path).get_capacity_existing(self)

    def _set_capacity_limit(self) -> Attribute:
        return ThermalFleet(self.source_path).get_capacity_limit(self)

    def _set_max_load(self) -> Attribute:
        """Limited to the 96 MW available capacity reported for 2023."""
        return ThermalFleet(self.source_path).get_max_load(self)

    def _set_opex_specific_variable(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_variable(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)
