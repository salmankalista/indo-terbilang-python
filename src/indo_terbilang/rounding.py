from __future__ import annotations

from typing import Literal

from .errors import TerbilangError

RoundingMode = Literal["half-up", "truncate"]


def round_decimal(
    integer: str,
    fraction: str,
    decimals: int,
    mode: RoundingMode,
) -> tuple[str, str]:
    """Membulatkan angka desimal berbasis string secara eksak tanpa floating-point arithmetic."""
    if isinstance(decimals, bool) or not isinstance(decimals, int) or decimals < 0:
        raise TerbilangError("INVALID_INPUT", "Desimal pembulatan tidak valid.")

    if mode not in ("half-up", "truncate"):
        raise TerbilangError("INVALID_INPUT", f'Mode pembulatan tidak valid: "{mode}".')

    if len(fraction) == decimals:
        return integer, fraction

    if len(fraction) < decimals:
        return integer, fraction.ljust(decimals, "0")

    kept_fraction = fraction[:decimals]
    next_digit = ord(fraction[decimals]) - 48

    if mode == "truncate" or next_digit < 5:
        return integer, kept_fraction

    digits = list(integer + kept_fraction)
    carry = 1
    for i in range(len(digits) - 1, -1, -1):
        if carry == 0:
            break
        total = int(digits[i]) + carry
        if total >= 10:
            digits[i] = str(total - 10)
        else:
            digits[i] = str(total)
            carry = 0

    if carry > 0:
        digits.insert(0, "1")

    merged = "".join(digits)
    if decimals == 0:
        return merged, ""

    split_idx = len(merged) - decimals
    return merged[:split_idx], merged[split_idx:]
