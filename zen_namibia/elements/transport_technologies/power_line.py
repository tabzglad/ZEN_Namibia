from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, TransportTechnology

from zen_namibia.datasets.dataset_collections.interconnectors import Interconnectors
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)


class PowerLine(TransportTechnology):
    """Power lines, one capacity per direction: SAPP cross-border lines and NamPower's
    corridors between the Namibian nodes."""

    name: str = "power_line"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["electricity"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return ZENNamibiaAssumptions(self.source_path).get_lifetime(self, "power_line_lifetime")

    # ---------- Optional methods for overriding default attributes ----------

    def _set_capacity_existing(self) -> Attribute:
        return Interconnectors(self.source_path).get_capacity_existing(self)

    def _set_capacity_limit(self) -> Attribute:
        return Interconnectors(self.source_path).get_capacity_limit(self)

    def _set_capacity_lower_limit(self) -> Attribute:
        """Lines commissioned after 2023 (Auas-Gerus, second Auas-Kokerboom) must be built."""
        return Interconnectors(self.source_path).get_capacity_lower_limit(self)

    def _set_opex_specific_variable(self) -> Attribute:
        """Tiny wheeling cost so the solver does not route power in loops."""
        return ZENNamibiaAssumptions(self.source_path).get_attribute(
            self, "opex_specific_variable", "power_line_wheeling_cost",
            unit=f"Euro/({self.power_unit}*h)")

    def _set_distance(self) -> Attribute:
        return Interconnectors(self.source_path).get_distance(self)
