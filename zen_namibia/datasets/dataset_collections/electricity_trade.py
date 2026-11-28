from __future__ import annotations

from math import inf
from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element

from zen_namibia.datasets.dataset_collections._sources import cite
from zen_namibia.datasets.dataset_collections.monetary_conversion import MonetaryConversion
from zen_namibia.datasets.datasets.carrier.nampower import NamPowerPrices, NamPowerTrade
from zen_namibia.datasets.datasets.carrier.nampower_import_contracts import (
    NamPowerImportContracts,
)
from zen_namibia.datasets.datasets.carrier.pypsa import STEPS_PER_YEAR
from zen_namibia.datasets.datasets.carrier.sapp import TOU_COLUMNS, SAPPMarketPrices
from zen_namibia.datasets.datasets.energy_system.manual_nodes import ManualNodes


class ElectricityTrade(DatasetCollection):
    """Electricity imports and exports at the neighbouring nodes.

    - South Africa (SAPP market and Eskom): hourly SAPP time-of-use price,
      limited only by the interconnector; the only node that exports.
    - Zambia and Zimbabwe (ZESCO and ZPC contracts): NamPower's average
      import price, capped at the contract sizes.
    """

    name = "electricity_trade"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset | DatasetCollection]:
        return {
            "sapp_market_prices": SAPPMarketPrices(self.source_path),
            "nampower_prices": NamPowerPrices(self.source_path),
            "nampower_trade": NamPowerTrade(self.source_path),
            "nampower_import_contracts": NamPowerImportContracts(self.source_path),
            "manual_nodes": ManualNodes(self.source_path),
            "monetary_conversion": MonetaryConversion(self.source_path),
        }

    @property
    def _nodes(self) -> ManualNodes:
        return self.data["manual_nodes"]

    def contract_price(self) -> float:
        """NamPower's average import price, used for the ZESCO and ZPC contracts."""
        nad = self.data["nampower_prices"].value("electricity_import_price")
        return self.data["monetary_conversion"].nad_to_euro(nad)

    def sapp_price(self, year: int) -> np.ndarray:
        """Hourly SAPP price in euros: each month's off-peak, standard or peak
        price, converted at that month's ECB USD/EUR rate."""
        sapp = self.data["sapp_market_prices"]
        usd_per_eur = self.data["monetary_conversion"].monthly_usd_per_eur(year)
        monthly = {period: sapp.monthly_usd_per_mwh(year, period) / usd_per_eur
                   for period in TOU_COLUMNS}
        return sapp.hourly_from_monthly(year, monthly)

    def _hourly(self, attr: Attribute, default: float, unit: str,
                by_node: dict[str, np.ndarray | float], source) -> Attribute:
        df = pd.DataFrame(
            {node: np.ones(STEPS_PER_YEAR) * values for node, values in by_node.items()},
            index=pd.RangeIndex(STEPS_PER_YEAR, name="time"),
        )
        return attr.set_data(default_value=default, unit=unit, df=df, source=source)

    def get_price_import(self, element: Element) -> Attribute:
        sapp_node = self._nodes.sapp_market_node()
        return self._hourly(
            element.price_import, self.contract_price(), f"Euro/({element.power_unit}*h)",
            {sapp_node: self.sapp_price(element.config.system.reference_year)},
            cite(self, f"{sapp_node} (SAPP market and Eskom): SAPP day-ahead monthly price for "
                       "each hour's time-of-use period (Eskom Megaflex hours), USD to euros at "
                       "the ECB monthly rate. Other nodes (ZESCO and ZPC contracts): NamPower's "
                       "average import price (contract prices are not published), N$ to euros "
                       "at the 2023 Bank of Namibia rate.",
                 "sapp_market_prices", "nampower_prices", "manual_nodes", "monetary_conversion"),
        )

    def get_price_export(self, element: Element) -> Attribute:
        """Exports earn the hourly SAPP price, capped at the contract import price.

        The cap stops the model from buying contract power from Zambia or
        Zimbabwe and reselling it into SAPP when the market is dearer.
        """
        sapp_node = self._nodes.sapp_market_node()
        export = np.minimum(self.sapp_price(element.config.system.reference_year),
                            self.contract_price())
        return self._hourly(
            element.price_export, 0.0, f"Euro/({element.power_unit}*h)", {sapp_node: export},
            cite(self, f"Exports at {sapp_node} earn the hourly SAPP price, capped at NamPower's "
                       "average import price so that contract imports are not resold into SAPP.",
                 "sapp_market_prices", "nampower_prices", "manual_nodes", "monetary_conversion"),
        )

    def get_availability_import(self, element: Element) -> Attribute:
        """No imports at the Namibian nodes; contract nodes capped at the contract
        size; South Africa limited only by the interconnector."""
        domestic = self._nodes.domestic_nodes()
        caps = self.data["nampower_import_contracts"].import_caps_mw().to_dict()
        if set(domestic) & set(caps):
            raise ValueError("import_contracts.csv cannot cap imports at a Namibian node")
        return self._hourly(
            element.availability_import, inf, element.power_unit,
            {**{node: 0.0 for node in domestic}, **caps},
            cite(self, "No imports at the Namibian nodes; hourly imports at the contract nodes capped "
                       "at the contract size (ZESCO 180 MW, ZPC 80 MW); Eskom and SAPP market "
                       "imports at South Africa limited only by the interconnector.",
                 "nampower_import_contracts", "manual_nodes"),
        )

    def get_availability_export(self, element: Element) -> Attribute:
        """Exports are SAPP market sales, so only the SAPP node can export.

        Exporting at a contract node would let the model buy and resell there
        at the same price when SAPP exceeds the contract price.
        """
        sapp_node = self._nodes.sapp_market_node()
        no_export = self._nodes.nodes().drop(sapp_node)
        return self._hourly(
            element.availability_export, inf, element.power_unit,
            {node: 0.0 for node in no_export},
            cite(self, f"Exports only at {sapp_node} (NamPower's exports are SAPP market sales).",
                 "manual_nodes"),
        )

    def get_availability_export_yearly(self, element: Element) -> Attribute:
        return self.data["nampower_trade"].get_availability_export_yearly(
            element, self._nodes.sapp_market_node())
