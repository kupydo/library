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
import shutil
from pathlib import Path
from kupydo.internal.project_config import *


@pytest.fixture(scope="module", autouse=True)
def dummy_repo_path(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("git_repo")
    os.chdir(tmp_path)
    (tmp_path / ".git").mkdir()
    heart_path = tmp_path / "clusters/dev"
    heart_path.mkdir(parents=True)
    (heart_path / "Heart.py").touch()

    kupydo_file = tmp_path / ".kupydo"
    kupydo_content = {
        "deployments": [
            {
                "id": "c5027735a24c3daa00fbc655b8aa20f3",
                "alias": "MyApp-123",
                "path": "clusters/dev/Heart.py",
                "pubkey": "age17qyz09pyjxfwyxdjwyugw7wxy8gtk0gc23t7y9qqxccg6hr8uyqsqlmh2k"
            }
        ]
    }
    with kupydo_file.open("w") as file:
        dump = orjson.dumps(kupydo_content)
        file.write(dump.decode("utf-8"))

    yield
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_read_file_contents():
    conf = ProjectPublicConfig()
    dpl = conf.deployments[0]
    assert dpl.id == "c5027735a24c3daa00fbc655b8aa20f3"
    assert dpl.alias == "MyApp-123"
    assert dpl.path == "clusters/dev/Heart.py"
    assert dpl.pubkey == "age17qyz09pyjxfwyxdjwyugw7wxy8gtk0gc23t7y9qqxccg6hr8uyqsqlmh2k"


def test_write_file_contents_and_update():
    conf1 = ProjectPublicConfig()
    dpl1 = conf1.deployments[0]
    assert dpl1.alias == "MyApp-123"

    conf2 = ProjectPublicConfig()
    dpl2 = conf2.deployments[0]
    dpl2.alias = "NewAlias"
    conf2.write()

    conf1.update()
    dpl1 = conf1.deployments[0]
    assert dpl1.alias == "NewAlias"
