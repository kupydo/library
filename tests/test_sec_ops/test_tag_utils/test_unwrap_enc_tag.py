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
from kupydo.internal import sec_ops


def test_valid_wrapped_sid():
	valid_wrapped_sid = "[ENC_ID>1234567890abcdef1234567890abcdef<ID_END]"
	expected_output = "1234567890abcdef1234567890abcdef"
	assert sec_ops.unwrap_enc_tag(valid_wrapped_sid) == expected_output, \
		"unwrap_sid should correctly unwrap a valid wrapped SID"


def test_invalid_wrapped_sid_format():
	invalid_wrapped_sid_format = "ABC[ENC_ID>1234567890abcdef1234567890abcdef<ID_END]XYZ"
	assert sec_ops.unwrap_enc_tag(invalid_wrapped_sid_format) is None, \
		"unwrap_sid should return None for incorrectly formatted wrapped SIDs"


def test_invalid_wrapped_sid_length():
	invalid_wrapped_sid_length = "[ENC_ID>12345<ID_END]"
	assert sec_ops.unwrap_enc_tag(invalid_wrapped_sid_length) is None, \
		"unwrap_sid should return None for wrapped SIDs with incorrect SID length"


def test_invalid_wrapped_sid_characters():
	invalid_wrapped_sid_characters = "[ENC_ID>1234567890abcdeg1234567890abcdeg<ID_END]"
	assert sec_ops.unwrap_enc_tag(invalid_wrapped_sid_characters) is None, \
		"unwrap_sid should return None for wrapped SIDs with invalid characters"


def test_empty_string():
	assert sec_ops.unwrap_enc_tag('') is None, \
		"unwrap_sid should return None for an empty string"
