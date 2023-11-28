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
import base64
import functools
from pathlib import Path
from kupydo.internal import utils


__all__ = [
    "read_encode_file",
    "read_cached_file_lines"
]


def read_encode_file(file_path: Path | str) -> str:
    target = Path(file_path)

    if isinstance(file_path, str) and file_path.startswith('.'):
        caller_path = utils.first_external_caller()[0]
        target = caller_path.parent / file_path

    target = target.resolve(strict=True)
    with target.open('rb') as file:
        return base64.b64encode(file.read()).decode()


@functools.cache
def read_cached_file_lines(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        return file.readlines()
