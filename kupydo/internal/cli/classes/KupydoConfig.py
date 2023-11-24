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
from pydantic import BaseModel, field_validator
from kupydo.internal.cli import utils


class KupydoProjectDetails(BaseModel):
	name: str
	path: str
	pubkey: str

	@field_validator("name")
	@classmethod
	def validate_name(cls, v: str) -> str:
		assert len(v) <= 20, "name must be less than or equal to 20 characters."
		assert v.isalnum(), "name must consist of alphanumeric characters: a-z, 0-9."
		return v

	@field_validator("path", mode="before")
	@classmethod
	def validate_path(cls, v: str) -> str:
		path = utils.resolve_repo_rel_path(v)
		assert path.is_file(), "path cannot point to a non-existent file."
		assert path.name == "Heart.py", "path must point to a file named 'Heart.py'."
		return v

	@field_validator("pubkey")
	@classmethod
	def validate_pubkey(cls, v: str) -> str:
		allowed_pattern = r'^age[0-9a-z]{59}$'
		forbidden_pattern = r"^AGE-SECRET-KEY-[0-9A-Z]{59}$"
		assert re.match(forbidden_pattern, v) is None, \
			"not allowed to assign an AGE secret key to the pubkey field."
		assert re.match(allowed_pattern, v) is not None, \
			"must assign a valid AGE public key to the pubkey field."
		return v


class KupydoConfig(BaseModel):
	projects: list[KupydoProjectDetails]
