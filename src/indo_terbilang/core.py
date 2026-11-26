from __future__ import annotations

from .constants import SCALES, UNITS
from .errors import assert_max_digits
from .parser import NumericInput, parse_numeric_input
from .rounding import RoundingMode, round_decimal
from .style import TerbilangStyle, apply_style_and_affixes


def _convert_triplet(n: int) -> str:
    words: list[str] = []
    hundreds = n // 100
    remainder = n % 100

    if hundreds == 1:
        words.append("seratus")
    elif hundreds > 1:
        words.extend((UNITS[hundreds], "ratus"))

    if remainder > 0:
        if remainder < 10:
            words.append(UNITS[remainder])
        elif remainder == 10:
            words.append("sepuluh")
        elif remainder == 11:
            words.append("sebelas")
        elif remainder < 20:
            words.extend((UNITS[remainder - 10], "belas"))
        else:
            tens = remainder // 10
            ones = remainder % 10
            words.extend((UNITS[tens], "puluh"))
            if ones > 0:
                words.append(UNITS[ones])

    return " ".join(words)


def _convert_integer_to_words(integer_str: str) -> str:
    if integer_str == "0":
        return "nol"

    segments: list[str] = []
    scale_idx = 0

    for end in range(len(integer_str), 0, -3):
        start = max(0, end - 3)
        chunk_val = int(integer_str[start:end])

        if chunk_val > 0:
            if scale_idx == 1 and chunk_val == 1:
                segments.append("seribu")
            else:
                words = _convert_triplet(chunk_val)
                scale_word = SCALES[scale_idx]
                segments.append(f"{words} {scale_word}" if scale_word else words)

        scale_idx += 1

    segments.reverse()
    return " ".join(segments)


def terbilang(
    value: NumericInput,
    *,
    style: TerbilangStyle = "lower",
    prefix: str | None = None,
    suffix: str | None = None,
    negative_prefix: str = "minus",
    decimal_word: str = "koma",
    trim_trailing_decimal_zeros: bool = False,
) -> str:
    """Mengonversi angka (`int | float | Decimal | str`) menjadi kalimat terbilang Bahasa Indonesia baku."""
    parsed = parse_numeric_input(value)
    fraction = (
        parsed.fraction.rstrip("0") if trim_trailing_decimal_zeros else parsed.fraction
    )

    int_words = _convert_integer_to_words(parsed.integer)
    text = int_words

    if fraction:
        frac_words = " ".join(UNITS[ord(ch) - 48] for ch in fraction)
        text = f"{int_words} {decimal_word.strip()} {frac_words}"

    if parsed.is_negative:
        text = f"{negative_prefix.strip()} {text}"

    return apply_style_and_affixes(text, style=style, prefix=prefix, suffix=suffix)


def terbilang_rupiah(
    value: NumericInput,
    *,
    style: TerbilangStyle = "lower",
    prefix: str | None = None,
    suffix: str | None = None,
    negative_prefix: str = "minus",
    currency_unit: str = "rupiah",
    include_sen: bool = True,
    sen_unit: str = "sen",
    rounding: RoundingMode = "half-up",
) -> str:
    """Mengonversi nominal angka menjadi kalimat terbilang mata uang Rupiah lengkap dengan sen."""
    parsed = parse_numeric_input(value)
    decimals = 2 if include_sen else 0
    rounded_int, rounded_frac = round_decimal(
        parsed.integer, parsed.fraction, decimals, rounding
    )

    assert_max_digits(rounded_int)

    sen_val = int(rounded_frac) if include_sen else 0
    is_zero = rounded_int == "0" and sen_val == 0
    is_negative = False if is_zero else parsed.is_negative

    int_words = _convert_integer_to_words(rounded_int)
    text = f"{int_words} {currency_unit.strip()}"

    if sen_val > 0:
        text = f"{text} {_convert_triplet(sen_val)} {sen_unit.strip()}"

    if is_negative:
        text = f"{negative_prefix.strip()} {text}"

    return apply_style_and_affixes(text, style=style, prefix=prefix, suffix=suffix)
