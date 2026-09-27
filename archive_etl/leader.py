"""MARC leader position 7 -> ``rdf:type``."""

from __future__ import annotations

from .prefixes import RICO, SDO

# Position 7 (0-indexed) of the leader is the bibliographic level code.
# 'c' = collection -> a RiC-O record set. Additionally typed as
# sdo:ArchiveComponent so the resource has a recognizable schema.org type
# for NDE AP consumers, alongside the RiC-O type that names what it actually
# is archivally.
LEADER_TYPE = {
    "c": [RICO.RecordSet, SDO.ArchiveComponent],
}


def types_from_leader(leader_text: str) -> list:
    if len(leader_text) <= 7:
        return []
    return LEADER_TYPE.get(leader_text[7], [])
