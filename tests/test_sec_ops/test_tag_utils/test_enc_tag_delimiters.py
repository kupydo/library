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


def test_returns_tuple():
	delimiters = sec_ops.enc_tag_delimiters()
	assert isinstance(delimiters, tuple), \
		"get_sid_delimiters should return a tuple"


def test_tuple_length():
	delimiters = sec_ops.enc_tag_delimiters()
	assert len(delimiters) == 2, \
		"Delimiters tuple should have exactly two elements"


def test_correct_values():
	delimiters = sec_ops.enc_tag_delimiters()
	assert delimiters[0] == "[ENC_ID>", \
		"The first delimiter does not match the expected prefix"
	assert delimiters[1] == "<ID_END]", \
		"The second delimiter does not match the expected suffix"
