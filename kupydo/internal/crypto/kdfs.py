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


__all__ = ["DerivedArgonKey"]


class DerivedArgonKey:
	__slots__ = (
		"hash",
		"salt"
	)

	def __init__(self, password: str, *, salt: str = None) -> None:
		if not salt:
			salt_bytes = secrets.token_bytes(32)
		else:
			salt_bytes = base64.b64decode(salt)
		argon = argon2.PasswordHasher(
			time_cost=2,
			memory_cost=2 ** 22,
			parallelism=4,
			hash_len=64,
			salt_len=len(salt_bytes)
		)
		b64_salt = base64.b64encode(salt_bytes)
		hash_tag = argon.hash(password, salt=b64_salt)
		key_hash = hash_tag.split('$')[-1]

		self.hash = key_hash.encode()
		self.salt = b64_salt.decode()
