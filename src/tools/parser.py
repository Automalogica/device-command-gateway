from abc import ABC, abstractmethod
from typing import Any
import json
import xml.etree.ElementTree as ET


class BaseParser(ABC):

    @abstractmethod
    def parse(self, payload: bytes) -> dict[str, Any]:
        """Converts raw payload to dict"""
        ...

    def _decode(self, payload: bytes) -> str:
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"Wrong encoding for payload: {e}") from e


class XMLHandler(BaseParser):

    def parse(self, payload: bytes) -> dict[str, Any]:
        raw = self._decode(payload)
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as e:
            raise ValueError(f"XML poorly formatted: {e}") from e

        return {child.tag: child.text for child in root}


class JSONHandler(BaseParser):

    def parse(self, payload: bytes) -> dict[str, Any]:
        raw = self._decode(payload)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON poorly formatted: {e}") from e

        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, received: {type(data).__name__}")

        return data