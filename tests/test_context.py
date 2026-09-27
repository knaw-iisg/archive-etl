"""Unit tests for context.py helpers, particularly text_content()."""

from __future__ import annotations

from archive_etl.context import text_content


def test_text_content_plain_string():
    """xmltodict collapses an attribute-less element (e.g. MARC's <leader>)
    to a bare string. This is the shape real harvest.py output actually
    has -- confirmed by fetching a live record -- and the shape this repo's
    own static fixtures now use after being corrected to match. Missing
    this shape silently dropped the item's rdf:type (RecordSet/
    ArchiveComponent) and the raw marc:leader--- triple for every record in
    a full 5,557-record harvest."""
    assert text_content("00000npcaa2200000 u 4500") == "00000npcaa2200000 u 4500"


def test_text_content_dict_with_text_key():
    """An element *with* attributes (e.g. a controlfield, which always has
    @tag) comes through as a dict."""
    assert text_content({"$text": "eng", "@tag": "008"}) == "eng"


def test_text_content_none_and_missing():
    assert text_content(None) is None
    assert text_content({}) is None
