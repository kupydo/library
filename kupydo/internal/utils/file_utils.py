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
from kupydo.internal import errors
from .path_utils import is_path_absolute


__all__ = [
    "read_encode_b64_file",
    "write_decode_b64_file",
    "read_cached_file_lines"
]


def read_encode_b64_file(abs_fp: Path | str) -> str:
    abs_fp = Path(abs_fp)
    if not is_path_absolute(abs_fp):
        raise errors.InvalidPathTypeError(
            abs_fp.as_posix(), "absolute"
        )
    with abs_fp.open('rb') as file:
        return base64.b64encode(file.read()).decode()


def write_decode_b64_file(abs_fp: Path | str, b64_data: str) -> None:
    abs_fp = Path(abs_fp)
    if not is_path_absolute(abs_fp):
        raise errors.InvalidPathTypeError(
            abs_fp.as_posix(), "absolute"
        )
    with abs_fp.open('wb') as file:
        file.write(base64.b64decode(b64_data.encode()))


@functools.cache
def read_cached_file_lines(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        return file.readlines()
