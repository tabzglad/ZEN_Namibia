from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, StorageTechnology

from zen_namibia.datasets.dataset_collections.technology_costs import TechnologyCosts
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.nampower_projects import (
    NamPowerCommittedProjects,
)
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes


class Battery(StorageTechnology):
    """Lithium-ion batteries like the Omburu BESS (51 MW / 51 MWh, 2026).

    The whole Omburu cost is put on storage energy with a fixed one-hour
    duration, because only one cost figure is published.
    """

    name: str = "battery"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "battery_lifetime")

    def _efficiency(self, attribute: str) -> Attribute:
        """Half of the round-trip losses on charging, half on discharging."""
        assumptions = ZENNamibiaAssumptions(self.source_path)
        return getattr(self, attribute).set_data(
            default_value=assumptions.value("battery_round_trip_efficiency") ** 0.5, unit="1",
            source=assumptions.assumption(
                "battery_round_trip_efficiency",
                description="Square root of the round-trip efficiency"),
        )

    def _set_efficiency_charge(self) -> Attribute:
        return self._efficiency("efficiency_charge")

    def _set_efficiency_discharge(self) -> Attribute:
        return self._efficiency("efficiency_discharge")

    def _set_energy_to_power_ratio_min(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_energy_to_power_ratio(self, "min")

    def _set_energy_to_power_ratio_max(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_energy_to_power_ratio(self, "max")

    def _set_capacity_limit(self) -> Attribute:
        return ManualNodes(self.source_path).get_new_technology_capacity_limit(self)

    def _set_capacity_limit_energy(self) -> Attribute:
        return ManualNodes(self.source_path).get_new_technology_capacity_limit(
            self, energy=True)

    def _set_capacity_lower_limit(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_capacity_lower_limit(self)

    def _set_capacity_lower_limit_energy(self) -> Attribute:
        return NamPowerCommittedProjects(self.source_path).get_capacity_lower_limit(
            self, energy=True)

    def _set_capex_specific_storage_energy(self) -> Attribute:
        """Omburu BESS N$500 m / 51 MWh, all on storage energy."""
        return TechnologyCosts(self.source_path).get_capex_specific_storage_energy(self)

    def _set_opex_specific_fixed_energy(self) -> Attribute:
        return TechnologyCosts(self.source_path).get_opex_specific_fixed_energy(self)
