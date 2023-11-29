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
from typing import cast
from dotmap import DotMap
from kupydo.internal.utils import data_utils


def test_match_dict_structure_with_identical_dicts():
    ref = {'a': 1, 'b': {'x': 10, 'y': 20}}
    comp = {'a': 5, 'b': {'x': 15, 'y': 25}}
    assert data_utils.match_dict_structure(ref, comp)


def test_match_dict_structure_with_dict_and_dotmap():
    ref = {'a': 1, 'b': {'x': 10, 'y': 20}}
    comp = DotMap(a=5, b=DotMap(x=15, y=25))
    assert data_utils.match_dict_structure(ref, comp)


def test_match_dict_structure_with_different_types():
    ref = {'a': 1, 'b': 2}
    comp = DotMap(a=1, b='2')
    assert not data_utils.match_dict_structure(ref, comp)


def test_match_dict_structure_with_non_matching_nested_keys():
    ref = {'a': {'x': 10}, 'b': 2}
    comp = DotMap(a=DotMap(y=10), b=2)
    assert not data_utils.match_dict_structure(ref, comp)


def test_match_dict_structure_with_empty_structures():
    ref = {}
    comp = DotMap()
    assert data_utils.match_dict_structure(ref, comp)


def test_match_dict_structure_with_non_dict_dotmap_input():
    ref = {'a': 1, 'b': 2}
    comp = cast(dict, 'Not a dictionary')
    assert not data_utils.match_dict_structure(ref, comp)


def test_match_dotmap_structure_with_nested_dotmaps():
    ref = DotMap(a=1, b=DotMap(x=10, y=DotMap(z=30)))
    comp = DotMap(a=1, b=DotMap(x=10, y=DotMap(z=30)))
    assert data_utils.match_dict_structure(ref, comp)
