"""MARC datafield 852 (location) -> ``iisgv:publisher`` (subfield 0) /
``iisgv:location`` (subfield 1)."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    publisher = subfield_text(datafield, 0)
    if publisher:
        g.add((item, IISGV.publisher, Literal(publisher)))

    location = subfield_text(datafield, 1)
    if location:
        g.add((item, IISGV.location, Literal(location)))
