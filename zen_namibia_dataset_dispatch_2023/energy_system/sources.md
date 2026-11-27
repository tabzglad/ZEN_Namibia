energy_system_namibia
=====================

discount_rate
-------------

Step 1
https://iopscience.iop.org/article/10.1088/1748-9326/ac228a

**Citation**

Löffler, Konstantin (2021). Social discounting, social costs of carbon, and their use in energy system models. Environmental Research Letters. https://doi.org/10.1088/1748-9326/ac228a

----

Step 2
Assumption: discount_rate = 0.08 1: 8% real, typical for utility investment in southern Africa; NamPower does not disclose its WACC (workbook sheet Capex & financial)

knowledge_depreciation_rate
---------------------------

Step 1
Taken from [leibowicz_2016].

**Citation**

Leibowicz, B. D., Krey, V., Grubler, A. (2016). Representing spatial technology diffusion in an energy system optimization model. Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2015.06.001

market_share_unbounded
----------------------

Step 1
Taken from [Mannhardt_2024]

**Citation**

Mannhardt, J., Gabrielli, P., Sansavini, G. (2024). Understanding the vicious cycle of myopic foresight and constrained technology deployment in transforming the European energy system. iScience. https://doi.org/10.1016/j.isci.2024.111369

set_nodes
---------

Step 1
Namibia and the neighbours it trades with, at their capital cities.

**Citation**

ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Coordinates of the capital cities

set_edges
---------

Step 1
One directed edge per direction of each SAPP interconnector in the model.

**Citations**

- **sapp_transfer_limits**: Southern African Power Pool (2023). SAPP interconnector transfer limits. SAPP Transfer Limits table (sapp.co.zw/transfer-limits). https://www.sapp.co.zw/transfer-limits. Note: Table is undated; applicable limit = lowest of thermal, voltage and stability limits