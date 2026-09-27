"""MARC datafield 545 (biographical/historical note) -> ``iisgv:biography``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.biography)
