import locale
from argparse import Namespace, ArgumentParser
from pathlib import Path

from pydantic_core import from_json

from loaders import load_vault_content
from misc.datamodels import VaultConfig
from process import CSVBuilder

locale.setlocale(locale.LC_TIME, "de_DE")


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Read data from obsidian vault.")
    arg_parser.add_argument(
        "-c",
        "--vault-conf",
        dest="vault_conf",
        type=Path,
        help="Json config to map the talkshows to vault dirs.",
        required=True,
    )
    arg_parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        type=Path,
        help="Path to .csv file you want to write.",
        required=False,
        default=Path("./output.csv"),
    )
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    arguments = call_for_args()
    config = VaultConfig.model_validate(
        from_json(arguments.vault_conf.open("r").read())
    )
    dataframe_raw = load_vault_content(config)
    print(f"Found '{dataframe_raw["episode_name"].unique().len()}' episodes...")
    print(f"Found '{dataframe_raw.shape[0]}' guests...")

    builder = CSVBuilder(dataframe_raw)

    builder.dataframe.write_csv(arguments.output_path)
    print(f"File written to '{arguments.output_path}'")
    print("Done, enjoy the data.")
