"""MARC datafield 100 (main entry - personal name, i.e. the archive's
creator). Preserves the raw ``marc:100-1--a``/``marc:100-1--e`` predicates
the current pipeline uses here rather than a semantic ``sdo:creator`` link --
that mapping was never built for archives (unlike biblio's 100 field), which
is tracked separately as a known gap.
"""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text
from ..prefixes import MARC


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    name = subfield_text(datafield, 0)
    if name:
        g.add((item, MARC["100-1--a"], Literal(name)))

    relator = subfield_text(datafield, 1)
    if relator:
        g.add((item, MARC["100-1--e"], Literal(relator)))
