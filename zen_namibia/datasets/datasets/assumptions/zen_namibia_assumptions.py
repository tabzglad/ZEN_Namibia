from __future__ import annotations

from pathlib import Path

import pandas as pd
from zen_creator import Attribute, Dataset, Element, MetaData
from zen_creator.datasets.datasets.metadata import AssumptionInformation

from zen_namibia.datasets.datasets._item_table import ItemValues, read_item_table


class ZENNamibiaAssumptions(ItemValues, Dataset[pd.DataFrame]):
    """All modelling assumptions of ZEN Namibia that are not taken from a source.

    Each value is in ``05-assumptions/zen_namibia_assumptions.csv`` with a
    description of why it was chosen.
    """

    name = "zen_namibia_assumptions"

    def _set_metadata(self) -> MetaData:
        return MetaData(
            name=self.name,
            title="ZEN Namibia modelling assumptions",
            author=["ZEN Namibia"],
            publication="ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv",
            publication_year=2026,
        )

    def _set_path(self) -> Path:
        return self.source_path / "05-assumptions" / "zen_namibia_assumptions.csv"

    def _set_data(self) -> pd.DataFrame:
        return read_item_table(self.path, note_column="description")

    def assumption(self, *items: str, description: str | None = None) -> AssumptionInformation:
        """Describe one or more assumptions, for an attribute's sources."""
        rows = [
            f"{item} = {self.data.loc[item, 'value']:g} {self.data.loc[item, 'unit']}: "
            f"{self.data.loc[item, 'description']}"
            for item in items
        ]
        text = "; ".join(rows)
        return AssumptionInformation(
            description=f"{description} ({text})" if description else f"Assumption: {text}",
            metadata=self.metadata,
        )

    def get_attribute(
        self, element: Element, attribute: str, item: str, unit: str | None = None
    ) -> Attribute:
        """Set an attribute to one assumed value."""
        return getattr(element, attribute).set_data(
            default_value=self.value(item), unit=unit, source=self.assumption(item)
        )

    def get_lifetime(self, element: Element, item: str) -> Attribute:
        return getattr(element, "lifetime").set_data(
            default_value=int(self.value(item)), unit="1", source=self.assumption(item)
        )
