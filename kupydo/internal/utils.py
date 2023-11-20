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
import uuid
import random
import string
import linecache
from pathlib import Path
from dotmap import DotMap
from types import TracebackType
from typing import Literal, TypeVar, Mapping


__all__ = [
    "get_library_dir",
    "generate_name",
    "extract_tb_line",
    "extract_tb_filepath",
    "deep_merge",
    "create_secret_id",
    "validate_secret_id"
]


T = TypeVar('T', bound=Mapping)


def get_library_dir() -> Path:
    return Path(__file__).parent.resolve()


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


def create_secret_id() -> str:
    return f"[ENC_ID:{uuid.uuid4().hex}:ID_END]"


def validate_secret_id(sec_id: str) -> bool:
    if ':' not in sec_id:
        return False
    elif sec_id.count(':') != 2:
        return False

    prefix, sec_id, suffix = sec_id.split(':')
    if not prefix == '[ENC_ID':
        return False
    elif not suffix == 'ID_END]':
        return False
    elif not len(sec_id) == 32:
        return False
    elif not all([
        c in '0123456789abcdef'
        for c in sec_id
    ]):
        return False
    return True
