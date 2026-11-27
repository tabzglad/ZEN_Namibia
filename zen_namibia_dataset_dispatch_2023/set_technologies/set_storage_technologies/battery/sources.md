battery
=======

lifetime
--------

Step 1
Assumption: battery_lifetime = 15 year: lithium-ion battery lifetime

capacity_limit
--------------

Step 1
Assumption: not built in the reference year (the calibrated 2023 fleet); unlimited in Namibia in later years; not allowed at the neighbouring nodes.

capacity_lower_limit
--------------------

Step 1
Committed projects online by each year: Omburu BESS (51 MW, 2026).

**Citation**

NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)

efficiency_charge
-----------------

Step 1
Square root of the round-trip efficiency (battery_round_trip_efficiency = 0.9 1: typical lithium-ion round-trip efficiency)

efficiency_discharge
--------------------

Step 1
Square root of the round-trip efficiency (battery_round_trip_efficiency = 0.9 1: typical lithium-ion round-trip efficiency)

capex_specific_storage_energy
-----------------------------

Step 1
Capex per MWh of storage (whole project cost) of Omburu BESS, 51 MW / 51 MWh, N$500 m; whole cost put on storage energy (1-hour battery); N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nampower_project_costs**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Project cost / capacity, nominal N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

capacity_limit_energy
---------------------

Step 1
Assumption: not built in the reference year (the calibrated 2023 fleet); unlimited in Namibia in later years; not allowed at the neighbouring nodes.

capacity_lower_limit_energy
---------------------------

Step 1
Committed projects online by each year: Omburu BESS (51 MW, 2026).

**Citation**

NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)

opex_specific_fixed_energy
--------------------------

Step 1
Assumed share of capex per year (see the assumptions file) times the capex per MWh.

**Citations**

- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **nampower_project_costs**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Project cost / capacity, nominal N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

energy_to_power_ratio_min
-------------------------

Step 1
Duration of the committed projects: Omburu BESS (51 MW, 2026).

**Citation**

NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)

energy_to_power_ratio_max
-------------------------

Step 1
Duration of the committed projects: Omburu BESS (51 MW, 2026).

**Citation**

NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)