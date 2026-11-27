from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

from zen_namibia.datasets.dataset_collections.renewable_fleet import RenewableFleet
from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)


class OnshoreWindTurbine(ConversionTechnology):
    """Onshore wind: the 2023 fleet, committed projects, and generic new
    capacity anywhere in Namibia after 2023."""

    name: str = "onshore_wind_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_input_carrier(self) -> Attribute:
        """No input carrier: wind is represented by max_load."""
        return Attribute(name="input_carrier", default_value=[], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["electricity"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "renewable_plant_lifetime")

    def _set_conversion_factor(self) -> Attribute:
        """No input carrier, so no conversion factor."""
        return self.conversion_factor

    # ---------- Optional methods for overriding default attributes ----------

    def _set_capacity_existing(self) -> Attribute:
        return RenewableFleet(self.source_path).get_capacity_existing(self)

    def _set_capacity_limit(self) -> Attribute:
        return RenewableFleet(self.source_path).get_capacity_limit(self)

    def _set_capacity_lower_limit(self) -> Attribute:
        return RenewableFleet(self.source_path).get_capacity_lower_limit(self)

    def _set_max_load(self) -> Attribute:
        """Renewables.ninja profile scaled to NamPower's 34.8% P50 yield."""
        return RenewableFleet(self.source_path).get_max_load(self)

    def _set_capex_specific_conversion(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_capex_specific_conversion(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        """IRENA Africa onshore wind O&M; variable O&M is taken as zero."""
        return TechnologyCosts(self.source_path).get_opex_specific_fixed(self)
