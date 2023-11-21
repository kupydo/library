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
    "extract_caller_block",
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


def extract_caller_block(file_path: Path, line_number: int) -> tuple[list[str], int, int]:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    open_parentheses = 0
    start = line_number - 1

    for i, line in enumerate(lines[start:], start=start):
        open_parentheses += line.count('(')
        open_parentheses -= line.count(')')
        if open_parentheses == 0:
            return lines, start, i


def find_kwarg_line(keyword: str, current_value: str) -> tuple[Path, int]:
    file_path, line_number = first_external_caller()
    lines, start, end = extract_caller_block(file_path, line_number)

    pattern_equal = rf"^\s*{re.escape(keyword)}\s*=\s*['\"]{re.escape(current_value)}['\"]\s*$"
    pattern_colon = rf"^\s*['\"]{re.escape(keyword)}['\"]\s*:\s*['\"]{re.escape(current_value)}['\"]\s*$"

    for i, line in enumerate(lines[start:end + 1], start=start):
        if ':' in line and '=' in line:
            pattern = (
                pattern_equal if
                line.index('=') < line.index(':')
                else pattern_colon
            )
            if re.search(pattern, line):
                return file_path, i
        elif ':' in line:
            if re.search(pattern_colon, line):
                return file_path, i
        elif '=' in line:
            if re.search(pattern_equal, line):
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
