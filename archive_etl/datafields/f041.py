"""MARC datafield 041 (language code) -> ``sdo:inLanguage``."""

from rdflib import Graph, URIRef

from .. import language


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    language.process(item, datafield, g)
