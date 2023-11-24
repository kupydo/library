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
import inspect
import linecache
from pathlib import Path
from dotmap import DotMap
from types import TracebackType
from typing import Literal, TypeVar, Mapping
from kupydo.internal.errors import RepoNotFoundError


__all__ = [
    "get_library_path",
    "find_repo_path",
    "repo_abs_to_rel_path",
    "repo_rel_to_abs_path",
    "extract_tb_line",
    "extract_tb_filepath",
    "first_external_caller",
    "generate_name",
    "deep_merge"
]


T = TypeVar('T', bound=Mapping)


def get_library_path() -> Path:
    return Path(__file__).parent.resolve()


def find_repo_path() -> Path:
    current_path = Path.cwd().resolve()
    while current_path != current_path.root:
        if (current_path / '.git').is_dir():
            return current_path
        current_path = current_path.parent
    raise RepoNotFoundError


def repo_abs_to_rel_path(abs_path: Path) -> str:
    return abs_path.relative_to(find_repo_path()).as_posix()


def repo_rel_to_abs_path(rel_path: str) -> Path:
    return (find_repo_path() / rel_path).resolve()


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


def first_external_caller() -> tuple[Path, int]:
    lib_path = get_library_path()
    for frame_info in inspect.stack():
        frame_file_path = Path(frame_info.filename)

        # always evaluates to true eventually
        if not frame_file_path.is_relative_to(lib_path):
            return frame_file_path, frame_info.lineno


def generate_name() -> str:
    chars = string.ascii_lowercase + string.digits
    chosen = ''.join(random.choices(chars, k=15))
    return f"{chosen[:5]}-{chosen[5:10]}-{chosen[10:]}"


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
