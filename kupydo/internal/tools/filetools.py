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
import re
import base64
import inspect
from pathlib import Path
from kupydo.internal import utils


__all__ = [
    "first_external_caller",
    "read_encode_file",
    "find_kwarg_line",
    "replace_kwarg_value"
]


def first_external_caller() -> tuple[Path, int]:
    lib_path = utils.get_library_dir()
    for frame_info in inspect.stack():
        frame_file_path = Path(frame_info.filename)

        # always evaluates to true eventually
        if not frame_file_path.is_relative_to(lib_path):
            return frame_file_path, frame_info.lineno


def read_encode_file(file_path: Path | str) -> str | None:
    target = Path(file_path)

    if file_path.startswith('.'):
        caller_path = first_external_caller()[0]
        target = caller_path.parent / file_path

    target = target.resolve(strict=True)
    with target.open('rb') as file:
        return base64.b64encode(file.read()).decode()


def find_kwarg_line(keyword: str, current_value: str) -> tuple[Path, int]:
    file_path, line_number = first_external_caller()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    open_parentheses = 0
    start_line = line_number - 1
    end_line = start_line

    for i, line in enumerate(lines[start_line:], start=start_line):
        open_parentheses += line.count('(')
        open_parentheses -= line.count(')')
        if open_parentheses == 0:
            end_line = i
            break

    pattern = re.escape(keyword) + r'="' + re.escape(current_value) + r'"'
    for i, line in enumerate(lines[start_line:end_line + 1], start=start_line):
        if re.search(pattern, line):
            return file_path, i


def replace_kwarg_value(file_path: Path, line_number: int,
                        old_value: str, new_value: str) -> None:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pattern = re.escape(old_value)
    lines[line_number] = re.sub(
        pattern,
        new_value,
        lines[line_number]
    )
    with open(file_path, 'w') as file:
        file.writelines(lines)
