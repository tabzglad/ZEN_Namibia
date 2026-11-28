onshore_wind_turbine
====================

lifetime
--------

Step 1
Assumption: renewable_plant_lifetime = 25 year: placeholder lifetime of photovoltaics and onshore wind; to be replaced with a sourced value

capacity_existing
-----------------

Step 1
Existing 2023 wind fleet per node: plants in renewable_plants.csv at their node.

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

capacity_limit
--------------

Step 1
Existing wind fleet per node in the reference year (calibrated 2023 run); unlimited in later years (assumption) at the nodes with an existing plant, and so an hourly profile: NAM_COAST, NAM_SOUTH; zero elsewhere.

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

capacity_lower_limit
--------------------

Step 1
Existing fleet per node plus committed projects online by each year: Diaz Wind (44 MW at NAM_SOUTH, 2026).

**Citations**

- **manual_renewable_plants**: ZEN Namibia (2026). Namibia wind and solar plants in operation in 2023. ZEN Namibia.. Note: 2023 operating-plant roster compiled from the project list; profile files are from Renewables.ninja
- **renewables_ninja**: Pfenninger, S., Staffell, I. (2016). Long-term patterns of European PV output using 30 years of validated hourly reanalysis and satellite data. Energy. https://doi.org/10.1016/j.energy.2016.08.060
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **nampower_committed_projects**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Commissioned after 2023 or under construction (expansion pipeline sheet)
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

max_load
--------

Step 1
Hourly 2023 Renewables.ninja power profiles of the wind plants at each node, normalized by each profile's simulated capacity and weighted by installed capacity; at NAM_SOUTH scaled to a 34.8% annual capacity factor (NamPower P50 yield of the Rosh Pinah wind farm).

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

- **irena_africa_planning_2021**: IRENA (2021). Planning and Prospects for Renewable Power: Africa. International Renewable Energy Agency, Abu Dhabi. https://www.irena.org/publications/2021/March/Planning-and-prospects-for-renewable-power-Africa. Note: As used in the TMP (2023) least-cost study for Namibia, Table 2
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

capex_specific_conversion
-------------------------

Step 1
Capex per MW of Luderitz wind (Cerim, IPP), 50 MW, N$1.4 bn; N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nampower_project_costs**: NamPower, Electricity Control Board (2026). Namibia Power Plants 2023 & Expansion Pipeline. Project workbook compiled from NamPower Integrated Annual Reports 2022-2025 and the Electricity Control Board licence register.. Note: Project cost / capacity, nominal N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR