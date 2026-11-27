from __future__ import annotations

from pathlib import Path

from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.dataset_collections.monetary_conversion import MonetaryConversion
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.technology.iea_future_of_hydrogen import (
    IEAFutureOfHydrogen2019,
)
from zen_namibia.datasets.datasets.technology.iea_global_hydrogen_review import (
    IEAGlobalHydrogenReview2024,
)
from zen_namibia.datasets.datasets.technology.rozzi_hydrogen_storage import (
    RozziHydrogenStorage,
)
from zen_namibia.datasets.datasets.technology.us_doe_hydrogen_storage import (
    USDOEHydrogenStorage,
)


class HydrogenTechnologyCosts(DatasetCollection):
    """Capex and fixed O&M of electrolysers and compressed hydrogen storage, in euros."""

    name = "hydrogen_technology_costs"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "iea_global_hydrogen_review_2024": IEAGlobalHydrogenReview2024(self.source_path),
            "iea_future_of_hydrogen_2019": IEAFutureOfHydrogen2019(self.source_path),
            "us_doe_hydrogen_storage": USDOEHydrogenStorage(self.source_path),
            "rozzi_hydrogen_storage": RozziHydrogenStorage(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "monetary_conversion": MonetaryConversion(self.source_path),
        }

    def _assumed(self, item: str) -> float:
        return self.data["assumptions"].value(item)

    def electrolyser_capex_per_mw(self) -> float:
        """Capex per MW of electricity input."""
        usd_per_kw = self.data["iea_global_hydrogen_review_2024"].value("electrolyser_capex")
        return self.data["monetary_conversion"].usd_to_euro(usd_per_kw * 1000.0)

    def storage_capex_per_mwh(self) -> float:
        """Tank capex per MWh of stored hydrogen (LHV)."""
        usd_per_kg = self.data["us_doe_hydrogen_storage"].value("hydrogen_storage_capex")
        return self.data["monetary_conversion"].usd_to_euro(
            usd_per_kg / self._assumed("hydrogen_lhv") * 1000.0)

    def compressor_capex_per_mw(self) -> float:
        """Compressor cost per MW of hydrogen charging: EUR/kW of compressor
        power times the compression energy per unit of hydrogen charged."""
        compression_share = 1.0 - self._assumed("hydrogen_storage_charge_efficiency")
        eur_per_kw = self.data["rozzi_hydrogen_storage"].value("hydrogen_storage_compressor_capex")
        return eur_per_kw * 1000.0 * compression_share

    # ---------- electrolyser ----------

    def get_electrolyser_capex(self, element: Element) -> Attribute:
        return element.capex_specific_conversion.set_data(
            default_value=self.electrolyser_capex_per_mw(), unit=f"Euro/{element.power_unit}",
            source=cite(self, "IEA 2030 installed electrolyser cost per kW of electricity "
                              "input; USD to euros at the 2023 ECB rate.",
                        "iea_global_hydrogen_review_2024", "monetary_conversion"))

    def get_electrolyser_opex_fixed(self, element: Element) -> Attribute:
        share = self.data["iea_future_of_hydrogen_2019"].value("electrolyser_fixed_om_share")
        return element.opex_specific_fixed.set_data(
            default_value=share * self.electrolyser_capex_per_mw(),
            unit=f"Euro/{element.power_unit}",
            source=cite(self, f"Fixed O&M of {share:.1%} of capex per year (IEA 2019) times "
                              "the IEA 2024 capex.", "iea_future_of_hydrogen_2019",
                        "iea_global_hydrogen_review_2024", "monetary_conversion"))

    # ---------- hydrogen storage ----------

    def get_storage_capex_power(self, element: Element) -> Attribute:
        """Without a power cost, the charge rating is free and its optimal size arbitrary."""
        return element.capex_specific_storage.set_data(
            default_value=self.compressor_capex_per_mw(), unit=f"Euro/{element.power_unit}",
            source=cite(self, "Compressor capex per kW of electrical input (Rozzi et al. 2024) "
                              "times the compression energy share of the hydrogen charged "
                              "(1 - charge efficiency, assumption).",
                        "rozzi_hydrogen_storage", "assumptions"))

    def get_storage_capex_energy(self, element: Element) -> Attribute:
        return element.capex_specific_storage_energy.set_data(
            default_value=self.storage_capex_per_mwh(), unit=f"Euro/({element.power_unit}*h)",
            source=cite(self, "US DOE stationary tank capex target per kg divided by the lower "
                              "heating value of hydrogen; USD to euros at the 2023 ECB rate.",
                        "us_doe_hydrogen_storage", "assumptions", "monetary_conversion"))

    def get_storage_opex_fixed(self, element: Element) -> Attribute:
        return element.opex_specific_fixed.set_data(
            default_value=self._assumed("hydrogen_storage_fixed_om_share")
            * self.compressor_capex_per_mw(),
            unit=f"Euro/{element.power_unit}",
            source=cite(self, "Assumed fixed O&M share of capex per year times the compressor "
                              "capex.", "assumptions", "rozzi_hydrogen_storage"))

    def get_storage_opex_fixed_energy(self, element: Element) -> Attribute:
        return element.opex_specific_fixed_energy.set_data(
            default_value=self._assumed("hydrogen_storage_fixed_om_share")
            * self.storage_capex_per_mwh(),
            unit=f"Euro/({element.power_unit}*h)",
            source=cite(self, "Assumed fixed O&M share of capex per year times the tank capex.",
                        "assumptions", "us_doe_hydrogen_storage", "monetary_conversion"))
