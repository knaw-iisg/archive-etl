"""Namespace/prefix declarations used throughout the pipeline."""

from rdflib import Namespace

BASE = "https://iisg.amsterdam/"
ID = BASE + "id/"

COLLECTION = Namespace(ID + "collection/")
MARC = Namespace(BASE + "marc/")
IISGV = Namespace(BASE + "vocab/")
DATASET = Namespace(ID + "dataset/")

SDO = Namespace("https://schema.org/")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
LEXVO_ISO639_3 = Namespace("http://lexvo.org/id/iso639-3/")
LEXVO_ISO3166 = Namespace("http://www.lexvo.org/page/iso3166/")
HANDLE = Namespace("http://hdl.handle.net/10622/")

DEFAULT_GRAPH = "https://iisg.amsterdam/graph/archive"

NAMESPACE_BINDINGS = {
    "collection": COLLECTION,
    "marc": MARC,
    "iisgv": IISGV,
    "dataset": DATASET,
    "sdo": SDO,
    "rico": RICO,
    "iso639-3": LEXVO_ISO639_3,
    "iso3166": LEXVO_ISO3166,
    "handle": HANDLE,
}
