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
from dotmap import DotMap


__all__ = ["match_dict_structure"]


def match_dict_structure(ref: dict | DotMap, compare: dict | DotMap) -> bool:
	for arg in [ref, compare]:
		if not isinstance(arg, (dict, DotMap)):
			return False

	if set(ref.keys()) != set(compare.keys()):
		return False

	for ref_key, ref_value in ref.items():
		comp_value = compare.get(ref_key)

		if isinstance(ref_value, (dict, DotMap)):
			if not match_dict_structure(ref_value, comp_value):
				return False
		elif comp_value is None or type(ref_value) != type(comp_value):
			return False

	return True
