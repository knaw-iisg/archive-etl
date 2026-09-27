"""Runs every static/archive/sourceData fixture through the full pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import Namespace

from archive_etl.fixtures import load_fixture
from archive_etl.pipeline import process_record

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "static" / "archive" / "sourceData"
SDO = Namespace("http://schema.org/")
IISGV = Namespace("https://iisg.amsterdam/vocab/")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")


def _fixture_paths():
    return sorted(FIXTURES_DIR.glob("*.json"))


@pytest.mark.parametrize("path", _fixture_paths(), ids=lambda p: p.stem)
def test_record_processes_without_error(path: Path):
    record = load_fixture(path)
    g = Graph()
    item = process_record(record, g)
    assert item is not None
    assert len(g) > 0


def test_arch00018_known_fields():
    record = load_fixture(FIXTURES_DIR / "archiveARCH00018.json")
    g = Graph()
    item = process_record(record, g)

    assert item == URIRef("https://iisg.amsterdam/id/collection/ARCH00018")
    assert (item, None, RICO.RecordSet) in g or (item, None, SDO.ArchiveComponent) in g

    names = {str(o) for o in g.objects(item, SDO.name)}
    assert "Michail Aleksandrovič Bakunin Papers" in names
    # sdo:name/description are untagged (see f245.py/f520.py docstrings):
    # 041 records the archived materials' languages, not the finding aid's.
    assert all(n.language is None for n in g.objects(item, SDO.name))

    languages = {str(o).rsplit("/", 1)[-1] for o in g.objects(item, SDO.inLanguage)}
    assert languages == {"rus", "ita", "fre", "ger"}

    countries = {str(o).rsplit("/", 1)[-1] for o in g.objects(item, IISGV.country)}
    assert countries == {"IT"}


def test_multi_country_record():
    record = load_fixture(FIXTURES_DIR / "record-COLL00107.json")
    g = Graph()
    item = process_record(record, g)

    countries = {str(o).rsplit("/", 1)[-1] for o in g.objects(item, IISGV.country)}
    assert countries == {"DE", "US"}


def test_nde_ap_dataset_link_and_typed_sd_date_published():
    from rdflib.namespace import XSD

    record = load_fixture(FIXTURES_DIR / "archiveARCH00018.json")
    g = Graph()
    item = process_record(record, g)

    assert (item, SDO.isPartOf, URIRef("https://iisg.amsterdam/id/dataset/archive")) in g
    dates = list(g.objects(item, SDO.sdDatePublished))
    assert dates
    assert dates[0].datatype == XSD.dateTime
