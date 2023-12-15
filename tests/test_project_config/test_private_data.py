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
import string
import pytest
from pydantic import ValidationError
from kupydo.internal.project_config import *


@pytest.fixture(name="valid_data")
def fixture_valid_data() -> dict:
	return {
		"id": "c5027735a24c3daa00fbc655b8aa20f3",
		"salt": "NgeNGzIVvMfcU40lUhUBb+ZjOFJEZKULk89XuXvVjbyyJ8jLCyQcmgZFdq8TOaM1",
		"part1": {
			"ciphertext": "d4b016440dafc963a32fe5ee3a36b9f7c70b7236",
			"nonce": "0da9d1ea6d1daa4b8e26665adf03ff4d",
			"tag": "123eb2f8bb6d428e3ff5ab901507c1fe",
		},
		"part2": {
			"ciphertext": "72a6cf1e6e4be440f7dd767641f6e861d2ccdda7",
			"nonce": "339552633b5c2a589d46dbc8526e37d1",
			"tag": "b73ec3fa75f2cbe2615be7d5d386f13a",
		},
		"part3": {
			"ciphertext": "77395e334a5b1a72216666e3ea2cb80a202d6ec7",
			"nonce": "008ff7c930d16b2722079896bf34ebf5",
			"tag": "962880399bbca58c52ba673dc086ad01",
		}
	}


def test_valid_data(valid_data: dict):
	dpd = DeploymentPrivateData(**valid_data)
	parts = [dpd.part1, dpd.part2, dpd.part3]
	for i, part in enumerate(parts, start=1):
		assert isinstance(part, AESCipher), \
			f"dpd.part{i} should be an instance of AESCipher."


def test_invalid_longer_salt(valid_data: dict):
	invalid_data = {**valid_data, "salt": valid_data["salt"] + '1'}
	errmsg = "salt must be 64 chars in length."
	with pytest.raises(ValidationError, match=errmsg):
		DeploymentPrivateData(**invalid_data)


def test_invalid_shorter_salt(valid_data: dict):
	invalid_data = {**valid_data, "salt": valid_data["salt"][:-1]}
	errmsg = "salt must be 64 chars in length."
	with pytest.raises(ValidationError, match=errmsg):
		DeploymentPrivateData(**invalid_data)


def test_invalid_salt_chars(valid_data: dict):
	invalid_chars = string.whitespace + string.punctuation
	invalid_chars = [c for c in invalid_chars if c not in '/+']
	for inv_char in invalid_chars:
		salt = valid_data["salt"][:-1] + inv_char
		invalid_data = {**valid_data, "salt": salt}
		errmsg = r"salt must consist of valid chars: a-z, A-Z, 0-9, '/\+'."
		with pytest.raises(ValidationError, match=errmsg):
			DeploymentPrivateData(**invalid_data)


def test_encrypt_decrypt(valid_data: dict):
	password = "password123"
	age_sk = "AGE-SECRET-KEY-1DGXNT7S5HG5XNSS5QRG038QN797E2TVM9MFSY2P8PPTQ038C4HWS5C6TTU"
	dpd = DeploymentPrivateData.encrypt(password, age_sk, valid_data["id"], testing=True)
	assert isinstance(dpd, DeploymentPrivateData), \
		"encrypt method should return an instance of DeploymentPrivateData."
	dec_age_sk = dpd.decrypt(password, testing=True)
	assert dec_age_sk == age_sk, \
		"decrypted age secret key must match the original secret key."
