from __future__ import annotations

import unittest
from decimal import Decimal

from indo_terbilang import terbilang


class TestTerbilang(unittest.TestCase):
    def test_zero_units_teens_tens_hundreds(self) -> None:
        self.assertEqual(terbilang(0), "nol")
        self.assertEqual(terbilang(-0.0), "nol")
        self.assertEqual(terbilang(1), "satu")
        self.assertEqual(terbilang(10), "sepuluh")
        self.assertEqual(terbilang(11), "sebelas")
        self.assertEqual(terbilang(19), "sembilan belas")
        self.assertEqual(terbilang(21), "dua puluh satu")
        self.assertEqual(terbilang(100), "seratus")
        self.assertEqual(terbilang(111), "seratus sebelas")
        self.assertEqual(terbilang(205), "dua ratus lima")

    def test_scales_and_kbbi_rules(self) -> None:
        self.assertEqual(terbilang(1000), "seribu")
        self.assertEqual(terbilang(1001), "seribu satu")
        self.assertEqual(terbilang(21000), "dua puluh satu ribu")
        self.assertEqual(terbilang(101000), "seratus satu ribu")
        self.assertEqual(terbilang(1000000), "satu juta")
        self.assertEqual(terbilang(1001000), "satu juta seribu")
        self.assertEqual(terbilang(10**9), "satu miliar")
        self.assertEqual(terbilang(10**12), "satu triliun")
        self.assertEqual(terbilang(10**15), "satu kuadriliun")
        self.assertEqual(terbilang(10**33), "satu desiliun")
        self.assertEqual(terbilang("1" + "0" * 35), "seratus desiliun")

    def test_decimals_negative_and_styles(self) -> None:
        self.assertEqual(terbilang(3.14), "tiga koma satu empat")
        self.assertEqual(terbilang("12.05"), "dua belas koma nol lima")
        self.assertEqual(terbilang(Decimal("12.50")), "dua belas koma lima nol")
        self.assertEqual(
            terbilang(Decimal("12.50"), trim_trailing_decimal_zeros=True),
            "dua belas koma lima",
        )
        self.assertEqual(
            terbilang("12.00", trim_trailing_decimal_zeros=True),
            "dua belas",
        )
        self.assertEqual(terbilang(-1500), "minus seribu lima ratus")
        self.assertEqual(
            terbilang(-1500, negative_prefix="negatif", style="sentence"),
            "Negatif seribu lima ratus",
        )
        self.assertEqual(
            terbilang(1500000, style="title", prefix="Terbilang:", suffix="rupiah"),
            "Terbilang: Satu Juta Lima Ratus Ribu Rupiah",
        )


if __name__ == "__main__":
    unittest.main()
