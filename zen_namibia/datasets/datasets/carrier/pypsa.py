from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from zen_creator import Dataset, MetaData

STEPS_PER_YEAR = 8760


class PyPSA(Dataset[pd.DataFrame]):
    """Hourly 2023 electricity demand shape for Namibia from PyPSA."""

    name = "pypsa"
    profile_year = 2023

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="Hourly electricity demand for Namibia",
            author=["PyPSA"],
            publication="PyPSA",
            publication_year=2023,
            note="exact PyPSA model and version still to be documented",
        )

    def _set_path(self) -> Path:
        return (
            self.source_path / "02-carrier" / "pypsa"
            / f"hourly_demand_{self.profile_year}.csv"
        )

    def _set_data(self) -> pd.DataFrame:
        hourly = pd.read_csv(self.path, parse_dates=["time"])
        if set(hourly.columns) != {"time", "demand_mw"}:
            raise ValueError(f"{self.path.name} must contain time,demand_mw")
        hourly["demand_mw"] = pd.to_numeric(hourly["demand_mw"], errors="raise")
        expected_time = pd.date_range(
            f"{self.profile_year}-01-01 00:00:00", periods=STEPS_PER_YEAR, freq="h"
        )
        if len(hourly) != STEPS_PER_YEAR or not hourly["time"].equals(
            pd.Series(expected_time)
        ):
            raise ValueError(
                f"{self.profile_year} hourly demand must contain every hour from "
                "Jan 1 00:00 through Dec 31 23:00 exactly once"
            )
        if hourly["demand_mw"].isna().any() or not np.isfinite(hourly["demand_mw"]).all():
            raise ValueError(f"{self.path.name} contains missing or non-finite demand")
        if (hourly["demand_mw"] < 0).any():
            raise ValueError("hourly demand values must be non-negative")
        profile = hourly[["demand_mw"]].copy()
        profile.index = pd.RangeIndex(STEPS_PER_YEAR, name="time")
        return profile

    def peak_hours(self, count: int) -> pd.Index:
        """Return the time steps of the ``count`` highest-demand hours."""
        return self.data["demand_mw"].nlargest(count).index
