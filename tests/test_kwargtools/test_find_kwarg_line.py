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
from kupydo.internal import tools
from kupydo.internal import errors


def test_find_kwarg_line_success():
	username = "asdfg"
	password = "qwerty"
	code_block = [
		f'auth = Secret.BasicAuth(',
		f'    username="{username}",',
		f'    password="{password}",',
		f'    name="login"',
		f')'
	]
	lineno1 = tools.find_kwarg_line(code_block, 0, 'username', username)
	lineno2 = tools.find_kwarg_line(code_block, 0, 'password', password)

	assert lineno1 == 1 and lineno2 == 2, \
		"Function line number output does not match expected line number"


def test_find_kwarg_line_failure():
	code_block = [
		"def example_func(a, b, c):",
		"    print(a, b, c)"
	]
	with pytest.raises(errors.KwargNotFoundError):
		tools.find_kwarg_line(code_block, 0, 'x', '10')


def test_no_kwarg_present():
	code_block = [
		"# Just a comment",
		"def no_kwarg_func(a, b):",
		"    print(a + b)"
	]
	with pytest.raises(errors.KwargNotFoundError):
		tools.find_kwarg_line(code_block, 0, 'a', '1')


def test_edge_case_empty_block():
	empty_block = []
	with pytest.raises(errors.KwargNotFoundError):
		tools.find_kwarg_line(empty_block, 0, 'x', '10')
