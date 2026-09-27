"""Factory for the repeated "first subfield's text -> a fixed predicate"
pattern used by several single-purpose archive fields."""

from __future__ import annotations

from typing import Callable

from rdflib import Graph, Literal, URIRef

from ..context import subfield_text


def simple_literal_handler(predicate: URIRef, *, index: int = 0) -> Callable[[URIRef, dict, Graph], None]:
    def process(item: URIRef, datafield: dict, g: Graph) -> None:
        text = subfield_text(datafield, index)
        if text:
            g.add((item, predicate, Literal(text)))

    return process
