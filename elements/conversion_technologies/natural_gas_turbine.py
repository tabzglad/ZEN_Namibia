from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, ConversionTechnology

# MOCK DATA: assumed lifetime of 25 years.
# TODO: replace with a real lifetime assumption once available.
LIFETIME = 25

# MOCK DATA: 2.5 MWh of natural gas needed per 1 MWh of electricity produced
# (roughly 40% efficiency). TODO: replace with a real conversion factor.
CONVERSION_FACTOR_GAS = 2.5


class NaturalGasTurbine(ConversionTechnology):
    """Class containing all data and assumptions for a gas-fired power plant.

    This technology exists so that the model has at least one conversion
    technology with an input carrier (photovoltaics has none) -- ZEN-garden
    cannot build a model where no technology has any input carrier at all.
    """

    name: str = "natural_gas_turbine"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """Set the reference carrier of the turbine to electricity (its output)."""
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        """Set the input carrier of the turbine to natural gas."""
        return Attribute(
            name="input_carrier", default_value=["natural_gas"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        """Set the output carrier of the turbine to electricity."""
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        return Attribute("lifetime", default_value=LIFETIME, unit="1", element=self)

    def _set_conversion_factor(self) -> Attribute:
        """Set how much natural gas is needed per unit of electricity output."""
        return Attribute(
            name="conversion_factor",
            default_value=[
                {
                    "natural_gas": {
                        "default_value": CONVERSION_FACTOR_GAS,
                        "unit": f"{self.power_unit}h/{self.power_unit}h",
                    }
                }
            ],
            element=self,
        )
