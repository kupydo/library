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


def test_line_with_equal_separator():
	line = 'key="value"'
	expected_output = ("key", "=", '"value"')
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should correctly separate line using '=' as separator"


def test_line_with_colon_separator():
	line = "'key' : 'value'"
	expected_output = ("'key' ", ":", " 'value'")
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should correctly separate line using ':' as separator"


def test_line_with_both_separators_equal_first():
	line = "key=value:other"
	expected_output = ("key", "=", "value:other")
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should prioritize '=' as separator when it appears before ':'"


def test_line_with_both_separators_colon_first():
	line = "key:value=other"
	expected_output = ("key", ":", "value=other")
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should prioritize ':' as separator when it appears before '='"


def test_line_with_double_equal_separators():
	line = "key=value=extra"
	expected_output = ("key", "=", "value=extra")
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should correctly handle line with double '=' separators, splitting at the first one"


def test_line_with_double_colon_separators():
	line = "key:value:extra"
	expected_output = ("key", ":", "value:extra")
	assert utils.separate_kwarg_line(line) == expected_output, \
		"Should correctly handle line with double ':' separators, splitting at the first one"


def test_line_without_separators():
	line = "justakeyword"
	assert utils.separate_kwarg_line(line) is None, \
		"Should return None when no separator is present"


def test_line_with_empty_value():
	line = "key="
	assert utils.separate_kwarg_line(line) is None, \
		"Should handle line with keyword and no value"


def test_line_with_empty_key():
	line = "=value"
	assert utils.separate_kwarg_line(line) is None, \
		"Should handle line with value and no keyword"


def test_empty_line():
	line = ""
	assert utils.separate_kwarg_line(line) is None, \
		"Should return None for an empty line"
