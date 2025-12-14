import argparse
import sys
from collections.abc import Sequence

from whitesmith.generate_handlers import generate_handlers
from whitesmith.generate_openapis import generate_openapis


def main(args: Sequence[str] = sys.argv) -> None:
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
    sp_action.set_defaults(handler=generate_handlers)

    sp_action = subparsers.add_parser("generate-openapi")
    sp_action.add_argument(
        "-o",
        "--out-dir",
        dest="outdir",
        default="tests",
        help="Directory where the schemas will be generated",
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
    sp_action.set_defaults(handler=generate_openapis)

    kwargs = parser.parse_args(args[1:])
    kwargs_dict = vars(kwargs)
    handler = kwargs_dict.pop("handler")
    handler(**kwargs_dict)
