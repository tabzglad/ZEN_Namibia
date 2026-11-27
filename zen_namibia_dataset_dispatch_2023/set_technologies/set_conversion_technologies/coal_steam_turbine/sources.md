coal_steam_turbine
==================

lifetime
--------

Step 1
Assumption: existing_plant_lifetime = 25 year: placeholder lifetime of the existing coal, HFO and hydro plants (Van Eck, Anixas I, Ruacana); irrelevant while they cannot be expanded; to be replaced with plant data

capacity_existing
-----------------

Step 1
Installed capacity in 2023 (van_eck_thermal_mw in capacities.csv), as one vintage built in 2023.

**Citation**

NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook

capacity_limit
--------------

Step 1
Capped at the installed capacity in the reference year in every year (not expandable); zero at the neighbouring nodes.

**Citation**

NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook

max_load
--------

Step 1
Van Eck available capacity / nameplate in 2023 (96 MW / 120 MW).

**Citation**

NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook

opex_specific_variable
----------------------

Step 1
NIRP 2022 variable O&M of Van_Eck (N$/kWh, 2020-2021 data, excluding fuel), scaled to 2023 with the Namibian CPI; N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nirp_2022**: Ministry of Mines and Energy, Namibia (2022). National Integrated Resource Plan (NIRP) Review and Update 2022 for the Electricity Supply Industry. Ministry of Mines and Energy, Namibia. https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf. Note: Costs based on 2020-2021 data, in N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

opex_specific_fixed
-------------------

Step 1
NIRP 2022 fixed O&M of Van Eck (N$/kW/year, 2020-2021 data), scaled to 2023 with the Namibian CPI; N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **nirp_2022**: Ministry of Mines and Energy, Namibia (2022). National Integrated Resource Plan (NIRP) Review and Update 2022 for the Electricity Supply Industry. Ministry of Mines and Energy, Namibia. https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf. Note: Costs based on 2020-2021 data, in N$
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

conversion_factor
-----------------

Step 1
Full-load heat rate of Van Eck (15.81 GJ/MWh) / 3.6 GJ/MWh.

**Citation**

Ministry of Mines and Energy, Namibia (2022). National Integrated Resource Plan (NIRP) Review and Update 2022 for the Electricity Supply Industry. Ministry of Mines and Energy, Namibia. https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf. Note: Costs based on 2020-2021 data, in N$