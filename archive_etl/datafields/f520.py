"""MARC datafield 520 (summary/abstract) -> ``sdo:description``.

Left without a language tag for the same reason as ``f245.py``'s
``sdo:name`` -- MARC 041 describes the archival materials' languages, not
the finding-aid text's own language.
"""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    text = subfield_text(datafield, 0)
    if text:
        g.add((item, SDO.description, Literal(text)))
