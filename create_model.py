from pathlib import Path

from zen_creator import Config, Model

# importing these registers the custom classes in zen_namibia/elements/ with
# zen_creator, so that Model.from_config() can find them by name
# (see source_data/config.yaml)
from zen_namibia.elements import carriers, conversion_technologies, energy_systems  # noqa: F401

from global_vars import INPUT_DATA_PATH

CONFIG_PATH = Path(__file__).resolve().parent / "source_data" / "config.yaml"


def create_model() -> Model:
    config = Config.load_from_yaml(CONFIG_PATH)
    if config.source_path is not None:
        source_path = Path(config.source_path)
        if not source_path.is_absolute():
            config.source_path = str(CONFIG_PATH.parent.parent / source_path)

    model = Model.from_config(config)

    # the built ZEN-garden dataset is written to INPUT_DATA_PATH
    model.name = INPUT_DATA_PATH.name
    model.output_folder = INPUT_DATA_PATH.parent

    model.build()
    model.validate()
    model.write()

    # ZEN-garden expects these folders to exist even without storage/transport techs
    (model.output_path / "set_technologies" / "set_storage_technologies").mkdir(
        parents=True, exist_ok=True
    )
    (model.output_path / "set_technologies" / "set_transport_technologies").mkdir(
        parents=True, exist_ok=True
    )

    return model


if __name__ == "__main__":
    create_model()
