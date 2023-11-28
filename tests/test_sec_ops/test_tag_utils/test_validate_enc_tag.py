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


VALID_SID = "1234567890abcdef1234567890abcdef"
INVALID_SID_CHARACTERS = "1234567890abcdeg1234567890abcdeg"
INVALID_SID_LENGTH = "12345678"


def test_with_valid_sid():
	wrapped_valid_sid = f"[ENC_ID>{VALID_SID}<ID_END]"
	assert sec_ops.validate_enc_tag(wrapped_valid_sid) == VALID_SID, \
		"Failed to validate a wrapped valid SID"


def test_with_invalid_sid_length():
	wrapped_invalid_sid = f"[ENC_ID>{INVALID_SID_LENGTH}<ID_END]"
	assert sec_ops.validate_enc_tag(wrapped_invalid_sid) is None, \
		"Incorrectly validated a wrapped SID with invalid length"


def test_with_invalid_sid_characters():
	wrapped_invalid_char_sid = f"[ENC_ID>{INVALID_SID_CHARACTERS}<ID_END]"
	assert sec_ops.validate_enc_tag(wrapped_invalid_char_sid) is None, \
		"Incorrectly validated a wrapped SID with invalid characters"


def test_without_checking_delimiters_valid_sid():
	assert sec_ops.validate_enc_tag(VALID_SID, check_delimiters=False) == VALID_SID, \
		"Failed to validate a valid SID without checking delimiters"


def test_without_checking_delimiters_invalid_sid():
	assert sec_ops.validate_enc_tag(INVALID_SID_LENGTH, check_delimiters=False) is None, \
		"Incorrectly validated an invalid SID without checking delimiters"


def test_with_missing_prefix_delimiter():
	missing_prefix_delimiter = f"{VALID_SID}<ID_END]"
	assert sec_ops.validate_enc_tag(missing_prefix_delimiter) is None, \
		"Incorrectly validated a SID missing the prefix delimiter"


def test_with_missing_suffix_delimiter():
	missing_suffix_delimiter = f"[ENC_ID>{VALID_SID}"
	assert sec_ops.validate_enc_tag(missing_suffix_delimiter) is None, \
		"Incorrectly validated a SID missing the suffix delimiter"
