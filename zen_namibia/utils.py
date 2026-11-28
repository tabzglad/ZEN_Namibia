"""Helpers that build ZEN-garden data frames from the model years. They hold no data."""
from __future__ import annotations

from math import inf
from typing import Callable, Iterable, Mapping

import pandas as pd
from zen_creator import Element


def model_years(element: Element) -> list[int]:
    """Optimized years: reference year plus interval steps."""
    system = element.config.system
    return [
        system.reference_year + i * system.interval_between_years
        for i in range(system.optimized_years)
    ]


def _ordered(*node_lists: Iterable[str]) -> list[str]:
    """Union of node lists, in order of first appearance."""
    return list(dict.fromkeys(node for nodes in node_lists for node in nodes))


def capacity_existing_df(capacity_by_node: Mapping[str, float], reference_year: int,
                         name: str = "capacity_existing") -> pd.DataFrame | None:
    """Return the existing fleet at each node as one vintage built in the reference year.

    ZEN-garden needs a construction year for each existing-capacity row. The
    reference year is used as the vintage so the reported fleet remains
    available during the modeled year. Returns None when there is no
    capacity, so no vintage row is written.
    """
    rows = {node: mw for node, mw in capacity_by_node.items() if mw > 0}
    if not rows:
        return None
    return pd.DataFrame(
        {name: list(rows.values())},
        index=pd.MultiIndex.from_tuples(
            [(node, reference_year) for node in rows], names=["node", "year_construction"]),
    )


def capacity_limit_df(element: Element, existing_by_node: Mapping[str, float],
                      expandable_nodes: Iterable[str] = (),
                      name: str = "capacity_limit") -> pd.DataFrame:
    """Capacity limit per node and year: only the existing capacity in the
    reference year (2023 stays the calibrated fleet); in later years unlimited
    at the expandable nodes and the existing capacity elsewhere. Nodes not
    listed take the attribute's default of zero."""
    reference_year = element.config.system.reference_year
    expandable = set(expandable_nodes)
    nodes = _ordered(existing_by_node, expandable_nodes)
    rows = {
        (node, year): (inf if year != reference_year and node in expandable
                       else existing_by_node.get(node, 0.0))
        for node in nodes for year in model_years(element)
    }
    return pd.DataFrame(
        {name: list(rows.values())},
        index=pd.MultiIndex.from_tuples(list(rows), names=["node", "year"]),
    )


def capacity_lower_limit_df(element: Element, existing_by_node: Mapping[str, float],
                            committed_by: Callable[[str, int], float],
                            nodes: Iterable[str],
                            name: str = "capacity_lower_limit") -> pd.DataFrame | None:
    """Minimum capacity at each node in each year after the reference year:
    existing capacity plus committed projects online by that year (committed_by:
    node, year -> MW). None if only the reference year is optimized."""
    reference_year = element.config.system.reference_year
    later = [y for y in model_years(element) if y > reference_year]
    if not later:
        return None
    rows = {(node, year): existing_by_node.get(node, 0.0) + committed_by(node, year)
            for node in _ordered(existing_by_node, nodes) for year in later}
    return pd.DataFrame(
        {name: list(rows.values())},
        index=pd.MultiIndex.from_tuples(list(rows), names=["node", "year"]),
    )
