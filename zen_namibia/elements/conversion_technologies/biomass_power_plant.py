from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.datasets.technology.nampower_otjikoto import NamPowerOtjikoto
from zen_namibia.datasets.datasets.technology.nampower_projects import (
    NamPowerCommittedProjects,
    NamPowerProjectCosts,
)
from zen_namibia.utils import new_technology_capacity_limit


class BiomassPowerPlant(ConversionTechnology):
    """Encroacher-bush biomass steam plants like Otjikoto (40 MW, COD 2027)."""

    name: str = "biomass_power_plant"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["biomass"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    def _set_lifetime(self) -> Attribute:
        return NamPowerProjectCosts(self.source_path).get_lifetime(self)

    def _set_conversion_factor(self) -> Attribute:
        """Fuel per MWh of electricity: 1 / 30% (Otjikoto fact sheet)."""
        return NamPowerOtjikoto(self.source_path).get_conversion_factor(self)

    def _set_capacity_limit(self) -> Attribute:
        return new_technology_capacity_limit(self)

    def _set_capacity_lower_limit(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_capacity_lower_limit(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        """Otjikoto estimated cost N$2.641 bn / 40 MW."""
        return TechnologyCosts(self.source_path).get_capex_specific_conversion(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """Assumed share of capex per year."""
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)
