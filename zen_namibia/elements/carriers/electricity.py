from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator import Model

from zen_creator import Attribute, Carrier

from zen_namibia.datasets.datasets.electricity_demand import ElectricityDemand
from zen_namibia.datasets.datasets.namibia_baseline import NamibiaBaseline


class Electricity(Carrier):
    """All data and assumptions for the electricity carrier."""

    name: str = "electricity"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        """Set the electricity demand, loaded from source_data/demands.csv."""
        return ElectricityDemand(self.source_path).get_demand(self)

    def _set_availability_import(self) -> Attribute:
        """Allow imports up to each year's observed annual import volume."""
        return Attribute(
            "availability_import", default_value=1.0e6, unit=self.power_unit,
            element=self,
        )

    def _set_availability_export(self) -> Attribute:
        """Allow exports up to each year's observed annual export volume."""
        return Attribute(
            "availability_export", default_value=1.0e6, unit=self.power_unit,
            element=self,
        )

    def _set_availability_import_yearly(self) -> Attribute:
        """Annual import cap from observed GWh, stored as MWh."""
        baseline = NamibiaBaseline(self.source_path).data.set_index("year")
        limits = baseline[["imports_gwh"]].rename(columns={"imports_gwh": "NAM"}) * 1000
        return Attribute(
            "availability_import_yearly", default_value=0.0,
            unit=f"{self.power_unit}*h", element=self, df=limits,
        )

    def _set_availability_export_yearly(self) -> Attribute:
        """Annual export cap from observed GWh, stored as MWh."""
        baseline = NamibiaBaseline(self.source_path).data.set_index("year")
        limits = baseline[["exports_gwh"]].rename(columns={"exports_gwh": "NAM"}) * 1000
        return Attribute(
            "availability_export_yearly", default_value=0.0,
            unit=f"{self.power_unit}*h", element=self, df=limits,
        )
