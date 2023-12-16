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
from .trace_utils import first_external_caller
from .path_utils import is_path_absolute


__all__ = [
    "read_encode_rel_file",
    "read_cached_file_lines"
]


def read_encode_rel_file(rel_fp: str) -> str:
    if is_path_absolute(rel_fp):
        raise errors.PathNotRelativeError(rel_fp)

    caller_path = first_external_caller()[0]
    target = (caller_path.parent / rel_fp).resolve()

    with target.open('rb') as file:
        return base64.b64encode(file.read()).decode()


@functools.cache
def read_cached_file_lines(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        return file.readlines()
