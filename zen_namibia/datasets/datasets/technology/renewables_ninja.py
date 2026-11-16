from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

STEPS_PER_YEAR = 8760


class RenewablesNinja(Dataset[dict[str, pd.Series]]):
    """Renewables.ninja hourly 2023 wind and solar profiles for Namibian sites.

    The data maps each ``pv_<site>.csv`` and ``wind_<site>.csv`` file name to
    its hourly output as a fraction of the simulated capacity. The same folder
    holds the Renewables.ninja (MERRA-2) weather series near Ruacana, used for
    hydro availability.
    """

    name = "renewables_ninja"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title=(
                "Long-term patterns of European PV output using 30 years of "
                "validated hourly reanalysis and satellite data"
            ),
            author=["Pfenninger, S.", "Staffell, I."],
            publication="Energy",
            publication_year=2016,
            url="https://www.renewables.ninja",
            doi="10.1016/j.energy.2016.08.060",
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "renewables_ninja"

    def _set_data(self) -> dict[str, pd.Series]:
        profiles = {
            profile_path.name: _load_hourly_profile(profile_path)
            for pattern in ("pv_*.csv", "wind_*.csv")
            for profile_path in sorted(self.path.glob(pattern))
        }
        if not profiles:
            raise FileNotFoundError(f"No Renewables.ninja profiles in {self.path}")
        return profiles

    def capacity_factor(self, profile_file: str) -> pd.Series:
        """Return one site's hourly output as a fraction of its capacity."""
        if profile_file not in self.data:
            raise FileNotFoundError(
                f"Missing Renewables.ninja profile {profile_file} in {self.path}"
            )
        return self.data[profile_file]

    def hydro_precipitation(self) -> pd.DataFrame:
        """Return hourly 2023 precipitation (mm/h) near Ruacana."""
        weather_path = self.path / "weather_ruacana_2023.csv"
        weather = pd.read_csv(weather_path, comment="#", parse_dates=["time"])
        required = {"time", "prectotland"}
        missing = required.difference(weather.columns)
        if missing:
            raise ValueError(
                "weather_ruacana_2023.csv is missing columns: "
                f"{', '.join(sorted(missing))}"
            )
        if len(weather) != STEPS_PER_YEAR or weather["time"].isna().any():
            raise ValueError("Hydro weather must contain 8,760 valid 2023 hourly rows")
        if (
            weather["time"].dt.year.nunique() != 1
            or int(weather["time"].dt.year.iloc[0]) != 2023
        ):
            raise ValueError("weather_ruacana_2023.csv must contain calendar-year 2023")
        weather["prectotland"] = pd.to_numeric(weather["prectotland"], errors="raise")
        if weather["prectotland"].isna().any() or (weather["prectotland"] < 0).any():
            raise ValueError(
                "Hydro weather precipitation must be complete and non-negative"
            )
        return weather[["time", "prectotland"]]


def _load_hourly_profile(profile_path: Path) -> pd.Series:
    """Read and validate one 2023 Renewables.ninja hourly power profile."""
    metadata = None
    with profile_path.open(encoding="utf-8-sig") as profile_file:
        for line in profile_file:
            line = line.strip()
            if line.startswith("# {"):
                metadata = json.loads(line[2:])
                break
    if metadata is None:
        raise ValueError(
            f"No Renewables.ninja simulation metadata in {profile_path.name}"
        )
    params = metadata.get("params", {})
    if params.get("date_from") != "2023-01-01" or params.get("date_to") != "2023-12-31":
        raise ValueError(f"{profile_path.name} must cover calendar year 2023")
    if params.get("local_time") not in {False, "false", "False", 0}:
        raise ValueError(f"{profile_path.name} must use UTC timestamps")
    if str(metadata.get("units", {}).get("electricity", "")).lower() != "kw":
        raise ValueError(f"{profile_path.name} electricity values must be in kW")
    simulated_capacity_kw = float(params.get("capacity", 0))
    if simulated_capacity_kw <= 0:
        raise ValueError(f"{profile_path.name} has invalid simulated capacity")

    data = pd.read_csv(profile_path, comment="#", parse_dates=["time"])
    if not {"time", "electricity"}.issubset(data.columns):
        raise ValueError(
            f"{profile_path.name} must include time and electricity columns"
        )
    expected_time = pd.date_range("2023-01-01 00:00", periods=STEPS_PER_YEAR, freq="h")
    if len(data) != len(expected_time) or not pd.DatetimeIndex(data["time"]).equals(
        expected_time
    ):
        raise ValueError(
            f"{profile_path.name} must contain consecutive hourly UTC data for 2023"
        )
    power_kw = pd.to_numeric(data["electricity"], errors="raise")
    if power_kw.isna().any() or (power_kw < 0).any():
        raise ValueError(f"{profile_path.name} has missing or negative generation")
    availability = power_kw / simulated_capacity_kw
    if (availability > 1.001).any():
        raise ValueError(f"{profile_path.name} exceeds its simulated capacity")
    return availability.clip(lower=0.0, upper=1.0).reset_index(drop=True)
