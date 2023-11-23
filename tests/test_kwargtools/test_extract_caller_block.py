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


def test_simple_function_call():
	lines = ["print('Hello World')"]
	result = tools.extract_caller_block(lines, 1)
	assert result.start == 0 and result.end == 0, \
		"Should correctly identify the block for a simple function call"


def test_multiline_class_instantiation():
	lines = [
		"MyClass(",
		"    first_kwarg=nested(func())",
		"    second_kwarg=OtherClass(",
		"        first_kwarg='asdfg'",
		"        second_kwarg=12345",
		"    )",
		")"
	]
	result = tools.extract_caller_block(lines, 1)
	assert result.start == 0 and result.end == 6, \
		"Should correctly identify the block for nested function calls"


def test_imbalanced_start_parentheses():
	lines = ["SomeFunction(", "   arg1, arg2"]
	result = tools.extract_caller_block(lines, 1)
	assert result is None, \
		"Should return None when parentheses are not balanced"


def test_imbalanced_end_parentheses():
	lines = ["SomeFunction", "   arg1, arg2)"]
	result = tools.extract_caller_block(lines, 1)
	assert result is None, \
		"Should return None when parentheses are not balanced"
