"""Country name -> ISO 3166-1 alpha-2 code lookup, used by MARC 651
(geographic subject heading) to resolve a country name into a lexvo IRI."""

from __future__ import annotations

import pycountry

# "United States" is special-cased because pycountry's canonical name for it
# is "United States of America" (exact-name lookup would miss the plain
# "United States" MARC subject heading text IISG's records actually use).
_SPECIAL_CASES = {
    "United States": "US",
}


def country_alpha2(name: str) -> str | None:
    if name in _SPECIAL_CASES:
        return _SPECIAL_CASES[name]
    try:
        matches = pycountry.countries.search_fuzzy(name)
    except LookupError:
        return None
    return matches[0].alpha_2 if matches else None
