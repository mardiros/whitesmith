import argparse
import sys
from pathlib import Path
from typing import Sequence

from .generate_handlers import generate_handlers


def generate(outdir: str, resources_mod: Sequence[str], overwrite: bool) -> None:
    outpath = Path(outdir)
    generate_handlers(outpath, resources_mod, overwrite)


def main() -> None:
    args = sys.argv
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="action", required=True)

    sp_action = subparsers.add_parser("generate")
    sp_action.add_argument(
        "-o",
        "--out-dir",
        dest="outdir",
        default="tests",
        help="Directory where the handlers will be generated",
    )
    sp_action.add_argument(
        "--overwrite", action="store_true", dest="overwrite", default=False
    )

    sp_action.add_argument(
        "-m",
        "--resource-module",
        dest="resources_mod",
        required=True,
        nargs="+",
        help="blacksmith resource module to scan",
    )
    sp_action.set_defaults(handler=generate)
    kwargs = parser.parse_args(args[1:])
    kwargs_dict = vars(kwargs)
    handler = kwargs_dict.pop("handler")
    handler(**kwargs_dict)
