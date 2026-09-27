"""MARC datafield 651 (subject added entry - geographic name), resolved to
a country -> ``iisgv:country`` / ``sdo:about``."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import subfield_text
from ..countries import country_alpha2
from ..prefixes import IISGV, LEXVO_ISO3166, SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    text = subfield_text(datafield, 0)
    if not text:
        return
    country_name = text.split(" (", 1)[0]
    if not country_name:
        return
    code = country_alpha2(country_name)
    if not code:
        return
    country = LEXVO_ISO3166[code]
    g.add((item, IISGV.country, country))
    g.add((item, SDO.about, country))
