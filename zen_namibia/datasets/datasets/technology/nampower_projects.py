"""NamPower project workbook: capex of recent projects and committed projects
(03-technology/nampower_projects/)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import SourceInformation

from zen_namibia.utils import capacity_lower_limit_df


def _folder(source_path: Path) -> Path:
    return Path(source_path) / "03-technology" / "nampower_projects"


def _workbook_metadata(name: str, note: str) -> MetaData:
    return MetaData(
        name=name,
        title="Namibia Power Plants 2023 & Expansion Pipeline",
        author=["NamPower", "Electricity Control Board"],
        publication=(
            "Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 "
            "and the Electricity Control Board licence register"
        ),
        publication_year=2026,
        note=note,
    )


class NamPowerProjectCosts(Dataset[pd.DataFrame]):
    """Capital costs of new plants from NamPower's own projects (N$, 2022-2025)."""

    name = "nampower_project_costs"

    def _set_metadata(self) -> MetaData:
        return _workbook_metadata(self.name, "Project cost / capacity, nominal N$")

    def _set_path(self) -> Path:
        return _folder(self.source_path) / "investment_costs.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        required = {"technology", "capex_nad_per_kw", "capex_nad_per_kwh", "lifetime_years"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError("investment_costs.csv is missing columns: " + ", ".join(sorted(missing)))
        if data["technology"].duplicated().any():
            raise ValueError("investment_costs.csv has duplicate technologies")
        return data.set_index("technology")

    def _value(self, technology: str, column: str) -> float:
        value = float(self.data.loc[technology, column])
        if not value > 0:
            raise ValueError(f"investment_costs.csv needs a positive {column} for {technology}")
        return value

    def capex_nad_per_mw(self, technology: str) -> float:
        """Capex per MW of power, in N$."""
        return self._value(technology, "capex_nad_per_kw") * 1000.0

    def capex_nad_per_mwh(self, technology: str) -> float:
        """Capex per MWh of storage energy, in N$."""
        return self._value(technology, "capex_nad_per_kwh") * 1000.0

    def reference_project(self, technology: str) -> str:
        return str(self.data.loc[technology, "reference_project"])

    def get_lifetime(self, element: Element) -> Attribute:
        return element.lifetime.set_data(
            default_value=int(self._value(element.name, "lifetime_years")), unit="1",
            source=SourceInformation(
                description=f"Design lifetime of {self.reference_project(element.name)}.",
                metadata=self.metadata,
            ),
        )


class NamPowerCommittedProjects(Dataset[pd.DataFrame]):
    """Projects built after 2023 or under construction, fixed in later years."""

    name = "nampower_committed_projects"

    def _set_metadata(self) -> MetaData:
        return _workbook_metadata(
            self.name, "Commissioned after 2023 or under construction (expansion pipeline sheet)"
        )

    def _set_path(self) -> Path:
        return _folder(self.source_path) / "committed_projects.csv"

    def _set_data(self) -> pd.DataFrame:
        data = pd.read_csv(self.path)
        required = {"project", "technology", "capacity_mw", "energy_mwh", "node", "expected_cod"}
        missing = required.difference(data.columns)
        if missing:
            raise ValueError("committed_projects.csv is missing columns: " + ", ".join(sorted(missing)))
        for column in ["capacity_mw", "energy_mwh", "expected_cod"]:
            data[column] = pd.to_numeric(data[column], errors="raise")
        if (data["capacity_mw"] <= 0).any():
            raise ValueError("committed_projects.csv needs positive capacity_mw")
        return data

    def projects(self, technology: str) -> pd.DataFrame:
        return self.data.loc[self.data["technology"] == technology]

    def committed_by(self, technology: str, year: int, column: str = "capacity_mw",
                     node: str | None = None) -> float:
        """Capacity (MW, or MWh for energy_mwh) of a technology online by a year,
        at one node or in total."""
        rows = self.projects(technology)
        rows = rows.loc[rows["expected_cod"] <= year]
        if node is not None:
            rows = rows.loc[rows["node"] == node]
        return float(rows[column].fillna(0.0).sum())

    def nodes(self, technology: str) -> list[str]:
        """Nodes with committed projects of a technology."""
        return list(dict.fromkeys(self.projects(technology)["node"]))

    def describe(self, technology: str) -> str:
        rows = self.projects(technology)
        if rows.empty:
            return "no committed projects"
        return ", ".join(f"{r.project} ({r.capacity_mw:g} MW at {r.node}, {r.expected_cod:.0f})"
                         for r in rows.itertuples())

    def get_capacity_lower_limit(self, element: Element, energy: bool = False) -> Attribute:
        """Minimum capacity in later years: the committed projects online by then
        at their nodes (for technologies with no capacity in the reference year)."""
        name = "capacity_lower_limit_energy" if energy else "capacity_lower_limit"
        column = "energy_mwh" if energy else "capacity_mw"
        unit = f"{element.power_unit}*h" if energy else element.power_unit
        return getattr(element, name).set_data(
            default_value=0.0, unit=unit,
            df=capacity_lower_limit_df(
                element, {},
                lambda node, year: self.committed_by(element.name, year, column, node),
                self.nodes(element.name), name=name),
            source=SourceInformation(
                description=f"Committed projects online by each year: {self.describe(element.name)}.",
                metadata=self.metadata,
            ),
        )

    def get_energy_to_power_ratio(self, element: Element, bound: str) -> Attribute:
        """Fixed storage duration (h) of the committed projects of a storage technology."""
        rows = self.projects(element.name)
        ratios = (rows["energy_mwh"] / rows["capacity_mw"]).unique()
        if len(ratios) != 1:
            raise ValueError(f"Committed {element.name} projects need one energy-to-power ratio")
        return getattr(element, f"energy_to_power_ratio_{bound}").set_data(
            default_value=float(ratios[0]), unit="h",
            source=SourceInformation(
                description=f"Duration of the committed projects: {self.describe(element.name)}.",
                metadata=self.metadata,
            ),
        )
