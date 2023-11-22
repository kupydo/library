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
from kupydo.internal import utils


def test_valid_sid():
	valid_sid = "1234567890abcdef1234567890abcdef"
	expected_output = f"[ENC_ID>{valid_sid}<ID_END]"
	assert utils.wrap_sid(valid_sid) == expected_output, \
		"wrap_sid should correctly wrap a valid SID"


def test_invalid_length():
	invalid_sid_length = "12345"
	assert utils.wrap_sid(invalid_sid_length) is None, \
		"wrap_sid should return None for SIDs with incorrect length"


def test_invalid_characters():
	invalid_sid_characters = "1234567890abcdeg" * 2
	assert utils.wrap_sid(invalid_sid_characters) is None, \
		"wrap_sid should return None for SIDs with invalid characters"


def test_empty_string():
	assert utils.wrap_sid('') is None, \
		"wrap_sid should return None for an empty string"
