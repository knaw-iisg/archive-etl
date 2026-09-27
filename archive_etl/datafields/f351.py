"""MARC datafield 351 (organization/arrangement) -> ``iisgv:arrangement``."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.arrangement)
