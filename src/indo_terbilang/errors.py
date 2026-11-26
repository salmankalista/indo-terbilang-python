from __future__ import annotations

from typing import Literal

from .constants import MAX_INTEGER_DIGITS

TerbilangErrorCode = Literal[
    "INVALID_INPUT",
    "NON_FINITE_NUMBER",
    "OUT_OF_RANGE",
]


class TerbilangError(ValueError):
    """Exception terstruktur yang dilempar ketika input atau opsi tidak valid."""

    def __init__(self, code: TerbilangErrorCode, message: str) -> None:
        super().__init__(message)
        self.code: TerbilangErrorCode = code


def assert_max_digits(integer_str: str) -> None:
    """Memastikan panjang digit bagian bulat tidak melebihi batas skala desiliun."""
    if len(integer_str) > MAX_INTEGER_DIGITS:
        raise TerbilangError(
            "OUT_OF_RANGE",
            f"Melebihi batas {MAX_INTEGER_DIGITS} digit.",
        )
