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
import string
import pytest
import shutil
from kupydo.internal.project_config import *


@pytest.fixture(scope="module", autouse=True)
def setup_test_environment(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("git_repo")
    os.chdir(tmp_path)
    (tmp_path / ".git").mkdir()
    heart_path = tmp_path / "clusters/dev"
    heart_path.mkdir(parents=True)
    (heart_path / "Heart.py").touch()
    (heart_path / "OtherFile.py").touch()
    yield
    shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture()
def valid_data() -> dict:
    return {
        "id": "c5027735a24c3daa00fbc655b8aa20f3",
        "alias": "MyApp-123",
        "path": "clusters/dev/Heart.py",
        "pubkey": "age17qyz09pyjxfwyxdjwyugw7wxy8gtk0gc23t7y9qqxccg6hr8uyqsqlmh2k"
    }


def test_valid_data(valid_data: dict):
    deployment = DeploymentPublicDetails(**valid_data)
    assert deployment is not None, \
        "DeploymentPublicDetails should be instantiated with valid data"


def test_invalid_id_length(valid_data: dict):
    invalid_data = {**valid_data, "id": "123"}  # Invalid length
    with pytest.raises(ValueError, match="id length must equal 32 characters."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_id_characters(valid_data: dict):
    invalid_data = {**valid_data, "id": "g" * 32}  # Invalid characters
    with pytest.raises(ValueError, match="id must consist of valid hex characters."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_alias_length(valid_data: dict):
    invalid_data = {**valid_data, "alias": "a" * 21}  # Invalid length
    with pytest.raises(ValueError, match="alias length must be less than or equal to 20 characters."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_alias_characters(valid_data: dict):
    punctuation = string.punctuation.replace('-', '')
    for invalid_char in punctuation + string.whitespace:
        invalid_data = {**valid_data, "alias": f"MyApp{invalid_char}123"}  # Invalid characters
        with pytest.raises(ValueError, match="alias must consist of any valid characters: a-z, A-Z, 0-9, '-'."):
            DeploymentPublicDetails(**invalid_data)


def test_invalid_posix_absolute_path(valid_data: dict):
    invalid_data = {**valid_data, "path": "/absolute/path/Heart.py"}  # Invalid absolute path
    with pytest.raises(ValueError, match="path must be a relative path."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_windows_absolute_path(valid_data: dict):
    invalid_data = {**valid_data, "path": "C:/absolute/path/Heart.py"}  # Invalid absolute path
    with pytest.raises(ValueError, match="path must be a relative path."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_path_nonexistent_file(valid_data: dict):
    invalid_data = {**valid_data, "path": "clusters/dev/Nonexistent.py"}  # Invalid nonexistent file
    with pytest.raises(ValueError, match="path cannot point to a non-existent file."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_path_wrong_filename(valid_data: dict):
    invalid_data = {**valid_data, "path": "clusters/dev/OtherFile.py"}  # Invalid filename
    with pytest.raises(ValueError, match="path must point to a file named 'Heart.py'."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_pubkey_secret_key(valid_data: dict):
    invalid_data = {**valid_data, "pubkey": "AGE-SECRET-KEY-" + "A" * 59}  # Invalid type
    with pytest.raises(ValueError, match="not allowed to assign an AGE secret key to the pubkey field."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_pubkey_length(valid_data: dict):
    invalid_data = {**valid_data, "pubkey": "age" + "a" * 58}  # Invalid length
    with pytest.raises(ValueError, match="must assign a valid AGE public key to the pubkey field."):
        DeploymentPublicDetails(**invalid_data)


def test_invalid_pubkey_format(valid_data: dict):
    invalid_data = {**valid_data, "pubkey": "fff" + "a" * 59}  # Invalid format
    with pytest.raises(ValueError, match="must assign a valid AGE public key to the pubkey field."):
        DeploymentPublicDetails(**invalid_data)
