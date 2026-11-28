hydro_turbine
=============

lifetime
--------

Step 1
Assumption: existing_plant_lifetime = 25 year: placeholder lifetime of the existing coal, HFO and hydro plants (Van Eck, Anixas I, Ruacana); irrelevant while they cannot be expanded; to be replaced with plant data

capacity_existing
-----------------

Step 1
Installed capacity in 2023 (ruacana_hydro_mw in capacities.csv, 347 MW) at NAM_NORTH, as one vintage built in 2023.

**Citations**

- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

capacity_limit
--------------

Step 1
Capped at the installed capacity in every year (not expandable); zero at all other nodes.

**Citations**

- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

max_load
--------

Step 1
Monthly availability from rainfall near Ruacana (Renewables.ninja MERRA-2), smoothed with a centred rolling mean plus a base flow (assumptions), scaled so that the annual upper bound equals NamPower's Ruacana generation (1,323 GWh, FY2022/23, used as a calendar-2023 value). Rainfall is only a seasonal proxy for river flow.

**Citations**

- **renewables_ninja**: Pfenninger, S., Staffell, I. (2016). Long-term patterns of European PV output using 30 years of validated hourly reanalysis and satellite data. Energy. https://doi.org/10.1016/j.energy.2016.08.060
- **nampower_capacities**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **manual_plant_locations**: ZEN Namibia (2026). Location of NamPower's power stations. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/plant_locations.csv.

opex_specific_fixed
-------------------

Step 1
NIRP 2022 fixed O&M of Ruacana (N$/kW/year, 2020-2021 data), scaled to 2023 with the Namibian CPI; N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nirp_2022**: Ministry of Mines and Energy, Namibia (2022). National Integrated Resource Plan (NIRP) Review and Update 2022 for the Electricity Supply Industry. Ministry of Mines and Energy, Namibia. https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf. Note: Costs based on 2020-2021 data, in N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR