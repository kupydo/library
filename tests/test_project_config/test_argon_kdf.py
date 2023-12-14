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
import time
import pytest
import base64
from kupydo.internal.project_config import DerivedArgonKey


def test_init_without_salt():
	password = "TestPassword"
	key = DerivedArgonKey(password, testing=True)
	assert key.salt is not None, \
		"Salt should be generated when not provided"
	assert key.hash is not None, \
		"Hash should be generated"


def test_init_with_salt():
	password = "TestPassword"
	salt = base64.b64encode(b"MyTestSalt").decode()
	key = DerivedArgonKey(password, salt=salt, testing=True)
	assert key.salt == salt, \
		"Provided salt should be used"


def test_password_hashing():
	password = "TestPassword"
	key = DerivedArgonKey(password, testing=True)
	assert isinstance(key.hash, bytes), \
		"Hash should be bytes"


def test_salt_encoding():
	password = "TestPassword"
	key = DerivedArgonKey(password, testing=True)
	assert isinstance(key.salt, str), "Salt should be a string"
	try:
		base64.b64decode(key.salt)
	except ValueError:
		pytest.fail("Salt is not properly base64 encoded")


def test_invalid_salt_input():
	password = "TestPassword"
	invalid_salt = "NotBase64"
	with pytest.raises(ValueError):
		DerivedArgonKey(password, salt=invalid_salt, testing=True)


def test_consistent_hash_with_same_salt():
	password = "TestPassword"
	salt = base64.b64encode(b"MyConsistentSalt").decode()
	key1 = DerivedArgonKey(password, salt=salt, testing=True)
	key2 = DerivedArgonKey(password, salt=salt, testing=True)
	assert key1.hash == key2.hash, \
		"Hashes should be identical for same password and salt"


def test_real_compute_cost():
	start = time.time()
	DerivedArgonKey("TestPassword")
	end = time.time()
	delta = end - start
	assert delta > 1.5, \
		"Argon hash compute cost must be larger than 1.5 seconds."
