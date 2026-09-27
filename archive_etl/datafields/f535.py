"""MARC datafield 535 (location of originals/duplicates) -> ``iisgv:locationOfOriginals``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.locationOfOriginals)
