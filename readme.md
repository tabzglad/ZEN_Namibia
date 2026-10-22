- Make sure you have conda installed
- Install zen garden and zen creator
- make sure you have gurobi installed (there is an academic licence available)

## Where to find what

- `source_data/` — zen-creator config (`config.yaml`) and raw data (e.g. `demand_electricity.csv`)
- `zen_namibia/elements/` — carrier/technology/energy-system definitions (edit these to change assumptions)
- `zen_namibia/datasets/` — classes that load raw data from `source_data/` into attributes
- `create_model.py` — builds the ZEN-garden dataset into `./zen_namibia_dataset/`
- `run_zen_garden.py` — solves that dataset, writes results into `./output/`
- `global_vars.py` — shared paths used by both scripts above
