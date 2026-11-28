import os
from pathlib import Path

import yaml
from zen_garden import run

from global_vars import INPUT_DATA_PATH

PROJECT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_DIR / "config_dispatch_2023.yaml"
NODEFILE_DIR = PROJECT_DIR / "gurobi_nodefiles"

CONFIG = {
    "analysis": {
        "dataset": str(INPUT_DATA_PATH),
        "objective": "total_cost",
        "sense": "min",
        "folder_output": str(PROJECT_DIR / "outputs_dispatch_2023"),
    },
    "solver": {
        "name": "gurobi",
        # Low-memory settings: sparser presolve, node files written to disk
        # once they pass 0.5 GB. One thread locally; on Euler, the cores
        # Slurm gives the job (euler/run.sbatch).
        "solver_options": {
            "Threads": int(os.environ.get("SLURM_CPUS_PER_TASK", 1)),
            # Barrier without crossover: dual simplex stalled for hours on the
            # degenerate multi-node LP (line flows with only a tie-breaker cost).
            "Method": 2,
            "Crossover": 0,
            "PreSparsify": 1,
            "NodefileStart": 0.5,
            "NodefileDir": str(NODEFILE_DIR),
        },
        "save_duals": False,
        "save_reduced_costs": False,
        "use_scaling": True,
    },
}


def run_zen_garden():
    NODEFILE_DIR.mkdir(exist_ok=True)
    CONFIG_PATH.write_text(yaml.safe_dump(CONFIG, sort_keys=False), encoding="utf-8")
    run(config=CONFIG_PATH)


if __name__ == "__main__":
    run_zen_garden()
