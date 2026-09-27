"""MARC datafield 902 (handle id) -> ``iisgv:nativeViewer``, as an
``xsd:anyURI``-typed string literal."""

from __future__ import annotations

from rdflib import XSD, Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import HANDLE, IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    text = subfield_text(datafield, 0)
    if not text:
        return
    parts = text.split("/", 1)
    if len(parts) != 2 or not parts[1]:
        return
    url = f"{HANDLE}{parts[1]}"
    g.add((item, IISGV.nativeViewer, Literal(url, datatype=XSD.anyURI)))
