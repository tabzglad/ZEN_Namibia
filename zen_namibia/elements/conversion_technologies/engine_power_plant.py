from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.datasets.technology.nampower_projects import (
    NamPowerCommittedProjects,
    NamPowerProjectCosts,
)
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022
from zen_namibia.utils import new_technology_capacity_limit


class EnginePowerPlant(ConversionTechnology):
    """New fuel-oil engine plants like Anixas II (54 MW, commissioned 2024).

    Assumptions: the NIRP heat rate and O&M of Anixas I, and the estimated
    HFO price (Anixas II runs on VLSFO/diesel and is gas-ready).
    """

    name: str = "engine_power_plant"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["hfo"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    def _set_lifetime(self) -> Attribute:
        return NamPowerProjectCosts(self.source_path).get_lifetime(self)

    def _set_conversion_factor(self) -> Attribute:
        """Full-load heat rate of Anixas I as a proxy."""
        return NIRP2022(self.source_path).get_conversion_factor(
            self, "anixas", "hfo", description=", Anixas I used as a proxy for new engines")

    def _set_capacity_limit(self) -> Attribute:
        return new_technology_capacity_limit(self)

    def _set_capacity_lower_limit(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_capacity_lower_limit(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """Anixas II final cost N$1.325 bn / 54 MW."""
        return TechnologyCosts(self.source_path).get_capex_specific_conversion(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)

    def _set_opex_specific_variable(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_variable(self)
