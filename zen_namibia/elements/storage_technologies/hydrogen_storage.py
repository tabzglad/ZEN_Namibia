from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, StorageTechnology

from zen_namibia.datasets.dataset_collections.hydrogen_technology_costs import (
    HydrogenTechnologyCosts,
)
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.utils import new_technology_capacity_limit


class HydrogenStorage(StorageTechnology):
    """Compressed hydrogen tanks, so electrolysers can follow wind and sun
    while the hydrogen demand stays flat. Tanks are costed per MWh stored and
    compressors per MW of charging power."""

    name: str = "hydrogen_storage"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["hydrogen"], element=self)

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "hydrogen_storage_lifetime")

    def _set_efficiency_charge(self) -> Attribute:
        """Compression energy, modelled as a hydrogen loss."""
        return ZENNamibiaAssumptions(self.source_path).get_attribute(
            self, "efficiency_charge", "hydrogen_storage_charge_efficiency", unit="1")

    def _set_capacity_limit(self) -> Attribute:
        return new_technology_capacity_limit(self)

    def _set_capacity_limit_energy(self) -> Attribute:
        return new_technology_capacity_limit(
            self, name="capacity_limit_energy", unit=f"{self.power_unit}*h")

    def _set_capex_specific_storage(self) -> Attribute:
        """Compressor cost per MW of charging power."""
        return HydrogenTechnologyCosts(self.source_path).get_storage_capex_power(self)

    def _set_opex_specific_fixed(self) -> Attribute:
        return HydrogenTechnologyCosts(self.source_path).get_storage_opex_fixed(self)

    def _set_capex_specific_storage_energy(self) -> Attribute:
        """US DOE stationary tank target per kg."""
        return HydrogenTechnologyCosts(self.source_path).get_storage_capex_energy(self)

    def _set_opex_specific_fixed_energy(self) -> Attribute:
        return HydrogenTechnologyCosts(self.source_path).get_storage_opex_fixed_energy(self)
