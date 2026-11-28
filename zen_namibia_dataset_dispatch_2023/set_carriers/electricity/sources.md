electricity
===========

demand
------

Step 1
Hourly electricity demand profile for reference year 2023; PyPSA hourly shape calibrated to NamPower annual energy and peak for 2023, flat annual average otherwise. Later optimized years scale the profile with NamPower reported energy, then NIRP 2022 growth of 2.7% per year. Split over the Namibian nodes by their share of annual use: distributor sales (ECB 2022) plus the largest mines (NAM_NORTH 30.0%, NAM_CENTRAL 32.0%, NAM_COAST 29.6%, NAM_SOUTH 8.5%).

**Citations**

- **nampower_demand**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **pypsa**: PyPSA (2023). Hourly electricity demand for Namibia. PyPSA.. Note: exact PyPSA model and version still to be documented
- **nirp_growth**: Ministry of Mines and Energy, Namibia (2022). NIRP Review and Update 2022: load forecast. National Integrated Resource Plan (NIRP) 2022, as cited in the TMP (2023) least-cost study for Namibia. https://www.internationalrivers.org/wp-content/uploads/sites/86/2023/07/TMP-report-Namibia-2023.pdf. Note: 2.7% per year average growth of electricity demand 2021-2040
- **regional_shares**:
  - **ecb_distribution_sales**: Electricity Control Board (2024). Electricity Supply Industry Statistical Bulletin 2022. Electricity Control Board, Namibia. https://www.ecb.org.na/wp-content/uploads/2024/02/ECB-Statistical-Bulletin-2022-draft-3.pdf. Note: Appendix Tables 6-8, pp. 42-43: domestic, commercial and large power user sales per licensee; rows matched to licensees with Tables 3-5 and 9-11
  - **manual_large_customers**: ZEN Namibia (2026). Electricity use of Namibia's largest mines. ZEN Namibia, data/raw_data/02-carrier/manual_large_customers/large_customers.csv.. Note: Compiled from Swakop Uranium (2024), Rossing (2023), Dundee Precious Metals (2022) and pv magazine (2024); some values derived or estimated (basis column)
  - **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
  - **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

availability_import
-------------------

Step 1
No imports at the Namibian nodes; hourly imports at the contract nodes capped at the contract size (ZESCO 180 MW, ZPC 80 MW); Eskom and SAPP market imports at South Africa limited only by the interconnector.

**Citations**

- **nampower_import_contracts**: Lusaka Times, The Brief, NewsDay, Southern Eye, Republikein (2024). NamPower electricity import contracts. Namibian, Zambian and Zimbabwean press reports (2014-2024).. Note: Contract sizes from press reports; contract prices are not published
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

availability_export
-------------------

Step 1
Exports only at ZAF (NamPower's exports are SAPP market sales).

**Citations**

- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town

availability_export_yearly
--------------------------

Step 1
Exports at ZAF unbounded in 2023; in later years capped at NamPower's 2025 exports (539 GWh).

**Citation**

NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook

price_import
------------

Step 1
ZAF (SAPP market and Eskom): SAPP day-ahead monthly price for each hour's time-of-use period (Eskom Megaflex hours), USD to euros at the ECB monthly rate. Other nodes (ZESCO and ZPC contracts): NamPower's average import price (contract prices are not published), N$ to euros at the 2023 Bank of Namibia rate.

**Citations**

- **sapp_market_prices**: Southern African Power Pool (2023). SAPP monthly market performance reports 2023. SAPP Market Performance Reports. https://www.sapp.co.zw/market-reports. Note: Monthly average DAM clearing price and monthly average off-peak, standard and peak prices (USc/kWh); hours mapped to periods with Eskom's Megaflex definitions
- **nampower_prices**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

price_export
------------

Step 1
Exports at ZAF earn the hourly SAPP price, capped at NamPower's average import price so that contract imports are not resold into SAPP.

**Citations**

- **sapp_market_prices**: Southern African Power Pool (2023). SAPP monthly market performance reports 2023. SAPP Market Performance Reports. https://www.sapp.co.zw/market-reports. Note: Monthly average DAM clearing price and monthly average off-peak, standard and peak prices (USc/kWh); hours mapped to periods with Eskom's Megaflex definitions
- **nampower_prices**: NamPower (2025). NamPower annual reports and statistics 2019-2025. NamPower Integrated Annual Reports.. Note: compiled in the ZEN Namibia baseline workbook
- **manual_nodes**: ZEN Namibia (2026). ZEN Namibia nodes. ZEN Namibia, data/raw_data/01-energy_system/manual_nodes/nodes.csv.. Note: Namibian nodes group the administrative regions; coordinates of a main town
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

price_shed_demand
-----------------

Step 1
Assumption: value_of_lost_load = 10000 EUR/MWh: cost of unmet electricity demand, as in ZEN-europe (price_shed_demand of 10,000 EUR/MWh); high enough that the model only leaves demand unmet when supply and imports cannot cover it