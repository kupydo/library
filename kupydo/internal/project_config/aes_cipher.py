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
from pydantic import BaseModel
from Cryptodome.Cipher import AES


__all__ = ["AESCipher"]


class AESCipher(BaseModel):
	ciphertext: str
	nonce: str
	tag: str

	@classmethod
	def encrypt(cls, key: bytes, plaintext: str) -> AESCipher | None:
		if len(plaintext) == 0:
			return None
		data_bytes = plaintext.encode("UTF-8")
		cipher = AES.new(key, AES.MODE_GCM)
		ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
		return AESCipher(
			ciphertext=ciphertext.hex(),
			nonce=cipher.nonce.hex(),
			tag=tag.hex()
		)

	def decrypt(self, key: bytes) -> str | None:
		try:
			ciphertext = bytes.fromhex(self.ciphertext)
			nonce = bytes.fromhex(self.nonce)
			tag = bytes.fromhex(self.tag)
			cipher = AES.new(key, AES.MODE_GCM, nonce)
			decrypted = cipher.decrypt_and_verify(ciphertext, tag)
			return decrypted.decode("UTF-8")
		except ValueError:
			return None
