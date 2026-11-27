from __future__ import annotations

from pathlib import Path

from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.dataset_collections.monetary_conversion import MonetaryConversion
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.irena_africa import IRENAAfricaPlanning2021
from zen_namibia.datasets.datasets.technology.irena_renewable_costs import (
    IRENARenewableCosts2023,
)
from zen_namibia.datasets.datasets.technology.nampower_projects import NamPowerProjectCosts
from zen_namibia.datasets.datasets.technology.nirp import NIRP2022

NIRP_PRICE_YEAR = 2020
# NIRP plant whose O&M each technology uses. New engines use Anixas I as a proxy.
NIRP_PLANT = {
    "coal_steam_turbine": "van_eck",
    "anixas_i": "anixas",
    "engine_power_plant": "anixas",
    "hydro_turbine": "ruacana",
}
# IRENA fixed O&M (USD/kW/year) of the renewables: dataset key and item.
IRENA_FIXED_OM = {
    "photovoltaics": ("irena_renewable_costs_2023", "pv_fixed_om"),
    "onshore_wind_turbine": ("irena_africa_planning_2021", "wind_fixed_om"),
}
# Technologies whose fixed O&M is an assumed share of capex.
FIXED_OM_SHARE = {
    "biomass_power_plant": "biomass_fixed_om_share",
    "battery": "battery_fixed_om_share",
}


class TechnologyCosts(DatasetCollection):
    """Capex and O&M of the power plants and batteries, in 2023 euros.

    - Capex: NamPower's own recent projects (N$).
    - O&M of existing plants: NIRP 2022 (N$, 2020-2021 data), scaled to 2023
      with the Namibian CPI.
    - Fixed O&M of PV and wind: IRENA (USD), not scaled with CPI, because
      these costs have fallen over time.
    - Fixed O&M of biomass plants and batteries: assumed share of capex.
    """

    name = "technology_costs"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "nampower_project_costs": NamPowerProjectCosts(self.source_path),
            "nirp_2022": NIRP2022(self.source_path),
            "irena_renewable_costs_2023": IRENARenewableCosts2023(self.source_path),
            "irena_africa_planning_2021": IRENAAfricaPlanning2021(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "monetary_conversion": MonetaryConversion(self.source_path),
        }

    @property
    def _money(self) -> MonetaryConversion:
        return self.data["monetary_conversion"]

    def _nirp_om(self, item: str) -> float:
        """NIRP N$/kWh or N$/kW/year (2020 prices) to 2023 euros per MWh or MW/year."""
        nirp = self.data["nirp_2022"].value(item)
        return self._money.nad_to_euro(nirp * 1000.0 * self._money.cpi_factor(NIRP_PRICE_YEAR))

    def capex_per_mw(self, technology: str) -> float:
        return self._money.nad_to_euro(
            self.data["nampower_project_costs"].capex_nad_per_mw(technology))

    def capex_per_mwh(self, technology: str) -> float:
        return self._money.nad_to_euro(
            self.data["nampower_project_costs"].capex_nad_per_mwh(technology))

    def _capex_source(self, technology: str, per: str):
        project = self.data["nampower_project_costs"].reference_project(technology)
        return cite(self, f"Capex per {per} of {project}; N$ to euros at the 2023 "
                          "Bank of Namibia rate.", "nampower_project_costs", "monetary_conversion")

    def get_capex_specific_conversion(self, element: Element) -> Attribute:
        return element.capex_specific_conversion.set_data(
            default_value=self.capex_per_mw(element.name), unit=f"Euro/{element.power_unit}",
            source=self._capex_source(element.name, "MW"))

    def get_capex_specific_storage_energy(self, element: Element) -> Attribute:
        return element.capex_specific_storage_energy.set_data(
            default_value=self.capex_per_mwh(element.name),
            unit=f"Euro/({element.power_unit}*h)",
            source=self._capex_source(element.name, "MWh of storage (whole project cost)"))

    def get_opex_specific_fixed(self, element: Element) -> Attribute:
        name = element.name
        if name in NIRP_PLANT:
            plant = NIRP_PLANT[name]
            value = self._nirp_om(f"{plant}_fixed_om")
            source = cite(self, f"NIRP 2022 fixed O&M of {plant.replace('_', ' ').title()} "
                                "(N$/kW/year, 2020-2021 data), scaled to 2023 with the Namibian "
                                "CPI; N$ to euros at the 2023 Bank of Namibia rate.",
                          "nirp_2022", "monetary_conversion")
        elif name in IRENA_FIXED_OM:
            key, item = IRENA_FIXED_OM[name]
            value = self._money.usd_to_euro(self.data[key].value(item) * 1000.0)
            source = cite(self, "IRENA fixed O&M (USD/kW/year), not scaled with CPI because "
                                "these costs have fallen over time; USD to euros at the 2023 ECB "
                                "rate. Variable O&M is taken as zero.", key, "monetary_conversion")
        elif name in FIXED_OM_SHARE:
            item = FIXED_OM_SHARE[name]
            value = self.data["assumptions"].value(item) * self.capex_per_mw(name)
            source = cite(self, "Assumed share of capex per year (see the assumptions file) "
                                "times the capex.", "assumptions", "nampower_project_costs",
                          "monetary_conversion")
        else:
            raise KeyError(f"No fixed O&M for {name}")
        return element.opex_specific_fixed.set_data(
            default_value=value, unit=f"Euro/{element.power_unit}", source=source)

    def get_opex_specific_fixed_energy(self, element: Element) -> Attribute:
        item = FIXED_OM_SHARE[element.name]
        return element.opex_specific_fixed_energy.set_data(
            default_value=self.data["assumptions"].value(item) * self.capex_per_mwh(element.name),
            unit=f"Euro/({element.power_unit}*h)",
            source=cite(self, "Assumed share of capex per year (see the assumptions file) "
                              "times the capex per MWh.", "assumptions",
                        "nampower_project_costs", "monetary_conversion"))

    def get_opex_specific_variable(self, element: Element) -> Attribute:
        plant = NIRP_PLANT[element.name]
        return element.opex_specific_variable.set_data(
            default_value=self._nirp_om(f"{plant}_variable_om"),
            unit=f"Euro/({element.power_unit}*h)",
            source=cite(self, f"NIRP 2022 variable O&M of {plant.title()} (N$/kWh, 2020-2021 "
                              "data, excluding fuel), scaled to 2023 with the Namibian CPI; N$ "
                              "to euros at the 2023 Bank of Namibia rate.",
                        "nirp_2022", "monetary_conversion"))
