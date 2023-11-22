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
from dotmap import DotMap
from kupydo.internal import utils


@pytest.fixture
def base():
    return DotMap(
        name="aaaaa",
        namespace="bbbbb",
        labels=DotMap(
            firstLabel="ccccc",
            secondLabel="ddddd"
        ),
        annotations=DotMap(
            firstAnno="eeeee",
            secondAnno="fffff"
        ),
        data=DotMap(
            firstData="ggggg",
            secondData="hhhhh"
        ),
        immutable=True
    )


@pytest.fixture
def update():
    return DotMap(
        name="iiiii",
        namespace="jjjjj",
        labels=DotMap(
            firstLabel=99999,
            secondLabel=88888
        ),
        annotations=None,
        data=DotMap(
            thirdData="kkkkk"
        ),
        immutable=None
    )


@pytest.fixture
def exclude():
    return DotMap(
        name=True,
        namespace=True
    )


def test_deep_merge_patch(base, update, exclude):
    result = utils.deep_merge(base, update, exclude, method='patch')
    assert result == DotMap(
        name="aaaaa",
        namespace="bbbbb",
        labels=DotMap(
            firstLabel=99999,
            secondLabel=88888
        ),
        annotations=DotMap(
            firstAnno="eeeee",
            secondAnno="fffff"
        ),
        data=DotMap(
            firstData="ggggg",
            secondData="hhhhh",
            thirdData="kkkkk"
        ),
        immutable=True
    ), "deep merge patch result does not equal the expected model"


def test_deep_merge_replace(base, update, exclude):
    result = utils.deep_merge(base, update, exclude, method='replace')
    assert result == DotMap(
        name="aaaaa",
        namespace="bbbbb",
        labels=DotMap(
            firstLabel=99999,
            secondLabel=88888
        ),
        annotations=None,
        data=DotMap(
            thirdData="kkkkk"
        ),
        immutable=None
    ), "deep merge replace result does not equal the expected model"
