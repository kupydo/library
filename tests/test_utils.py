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


def test_deep_merge_replace_simple():
    base = {"a": {"b": {"c": 1}}}
    update = {"a": {"b": {"c": 2}}}
    expected = {"a": {"b": {"c": 2}}}
    assert utils.deep_merge(base, update, dict(), method='replace') == expected


def test_deep_merge_replace_nested():
    base = {"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 4}
    update = {"a": {"b": {"c": 10}}}
    expected = {"a": {"b": {"c": 10, "d": 2}, "e": 3}, "f": 4}
    assert utils.deep_merge(base, update, dict(), method='replace') == expected


def test_deep_merge_patch():
    base = {"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 4}
    update = {"a": {"b": {"c": None}, "e": None}, "f": 5}
    expected = {"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 5}
    assert utils.deep_merge(base, update, dict(), method='patch') == expected


def test_deep_merge_exclude():
    base = {"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 4}
    update = {"a": {"b": {"c": 10, "d": 20}, "e": 30}, "f": 40}
    exclude = {"a": {"b": {"c": True}}}
    expected = {"a": {"b": {"c": 1, "d": 20}, "e": 30}, "f": 40}
    assert utils.deep_merge(base, update, exclude, method='replace') == expected
