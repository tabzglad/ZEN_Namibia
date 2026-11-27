hydrogen_storage
================

lifetime
--------

Step 1
Assumption: hydrogen_storage_lifetime = 30 year: pressure vessel lifetime

capacity_limit
--------------

Step 1
Assumption: not built in the reference year (the calibrated 2023 fleet); unlimited in Namibia in later years; not allowed at the neighbouring nodes.

opex_specific_fixed
-------------------

Step 1
Assumed fixed O&M share of capex per year times the compressor capex.

**Citations**

- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **rozzi_hydrogen_storage**: Rozzi, E., Minuto, F. D., Lanzini, A. (2024). Techno-economic dataset for hydrogen storage-based microgrids. Data in Brief 56, 110795. https://doi.org/10.1016/j.dib.2024.110795. Note: Reference cost of the compressor cost function, Table 4 (units inferred from Table 3)

efficiency_charge
-----------------

Step 1
Assumption: hydrogen_storage_charge_efficiency = 0.93 1: about 2.3 kWh/kg compression energy, modelled as a hydrogen loss on charging

capex_specific_storage
----------------------

Step 1
Compressor capex per kW of electrical input (Rozzi et al. 2024) times the compression energy share of the hydrogen charged (1 - charge efficiency, assumption).

**Citations**

- **rozzi_hydrogen_storage**: Rozzi, E., Minuto, F. D., Lanzini, A. (2024). Techno-economic dataset for hydrogen storage-based microgrids. Data in Brief 56, 110795. https://doi.org/10.1016/j.dib.2024.110795. Note: Reference cost of the compressor cost function, Table 4 (units inferred from Table 3)
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.

capex_specific_storage_energy
-----------------------------

Step 1
US DOE stationary tank capex target per kg divided by the lower heating value of hydrogen; USD to euros at the 2023 ECB rate.

**Citations**

- **us_doe_hydrogen_storage**: US Department of Energy (2020). Hydrogen Delivery Technical Targets. DOE Hydrogen and Fuel Cell Technologies Office, Multi-Year Program Plan. https://www.energy.gov/eere/fuelcells/doe-technical-targets-hydrogen-delivery. Note: Stationary gaseous storage, 160 bar, FY2020 purchased capital cost target
- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

capacity_limit_energy
---------------------

Step 1
Assumption: not built in the reference year (the calibrated 2023 fleet); unlimited in Namibia in later years; not allowed at the neighbouring nodes.

opex_specific_fixed_energy
--------------------------

Step 1
Assumed fixed O&M share of capex per year times the tank capex.

**Citations**

- **assumptions**: ZEN Namibia (2026). ZEN Namibia modelling assumptions. ZEN Namibia, data/raw_data/05-assumptions/zen_namibia_assumptions.csv.
- **us_doe_hydrogen_storage**: US Department of Energy (2020). Hydrogen Delivery Technical Targets. DOE Hydrogen and Fuel Cell Technologies Office, Multi-Year Program Plan. https://www.energy.gov/eere/fuelcells/doe-technical-targets-hydrogen-delivery. Note: Stationary gaseous storage, 160 bar, FY2020 purchased capital cost target
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR