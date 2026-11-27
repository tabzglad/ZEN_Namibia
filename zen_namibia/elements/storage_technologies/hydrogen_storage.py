from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, StorageTechnology

from zen_namibia.datasets.datasets.technology.hydrogen import hydrogen_assumptions
from zen_namibia.utils import capacity_limit_attribute


class HydrogenStorage(StorageTechnology):
    """Compressed hydrogen tanks, so electrolysers can follow wind and sun
    while the hydrogen demand stays flat. Tanks are costed per MWh stored and
    compressors per MW of charging power."""

    name: str = "hydrogen_storage"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _h2(self, item: str) -> float:
        return hydrogen_assumptions(self.source_path).value(item)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["hydrogen"], element=self)

    def _set_lifetime(self) -> Attribute:
        return Attribute("lifetime", default_value=self._h2("hydrogen_storage_lifetime"), unit="1", element=self)

    def _set_efficiency_charge(self) -> Attribute:
        """Compression energy, modelled as a hydrogen loss (assumption)."""
        return Attribute(
            "efficiency_charge", default_value=self._h2("hydrogen_storage_charge_efficiency"),
            unit="1", element=self,
        )

    def _set_capacity_limit(self) -> Attribute:
        return capacity_limit_attribute(self, 0.0, expandable=True)

    def _set_capacity_limit_energy(self) -> Attribute:
        return capacity_limit_attribute(
            self, 0.0, expandable=True, name="capacity_limit_energy",
            unit=f"{self.power_unit}*h",
        )

    def _set_capex_specific_storage(self) -> Attribute:
        """Compressor cost per MW of charging power (hydrogen.csv). Without it,
        the power rating costs nothing and its optimal size is arbitrary."""
        return Attribute(
            "capex_specific_storage",
            default_value=hydrogen_assumptions(self.source_path).storage_compressor_capex_euro_per_mw(),
            unit=f"Euro/{self.power_unit}", element=self,
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            "opex_specific_fixed",
            default_value=self._h2("hydrogen_storage_fixed_om_share")
            * hydrogen_assumptions(self.source_path).storage_compressor_capex_euro_per_mw(),
            unit=f"Euro/{self.power_unit}", element=self,
        )

    def _set_capex_specific_storage_energy(self) -> Attribute:
        """US DOE stationary tank target, USD 700/kg (hydrogen.csv)."""
        return Attribute(
            "capex_specific_storage_energy",
            default_value=hydrogen_assumptions(self.source_path).storage_capex_euro_per_mwh(),
            unit=f"Euro/({self.power_unit}*h)", element=self,
        )

    def _set_opex_specific_fixed_energy(self) -> Attribute:
        return Attribute(
            "opex_specific_fixed_energy",
            default_value=self._h2("hydrogen_storage_fixed_om_share")
            * hydrogen_assumptions(self.source_path).storage_capex_euro_per_mwh(),
            unit=f"Euro/({self.power_unit}*h)", element=self,
        )
