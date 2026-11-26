from __future__ import annotations

import re

from .constants import ZERO_ONLY_PATTERN
from .errors import TerbilangError, assert_max_digits

_CURRENCY_PREFIX_PATTERN = re.compile(r"^(?:rp|idr)\s*", re.IGNORECASE)
_GROUPED_THOUSANDS_PATTERN = re.compile(r"\d{1,3}(?:\.\d{3})+")
_PLAIN_DIGITS_PATTERN = re.compile(r"\d+")


def parse_rupiah(value: str) -> str:
    """Mengekstrak string terformat Rupiah menjadi string numerik kanonik."""
    if not isinstance(value, str):
        raise TerbilangError("INVALID_INPUT", "Input harus string.")

    raw = value.strip()
    if raw == "":
        raise TerbilangError("INVALID_INPUT", "Input kosong.")

    is_negative = False
    if raw.startswith("(") and raw.endswith(")"):
        is_negative = True
        raw = raw[1:-1].strip()
        if raw.startswith("-") or raw.startswith("+"):
            raise TerbilangError("INVALID_INPUT", "Tanda negatif ganda tidak valid.")
    elif raw.startswith("-"):
        is_negative = True
        raw = raw[1:].strip()
    elif raw.startswith("+"):
        raw = raw[1:].strip()

    raw = _CURRENCY_PREFIX_PATTERN.sub("", raw).strip()

    comma_idx = raw.find(",")
    if comma_idx != -1:
        int_raw = raw[:comma_idx]
        frac_raw = raw[comma_idx + 1 :]
        if _PLAIN_DIGITS_PATTERN.fullmatch(frac_raw) is None:
            raise TerbilangError("INVALID_INPUT", "Bagian desimal Rupiah tidak valid.")
    else:
        int_raw = raw
        frac_raw = ""

    if "." in int_raw:
        if _GROUPED_THOUSANDS_PATTERN.fullmatch(int_raw) is None:
            raise TerbilangError("INVALID_INPUT", "Pemisah ribuan tidak valid.")
        clean_int = int_raw.replace(".", "")
    else:
        if _PLAIN_DIGITS_PATTERN.fullmatch(int_raw) is None:
            raise TerbilangError("INVALID_INPUT", "Format Rupiah tidak valid.")
        clean_int = int_raw

    normalized_int = clean_int.lstrip("0") or "0"
    assert_max_digits(normalized_int)

    is_zero = (
        normalized_int == "0" and ZERO_ONLY_PATTERN.fullmatch(frac_raw) is not None
    )
    sign = "-" if is_negative and not is_zero else ""

    return f"{sign}{normalized_int}.{frac_raw}" if frac_raw else f"{sign}{normalized_int}"
