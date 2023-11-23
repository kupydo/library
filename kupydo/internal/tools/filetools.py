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
from collections import defaultdict
from kupydo.internal import utils
from kupydo.internal.registry import *
from .kwargtools import *
from .sidtools import *


__all__ = [
    "read_encode_file",
    "read_cached_file_lines",
    "switch_file_secret_values"
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


def switch_file_secret_values(sfd_list: list[SecretFieldDetails]) -> None:
    secrets_by_file: dict[Path, list[SecretFieldDetails]] = defaultdict(list)
    for sfd in sfd_list:
        secrets_by_file[sfd.file_path].append(sfd)

    if not all(path.is_file() for path in secrets_by_file.keys()):
        raise FileNotFoundError("Cannot write registered secrets into missing files.")

    for path, sfd_list in secrets_by_file.items():
        with path.open('r') as file:
            lines = file.readlines()

        for sfd in sfd_list:
            parts = separate_kwarg_line(lines[sfd.line_number])
            if parts and sfd.field_keyword in parts.keyword:
                old, new = None, None

                if sfd.secret_value in parts.value:
                    old, new = sfd.secret_value, wrap_sid(sfd.identifier)
                elif wrapped_sid := sanitize_wrapped_sid(parts.value):
                    if validate_sid(wrapped_sid):
                        old, new = wrapped_sid, sfd.secret_value

                if old and new:
                    lines[sfd.line_number] = ''.join([
                        parts.keyword,
                        parts.separator,
                        parts.value.replace(old, new)
                    ])

        with path.open('w') as file:
            file.writelines(lines)
