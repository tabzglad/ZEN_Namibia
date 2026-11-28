from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.hydrogen_technology_costs import (
    HydrogenTechnologyCosts,
)
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.iea_future_of_hydrogen import (
    IEAFutureOfHydrogen2019,
)
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes


class Electrolyser(ConversionTechnology):
    """Grid-connected electrolysers in Namibia (Hyphen Phase 1 plans 1.5 GW).

    Capacity is measured in MW of electricity input, so it can be compared
    with Hyphen's electrolyser size. The size is optimized, not imposed.
    """

    name: str = "electrolyser"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["electricity"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["hydrogen"], element=self)

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "electrolyser_lifetime")

    def _set_conversion_factor(self) -> Attribute:
        """Hydrogen out (LHV) per MWh of electricity in."""
        return IEAFutureOfHydrogen2019(self.source_path).get_conversion_factor(self)

    def _set_capacity_limit(self) -> Attribute:
        return ManualNodes(self.source_path).get_new_technology_capacity_limit(self, hydrogen_only=True)

    def _set_capex_specific_conversion(self) -> Attribute:
        return HydrogenTechnologyCosts(self.source_path).get_electrolyser_capex(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        return HydrogenTechnologyCosts(self.source_path).get_electrolyser_opex_fixed(self)
