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
import string
from dotmap import DotMap
from pydantic import ValidationError
from Cryptodome.Random import get_random_bytes
from kupydo.internal.project_config import AESCipher


@pytest.fixture(name="valid_data")
def fixture_valid_data() -> DotMap:
	return DotMap(
		ciphertext="d4b016440dafc963a32fe5ee3a36b9f7c70b7236",
		nonce="0da9d1ea6d1daa4b8e26665adf03ff4d",
		tag="123eb2f8bb6d428e3ff5ab901507c1fe"
	)


@pytest.fixture(name="non_hex_chars")
def fixture_non_hex_chars() -> list[str]:
	return [
		c for c in string.printable
		if c not in '0123456789abcdef'
	]


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


def test_decrypt_invalid_ciphertext(valid_data: DotMap):
	key = get_random_bytes(32)
	invalid_data = {**valid_data, "ciphertext": valid_data.ciphertext[::-1]}
	decrypted = AESCipher(**invalid_data).decrypt(key)
	assert decrypted is None, \
		"Decryption should return None for invalid ciphertext."


def test_decrypt_invalid_nonce(valid_data: DotMap):
	key = get_random_bytes(32)
	invalid_data = {**valid_data, "nonce": valid_data.nonce[::-1]}
	decrypted = AESCipher(**invalid_data).decrypt(key)
	assert decrypted is None, \
		"Decryption should return None for invalid nonce."


def test_decrypt_invalid_tag(valid_data: DotMap):
	key = get_random_bytes(32)
	invalid_data = {**valid_data, "tag": valid_data.tag[::-1]}
	decrypted = AESCipher(**invalid_data).decrypt(key)
	assert decrypted is None, \
		"Decryption should return None for invalid tag."


def test_ciphertext_invalid_length(valid_data: DotMap):
	invalid_data = {**valid_data, "ciphertext": ''}
	errmsg = "AES ciphertext length must be greater than 0."
	with pytest.raises(ValidationError, match=errmsg):
		AESCipher(**invalid_data)


def test_nonce_invalid_length(valid_data: DotMap):
	for bad_nonce in [valid_data.nonce[:-1], valid_data.nonce + "1"]:
		invalid_data = {**valid_data, "nonce": bad_nonce}
		errmsg = "AES nonce must be 32 chars in length."
		with pytest.raises(ValidationError, match=errmsg):
			AESCipher(**invalid_data)


def test_tag_invalid_length(valid_data: DotMap):
	for bad_tag in [valid_data.tag[:-1], valid_data.tag + "1"]:
		invalid_data = {**valid_data, "tag": bad_tag}
		errmsg = "AES tag must be 32 chars in length."
		with pytest.raises(ValidationError, match=errmsg):
			AESCipher(**invalid_data)


def test_ciphertext_invalid_chars(valid_data: DotMap, non_hex_chars: list[str]):
	for bad_char in non_hex_chars:
		bad_ciphertext = valid_data.ciphertext[:-1] + bad_char
		invalid_data = {**valid_data, "ciphertext": bad_ciphertext}
		errmsg = "AES ciphertext must only consist of hex chars."
		with pytest.raises(ValidationError, match=errmsg):
			AESCipher(**invalid_data)


def test_nonce_invalid_chars(valid_data: DotMap, non_hex_chars: list[str]):
	for bad_char in non_hex_chars:
		bad_nonce = valid_data.nonce[:-1] + bad_char
		invalid_data = {**valid_data, "nonce": bad_nonce}
		errmsg = "AES nonce must only consist of hex chars."
		with pytest.raises(ValidationError, match=errmsg):
			AESCipher(**invalid_data)


def test_tag_invalid_chars(valid_data: DotMap, non_hex_chars: list[str]):
	for bad_char in non_hex_chars:
		bad_tag = valid_data.tag[:-1] + bad_char
		invalid_data = {**valid_data, "tag": bad_tag}
		errmsg = "AES tag must only consist of hex chars."
		with pytest.raises(ValidationError, match=errmsg):
			AESCipher(**invalid_data)
