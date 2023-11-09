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
import random
import string


__all__ = ["generate_name"]


def generate_name():
    chars = string.ascii_lowercase + string.digits
    chosen = ''.join(random.choices(chars, k=15))
    return f"{chosen[:5]}-{chosen[5:10]}-{chosen[10:]}"
