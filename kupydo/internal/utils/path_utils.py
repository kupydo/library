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
from pathlib import Path, PurePosixPath, PureWindowsPath
from kupydo.internal.errors import *


__all__ = [
    "find_lib_path",
    "find_repo_path",
    "is_path_absolute",
    "repo_abs_to_rel_path",
    "repo_rel_to_abs_path",
]


def find_lib_path() -> Path:
    current_path = Path(__file__).resolve()
    while current_path != current_path.parent:
        lib_path = current_path / 'internal'
        if lib_path.is_dir():
            return lib_path
        current_path = current_path.parent
    raise RuntimeError("Must find internal dir!")


def find_repo_path() -> Path:
    current_path = Path.cwd().resolve()
    while current_path != current_path.parent:
        if (current_path / '.git').is_dir():
            return current_path
        current_path = current_path.parent
    raise RepoNotFoundError


def is_path_absolute(path: str) -> bool:
    for path_cls in [PurePosixPath, PureWindowsPath]:
        if path_cls(path).is_absolute():
            return True
    return False


def repo_abs_to_rel_path(abs_path: Path) -> str:
    return abs_path.relative_to(find_repo_path()).as_posix()


def repo_rel_to_abs_path(rel_path: str) -> Path:
    return (find_repo_path() / rel_path).resolve()
