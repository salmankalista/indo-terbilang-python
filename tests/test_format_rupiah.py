from __future__ import annotations

import unittest
from decimal import Decimal

from indo_terbilang import TerbilangError, format_rupiah


class TestFormatRupiah(unittest.TestCase):
    def test_standard_formatting(self) -> None:
        self.assertEqual(format_rupiah(0), "Rp 0,00")
        self.assertEqual(format_rupiah(-0.0), "Rp 0,00")
        self.assertEqual(format_rupiah(1500000), "Rp 1.500.000,00")
        self.assertEqual(format_rupiah(Decimal("1250.567")), "Rp 1.250,57")
        self.assertEqual(format_rupiah(1500000, decimals=0), "Rp 1.500.000")
        self.assertEqual(format_rupiah("1500.50", decimals="auto"), "Rp 1.500,5")
        self.assertEqual(format_rupiah(1500, symbol="", thousands_separator=""), "1500,00")

    def test_negatives_and_compact(self) -> None:
        self.assertEqual(format_rupiah(-1500000), "-Rp 1.500.000,00")
        self.assertEqual(
            format_rupiah(-1500000, negative_format="parentheses"),
            "(Rp 1.500.000,00)",
        )
        self.assertEqual(format_rupiah("-0.001"), "Rp 0,00")
        self.assertEqual(format_rupiah(500, compact=True), "Rp 500")
        self.assertEqual(format_rupiah(1500000, compact=True), "Rp 1,5 jt")
        self.assertEqual(
            format_rupiah(2350000000, compact=True, compact_decimals=2),
            "Rp 2,35 M",
        )
        self.assertEqual(format_rupiah("999.96", compact=True), "Rp 1 rb")
        self.assertEqual(format_rupiah(999990, compact=True), "Rp 1 jt")

    def test_invalid_options(self) -> None:
        for bad in (-1, 21, True, 1.5):
            with self.assertRaises(TerbilangError):
                format_rupiah(1000, decimals=bad)  # type: ignore[arg-type]
        for bad in (-1, 7, True):
            with self.assertRaises(TerbilangError):
                format_rupiah(1000, compact=True, compact_decimals=bad)
        with self.assertRaises(TerbilangError):
            format_rupiah(1000, negative_format="brackets")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
