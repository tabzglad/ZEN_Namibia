photovoltaics
=============

lifetime
--------

Step 1
Assumption: renewable_plant_lifetime = 25 year: placeholder lifetime of photovoltaics and onshore wind; to be replaced with a sourced value

capacity_existing
-----------------

Step 1
Existing 2023 solar fleet per node: plants in renewable_plants.csv at their node, plus NamPower's Omburu PV unit (capacities.csv).

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

capacity_limit
--------------

Step 1
Existing solar fleet per node in the reference year (calibrated 2023 run); unlimited in later years (assumption) at the nodes with an existing plant, and so an hourly profile: NAM_CENTRAL, NAM_SOUTH, NAM_NORTH, NAM_COAST; zero elsewhere.

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

capacity_lower_limit
--------------------

Step 1
Existing fleet per node plus committed projects online by each year: Khan Solar PV (20 MW at NAM_COAST, 2025), Otjikoto Solar (ISPS) (10 MW at NAM_NORTH, 2025), Sores Gaib (Rosh Pinah) PV (100 MW at NAM_SOUTH, 2027).

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **renewables_ninja**: Pfenninger, S., Staffell, I. (2016). Long-term patterns of European PV output using 30 years of validated hourly reanalysis and satellite data. Energy. https://doi.org/10.1016/j.energy.2016.08.060
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **nampower_committed_projects**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

max_load
--------

Step 1
Hourly 2023 Renewables.ninja power profiles of the solar plants at each node, normalized by each profile's simulated capacity and weighted by installed capacity.

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **renewables_ninja**: Pfenninger, S., Staffell, I. (2016). Long-term patterns of European PV output using 30 years of validated hourly reanalysis and satellite data. Energy. https://doi.org/10.1016/j.energy.2016.08.060
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

opex_specific_fixed
-------------------

Step 1
IRENA fixed O&M (USD/kW/year), not scaled with CPI because these costs have fallen over time; USD to euros at the 2023 ECB rate. Variable O&M is taken as zero.

**Citations**

- **irena_renewable_costs_2023**: IRENA (2024). Renewable Power Generation Costs in 2023. International Renewable Energy Agency, Abu Dhabi. https://www.irena.org/Publications/2024/Sep/Renewable-Power-Generation-Costs-in-2023. Note: Average all-in O&M cost of utility-scale solar PV in 2023 (global survey), 2023 USD
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

capex_specific_conversion
-------------------------

Step 1
Capex per MW of Sores Gaib (Rosh Pinah) PV, 100 MW, N$1.621 bn; N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nampower_project_costs**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Project cost / capacity, nominal N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR