import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol

import tamahagane as th


class SubParser(Protocol):
    def add_parser(self, name: str, *, help: str) -> argparse.ArgumentParser: ...


CommandHandler = Callable[[SubParser], None]


@dataclass
class Registries:
    subparsers: SubParser


def cli_command(wrapped: CommandHandler) -> CommandHandler:

    def callback(registries: Registries) -> None:
        wrapped(registries.subparsers)

    th.attach(wrapped, callback, category="subparsers")
    return wrapped


def main(args: Sequence[str] = sys.argv) -> None:
    parser = argparse.ArgumentParser(description="CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    registry = Registries(subparsers=subparsers)
    scanner = th.Scanner[Registries](registry)
    scanner.scan("whitesmith.bin")

    kwargs = vars(parser.parse_args(args[1:]))
    handler = kwargs.pop("handler", None)
    if handler:
        kwargs.pop("command", None)
        handler(**kwargs)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
