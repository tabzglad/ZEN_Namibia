from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData

COLUMNS = ["line", "node_from", "node_to", "voltage_kv", "circuits", "commissioned", "in_model"]


class ManualTransmission(Dataset[pd.DataFrame]):
    """NamPower's internal transmission lines between the Namibian nodes.

    Compiled per line from NamPower's environmental clearance applications
    (MEFT EIA portal), the World Bank's transmission project appraisal and
    press reports (see the source column). NamPower does not publish transfer
    limits, so the capacity per circuit is an assumption by voltage.
    """

    name = "manual_transmission"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="NamPower transmission lines between the model's Namibian nodes",
            author=["ZEN Namibia"],
            publication="ZEN Namibia, data/raw_data/03-technology/manual_transmission/corridors.csv",
            publication_year=2026,
            note=("Compiled from NamPower ECC renewal applications (MEFT EIA portal, 2020-2025), "
                  "World Bank P177328 appraisal (2023), Windhoek Express (2024) and Windhoek "
                  "Observer (2026)"),
        )

    def _set_path(self) -> Path:
        return self.source_path / "03-technology" / "manual_transmission" / "corridors.csv"

    def _set_data(self) -> pd.DataFrame:
        raw = pd.read_csv(self.path)
        missing = set(COLUMNS).difference(raw.columns)
        if missing:
            raise ValueError(f"corridors.csv is missing columns: {', '.join(sorted(missing))}")
        if raw["line"].duplicated().any():
            raise ValueError("corridors.csv has duplicate lines")
        data = raw.loc[raw["in_model"].str.strip().str.lower() == "yes"].copy()
        if (data["node_from"] == data["node_to"]).any():
            raise ValueError("corridors.csv: a modelled line must join two different nodes")
        data["voltage_kv"] = pd.to_numeric(data["voltage_kv"], errors="raise").astype(int)
        data["circuits"] = pd.to_numeric(data["circuits"], errors="raise").astype(int)
        existing = data["commissioned"].astype(str).str.strip().str.lower() == "existing"
        data["commissioned"] = pd.to_numeric(data["commissioned"].where(~existing, 0),
                                             errors="raise").astype(int)
        return data

    def lines_online(self, year: int) -> pd.DataFrame:
        """Lines in service in a year (existing lines have commissioned = 0)."""
        return self.data.loc[self.data["commissioned"] <= year]
