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
import orjson
from pathlib import Path
from dotmap import DotMap
from typing import Callable
from kupydo.internal.project_config import *


@pytest.fixture(name="depl")
def fixture_depl() -> DotMap:
    return DotMap(
        first={"id": "c5027735a24c3daa00fbc655b8aa20f3"},
        second={"id": "846ef331b4e9df983d8e6b9905d518e1"}
    )


@pytest.fixture(name="temp_repo")
def fixture_temp_repo(tmp_path: Path, depl: DotMap) -> Callable:
    def real_base_config(garbage: bool = False, dupe_id: bool = False):
        os.chdir(tmp_path)
        base_file = tmp_path / ".base"
        with base_file.open("w") as file:
            if garbage:
                content = '{"deployments" : [error]}'
            else:
                content = orjson.dumps({
                    "deployments": [
                        depl.first,
                        depl.first if dupe_id else depl.second
                    ]
                }).decode("utf-8")
            file.write(content)

        class RealBaseConfig(ProjectBaseConfig):
            @staticmethod
            def _get_config_path() -> Path:
                return base_file

        return RealBaseConfig
    return real_base_config


def test_read_file_contents(temp_repo: Callable, depl: DotMap):
    rbc_class = temp_repo()
    conf = rbc_class()
    for pd, fd in zip(conf.deployments, depl.values()):
        assert getattr(pd, "id") == fd["id"]


def test_write_file_contents_and_update(temp_repo: Callable, depl: DotMap):
    rbc_class = temp_repo()
    new_id = "a" * 32

    conf1 = rbc_class()
    assert conf1.deployments[0].id == depl.first["id"]
    assert conf1.deployments[1].id == depl.second["id"]

    conf2 = rbc_class()
    conf2.deployments[0].id = new_id
    conf2.write()

    conf1.update()
    assert conf1.deployments[0].id == new_id
    assert conf1.deployments[1].id == depl.second["id"]


def test_duplicate_id(temp_repo: Callable):
    rbc_class = temp_repo(dupe_id=True)
    errmsg = "duplicate id values not allowed in public config file."
    with pytest.raises(ValueError, match=errmsg):
        rbc_class()


def test_garbage_file_contents(temp_repo: Callable):
    rbc_class = temp_repo(garbage=True)
    with pytest.raises(orjson.JSONDecodeError):
        rbc_class()
