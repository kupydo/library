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


@utils.deepcopy_cache
def complex_function(x):
    return [x, {"key": x}]


def test_caching_behavior():
    result1 = complex_function(10)
    result2 = complex_function(10)
    assert result1 == result2


def test_deepcopy_functionality():
    result1 = complex_function(10)
    result2 = complex_function(10)

    result1[0] = 20
    assert result2[0] == 10


def test_functionality_preservation():
    result = complex_function(15)
    assert result == [15, {"key": 15}]
