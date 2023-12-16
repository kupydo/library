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
import os
import pytest
from pathlib import Path
from kupydo.internal import utils
from kupydo.internal.errors import *


def test_find_lib_path_does_not_raise_error():
    try:
        utils.find_lib_path()
    except RuntimeError:
        pytest.fail("find_lib_path must find the 'internal' directory!")


def test_find_lib_path_finds_internal_dir():
    path = utils.find_lib_path()

    assert path.name == 'internal', \
        "The name of the found directory is not 'internal'."


def test_find_repo_path_raises_error(tmp_path: Path):
    os.chdir(tmp_path)

    with pytest.raises(RepoNotFoundError):
        utils.find_repo_path()


def test_is_path_absolute():
    paths = [
        ("/home/user/file", True),
        ("C:/home/user/file", True),
        ("./home/user/file", False),
        ("home/user/file", False)
    ]
    for path, expected in paths:
        assert utils.is_path_absolute(path) is expected, \
            f"Path '{path}' was not identified as \
            {'absolute' if expected else 'relative'}."
