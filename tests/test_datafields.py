"""Unit tests for individual datafield handlers, using small hand-built
MARC subfield snippets (independent of the OAI fixtures)."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import Namespace

from archive_etl.datafields import f506, f583, f651, f852, f902

SDO = Namespace("http://schema.org/")
IISGV = Namespace("https://iisg.amsterdam/vocab/")
ISO3166 = Namespace("http://www.lexvo.org/page/iso3166/")

ITEM = URIRef("https://iisg.amsterdam/id/collection/1")


def test_f506_access_and_restriction():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Not restricted.\n\nExcept for X."}}
    f506.process(ITEM, datafield, g)
    assert (ITEM, IISGV.access, Literal("Not restricted.")) in g
    assert (ITEM, IISGV.accessRestriction, Literal("Except for X.")) in g


def test_f506_access_only():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Not restricted."}}
    f506.process(ITEM, datafield, g)
    assert (ITEM, IISGV.access, Literal("Not restricted.")) in g
    assert not list(g.objects(ITEM, IISGV.accessRestriction))


def test_f583_action_note_both_values():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Processing Information: Inventory made in 2003."}}
    f583.process(ITEM, datafield, g)
    values = {str(o) for o in g.objects(ITEM, IISGV.actionNote)}
    assert values == {
        "Inventory made in 2003.",
        "Processing Information: Inventory made in 2003.",
    }


def test_f651_united_states_special_case():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "United States (something)"}}
    f651.process(ITEM, datafield, g)
    assert (ITEM, IISGV.country, ISO3166.US) in g
    assert (ITEM, SDO.about, ISO3166.US) in g


def test_f651_country_lookup():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "Germany (something)"}}
    f651.process(ITEM, datafield, g)
    assert (ITEM, IISGV.country, ISO3166.DE) in g


def test_f852_publisher_and_location():
    g = Graph()
    datafield = {"marc:subfield": [
        {"@code": "a", "$text": "International Institute of Social History"},
        {"@code": "b", "$text": "IISH"},
    ]}
    f852.process(ITEM, datafield, g)
    assert (ITEM, IISGV.publisher, Literal("International Institute of Social History")) in g
    assert (ITEM, IISGV.location, Literal("IISH")) in g


def test_f902_handle_url():
    g = Graph()
    datafield = {"marc:subfield": {"@code": "a", "$text": "10622/ARCH00018"}}
    f902.process(ITEM, datafield, g)
    values = list(g.objects(ITEM, IISGV.nativeViewer))
    assert len(values) == 1
    assert str(values[0]) == "http://hdl.handle.net/10622/ARCH00018"
