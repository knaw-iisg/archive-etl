"""MARC datafield 041 ($a language code(s) of the archival materials) ->
``sdo:inLanguage``. Repeatable: an archive can legitimately hold materials
in several languages. Each subfield's text is already an ISO 639-3 code,
used directly with no bibliographic/terminology-code remapping.

Note this is the language of what's *in* the archive, not of the
finding-aid text describing it -- see ``pipeline.py``'s docstring and
``datafields/f245.py`` for why it isn't used to tag ``sdo:name``/
``sdo:description``.
"""

from __future__ import annotations

from rdflib import Graph, URIRef

from .context import as_array, get_text, mint_id
from .prefixes import LEXVO_ISO639_3, SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        code = get_text(sub)
        if code:
            g.add((item, SDO.inLanguage, LEXVO_ISO639_3[mint_id(code)]))
