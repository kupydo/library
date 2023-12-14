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
import argon2
import base64
import secrets


__all__ = ["ArgonKDF"]


class ArgonKDF:
	__slots__ = (
		"hash",
		"salt"
	)

	@property
	def _sb_len_(self) -> int:
		# 48-len salt_bytes results in a 64-len base64 salt str.
		# Do not reduce this value without increasing memory_cost.
		return 48

	def __init__(self, password: str, *, salt: str = None, testing: bool = False) -> None:
		dec, gen = base64.b64decode, secrets.token_bytes
		salt_bytes = dec(salt) if salt else gen(self._sb_len_)

		argon = argon2.PasswordHasher(
			memory_cost=2 ** (10 if testing else 23),
			time_cost=1,
			parallelism=4,
			hash_len=64,
			salt_len=len(salt_bytes)
		)
		b64_salt = base64.b64encode(salt_bytes)
		hash_tag = argon.hash(password, salt=b64_salt)
		key_hash = hash_tag.split('$')[-1]

		self.hash = key_hash.encode()
		self.salt = b64_salt.decode()
