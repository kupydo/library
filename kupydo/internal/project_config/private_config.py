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
from __future__ import annotations
import string
from pathlib import Path
from pydantic import PrivateAttr, field_validator, model_validator
from Cryptodome.Hash import SHA3_256
from kupydo.internal import utils
from .argon_kdf import ArgonKDF
from .aes_cipher import AESCipher
from .base_config import *

__all__ = ["DeploymentPrivateData", "ProjectPrivateConfig"]


class DeploymentPrivateData(DeploymentBaseData):
	salt: str
	part1: AESCipher
	part2: AESCipher
	part3: AESCipher
	_age_sk_tag_ = PrivateAttr(default="AGE-SECRET-KEY-")

	@field_validator("salt")
	@classmethod
	def validate_salt(cls, v: str) -> str:
		assert len(v) == 64, \
			"salt must be 64 chars in length."
		valid_chars = string.ascii_letters + string.digits + '/+'
		assert all([c in valid_chars for c in v]), \
			"salt must consist of valid chars: a-z, A-Z, 0-9, '/+'."
		return v

	@classmethod
	def encrypt(cls, password: str, age_sk: str, depl_id: str, testing: bool = False) -> DeploymentPrivateData:
		ask_data = age_sk.lstrip(cls._age_sk_tag_.get_default())
		key = ArgonKDF(password, testing=testing)
		return DeploymentPrivateData(
			id=depl_id,
			salt=key.salt,
			part1=AESCipher.encrypt(key.hash[:24], ask_data[:20]),
			part2=AESCipher.encrypt(key.hash[24:48], ask_data[20:40]),
			part3=AESCipher.encrypt(key.hash[48:72], ask_data[40:] + ' ')
		)

	def decrypt(self, password: str, testing: bool = False) -> str:
		key = ArgonKDF(password, salt=self.salt, testing=testing)
		part1 = self.part1.decrypt(key.hash[:24])
		part2 = self.part2.decrypt(key.hash[24:48])
		part3 = self.part3.decrypt(key.hash[48:72]).rstrip()
		return self._age_sk_tag_ + part1 + part2 + part3


class ProjectPrivateConfig(ProjectBaseConfig):
	deployments: list[DeploymentPrivateData]

	@model_validator(mode="before")
	@classmethod
	def check_duplicates(cls, data: dict) -> dict:
		errmsg = "duplicate {0} values not allowed in private config file."
		if data:
			for key in ["id", "salt"]:
				values = [item[key] for item in data["deployments"]]
				assert len(set(values)) == len(values), errmsg.format(key)
			for key2 in ["ciphertext", "nonce", "tag"]:
				values = list()
				for item in data["deployments"]:
					for key1 in ["part1", "part2", "part3"]:
						values.append(item[key1][key2])
				assert len(set(values)) == len(values), errmsg.format(key2)
		return data

	@staticmethod
	def get_config_path() -> Path:
		hash_obj = SHA3_256.new()
		repo_path = utils.find_repo_path()
		hash_obj.update(repo_path.as_posix().encode())
		file_name = hash_obj.hexdigest()[:32]
		conf_dir = Path.home() / '.kupydo'
		conf_dir.mkdir(parents=True, exist_ok=True)
		conf_file = conf_dir / file_name
		conf_file.touch(exist_ok=True)
		return conf_file
