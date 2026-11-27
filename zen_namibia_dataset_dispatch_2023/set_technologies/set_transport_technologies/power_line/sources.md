power_line
==========

lifetime
--------

Step 1
Assumption: power_line_lifetime = 40 year: placeholder lifetime of the cross-border lines; irrelevant while lines cannot be expanded

capacity_existing
-----------------

Step 1
SAPP applicable transfer limit per direction (model_limit_mw in interconnectors.csv; parallel lines summed; the listed direction is assumed for the reverse direction too).

**Citation**

Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits

capacity_limit
--------------

Step 1
Lines are not expandable: each edge is capped at its transfer limit.

**Citation**

Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits

opex_specific_variable
----------------------

Step 1
Assumption: power_line_wheeling_cost = 0.01 EUR/MWh: numerical tie-breaker, not a tariff: without it, flows in both directions or wheeling through Namibia cost nothing and the reported line flows are arbitrary

distance
--------

Step 1
Great-circle distance between the capital cities of the two nodes (informative only: no line losses or costs).

**Citations**

- **sapp_transfer_limits**: Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Coordinates of the capital cities