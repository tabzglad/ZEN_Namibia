electrolyser
============

lifetime
--------

Step 1
Assumption: electrolyser_lifetime = 25 year: plant lifetime; stack replacements counted in fixed O&M

capacity_limit
--------------

Step 1
Assumption: not built in the reference year (the calibrated 2023 fleet); unlimited in later years only at NAM_SOUTH, the node of Hyphen's hydrogen plant; not allowed at the neighbouring nodes.

opex_specific_fixed
-------------------

Step 1
Fixed O&M of 1.5% of capex per year (IEA 2019) times the IEA 2024 capex.

**Citations**

- **iea_future_of_hydrogen_2019**: IEA (2019). The Future of Hydrogen: Seizing today's opportunities. International Energy Agency, Paris. https://www.iea.org/reports/the-future-of-hydrogen. Note: Assumptions annex
- **iea_global_hydrogen_review_2024**: IEA (2024). Global Hydrogen Review 2024. International Energy Agency, Paris. https://www.iea.org/reports/global-hydrogen-review-2024. Note: Stated Policies 2030 installed cost of non-Chinese electrolysers, as reported by Argus Media (Oct 2024)
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

capex_specific_conversion
-------------------------

Step 1
IEA 2030 installed electrolyser cost per kW of electricity input; USD to euros at the 2023 ECB rate.

**Citations**

- **iea_global_hydrogen_review_2024**: IEA (2024). Global Hydrogen Review 2024. International Energy Agency, Paris. https://www.iea.org/reports/global-hydrogen-review-2024. Note: Stated Policies 2030 installed cost of non-Chinese electrolysers, as reported by Argus Media (Oct 2024)
- **monetary_conversion**:
  - **bank_of_namibia**: Bank of Namibia (2026). Quarterly Bulletin: foreign exchange rates and consumer price index. Bank of Namibia Quarterly Bulletin (December 2024, March 2026). https://www.bon.com.na. Note: Annual averages computed from the monthly period averages; 2023 N$/EUR from the December 2024 bulletin, Table IV.J, p. 147; CPI from the March 2026 bulletin
  - **ecb**: European Central Bank (2024). Euro foreign exchange reference rates, US dollar. ECB Data Portal, series EXR.A.USD.EUR.SP00.A and EXR.M.USD.EUR.SP00.A. https://data.ecb.europa.eu/data/datasets/EXR

conversion_factor
-----------------

Step 1
2030 electrolyser efficiency of 69% (LHV).

**Citation**

IEA (2019). The Future of Hydrogen: Seizing today's opportunities. International Energy Agency, Paris. https://www.iea.org/reports/the-future-of-hydrogen. Note: Assumptions annex