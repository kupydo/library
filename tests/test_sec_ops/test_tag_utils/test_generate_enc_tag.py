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
import re
from kupydo.internal import sec_ops


def test_returns_string():
    sid = sec_ops.generate_enc_tag()
    assert isinstance(sid, str), \
        "generate_sid should return a string"


def test_length():
    sid = sec_ops.generate_enc_tag()
    assert len(sid) == 32, \
        "generate_sid should return a 32-character string"


def test_uniqueness():
    sids = {sec_ops.generate_enc_tag() for _ in range(100)}
    assert len(sids) == 100, \
        "generate_sid should generate unique SIDs"


def test_sid_format():
    sid = sec_ops.generate_enc_tag()
    assert re.match(r'^[0-9a-f]{32}$', sid), \
        "generate_sid should return a valid hexadecimal string"
