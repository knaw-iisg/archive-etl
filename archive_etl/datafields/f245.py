"""MARC datafield 245 (title statement) -> ``sdo:name`` plus
``sdo:temporalCoverage``.

``sdo:name`` is deliberately left without a language tag: MARC 041 records
the language(s) of the *archival materials* being described (e.g. foreign
correspondence), not the language the finding-aid text itself is written
in -- those are frequently different (see the module docstring in
``pipeline.py``), so tagging ``sdo:name`` from 041 would often be wrong.
"""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))

    if len(subfields) >= 1 and get_code(subfields[0]) == "a":
        text = get_text(subfields[0])
        if text:
            g.add((item, SDO.name, Literal(text)))

    if len(subfields) >= 2 and get_code(subfields[1]) == "f":
        text = get_text(subfields[1])
        if text:
            g.add((item, SDO.temporalCoverage, Literal(text)))
