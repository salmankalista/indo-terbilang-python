from __future__ import annotations

from typing import Literal

from .constants import COMPACT_UNITS, ZERO_ONLY_PATTERN
from .errors import TerbilangError
from .parser import NumericInput, parse_numeric_input
from .rounding import RoundingMode, round_decimal

NegativeFormat = Literal["minus", "parentheses"]


def _insert_thousands_separator(int_str: str, separator: str) -> str:
    if separator == "" or len(int_str) <= 3:
        return int_str
    groups = [
        int_str[max(0, end - 3) : end] for end in range(len(int_str), 0, -3)
    ]
    groups.reverse()
    return separator.join(groups)


def _apply_rupiah_affixes(
    number_text: str,
    *,
    is_negative: bool,
    symbol: str,
    space_after_symbol: bool,
    negative_format: NegativeFormat,
) -> str:
    if symbol:
        core = f"{symbol}{' ' if space_after_symbol else ''}{number_text}"
    else:
        core = number_text

    if not is_negative:
        return core
    return f"({core})" if negative_format == "parentheses" else f"-{core}"


def _divide_by_power_and_round(
    integer: str,
    fraction: str,
    power: int,
    decimals: int,
    rounding: RoundingMode,
) -> tuple[str, str]:
    split_at = len(integer) - power
    shifted_int = integer[:split_at] if split_at > 0 else "0"
    shifted_frac = (
        integer[split_at:] if split_at > 0 else integer.rjust(power, "0")
    ) + fraction
    return round_decimal(shifted_int, shifted_frac, decimals, rounding)


def _format_compact_rupiah(
    is_negative_input: bool,
    integer: str,
    fraction: str,
    *,
    symbol: str,
    space_after_symbol: bool,
    thousands_separator: str,
    decimal_separator: str,
    rounding: RoundingMode,
    negative_format: NegativeFormat,
    compact_decimals: int,
) -> str:
    if (
        isinstance(compact_decimals, bool)
        or not isinstance(compact_decimals, int)
        or compact_decimals < 0
        or compact_decimals > 6
    ):
        raise TerbilangError("INVALID_INPUT", "Opsi compact_decimals harus 0-6.")

    scale_idx = -1
    for i, (power, _) in enumerate(COMPACT_UNITS):
        if len(integer) > power:
            scale_idx = i
            break

    rounded_int = integer
    rounded_frac = fraction
    label = ""

    if scale_idx == -1:
        rounded_int, rounded_frac = round_decimal(
            integer, fraction, compact_decimals, rounding
        )
        if len(rounded_int) > 3:
            scale_idx = len(COMPACT_UNITS) - 1

    if scale_idx != -1:
        power, unit_label = COMPACT_UNITS[scale_idx]
        rounded_int, rounded_frac = _divide_by_power_and_round(
            integer, fraction, power, compact_decimals, rounding
        )
        if len(rounded_int) > 3 and scale_idx > 0:
            power, unit_label = COMPACT_UNITS[scale_idx - 1]
            rounded_int, rounded_frac = _divide_by_power_and_round(
                integer, fraction, power, compact_decimals, rounding
            )
        label = f" {unit_label}"

    final_frac = rounded_frac.rstrip("0")
    is_zero = rounded_int == "0" and final_frac == ""
    is_negative = False if is_zero else is_negative_input
    formatted_int = _insert_thousands_separator(rounded_int, thousands_separator)
    number_part = (
        f"{formatted_int}{decimal_separator}{final_frac}"
        if final_frac
        else formatted_int
    )

    return _apply_rupiah_affixes(
        f"{number_part}{label}",
        is_negative=is_negative,
        symbol=symbol,
        space_after_symbol=space_after_symbol,
        negative_format=negative_format,
    )


def format_rupiah(
    value: NumericInput,
    *,
    symbol: str = "Rp",
    space_after_symbol: bool = True,
    thousands_separator: str = ".",
    decimal_separator: str = ",",
    decimals: int | Literal["auto"] = 2,
    rounding: RoundingMode = "half-up",
    negative_format: NegativeFormat = "minus",
    compact: bool = False,
    compact_decimals: int = 1,
) -> str:
    """Memformat angka (`int | float | Decimal | str`) menjadi string mata uang Rupiah secara deterministik."""
    if negative_format not in ("minus", "parentheses"):
        raise TerbilangError(
            "INVALID_INPUT", f'Opsi negative_format tidak valid: "{negative_format}".'
        )

    parsed = parse_numeric_input(value)

    if compact:
        return _format_compact_rupiah(
            parsed.is_negative,
            parsed.integer,
            parsed.fraction,
            symbol=symbol,
            space_after_symbol=space_after_symbol,
            thousands_separator=thousands_separator,
            decimal_separator=decimal_separator,
            rounding=rounding,
            negative_format=negative_format,
            compact_decimals=compact_decimals,
        )

    if decimals != "auto" and (
        isinstance(decimals, bool)
        or not isinstance(decimals, int)
        or decimals < 0
        or decimals > 20
    ):
        raise TerbilangError(
            "INVALID_INPUT", "Opsi decimals harus 'auto' atau integer 0-20."
        )

    if decimals == "auto":
        final_int = parsed.integer
        final_frac = parsed.fraction.rstrip("0")
        is_negative = parsed.is_negative
    else:
        final_int, final_frac = round_decimal(
            parsed.integer, parsed.fraction, decimals, rounding
        )
        is_zero = (
            final_int == "0" and ZERO_ONLY_PATTERN.fullmatch(final_frac) is not None
        )
        is_negative = False if is_zero else parsed.is_negative

    formatted_int = _insert_thousands_separator(final_int, thousands_separator)
    number_text = (
        f"{formatted_int}{decimal_separator}{final_frac}"
        if final_frac
        else formatted_int
    )

    return _apply_rupiah_affixes(
        number_text,
        is_negative=is_negative,
        symbol=symbol,
        space_after_symbol=space_after_symbol,
        negative_format=negative_format,
    )
