# archive-etl

Maps IISG's OAI-PMH-harvested MARCXML archival descriptions to RDF: mostly
schema.org plus the [RiC-O](https://www.ica.org/standards/RiC/ontology)
`rico:RecordSet` type for what an archival unit actually is, and a small
`iisgv:` vocabulary for fields with no natural schema.org home. Aims at the
[NDE Schema.org Application Profile](https://docs.nde.nl/schema-profile/)
(SCHEMA-AP-NDE) -- persistent item URIs, `sdo:sdDatePublished` (typed
`xsd:dateTime`), `sdo:isPartOf` a dataset. See `archive_etl/nde_ap.py`'s
docstring for what's covered and what's deliberately left open.

**`sdo:name`/`sdo:description` are not language-tagged.** MARC 041 records
the language(s) of the *archival materials* (e.g. foreign correspondence),
not the language the finding-aid text is written in -- those routinely
differ (a Russian anarchist's papers, described in English). Tagging from
041 was tried and produced visibly wrong results (an English title tagged
`@rus`), so it was removed rather than shipped; see `datafields/f245.py`.

**Known gap:** MARC 100 (the archive's creator) currently only produces raw
`marc:100-1--a`/`marc:100-1--e` predicates, not a semantic `sdo:creator`
link -- that mapping was never built here (this mirrors how the source
TypeScript pipeline behaves too).

## Public instance

This pipeline's output is merged with six others into a single public
knowledge graph, browsable at **https://kb.zijdeman.nl** and queryable
directly at **https://sparql.zijdeman.nl** (or via QLever's own query UI
at **https://kg.zijdeman.nl**) -- see
[iisg-kb-viewer](https://github.com/knaw-iisg/iisg-kb-viewer) and
[triplestore](https://github.com/knaw-iisg/triplestore).

## Install

```bash
python -m venv .venv
.venv/bin/pip install -e ".[test]"
```

## Run

```bash
# All sample records under static/archive/sourceData/:
python -m archive_etl.cli --source fixtures --out archive.ttl

# Just one record, printed to stdout:
python -m archive_etl.cli --source fixtures --record-id ARCH00018

# Live OAI-PMH harvest of the full iish.archieven set (slow -- add --limit):
python -m archive_etl.cli --source oai --limit 50 --out archive.ttl
```

## Test

```bash
.venv/bin/pytest
```

## Layout

Mirrors [biblio-etl](https://github.com/knaw-iisg/biblio-etl)'s structure:

- `archive_etl/datafields/f<tag>.py` -- one MARC datafield tag per module.
- `archive_etl/pipeline.py` -- per-record orchestration: leader -> type,
  raw `marc:leader---`/`marc:NNN---` preservation for the leader and
  controlfields, then dispatches each datafield by tag.
- `archive_etl/nde_ap.py` -- record-level NDE AP enrichment (dataset link,
  `sdDatePublished`), applied after field mapping.
- `archive_etl/harvest.py` -- OAI-PMH client; `static/archive/sourceData/`
  fixtures are interchangeable inputs with it for `pipeline.process_record`.
