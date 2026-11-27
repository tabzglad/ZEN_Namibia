from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Dataset, MetaData


class NamPowerImportContracts(Dataset[pd.DataFrame]):
    """NamPower's bilateral import contracts (ZESCO, ZPC, Eskom) and SAPP trade."""

    name = "nampower_import_contracts"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="NamPower electricity import contracts",
            author=["Lusaka Times", "The Brief", "NewsDay", "Southern Eye", "Republikein"],
            publication="Namibian, Zambian and Zimbabwean press reports (2014-2024)",
            publication_year=2024,
            note="Contract sizes from press reports; contract prices are not published",
        )

    def _set_path(self) -> Path:
        return self.source_path / "02-carrier" / "nampower" / "import_contracts.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        required = {"supplier", "node", "contract_mw", "cap_in_model"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError(
                "import_contracts.csv is missing columns: " + ", ".join(sorted(missing))
            )
        flags = data["cap_in_model"].str.strip().str.lower()
        if not flags.isin(["yes", "no"]).all():
            raise ValueError("import_contracts.csv cap_in_model must be yes or no")
        data["cap_in_model"] = flags == "yes"
        data["contract_mw"] = pd.to_numeric(data["contract_mw"], errors="raise")
        capped = data.loc[data["cap_in_model"]]
        if capped["contract_mw"].isna().any() or (capped["contract_mw"] <= 0).any():
            raise ValueError("import_contracts.csv needs a positive contract_mw for capped contracts")
        return data

    def import_caps_mw(self) -> pd.Series:
        """Hourly import limit per node in MW from the capped contracts."""
        capped = self.data.loc[self.data["cap_in_model"]]
        return capped.groupby("node")["contract_mw"].sum()
