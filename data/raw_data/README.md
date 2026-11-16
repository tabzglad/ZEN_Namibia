# Namibia energy model data

This folder holds the raw data and assumptions for the Namibia energy model for 2023.

## Input files

The folders follow ZEN-europe: `<category>/<source>/`. Each source folder is read
by the dataset class with the same name in `zen_namibia/datasets/datasets/`.

| Folder | Files | Content |
| --- | --- | --- |
| `02-carrier/nampower/` | `demand.csv` | annual energy use, average and peak demand, sales |
| | `imports_exports.csv` | annual imports by origin and exports (GWh); not used by the model at the moment |
| `02-carrier/pypsa/` | `hourly_demand_2023.csv` | hourly 2023 demand shape |
| `03-technology/nampower/` | `capacities.csv` | installed plant capacities per year (MW) |
| `03-technology/renewables_ninja/` | `pv_<site>.csv`, `wind_<site>.csv` | hourly 2023 output of each wind and solar site |
| | `weather_ruacana_2023.csv` | hourly 2023 weather near Ruacana, for hydro availability |
| `03-technology/manual_renewable_plants/` | `renewable_plants.csv` | own list of wind and solar plants: capacity and profile file |

## How the 2023 model is set up

The demand profile has 8,760 hourly values. The two missing year-end values were filled, then the profile was scaled to NamPower's 2023 figures: 4,055 GWh of energy use and a 632 MW peak.

The model uses existing capacity only: 347 MW hydro, 120 MW coal, 22.5 MW diesel, 5.22 MW wind and 292.9 MW solar. Wind and solar availability changes hour by hour using the supplied plant profiles. Each profile is normalized by its Renewables.ninja simulation capacity, scaled to the plant's installed capacity, and combined into a technology-wide availability profile. Solar availability is zero at night. The capacity factors in `renewable_plants.csv` are calculated from these profiles; they differ from earlier estimates for Miles 7, Gaib Solar and Rosh Pinah.

Hydro availability follows a seasonal profile based on precipitation near Ruacana. The weather point does not measure river flow. The profile is calibrated to a 1,323 GWh annual upper limit from NamPower's fiscal-year 2023 report, so treat it as an assumption for calendar 2023, not measured monthly generation.

## Important limitations

Several inputs are still estimates. Conversion efficiencies use the plants' full-load heat rates in Namibia's 2022 National Integrated Resource Plan: about 22.8% for Van Eck coal and 44.8% for Anixas. The Van Eck table's heat-rate unit appears inconsistent, so its value is interpreted as GJ/MWh, consistent with the report's coal-consumption figure. Anixas burns HFO in operation; diesel/LFO is used for starting and flashing, although the model's input carrier is still named `diesel`. Fuel prices, plant operating costs and import prices are missing, so total cost is not meaningful. The hourly generation mix is a model result, not recorded plant dispatch.

## Sources

Demand, capacities, imports and sales are based on the baseline workbook, PyPSA demand data, and NamPower reports and statistics for 2019–2025. Van Eck and Anixas heat rates are from the [Namibia NIRP Review and Update (2022)](https://www.mme.gov.na/files/publications/611_NIRP_2022for_theElectricitySupplyIndustry_NamibiaSigned.pdf). Wind and solar profiles are from Renewables.ninja under the CC BY 4.0 license; the files were renamed to `pv_<site>.csv` and `wind_<site>.csv`, and each keeps its original attribution header. Hydro weather is from Renewables.ninja. The PDFs remain in their original Downloads folder.
