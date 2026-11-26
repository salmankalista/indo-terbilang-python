from __future__ import annotations

from typing import Literal

from .errors import TerbilangError

TerbilangStyle = Literal["lower", "upper", "title", "sentence"]


def apply_style_and_affixes(
    text: str,
    *,
    style: TerbilangStyle = "lower",
    prefix: str | None = None,
    suffix: str | None = None,
) -> str:
    """Menggabungkan awalan/akhiran lalu menerapkan transformasi gaya huruf (`style`)."""
    parts: list[str] = []

    if prefix is not None:
        clean_prefix = prefix.strip()
        if clean_prefix:
            parts.append(clean_prefix)

    parts.append(text)

    if suffix is not None:
        clean_suffix = suffix.strip()
        if clean_suffix:
            parts.append(clean_suffix)

    combined = " ".join(parts)

    if style == "lower":
        return combined.lower()
    if style == "upper":
        return combined.upper()
    if style == "title":
        return " ".join(
            (word[:1].upper() + word[1:].lower()) if word else ""
            for word in combined.split(" ")
        )
    if style == "sentence":
        return combined[:1].upper() + combined[1:].lower()

    raise TerbilangError("INVALID_INPUT", f'Style tidak valid: "{style}".')
