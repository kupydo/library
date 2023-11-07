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
from typehints import MetaDict
from pydantic import validate_call


class MetadataValues:
    @validate_call
    def __init__(
            self,
            name: str,
            namespace: str = None,
            annotations: MetaDict = None,
            labels: MetaDict = None
    ) -> None:
        self.__values__ = dict(
            name=name,
            namespace=namespace,
            annotations=annotations,
            labels=labels
        )

    @property
    def name(self) -> str:
        return self.__values__.get("name", "")

    @name.setter
    @validate_call
    def name(self, value: str) -> None:
        self.__values__["name"] = value

    @property
    def namespace(self) -> str:
        return self.__values__.get("namespace", "")

    @namespace.setter
    @validate_call
    def namespace(self, value: str | None = None) -> None:
        self.__values__["namespace"] = value

    @property
    def annotations(self) -> MetaDict:
        return self.__values__.get("annotations", {})

    @annotations.setter
    @validate_call
    def annotations(self, value: MetaDict = None) -> None:
        self.__values__["annotations"] = value

    @property
    def labels(self) -> MetaDict:
        return self.__values__.get("labels", {})

    @labels.setter
    @validate_call
    def labels(self, value: MetaDict = None) -> None:
        self.__values__["labels"] = value
