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
import site
from pathlib import Path
from email.parser import Parser
from kupydo.internal.errors import *


class PackageInfo:
    name: str
    version: str
    summary: str
    license: str
    author: str
    homepage: str

    def __init__(self):
        data = self._read_package_info()
        for k, v in data.items():
            k = k.replace('-', '').lower()
            if k in self.__annotations__:
                setattr(self, k, v)
        for k in self.__annotations__.keys():
            if k not in self.__dict__:
                raise InvalidPackageError

    @staticmethod
    def _read_package_info() -> dict:
        for site_dir in site.getsitepackages():
            sd = Path(site_dir)
            if "site-packages" in sd.as_posix():
                for child in sd.iterdir():
                    if child.name.startswith('kupydo') and child.suffix == '.dist-info':
                        meta = child / 'METADATA'
                        if meta.is_file():
                            parser = Parser()
                            contents = meta.read_text()
                            parsed_metadata = parser.parsestr(contents)
                            return dict(parsed_metadata)
        raise InvalidPackageError
