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
import random
import string
import base64
import inspect
import linecache
from pathlib import Path
from dotmap import DotMap
from types import TracebackType
from typing import Literal, TypeVar, Mapping


__all__ = [
    "generate_name",
    "extract_tb_line",
    "extract_tb_filepath",
    "deep_merge"
]

T = TypeVar('T', bound=Mapping)


def generate_name() -> str:
    chars = string.ascii_lowercase + string.digits
    chosen = ''.join(random.choices(chars, k=15))
    return f"{chosen[:5]}-{chosen[5:10]}-{chosen[10:]}"


def extract_tb_line(tb: TracebackType) -> str:
    path = Path(tb.tb_frame.f_code.co_filename).as_posix()
    return linecache.getline(path, tb.tb_lineno).strip()


def extract_tb_filepath(tb: TracebackType) -> str:
    path = Path(tb.tb_frame.f_code.co_filename)
    try:
        index = path.parts.index('kupydo')
        path = Path(*path.parts[index:])
    except ValueError:
        pass
    return path.as_posix()


def deep_merge(base: T,
               update: dict | DotMap,
               exclude: dict | DotMap,
               method: Literal['patch', 'replace']) -> T:
    def is_mapping(v):
        return isinstance(v, dict | DotMap)

    if method == 'replace':
        for key in list(base.keys()):
            if key not in update and not is_mapping(base[key]):
                del base[key]

    for key, value in update.items():
        if method == 'patch' and value is None:
            continue
        if exclude and key in exclude:
            if is_mapping(value) and is_mapping(base.get(key)) and is_mapping(exclude[key]):
                deep_merge(base[key], value, exclude[key], method)
            continue
        if key in base and is_mapping(value) and is_mapping(base[key]):
            deep_merge(base[key], value, dict(), method)
        else:
            base[key] = value
    return base


def read_encode_files(file_names: list[str] | None) -> dict[str, str] | None:
    if not file_names:
        return

    caller_frame = inspect.stack()[2]
    caller_path = Path(caller_frame.filename).parent

    encoded_files = dict()

    for file_name in file_names:
        file_path = caller_path / file_name

        with file_path.open("rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")
            encoded_files[file_name] = encoded_content

    return encoded_files
