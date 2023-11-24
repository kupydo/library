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
from typer import Typer


init_app = Typer(name="init")


@init_app.callback(invoke_without_command=True)
def cmd_decrypt():
	print("initing")
