"""Helpers that build ZEN-garden data frames from the model years. They hold no data."""
from __future__ import annotations

from math import inf
from typing import Callable

import pandas as pd
from zen_creator import Attribute, Element
from zen_creator.datasets.datasets.metadata import AssumptionInformation

DOMESTIC_NODE = "NAM"


def model_years(element: Element) -> list[int]:
    """Optimized years: reference year plus interval steps."""
    system = element.config.system
    return [
        system.reference_year + i * system.interval_between_years
        for i in range(system.optimized_years)
    ]


def capacity_existing_df(capacity: float, reference_year: int, node: str = DOMESTIC_NODE,
                         name: str = "capacity_existing") -> pd.DataFrame | None:
    """Return the existing fleet as one vintage built in the reference year.

    ZEN-garden needs a construction year for each existing-capacity row. For
    this one-year snapshot, the reference year is used as the vintage so the
    reported fleet remains available during the modeled year. Returns None
    when there is no capacity, so no vintage row is written.
    """
    if capacity <= 0:
        return None
    return pd.DataFrame(
        {name: [capacity]},
        index=pd.MultiIndex.from_tuples([(node, reference_year)], names=["node", "year_construction"]),
    )


def capacity_limit_df(element: Element, existing: float, expandable: bool,
                      name: str = "capacity_limit", node: str = DOMESTIC_NODE) -> pd.DataFrame:
    """Capacity limit per year: only the existing capacity in the reference year
    (2023 stays the calibrated fleet), unlimited later if expandable. Other nodes
    take the attribute's default of zero."""
    reference_year = element.config.system.reference_year
    years = model_years(element)
    limits = [existing if (year == reference_year or not expandable) else inf for year in years]
    return pd.DataFrame(
        {name: limits},
        index=pd.MultiIndex.from_tuples([(node, y) for y in years], names=["node", "year"]),
    )


def capacity_lower_limit_df(element: Element, existing: float,
                            committed_by_year: Callable[[int], float],
                            name: str = "capacity_lower_limit",
                            node: str = DOMESTIC_NODE) -> pd.DataFrame | None:
    """Minimum capacity in each year after the reference year: existing capacity
    plus committed projects online by that year. None if only the reference
    year is optimized."""
    reference_year = element.config.system.reference_year
    later = [y for y in model_years(element) if y > reference_year]
    if not later:
        return None
    return pd.DataFrame(
        {name: [existing + committed_by_year(y) for y in later]},
        index=pd.MultiIndex.from_tuples([(node, y) for y in later], names=["node", "year"]),
    )


def new_technology_capacity_limit(element: Element, name: str = "capacity_limit",
                                  unit: str | None = None) -> Attribute:
    """Capacity limit of a technology that Namibia did not have in the reference
    year: none in that year, unlimited in Namibia later, none at other nodes."""
    return getattr(element, name).set_data(
        default_value=0.0,
        unit=unit or element.power_unit,
        df=capacity_limit_df(element, 0.0, expandable=True, name=name),
        source=AssumptionInformation(
            description=(
                "Assumption: not built in the reference year (the calibrated 2023 fleet); "
                "unlimited in Namibia in later years; not allowed at the neighbouring nodes."
            )
        ),
    )
