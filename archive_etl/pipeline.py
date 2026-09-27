"""Per-record OAI/MARC-JSON -> RDF pipeline."""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, URIRef

from . import nde_ap
from .context import as_array, mint_id
from .datafields import DATAFIELD_HANDLERS
from .leader import types_from_leader
from .prefixes import COLLECTION, MARC


def item_iri_from_record(record: dict) -> URIRef | None:
    identifier = record.get("header", {}).get("identifier")
    if not identifier:
        return None
    parts = identifier.split("/", 1)
    if len(parts) != 2 or not parts[1]:
        return None
    return COLLECTION[mint_id(parts[1])]


def process_record(record: dict, g: Graph) -> URIRef | None:
    """Process a single OAI-harvested archive record (already parsed from
    MARCXML into the ``marc:record``-style JSON shape used by
    ``static/archive/sourceData/*.json``) into ``g``. Returns the minted
    item IRI, or ``None`` if the record has no usable identifier."""
    item = item_iri_from_record(record)
    if item is None:
        return None

    marc_record = record.get("metadata", {}).get("marc:record", {})

    leader = marc_record.get("marc:leader", {})
    leader_text = leader.get("$text") if isinstance(leader, dict) else None
    if leader_text:
        leader_text = str(leader_text)
        for rdf_type in types_from_leader(leader_text):
            g.add((item, RDF.type, rdf_type))
        g.add((item, MARC["leader---"], Literal(leader_text)))

    for controlfield in as_array(marc_record.get("marc:controlfield")):
        tag = controlfield.get("@tag")
        text = controlfield.get("$text")
        if tag and text is not None:
            g.add((item, MARC[f"{tag}---"], Literal(str(text))))

    for datafield in as_array(marc_record.get("marc:datafield")):
        tag = datafield.get("@tag")
        for handler in DATAFIELD_HANDLERS.get(tag, []):
            handler(item, datafield, g)

    nde_ap.enrich(item, record, g)

    return item
