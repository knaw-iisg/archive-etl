"""NDE Schema.org Application Profile (SCHEMA-AP-NDE) enrichment, applied to
every record after its MARC fields are mapped.

Reference: https://docs.nde.nl/schema-profile/ -- per-item requirements used
here: persistent URI (items are minted at ``collection:<id>``),
language-tagged ``sdo:name``/``sdo:description`` (handled directly by
``datafields/f245.py``/``f520.py`` via the language resolved from MARC 041
-- see ``pipeline.py``), ``sdo:sdDatePublished`` (typed ``xsd:dateTime``),
and ``sdo:isPartOf`` linking to the dataset.

Unlike biblio's 6XX subject fields, archive's only controlled-vocabulary
link (651 -> a country, via ``sdo:about``) points at an external lexvo.org
resource, not a locally-minted IISG entity -- so there's no DefinedTerm
wrapping to do here; typing someone else's resource as our own DefinedTerm
would misrepresent it.

What this deliberately does *not* do: register the Archive dataset in the
NDE Dataset Register (license, catalog, access-rights) -- see the
``# TODO(IISG)`` marker below, and a real ``sdo:creator`` mapping for the
archive's creator (currently only raw ``marc:100-1--a``/``100-1--e``
predicates, from ``datafields/f100.py`` -- tracked separately).
"""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, URIRef
from rdflib.namespace import XSD

from .prefixes import DATASET, SDO

DATASET_IRI = DATASET["archive"]


def _emit_dataset_description(g: Graph) -> None:
    if (DATASET_IRI, RDF.type, SDO.Dataset) in g:
        return
    g.add((DATASET_IRI, RDF.type, SDO.Dataset))
    g.add((DATASET_IRI, SDO.name, Literal("IISG Archieven", lang="nl")))
    g.add((DATASET_IRI, SDO.name, Literal("IISH Archives", lang="en")))
    g.add((DATASET_IRI, SDO.description, Literal(
        "Archiefbeschrijvingen van het Internationaal Instituut voor Sociale "
        "Geschiedenis (IISG).", lang="nl",
    )))
    # TODO(IISG): sdo:license, sdo:includedInDataCatalog, sdo:accessRights --
    # not derivable from this codebase, need an answer from IISG.


def enrich(item: URIRef, record: dict, g: Graph, *, dataset_iri: URIRef = DATASET_IRI) -> None:
    datestamp = record.get("header", {}).get("datestamp")
    if datestamp:
        g.add((item, SDO.sdDatePublished, Literal(str(datestamp), datatype=XSD.dateTime)))

    g.add((item, SDO.isPartOf, dataset_iri))
    _emit_dataset_description(g)
