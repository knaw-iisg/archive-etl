"""MARC datafield 583 (action note) -> ``iisgv:actionNote``. Both the text
after a leading ``"label: "`` prefix (when present) and the full raw text
are recorded -- two distinct values on the same predicate, not a
fallback/override pair."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    text = subfield_text(datafield, 0)
    if not text:
        return
    parts = text.split(": ", 1)
    if len(parts) > 1 and parts[1]:
        g.add((item, IISGV.actionNote, Literal(parts[1])))
    g.add((item, IISGV.actionNote, Literal(text)))
