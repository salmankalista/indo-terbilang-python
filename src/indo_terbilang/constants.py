from __future__ import annotations

import re
from typing import Final

MAX_INTEGER_DIGITS: Final[int] = 36
MAX_EXPONENT_ABS: Final[int] = 100

ZERO_ONLY_PATTERN: Final[re.Pattern[str]] = re.compile(r"0*")

UNITS: Final[tuple[str, ...]] = (
    "nol",
    "satu",
    "dua",
    "tiga",
    "empat",
    "lima",
    "enam",
    "tujuh",
    "delapan",
    "sembilan",
)

SCALES: Final[tuple[str, ...]] = (
    "",
    "ribu",
    "juta",
    "miliar",
    "triliun",
    "kuadriliun",
    "kuintiliun",
    "sekstiliun",
    "septiliun",
    "oktiliun",
    "noniliun",
    "desiliun",
)

COMPACT_UNITS: Final[tuple[tuple[int, str], ...]] = (
    (12, "T"),
    (9, "M"),
    (6, "jt"),
    (3, "rb"),
)
