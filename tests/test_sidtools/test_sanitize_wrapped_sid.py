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
from kupydo.internal import tools


def test_valid_sid_with_brackets():
	assert tools.sanitize_wrapped_sid("abc[123]xyz") == "[123]", \
		"Should extract substring between brackets"


def test_missing_opening_bracket():
	assert tools.sanitize_wrapped_sid("abc123]xyz") is None, \
		"Should return None if opening bracket is missing"


def test_missing_closing_bracket():
	assert tools.sanitize_wrapped_sid("abc[123xyz") is None, \
		"Should return None if closing bracket is missing"


def test_brackets_in_wrong_order():
	assert tools.sanitize_wrapped_sid("abc]123[xyz") is None, \
		"Should return None if brackets are in the wrong order"


def test_empty_string():
	assert tools.sanitize_wrapped_sid("") is None, \
		"Should return None for an empty string"


def test_no_brackets():
	assert tools.sanitize_wrapped_sid("abc123xyz") is None, \
		"Should return None if no brackets are present"
