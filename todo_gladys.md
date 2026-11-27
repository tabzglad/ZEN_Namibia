## Setup
- Use zen-creator 2.1.0 or newer: `pip install --upgrade zen-creator`

## Current scope
Details and sources: `data/raw_data/README.md`.

- **Model:** hourly, cost-driven; 2023 (calibrated fleet, no new capacity) and 2030 (investment allowed), 8% discount rate.
- **Investment (2030):** PV, onshore wind, engines, biomass, batteries; capex from NamPower projects (`03-technology/expansion/`); committed projects (Anixas II, Rosh Pinah PV, Omburu BESS, Otjikoto biomass, Diaz wind, ...) fixed; coal, hydro, Anixas I and lines not expandable.
- **Green hydrogen (2030):** Hyphen Phase 1, 175 kt H2/yr (666 MW flat) from 2028; grid-connected electrolysers (69%, $1,350/kW) and compressed storage ($700/kg) sized by the model (`03-technology/hydrogen/`).
- **Wind:** Renewables.ninja profile scaled to a 34.8% capacity factor (NamPower Rosh Pinah P50).
- **Demand growth:** later years scale 2023 demand: NamPower actuals to 2025, then NIRP 2.7%/yr (4,938 GWh in 2030, 6,445 GWh in 2040). Set `optimized_years` / `interval_between_years` to use it.
- **Nodes:** Namibia (demand and plants); South Africa, Zambia, Zimbabwe (trade only).
- **Lines:** South Africa 575 MW, Zambia 300 MW, Kariba (Zambia–Zimbabwe) 428 MW.
- **Imports:** South Africa at the SAPP time-of-use price (monthly off-peak/standard/peak, Eskom hours, €20–229/MWh); ZESCO (180 MW) and ZPC (80 MW) contracts at €95/MWh.
- **Exports:** via South Africa only, hourly SAPP price capped at €95/MWh; after 2023 capped at 539 GWh/yr (NamPower 2025 exports).
- **Costs:** coal, estimated HFO price, NIRP and IRENA O&M, in 2023 euros.

## Current results
2023 + 2030 with hydrogen: objective €1.70 bn (results in `outputs_dispatch_2023/`). 2030: PV 3,658 MW, wind 366 MW, electrolyser 1,958 MW, hydrogen storage 7,389 MWh; imports 2,558 GWh, of which ~2,281 GWh while electrolysers run (no-imports-for-hydrogen rule not yet enforced); exports 539 GWh (at cap). Table below is the earlier 2023-only run (objective €197.88M).

| Item | Model (GWh) | NamPower (GWh) |
|---|---|---|
| Van Eck | 55.9 | 44.3 |
| Anixas I | 0 | 5–6 |
| Imports SA / Zambia / Zimbabwe | 1,578 / 459 / 143 | 676 / 1,478 / 330 |
| Exports | 11.6 | 198 |
| Ruacana hydro | 1,323 | 1,323 |
| PV / wind | 480.1 / 27.9 | not reported |

## Next steps
1. **Anixas I:** never runs (€400/MWh vs SAPP peak ≤ €229/MWh); it runs in real shortages, which the model lacks (SA imports unlimited up to the line). Also confirm SAPP's time-of-use hours (Eskom's assumed).
2. **Exports:** model exports only domestic surplus (11.6 GWh). NamPower's 198 GWh (FY2022/23) is mostly contract imports it could not use, resold to SAPP, which the model does not represent. For future years: revisit the €95/MWh export price cap and SAPP export limits.
3. **Zambia link:** 300 MW confirmed (IAR 2023 p. 22). The ZLI carried 1,396 GWh in FY2022/23, but the model routes only 603 GWh via Zambia (contracts at €95/MWh lose to off-peak SAPP via South Africa).
4. **Costs:** actual HFO price; check NIRP O&M; ZESCO and ZPC contract prices; IPP contract prices for PV and wind.
5. **Demand growth:** check 2.7% in the NIRP 2022 itself (Ch. 3, App. A2).
6. **Hydrogen:** rerun and read results; check the no-imports-for-hydrogen rule (compare 2030 imports with a run without hydrogen, add an import cap if they rise); verify the 69% electrolyser efficiency (IEA); add ammonia synthesis and desalination electricity; existing PV/wind are charged capex in 2023 (+€15.5M).
7. **Later:** line losses; Angola and Botswana links.


## Jans comments

### Structural comments
- For many items, you just set the attribute like this (see in biomass.py):
```python
return Attribute(
    "price_import",
    default_value=expansion_assumptions(self.source_path).biomass_fuel_price(),
    unit=f"Euro/({self.power_unit}*h)", element=self,
)
```
Which means that the source.md is not created. Ideally you should refer to a dataset or dataset collection entry (which you do here, but you didnt define a `get_price_import(element)` in the dataset entry, which should return  `element.price_import.set_data(...,source=SourceInformation(...))`).

You can compare your implementation with the one in Zen_Europe, to see how it should be done (that way you also create a source.md file in the output folder). See the documentation here: https://zen-europe.readthedocs.io/en/latest/files/developer_guide/extending.html#expose-attributes-through-get-attribute

- The conventions for dataset/ dataset collection definitions are not met. In your case a dataset actually contains multiple sources (see e.g. NamPowerCosts, which is a combination of multiple source `["NamPower", "Bank of Namibia", "ZEN Namibia"]`). Each of them should have their individual dataset. You can read up on the conventions here: https://zen-europe.readthedocs.io/en/latest/files/developer_guide/extending.html#one-source-one-dataset. 

- the elements should not read or transform data (this is done in the dataset/ dataset collections). `anixas_i.py` hardcodes the heat rate and the 21.5 MW net capacity.

- In the raw data: split files that mix sources into individual files (one file - one source and one dataset class).

- You can use dataset collections as you do now when you have combined datasets. A simple example is e.g. import/export prices for HFO, which is a combination of INSEE, NIRP and CPI, exchange rate) 

- CPI and exchange rates ccan go into `raw_data/04-monetary` and `datasets/financial`

- Whereever you make your own assumptions (which is totally fine!) just create one file in the raw_data and a corresponding dataset.

- You can check that each element folder in the final dataset has a sources.md file.

### Model comments
- Take into account exiting capacities and planned capacities, but also allow for a "generic" expansion. I.e. you can just build onshore wind, pv, etc. without having to specify a specific project. 
- If possible, I would suggest to have a higher spatial resolution of namibia (not neighboring countries), e.g. with 2-4 nodes in Namibia itself with respective power transmission between them. This is to capture spatial effects as well - e.g. you can only produce H2 at the coast.
- You can easily reduce the number of hours the model uses (Zen Europe only uses 5 hours, but I think you can go to 100-1000 hours).

### Scneario comments

- **Modelling electricity access and demand growth:** You currently assume an annual demand growth of 2.7%, which feels to me like a growth without an increase of access to electricity. I would suggest you also calculate (in addition to the current demand growth), the growth that would happen if everyone who does not have electricity today had electricity in 2040. You can essentially calculate the average electricity demand of a person today with electricity access, and scale that then to the total population in 2040. I would still suggest to keep the 2.7% growth as a general growth per capita ontop of the access growth. I suggest to then degine different scenarios: 
    - 2.7% growth per capita (constant electricity access rate)
    - 1-2 scenarios in between, e.g. electricity access targets of 80% and 90% or so
    - 2.7% growth per capita + access growth (everyone has electricity in 2040)
    - 
- **Modeling a budget:** I suggest to have the following scenarios (aligning with your MS teams message):
  - Domestic access priority: For 2030 and 2040: no hydrogen production with 3-4 different electricity access rates (see point above) -> Setting the baseline of how much does it cost to provide electricity access.
  - Hydrogen production in island mode for export: No interaction with the grid, but hydrogen production is allowed with additional solar/wind capacity. Technically, you do not need to run the full model then, because the H2 production is completly independent of the rest of the energy system. You can either define a H2 demand and calculate the respective cost for H2 or directly define a H2 price.
  - Hydrogen production with grid connection for export: Domestic access + hydrogen production with grid connection. Again with different access rates. Either with a H2 demand or a H2 price.
  - Integrated hydrogen system: Hydrogen production with grid connection for export and for domestic use. Again with different access rates. 
- You can either implicitly then calculate the budget from each scenario or explicitly define a budget that Namibia can spend on its energy system. We can talk about this in more detail - but this is independent from the scenario definitions.


### Midterm presentation
- Next week Thursday in the group meeting.
- 10 min presentation + Q&A
- Focus on the model that you build so far and show results for the runs of 2023 (potentially also for 2030 and 2040, if you have them)
- Then show the scenario definitions that you are planning to run.