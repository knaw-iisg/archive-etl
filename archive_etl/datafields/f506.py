"""MARC datafield 506 (restrictions on access) -> ``iisgv:access`` /
``iisgv:accessRestriction``, split on a blank line."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    text = subfield_text(datafield, 0)
    if not text:
        return
    parts = text.split("\n\n", 1)
    g.add((item, IISGV.access, Literal(parts[0])))
    if len(parts) > 1 and parts[1]:
        g.add((item, IISGV.accessRestriction, Literal(parts[1])))
