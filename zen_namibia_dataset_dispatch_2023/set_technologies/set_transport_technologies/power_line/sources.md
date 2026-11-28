power_line
==========

lifetime
--------

Step 1
Assumption: power_line_lifetime = 40 year: placeholder lifetime of the cross-border lines; irrelevant while lines cannot be expanded

capacity_existing
-----------------

Step 1
Lines in service in 2023: SAPP transfer limit per direction for the cross-border lines; for NamPower's internal corridors, the circuits in service times an assumed capacity per circuit by voltage (surge impedance loading).

**Citations**

- **sapp_transfer_limits**: Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits
- **manual_transmission**: ZEN Namibia (2026). NamPower transmission lines between the model's Namibian nodes. ZEN Namibia, data/raw_data/03-technology/manual_transmission/corridors.csv.. Note: Compiled from NamPower ECC renewal applications (MEFT EIA portal, 2020-2025), World Bank P177328 appraisal (2023), Windhoek Express (2024) and Windhoek Observer (2026)
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

capacity_limit
--------------

Step 1
Lines in service in each year, not expandable beyond them: SAPP transfer limit per direction for the cross-border lines; for NamPower's internal corridors, the circuits in service times an assumed capacity per circuit by voltage (surge impedance loading).

**Citations**

- **sapp_transfer_limits**: Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits
- **manual_transmission**: ZEN Namibia (2026). NamPower transmission lines between the model's Namibian nodes. ZEN Namibia, data/raw_data/03-technology/manual_transmission/corridors.csv.. Note: Compiled from NamPower ECC renewal applications (MEFT EIA portal, 2020-2025), World Bank P177328 appraisal (2023), Windhoek Express (2024) and Windhoek Observer (2026)
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

capacity_lower_limit
--------------------

Step 1
Lines in service in each later year must be built, including those commissioned after the reference year: SAPP transfer limit per direction for the cross-border lines; for NamPower's internal corridors, the circuits in service times an assumed capacity per circuit by voltage (surge impedance loading).

**Citations**

- **sapp_transfer_limits**: Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits
- **manual_transmission**: ZEN Namibia (2026). NamPower transmission lines between the model's Namibian nodes. ZEN Namibia, data/raw_data/03-technology/manual_transmission/corridors.csv.. Note: Compiled from NamPower ECC renewal applications (MEFT EIA portal, 2020-2025), World Bank P177328 appraisal (2023), Windhoek Express (2024) and Windhoek Observer (2026)
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

opex_specific_variable
----------------------

Step 1
Assumption: power_line_wheeling_cost = 0.01 EUR/MWh: numerical tie-breaker, not a tariff: without it, flows in both directions or wheeling through Namibia cost nothing and the reported line flows are arbitrary

distance
--------

Step 1
Great-circle distance between the coordinates of the two nodes (informative only: no line losses or costs).

**Citations**

- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town