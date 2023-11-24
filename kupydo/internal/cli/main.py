#
#   MIT License
#
#   Copyright (c) 2023, Mattias Aabmets
#
#   The contents of this file are subject to the terms and conditions defined in the License.
#   You may not use, modify, or distribute this file except in compliance with the License.
#
#   SPDX-License-Identifier: MIT
#
from typing import Annotated
from typer import Typer, Option
from rich.console import Console
from kupydo.internal.cli.commands import *
from kupydo.internal.cli.classes import PackageInfo


app = Typer()


app.add_typer(init_app)
app.add_typer(enc_app)
app.add_typer(dec_app)


Version = Annotated[bool, Option(
    '--version', '-v', show_default=False,
    help='Print the package version to console and exit.'
)]
Info = Annotated[bool, Option(
    '--info', '-i', show_default=False,
    help='Print package info to console and exit.'
)]


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(version: Version = False, info: Info = False):
    if version:
        pkg_info = PackageInfo()
        print(pkg_info.version)
    elif info:
        title_color = "[{}]".format("#ff5fff")
        key_color = "[{}]".format("#87d7d7")
        value_color = "[{}]".format("#ffd787")
        indent1, indent2 = 3 * ' ', 5 * ' '

        pkg_info = PackageInfo()
        console = Console(soft_wrap=True)
        console.print(f"\n{indent1}{title_color}Package Info:")

        for k, v in vars(pkg_info).items():
            k = f"{key_color}{k}"
            v = f"{value_color}{v}"
            console.print(f"{indent2}{k}: {v}")

        console.print('')
