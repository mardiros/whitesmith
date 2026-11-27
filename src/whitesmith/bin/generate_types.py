import os
import sys
from pathlib import Path
from typing import Any, TextIO

import blacksmith
from blacksmith.domain.registry import registry
from jinja2 import Environment, PackageLoader

from whitesmith.entrypoints.cli import SubParser, cli_command

env = Environment(loader=PackageLoader("whitesmith"), autoescape=False)


def snake_to_pascal(snake_str: str) -> str:
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


env.filters["snake_to_pascal"] = snake_to_pascal


def safe_get_type(obj: Any, *path: list[str | int]) -> str:
    try:
        for key in path:
            if isinstance(key, int) or isinstance(obj, dict):
                obj = obj[key]
            else:
                obj = getattr(obj, key)  # type: ignore
        return obj
    except (KeyError, AttributeError, IndexError):
        return "None"


def safe_type_exists(obj: Any, *path: list[str | int]) -> bool:
    try:
        for key in path:
            if isinstance(key, int) or isinstance(obj, dict):
                obj = obj[key]
            else:
                obj = getattr(obj, key)  # type: ignore
        return obj is not None
    except (KeyError, AttributeError, IndexError):
        return False


env.globals["safe_type_exists"] = safe_type_exists  # type: ignore
env.globals["safe_get_type"] = safe_get_type  # type: ignore
env.globals["sorted"] = sorted  # type: ignore

types_template = env.get_template("types.jinja2")


def safe_open(output: str, overwrite: bool) -> TextIO:
    output_path = Path(output)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Output file {output} already exists")
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    if not output_path.parent.is_dir():
        raise NotADirectoryError(f"Parent directory of {output} does not exist")
    if not output_path.parent.is_dir() or not os.access(output_path.parent, os.W_OK):
        raise PermissionError(f"Parent directory of {output} is not writable")
    return output_path.open("w")


def handler(
    resources_mod: list[str],
    sync: bool = False,
    async_: bool = False,
    overwrite: bool = False,
    output: str | None = None,
) -> None:
    blacksmith.scan(*resources_mod)

    if not any([sync, async_]):
        sync = async_ = True

    if output:
        stream = safe_open(output, overwrite)
    else:
        stream = sys.stdout

    try:
        types = types_template.render(
            clients=registry.clients, sync=sync, async_=async_
        )
        print(types, file=stream)
    finally:
        if output:
            stream.close()


@cli_command
def main(subparsers: SubParser) -> None:
    sp_action = subparsers.add_parser("generate-types", help="Generate types")
    sp_action.add_argument(
        "--sync", action="store_true", help="Generate synchronous stubs"
    )
    sp_action.add_argument(
        "--async",
        action="store_true",
        dest="async_",
        help="Generate asynchronous stubs",
    )
    sp_action.add_argument("-o", "--output", type=str, help="Output file path")

    sp_action.add_argument(
        "-m",
        "--resource-module",
        dest="resources_mod",
        required=True,
        action="append",
        help="Blacksmith resource module to scan",
    )

    sp_action.add_argument(
        "--overwrite",
        action="store_true",
        dest="overwrite",
        help="Overwite existing file instead of fialed.",
    )

    sp_action.set_defaults(handler=handler)
