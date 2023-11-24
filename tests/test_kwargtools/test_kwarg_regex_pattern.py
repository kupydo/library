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
from kupydo.internal import tools


def test_with_equal():
    line = "  key = value  "
    keyword = "key"
    value = "value"
    pattern = tools.kwarg_regex_pattern(line, keyword, value)
    assert pattern == r"^.*\s*key\s*=\s*['\"]value['\"].*\s*$", \
        "Should generate correct regex for '=' separator"


def test_with_colon():
    line = "  'key' : 'value'  "
    keyword = "key"
    value = "value"
    pattern = tools.kwarg_regex_pattern(line, keyword, value)
    assert pattern == r"^.*\s*['\"]key['\"]\s*:\s*['\"]value['\"].*\s*$", \
        "Should generate correct regex for ':' separator"


def test_invalid_line_format():
    line = "not a valid key value line"
    keyword = "key"
    value = "value"
    pattern = tools.kwarg_regex_pattern(line, keyword, value)
    assert pattern is None, \
        "Should return None for a line that does not match expected format"


def test_special_characters_in_keyword_value():
    line = "special$key='special@value'"
    keyword = "special$key"
    value = "special@value"
    pattern = tools.kwarg_regex_pattern(line, keyword, value)
    escaped_keyword = re.escape(keyword)
    escaped_value = re.escape(value)
    expected_pattern = rf"^.*\s*{escaped_keyword}\s*=\s*['\"]{escaped_value}['\"].*\s*$"
    assert pattern == expected_pattern, \
        "Should correctly escape special characters in keyword and value"
