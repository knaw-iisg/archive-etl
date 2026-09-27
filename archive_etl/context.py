"""Small shared utilities used across the ``datafields`` handlers."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote


def as_array(value: Any) -> list:
    """MARC subfields/datafields are a single dict when there's exactly one,
    or a list when there are several -- this normalizes both to a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_code(subfield: dict) -> str | None:
    return subfield.get("@code")


def get_text(subfield: dict) -> str | None:
    text = subfield.get("$text")
    if text is None:
        return None
    return str(text)


def subfield_text(datafield: dict, index: int = 0) -> str | None:
    """The text of the ``index``-th subfield of a datafield, or ``None`` if
    there aren't that many."""
    subfields = as_array(datafield.get("marc:subfield"))
    if index >= len(subfields):
        return None
    return get_text(subfields[index])


def mint_id(local_id: str) -> str:
    """Percent-encode characters that aren't valid in an IRI path segment."""
    return quote(local_id, safe="")
