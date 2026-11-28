from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from zen_creator import Attribute, Dataset, DatasetCollection, Element
from zen_creator.utils.attribute import SourceInformation

from zen_namibia.datasets.datasets.carrier.nampower import NamPowerDemand
from zen_namibia.datasets.datasets.carrier.nirp import NIRPDemandGrowth
from zen_namibia.datasets.datasets.carrier.pypsa import STEPS_PER_YEAR, PyPSA
from zen_namibia.datasets.dataset_collections.regional_demand_shares import RegionalDemandShares
from zen_namibia.utils import model_years


class ElectricityDemand(DatasetCollection):
    """Hourly demand: the PyPSA shape scaled to NamPower's annual energy and peak.

    Later optimized years scale the whole hourly profile by a yearly factor:
    NamPower's reported energy where available (demand.csv), otherwise the
    last reported year grown at the NIRP 2022 rate (2.7% per year).
    """

    name = "electricity_demand"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> dict[str, Dataset[Any] | DatasetCollection]:
        return {
            "nampower_demand": NamPowerDemand(self.source_path),
            "pypsa": PyPSA(self.source_path),
            "nirp_growth": NIRPDemandGrowth(self.source_path),
            "regional_shares": RegionalDemandShares(self.source_path),
        }

    def energy_gwh(self, year: int) -> float:
        """Annual energy demand: NamPower actual if reported, else NIRP growth
        from the last reported year."""
        reported = self.data["nampower_demand"].data.set_index("year")[
            "energy_consumption_gwh"
        ]
        if year in reported.index:
            return float(reported[year])
        if year < reported.index.min():
            raise ValueError(f"No demand data or projection before {reported.index.min()}")
        last = int(reported.index.max())
        rate = self.data["nirp_growth"].annual_growth_rate()
        return float(reported[last]) * (1.0 + rate) ** (year - last)

    def yearly_variation(self, element: Element) -> pd.DataFrame:
        """Demand in each optimized year relative to the reference year."""
        years = model_years(element)
        base = self.energy_gwh(element.config.system.reference_year)
        factors = [self.energy_gwh(year) / base for year in years]
        return pd.DataFrame(
            {node: factors for node in self.data["regional_shares"].shares().index},
            index=pd.Index(years, name="year"),
        )

    def _profile_for_year(self, year: int) -> pd.Series:
        """Scale the PyPSA data to NamPower's data."""
        row = self.data["nampower_demand"].demand_in(year)
        average_demand_mw = float(row["demand_mw"])
        energy_consumption_gwh = float(row["energy_consumption_gwh"])
        peak_demand_mw = float(row["peak_demand_mw"])

        pypsa = self.data["pypsa"]
        if year != pypsa.profile_year:
            return pd.Series(np.full(STEPS_PER_YEAR, average_demand_mw),
                             index=pd.RangeIndex(STEPS_PER_YEAR, name="time"))

        demand = pypsa.data["demand_mw"].astype(float).copy()
        # Fill the two known zero rows by interpolating across the year boundary.
        if demand.iloc[-2:].eq(0).all():
            last_valid, first = demand.iloc[-3], demand.iloc[0]
            demand.iloc[-2] = last_valid + (first - last_valid) / 3
            demand.iloc[-1] = last_valid + 2 * (first - last_valid) / 3
        source_mean = float(demand.mean())
        source_peak = float(demand.max())
        target_mean = energy_consumption_gwh * 1000 / STEPS_PER_YEAR
        if source_peak <= source_mean:
            raise ValueError(
                f"{year} hourly demand must have a peak above its annual mean"
            )
        spread_scale = (peak_demand_mw - target_mean) / (source_peak - source_mean)
        demand = (demand - source_mean) * spread_scale + target_mean
        if (demand < 0).any():
            raise ValueError(
                f"Calibrating {year} demand to NamPower energy and peak produced "
                "negative values"
            )
        return pd.Series(demand.to_numpy(), index=pd.RangeIndex(STEPS_PER_YEAR, name="time"))

    def regional_profiles(self, year: int) -> pd.DataFrame:
        """National hourly profile split over the Namibian nodes by their share
        of annual demand (the same hourly shape at every node: no regional
        load shapes are published)."""
        national = self._profile_for_year(year)
        shares = self.data["regional_shares"].shares()
        return pd.DataFrame({node: national.to_numpy() * share for node, share in shares.items()},
                            index=national.index)

    def get_demand(self, element: Element) -> Attribute:
        """Create the 8760-hour demand profile for the configured reference year."""
        reference_year = element.config.system.reference_year
        profile_year = self.data["pypsa"].profile_year
        rate = self.data["nirp_growth"].annual_growth_rate()
        return element.demand.set_data(
            default_value=0.0,
            unit=element.power_unit,
            df=self.regional_profiles(reference_year),
            yearly_variations_df=self.yearly_variation(element),
            source=SourceInformation(
                description=(
                    "Hourly electricity demand profile for reference year "
                    f"{reference_year}; PyPSA hourly shape calibrated to NamPower "
                    f"annual energy and peak for {profile_year}, flat annual "
                    "average otherwise. Later optimized years scale the profile "
                    "with NamPower reported energy, then NIRP 2022 growth of "
                    f"{rate:.1%} per year. Split over the Namibian nodes by their share of "
                    "annual use: distributor sales (ECB 2022) plus the largest mines ("
                    + ", ".join(f"{n} {v:.1%}" for n, v in
                                self.data["regional_shares"].shares().items()) + ")."
                ),
                metadata=self.metadata,
            ),
        )
