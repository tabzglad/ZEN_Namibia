from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

from zen_namibia.datasets.datasets.carrier.nampower import load_costs


class HydrogenAssumptions(Dataset[pd.DataFrame]):
    """Green hydrogen demand (Hyphen Phase 1) and electrolyser and storage costs."""

    name = "hydrogen_assumptions"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Green hydrogen demand and technology assumptions",
            author=["ZEN Namibia"],
            publication="Hyphen project updates (Engineering News 2026, Windhoek Express 2025), IEA, US DOE",
            publication_year=2026,
            note="Values and sources in 03-technology/hydrogen/hydrogen.csv; several are flagged assumptions",
        )

    def _set_path(self) -> Path:
        return Path(self.source_path) / "03-technology" / "hydrogen" / "hydrogen.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        if not {"item", "value"}.issubset(data.columns) or data["item"].duplicated().any():
            raise ValueError("hydrogen.csv needs unique items with values")
        data["value"] = pd.to_numeric(data["value"], errors="raise")
        return data.set_index("item")

    def value(self, item: str) -> float:
        return float(self.data.loc[item, "value"])

    def _usd_to_euro(self, usd: float) -> float:
        return usd / load_costs(self.source_path).value("usd_per_eur_2023")

    def demand_mw(self) -> float:
        """Flat hydrogen demand in MW (LHV) from the annual tonnes."""
        mwh_per_year = self.value("hydrogen_demand") * self.value("hydrogen_lhv")  # t * MWh/t
        return mwh_per_year / 8760.0

    def electrolyser_capex_euro_per_mw(self) -> float:
        """Capex per MW of electricity input."""
        return self._usd_to_euro(self.value("electrolyser_capex") * 1000.0)

    def storage_compressor_capex_euro_per_mw(self) -> float:
        """Compressor cost per MW of hydrogen charging: EUR/kW of compressor
        power times the compression energy per unit of hydrogen charged."""
        compression_share = 1.0 - self.value("hydrogen_storage_charge_efficiency")
        return self.value("hydrogen_storage_compressor_capex") * 1000.0 * compression_share

    def storage_capex_euro_per_mwh(self) -> float:
        """Capex per MWh of stored hydrogen (LHV)."""
        return self._usd_to_euro(self.value("hydrogen_storage_capex") / self.value("hydrogen_lhv") * 1000.0)


@lru_cache(maxsize=None)
def hydrogen_assumptions(source_path: Path | str) -> HydrogenAssumptions:
    return HydrogenAssumptions(source_path)
