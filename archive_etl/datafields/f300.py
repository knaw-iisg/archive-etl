"""MARC datafield 300 (physical description) -> ``iisgv:physicalDescription``,
one triple per subfield."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_text
from ..prefixes import IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        text = get_text(sub)
        if text:
            g.add((item, IISGV.physicalDescription, Literal(text)))
