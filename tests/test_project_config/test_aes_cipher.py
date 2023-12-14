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
from Cryptodome.Random import get_random_bytes
from kupydo.internal.project_config import AESCipher


def test_encrypt_decrypt():
	key = get_random_bytes(32)
	plaintext = "Hello, World!"

	encrypted = AESCipher.encrypt(key, plaintext)
	assert isinstance(encrypted, AESCipher), \
		"Encryption should return an AESCipher instance."

	decrypted = encrypted.decrypt(key)
	assert decrypted == plaintext, \
		"Decrypted text should match the original plaintext."


def test_decrypt_with_wrong_key():
	key = get_random_bytes(32)
	wrong_key = get_random_bytes(32)
	plaintext = "Hello, World!"

	encrypted = AESCipher.encrypt(key, plaintext)

	decrypted = encrypted.decrypt(wrong_key)
	assert decrypted is None, \
		"Decryption with a wrong key should return None."


def test_encrypt_empty_string():
	key = get_random_bytes(32)
	plaintext = ""

	encrypted = AESCipher.encrypt(key, plaintext)
	assert encrypted is None, \
		"Encryption of an empty string should return None."


def test_decrypt_invalid_data():
	key = get_random_bytes(32)
	encrypted = AESCipher(ciphertext='invalid', nonce='invalid', tag='invalid')

	decrypted = encrypted.decrypt(key)
	assert decrypted is None, \
		"Decryption should return None for invalid data."
