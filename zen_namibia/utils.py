from __future__ import annotations

import pandas as pd


def capacity_existing_df(capacity: float, reference_year: int) -> pd.DataFrame | None:
    """Return the existing fleet as one vintage built in the reference year.

    ZEN-garden needs a construction year for each existing-capacity row. For
    this one-year snapshot, the reference year is used as the vintage so the
    reported fleet remains available during the modeled year. Returns None
    when there is no capacity, so no vintage row is written.
    """
    if capacity <= 0:
        return None
    return pd.DataFrame(
        {"capacity_existing": [capacity]},
        index=pd.MultiIndex.from_tuples(
            [("NAM", reference_year)], names=["node", "year_construction"]
        ),
    )
