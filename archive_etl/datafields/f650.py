"""MARC datafield 650 (subject added entry - topical term) ->
``iisgv:topicalTerm``, from the first subfield only."""

from ..prefixes import IISGV
from .common import simple_literal_handler

process = simple_literal_handler(IISGV.topicalTerm)
