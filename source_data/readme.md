# Namibia baseline source data

These three CSV files hold the baseline values used by the ZEN-garden Namibia model.

## Files

- `capacities.csv`: installed capacity by plant category and year (MW). Ruacana maps to hydro, Van Eck to coal/thermal, Anixas to diesel, and Omburu to photovoltaic capacity.
- `imports.csv`: annual imports (GWh), supplier breakdown, reported import share, and exports. Supplier volumes are retained as source data; the model currently uses aggregate imports/exports.
- `demands.csv`: annual energy consumption (GWh), average demand (MW), peak demand (MW), sales to Namibia customers, and total units sold.

## Sources

The values were transcribed from the Namibia baseline workbook `baseline_data_nam.xlsx` and cross-referenced against the NamPower annual reports and electricity statistics provided for this project:

- `NamPower_Annual_Report_2020.pdf` (2019–2020 baseline values)
- `NamPower_Annual_Report_2021.pdf` (2021 values)
- `NamPower_Annual_Report_2022_Integrated.pdf` (2022 values)
- `NamPower_Annual_Report_2023_Integrated.pdf` (2023 values)
- `NamPower_Integrated_Annual_Report_2024.pdf` (2024 values)
- `Electricity_July-2026.pdf` (2025 values)

The PDFs remain in their original Downloads folders and are not copied into this directory.

## Calculations and interpretation

- `average_demand_mw` is annual energy consumption in GWh divided by 8.76 (the annual hours-to-MW conversion for 8,760 hours), rounded to six decimal places.
- The annual reports distinguish energy consumption, sales, exports, and total units sold. These columns are preserved separately; they are not interchangeable measures.
- Supplier imports are kept separately in `imports.csv`. The current ZEN-garden model has one aggregate electricity-import variable, so it uses the total imports column as an annual upper bound rather than assigning flows to each supplier.
- Plant capacities are transcribed annual installed-capacity values. The model's existing-capacity parameters use the 2019 reference-year plant values. Van Eck is mapped to coal steam, Anixas to diesel generation, Ruacana to hydro, and Omburu to PV.
- Coal steam and diesel generation now name `coal` and `diesel` as input carriers. Their fuel import availability is currently a large placeholder, with zero fuel prices and a 1:1 conversion factor; replace these assumptions when fuel supply and plant-efficiency data are available. Wind, hydro, and PV have no fuel input; the natural-gas turbine remains linked to `natural_gas`.
- Dashes or blank capacity entries in the source table are represented as zero where no capacity was listed.
- This baseline workbook does not provide generation fuel use, technology conversion efficiencies, or fuel prices. Those assumptions require separate sources before they can be calibrated.
