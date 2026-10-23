from pathlib import Path

import yaml
from zen_garden import run

from global_vars import INPUT_DATA_PATH

CONFIG_PATH = Path("./config.yaml")

CONFIG = {
    "analysis": {
        "dataset": str(INPUT_DATA_PATH),
        "objective": "total_cost",
        "sense": "min",
    },
    "solver": {
        "name": "gurobi",
    },
}


def run_zen_garden():
    CONFIG_PATH.write_text(yaml.safe_dump(CONFIG, sort_keys=False), encoding="utf-8")
    run(config=CONFIG_PATH)


if __name__ == "__main__":
    run_zen_garden()
