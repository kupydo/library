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
import json
import pytest
from pathlib import Path
from dotmap import DotMap
from kupydo.internal.errors import BadStatusFileError
from kupydo.internal.ext_tools import *


GET_BIN_PATH = 'kupydo.internal.ext_tools.status_file.get_bin_path'


def test_file_path(tmp_path, mocker):
    mocker.patch(GET_BIN_PATH, return_value=tmp_path)
    assert StatusFile._file_path() == tmp_path / "status.json"


def test_default_object():
    dsf = StatusFile._default()
    assert isinstance(dsf, StatusFile)
    assert 'sops' in dsf and 'age' in dsf


def test_validation_success():
    vsf = StatusFile(dict(
        sops=dict(current_version='1.2.3', last_update='2021-12-31'),
        age=dict(current_version='4.5.6', last_update='2003-06-09')
    ))
    sf = StatusFile._validate(vsf)
    assert isinstance(sf, StatusFile) and sf is vsf


def test_invalid_sops_version():
    vsf = StatusFile(dict(
        sops=dict(current_version='wth_is_this', last_update='2021-12-31'),
        age=dict(current_version='4.5.6', last_update='2003-06-09')
    ))
    sf = StatusFile._validate(vsf)
    assert isinstance(sf, StatusFile) and sf is not vsf


def test_invalid_sops_date():
    vsf = StatusFile(dict(
        sops=dict(current_version='1.2.3', last_update='wth_is_this'),
        age=dict(current_version='4.5.6', last_update='2003-06-09')
    ))
    sf = StatusFile._validate(vsf)
    assert isinstance(sf, StatusFile) and sf is not vsf


def test_invalid_age_version():
    vsf = StatusFile(dict(
        sops=dict(current_version='1.2.3', last_update='2021-12-31'),
        age=dict(current_version='wth_is_this', last_update='2003-06-09')
    ))
    sf = StatusFile._validate(vsf)
    assert isinstance(sf, StatusFile) and sf is not vsf


def test_invalid_age_date():
    vsf = StatusFile(dict(
        sops=dict(current_version='1.2.3', last_update='2021-12-31'),
        age=dict(current_version='4.5.6', last_update='wth_is_this')
    ))
    sf = StatusFile._validate(vsf)
    assert isinstance(sf, StatusFile) and sf is not vsf


@pytest.fixture
def status_file(tmp_path: Path) -> callable:
    def closure(*, valid=True):
        path = tmp_path / "status.json"
        extra = {} if valid else {"invalid": "invalid"}
        contents = {
            "comment": "THIS FILE IS MANAGED BY KUPYDO. DO NOT EDIT MANUALLY!",
            "tools": {
                "sops": {
                    "current_version": "1.2.3",
                    "last_update": "2021-12-31"
                },
                "age": {
                    "current_version": "4.5.6",
                    "last_update": "2003-06-09"
                },
                **extra
            }
        }
        path.write_text(json.dumps(contents))
        return tmp_path
    return closure


def test_valid_file_read(mocker, status_file):
    tmp_path = status_file(valid=True)
    mocker.patch(GET_BIN_PATH, return_value=tmp_path)
    sf = StatusFile.read()
    assert sf.sops.current_version == '1.2.3'
    assert sf.age.current_version == '4.5.6'
    assert sf.sops.last_update == '2021-12-31'
    assert sf.age.last_update == '2003-06-09'


def test_invalid_file_read(mocker, status_file):
    tmp_path = status_file(valid=False)
    mocker.patch(GET_BIN_PATH, return_value=tmp_path)
    sf = StatusFile.read()
    assert sf.sops.current_version == '0.0.0'
    assert sf.age.current_version == '0.0.0'
    assert sf.sops.last_update == '2000-01-01'
    assert sf.age.last_update == '2000-01-01'


def test_file_valid_update():
    sf = StatusFile._default()
    dummy_sops_release = DotMap(
        tool=DotMap(name="sops"),
        tag="1.2.3"
    )
    sf.update(dummy_sops_release)
    assert sf.sops.current_version == "1.2.3"
    assert sf.sops.last_update != "2000-01-01"


def test_file_update_with_invalid_tool_name():
    sf = StatusFile._default()
    invalid_tool_name = DotMap(
        tool=DotMap(name="your mum"),
        tag="1.2.3"
    )
    with pytest.raises(BadStatusFileError):
        sf.update(invalid_tool_name)


def test_file_update_with_invalid_tag_format():
    sf = StatusFile._default()
    invalid_tool_name = DotMap(
        tool=DotMap(name="sops"),
        tag="your mum"
    )
    with pytest.raises(BadStatusFileError):
        sf.update(invalid_tool_name)


def test_file_writing(mocker, status_file):
    tmp_path = status_file(valid=True)
    mocker.patch(GET_BIN_PATH, return_value=tmp_path)
    StatusFile._default().write()
    sf = StatusFile.read()
    assert sf.sops.current_version == '0.0.0'
    assert sf.age.current_version == '0.0.0'
    assert sf.sops.last_update == '2000-01-01'
    assert sf.age.last_update == '2000-01-01'
