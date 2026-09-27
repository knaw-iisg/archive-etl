"""MARC datafield 524 (preferred citation) -> ``iisgv:preferCite``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.preferCite)
