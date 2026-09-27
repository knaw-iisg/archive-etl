"""MARC datafield 530 (additional physical form note) -> ``iisgv:physicalNote``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.physicalNote)
