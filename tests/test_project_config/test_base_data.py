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
import pytest
import string
from pydantic import ValidationError
from kupydo.internal.project_config import *


@pytest.fixture(name="valid_id")
def fixture_valid_id() -> str:
	return "c5027735a24c3daa00fbc655b8aa20f3"


@pytest.fixture(name="non_hex_chars")
def fixture_non_hex_chars() -> list[str]:
	return [
		c for c in string.printable
		if c not in '0123456789abcdef'
	]


def test_valid_id(valid_id: str):
	instance = DeploymentBaseData(id=valid_id)
	assert instance.id == valid_id, \
		"Valid ID should be accepted"


def test_invalid_longer_id_len(valid_id: str):
	invalid_longer_id = valid_id + '1'
	errmsg = "id length must equal 32 characters."
	with pytest.raises(ValidationError, match=errmsg):
		DeploymentBaseData(id=invalid_longer_id)


def test_invalid_shorter_id_len(valid_id: str):
	invalid_shorter_id = valid_id[:-1]
	errmsg = "id length must equal 32 characters."
	with pytest.raises(ValidationError, match=errmsg):
		DeploymentBaseData(id=invalid_shorter_id)


def test_invalid_id_chars(valid_id: str, non_hex_chars: list[str]):
	for bad_char in non_hex_chars:
		invalid_id = valid_id[:-1] + bad_char
		errmsg = "id must consist of valid hex characters."
		with pytest.raises(ValidationError, match=errmsg):
			DeploymentBaseData(id=invalid_id)
