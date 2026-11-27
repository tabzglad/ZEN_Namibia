from __future__ import annotations

from pathlib import Path

from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.dataset_collections.monetary_conversion import (
    PRICE_YEAR,
    MonetaryConversion,
)
from zen_namibia.datasets.datasets.assumptions.zen_namibia_assumptions import (
    ZENNamibiaAssumptions,
)
from zen_namibia.datasets.datasets.carrier.insee import INSEEFuelPrices
from zen_namibia.datasets.datasets.carrier.nampower import NamPowerPrices
from zen_namibia.datasets.datasets.technology.nampower_otjikoto import NamPowerOtjikoto
from zen_namibia.datasets.datasets.technology.nirp import GJ_PER_MWH, NIRP2022

NIRP_PRICE_YEAR = 2020


class FuelPrices(DatasetCollection):
    """Prices of coal, heavy fuel oil and wood chips in euros per MWh of fuel."""

    name = "fuel_prices"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "nampower_prices": NamPowerPrices(self.source_path),
            "nirp_2022": NIRP2022(self.source_path),
            "insee": INSEEFuelPrices(self.source_path),
            "nampower_otjikoto": NamPowerOtjikoto(self.source_path),
            "assumptions": ZENNamibiaAssumptions(self.source_path),
            "monetary_conversion": MonetaryConversion(self.source_path),
        }

    @property
    def _money(self) -> MonetaryConversion:
        return self.data["monetary_conversion"]

    def coal_price(self) -> float:
        """Van Eck coal price per MWh of coal: N$/t divided by the coal energy
        content implied by the NIRP heat rate and coal use."""
        nad_per_tonne = self.data["nampower_prices"].value("coal_price")
        return self._money.nad_to_euro(nad_per_tonne / self.data["nirp_2022"].coal_mwh_per_tonne())

    def hfo_price(self) -> float:
        """Estimated delivered HFO price for Anixas in the price year.

        The NIRP 2020 delivered price is split into the 2020 market price
        (NW Europe HFO 380 cst FOB) and a delivery cost (shipping, inland
        transport, handling, margins). The price-year price is that year's
        market price plus the 2020 delivery cost scaled with the Namibian CPI.
        """
        gj_per_tonne = self.data["assumptions"].value("hfo_energy_content")
        insee = self.data["insee"]
        fob_2020 = (insee.hfo_fob_eur_per_tonne(NIRP_PRICE_YEAR) / gj_per_tonne
                    * self._money.nad_per_eur(NIRP_PRICE_YEAR))
        delivery_2020 = self.data["nirp_2022"].value("hfo_delivered_price_2020") - fob_2020
        if delivery_2020 <= 0:
            raise ValueError("NIRP 2020 HFO price must exceed the 2020 FOB market price")
        fob = insee.hfo_fob_eur_per_tonne(PRICE_YEAR) / gj_per_tonne * self._money.nad_per_eur()
        delivered = fob + delivery_2020 * self._money.cpi_factor(NIRP_PRICE_YEAR)  # N$/GJ
        return self._money.nad_to_euro(delivered * GJ_PER_MWH)

    def biomass_price(self) -> float:
        """Wood-chip price per MWh of fuel energy."""
        otjikoto = self.data["nampower_otjikoto"]
        return self._money.nad_to_euro(
            otjikoto.value("biomass_fuel_price") / otjikoto.wood_chip_mwh_per_tonne())

    def get_price_import(self, element: Element) -> Attribute:
        sources = {
            "coal": (self.coal_price, cite(
                self, "Van Eck coal price (NamPower, FY2022/23) per MWh of coal, using the coal "
                      "energy content implied by the NIRP heat rate and coal use; N$ to euros "
                      "at the 2023 Bank of Namibia rate.",
                "nampower_prices", "nirp_2022", "monetary_conversion")),
            "hfo": (self.hfo_price, cite(
                self, "Estimated 2023 delivered HFO price for Anixas: the NIRP 2020 delivered "
                      "price minus the 2020 INSEE market price gives a delivery cost, which is "
                      "scaled to 2023 with the Namibian CPI and added to the 2023 INSEE market "
                      "price; N$ to euros at the Bank of Namibia rates.",
                "nirp_2022", "insee", "assumptions", "monetary_conversion")),
            "biomass": (self.biomass_price, cite(
                self, "Otjikoto wood-chip price per tonne divided by the wood-chip energy "
                      "content; N$ to euros at the 2023 Bank of Namibia rate.",
                "nampower_otjikoto", "monetary_conversion")),
        }
        price, source = sources[element.name]
        return element.price_import.set_data(
            default_value=price(), unit=f"Euro/({element.power_unit}*h)", source=source)
