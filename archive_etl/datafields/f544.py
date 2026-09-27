"""MARC datafield 544 (location of related archival materials) -> ``iisgv:seeAlso``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.seeAlso)
