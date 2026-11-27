# ZEN Namibia

ZEN-garden model of the Namibian electricity system, built with zen-creator.
The current setup is a fixed-fleet 2023 dispatch snapshot (8,760 hours, no
investment) with four nodes: Namibia (`NAM`) and its neighbours South Africa
(`ZAF`), Zambia (`ZMB`) and Zimbabwe (`ZWE`), joined by cross-border power
lines. Zimbabwe connects to Namibia only through Zambia.

## Setup

- Install conda and create the `ZEN-garden` environment
- Install zen-creator 2.1 or newer and ZEN-garden 3.1 or newer into it
- Install Gurobi (an academic licence is available)

## Workflow

Run both scripts from this folder (`ZEN_Namibia/`):

1. `python create_model.py` — builds the ZEN-garden dataset into
   `./zen_namibia_dataset_dispatch_2023/`
2. `python run_zen_garden.py` — writes `config_dispatch_2023.yaml`, solves the
   dataset and writes results into `./outputs_dispatch_2023/`

The dataset and output folder names are set in `global_vars.py` and
`run_zen_garden.py`.

## Where to find what

- `data/zen_namibia_config.yaml` — zen-creator config: reference year, time
  steps, and which carriers/technologies are inserted
- `data/raw_data/` — raw inputs, one folder per source
  (`<category>/<source>/`, as in ZEN-europe); see `data/raw_data/README.md`
  for files, sources and assumptions
The code follows the ZEN-europe conventions
([extending guide](https://zen-europe.readthedocs.io/en/latest/files/developer_guide/extending.html)):
data flows raw file → dataset (one source) → dataset collection (combines
sources) → element. Every attribute is set through `set_data(...,
source=...)`, so each element folder of the built dataset has a `sources.md`
listing where its values come from.

- `zen_namibia/elements/` — carriers, technologies and the energy system. Each
  `_set_<attribute>()` only chooses a dataset, collection or assumption; it
  does not read or transform data.
- `zen_namibia/datasets/datasets/` — one dataset class per source, by
  category: `energy_system/` (model nodes), `carrier/` (NamPower demand, trade
  and prices; import contracts; NIRP demand growth; PyPSA demand shape; SAPP
  market prices; INSEE HFO prices; Hyphen hydrogen project), `technology/`
  (NamPower capacities and plant performance; NamPower project costs and
  committed projects; Otjikoto fact sheet; NIRP 2022 plant data; IRENA;
  IEA; US DOE; Rozzi et al.; Renewables.ninja; SAPP transfer limits; own
  list of wind/solar plants), `financial/` (Bank of Namibia exchange rates and
  CPI; ECB exchange rates) and `assumptions/` (all of ZEN Namibia's own
  modelling assumptions, from `05-assumptions/zen_namibia_assumptions.csv`).
- `zen_namibia/datasets/dataset_collections/` — combine several sources:
  electricity demand and trade, fuel prices, technology costs, hydrogen
  demand and technology costs, renewable fleet, hydro and thermal
  availability, interconnectors, and currency conversion.
- `create_model.py` — builds and writes the dataset (existing-capacity
  vintages are set in the technology classes)
- `run_zen_garden.py` — solves the built dataset
- `global_vars.py` — shared paths used by both scripts

## Notes

- All year-dependent inputs follow `system.reference_year` in
  `data/zen_namibia_config.yaml`. The hourly demand profile in
  `hourly_demand_2023.csv` is only available for 2023; other years use a flat
  annual-average profile.
- Demand growth: with `optimized_years` > 1 (and `interval_between_years`),
  later years scale the hourly profile by a yearly factor
  (`demand_yearly_variation.csv`): NamPower's reported energy up to 2025
  (`demand.csv`), then 2.7% per year (NIRP 2022, `02-carrier/nirp/`). The
  default run optimizes 2023 only. The fleet stays fixed at 2023 unless
  `allow_investment` is switched on.
- Natural gas is not included until sourced 2023 capacity and fuel data are available.
- Import/export prices and the Van Eck coal price are NamPower's
  (`02-carrier/nampower/prices.csv`); the Anixas I 2023 HFO price is estimated
  from the NIRP 2020 price and INSEE market prices (`FuelPrices`). Van Eck, Anixas I
  and Ruacana O&M come from the NIRP (2020–2021 values); NIRP values are scaled to
  2023 prices with CPI. PV and wind fixed O&M come from IRENA (PV 2023 survey,
  wind Africa 2021) and are not CPI-scaled, because these costs have fallen.
- Electricity is imported only at the `ZAF`, `ZMB` and `ZWE` nodes and
  exported only at `ZAF` (SAPP sales). It reaches Namibia through the
  `power_line` transport technology, limited per direction to 575 MW South
  Africa and 428 MW Zimbabwe–Zambia (Kariba) (SAPP transfer limits) and
  300 MW Zambia (Caprivi Link rating). Neighbour nodes have no demand or
  plants. Imports are capped per hour at the ZESCO (180 MW) and ZPC (80 MW)
  contract sizes in `import_contracts.csv`. South Africa (SAPP market and Eskom) trades at the 2023 SAPP
  day-ahead price by time of use (each month's off-peak, standard and peak
  price, mapped to hours with Eskom's Megaflex periods); Zambia and Zimbabwe (ZESCO, ZPC contracts) at
  NamPower's average import price. Exports earn the SAPP price, capped at the
  contract import price so contract imports cannot be resold. Fuel supply is
  unbounded. Historical annual trade values are used for comparison, not
  imposed as model caps.

## Running on ETH Euler

1. On a login node, clone the repository and run `bash euler/setup_env.sh` once. It creates a Python environment in `~/venvs/zen_namibia`.
2. If a module in `euler/modules.sh` is missing, check `module avail python` / `module avail gurobi` and edit that file.
3. Submit with `sbatch euler/run.sbatch` from the repository root. The job builds the dataset and solves (8 cores, 64 GB, 24 h; Gurobi uses all 8 cores).
4. Follow with `squeue -u $USER`; the log is in `euler/logs/`. Copy `outputs_dispatch_2023/` back with `scp -r` or commit it from Euler.

## Troubleshooting

- If Python exits with Windows exception `0xc06d007f` inside `numpy.linalg`, reinstall NumPy in the active `ZEN-garden` environment (`conda install --force-reinstall numpy`).
