from __future__ import annotations

import math
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from .constants import MAX_EXPONENT_ABS, MAX_INTEGER_DIGITS, ZERO_ONLY_PATTERN
from .errors import TerbilangError, assert_max_digits

NumericInput = Union[int, float, Decimal, str]

_MAX_ABS_INT = 10**MAX_INTEGER_DIGITS
_DECIMAL_PATTERN = re.compile(r"(?:\d+(?:\.\d+)?|\.\d+)")
_EXPONENT_PATTERN = re.compile(r"[+-]?\d+")


@dataclass(frozen=True, slots=True)
class ParsedDecimal:
    is_negative: bool
    integer: str
    fraction: str


def _normalize_decimal_separator(raw: str) -> str:
    if "." in raw and "," in raw:
        raise TerbilangError("INVALID_INPUT", "Pemisah titik dan koma bercampur.")
    normalized = raw.replace(",", ".") if "," in raw else raw
    if _DECIMAL_PATTERN.fullmatch(normalized) is None:
        raise TerbilangError("INVALID_INPUT", f'Format angka tidak valid: "{raw}".')
    return normalized


def _expand_scientific(mantissa: str, exp: int) -> tuple[str, str]:
    dot_idx = mantissa.find(".")
    int_part = mantissa if dot_idx == -1 else mantissa[:dot_idx]
    frac_part = "" if dot_idx == -1 else mantissa[dot_idx + 1 :]
    digits = int_part + frac_part
    new_dot_pos = len(int_part) + exp

    if new_dot_pos <= 0:
        return "0", ("0" * (-new_dot_pos)) + digits
    if new_dot_pos >= len(digits):
        return digits + ("0" * (new_dot_pos - len(digits))), ""
    return digits[:new_dot_pos], digits[new_dot_pos:]


def _split_standard_decimal(normalized: str) -> tuple[str, str]:
    dot_idx = normalized.find(".")
    if dot_idx == -1:
        return normalized, ""
    int_part = normalized[:dot_idx]
    return ("0" if int_part == "" else int_part), normalized[dot_idx + 1 :]


def parse_numeric_input(value: NumericInput) -> ParsedDecimal:
    """Memvalidasi dan menormalisasi `int | float | Decimal | str` ke struktur desimal berbasis string."""
    if isinstance(value, bool):
        raise TerbilangError("INVALID_INPUT", "Tipe bool tidak didukung.")

    raw: str
    if isinstance(value, int):
        is_negative = value < 0
        abs_val = -value if is_negative else value
        if abs_val >= _MAX_ABS_INT:
            raise TerbilangError(
                "OUT_OF_RANGE",
                f"Melebihi batas {MAX_INTEGER_DIGITS} digit.",
            )
        return ParsedDecimal(
            is_negative=is_negative, integer=str(abs_val), fraction=""
        )

    if isinstance(value, float):
        if not math.isfinite(value):
            raise TerbilangError("NON_FINITE_NUMBER", "Angka harus finite.")
        if value == 0.0:
            return ParsedDecimal(is_negative=False, integer="0", fraction="")
        raw = repr(value)
    elif isinstance(value, Decimal):
        if not value.is_finite():
            raise TerbilangError("NON_FINITE_NUMBER", "Decimal harus finite.")
        raw = str(value)
    elif isinstance(value, str):
        raw = value.strip()
        if raw == "":
            raise TerbilangError("INVALID_INPUT", "Input kosong.")
    else:
        raise TerbilangError("INVALID_INPUT", "Tipe input tidak didukung.")

    is_negative = False
    body = raw
    if body.startswith("-"):
        is_negative = True
        body = body[1:]
    elif body.startswith("+"):
        body = body[1:]

    e_idx = body.find("e")
    if e_idx == -1:
        e_idx = body.find("E")

    if e_idx != -1:
        mantissa = _normalize_decimal_separator(body[:e_idx])
        exp_raw = body[e_idx + 1 :]
        if _EXPONENT_PATTERN.fullmatch(exp_raw) is None:
            raise TerbilangError("INVALID_INPUT", "Eksponen tidak valid.")
        exp = int(exp_raw)
        if abs(exp) > MAX_EXPONENT_ABS:
            raise TerbilangError("OUT_OF_RANGE", "Eksponen melebihi batas.")
        integer, fraction = _expand_scientific(mantissa, exp)
    else:
        integer, fraction = _split_standard_decimal(_normalize_decimal_separator(body))

    trimmed_integer = integer.lstrip("0") or "0"
    assert_max_digits(trimmed_integer)

    is_zero = (
        trimmed_integer == "0" and ZERO_ONLY_PATTERN.fullmatch(fraction) is not None
    )
    return ParsedDecimal(
        is_negative=False if is_zero else is_negative,
        integer=trimmed_integer,
        fraction=fraction,
    )
