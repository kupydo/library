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
from pathlib import Path
from kupydo.internal.cli.errors import *


__all__ = [
    "find_repo_path",
    "resolve_repo_rel_path"
]


def find_repo_path() -> Path:
    current_path = Path.cwd()
    while current_path != current_path.root:
        if (current_path / '.git').is_dir():
            return current_path
        current_path = current_path.parent
    raise RepoNotFoundError


def resolve_repo_rel_path(rel_path: str) -> Path:
    return (find_repo_path() / rel_path).resolve()
