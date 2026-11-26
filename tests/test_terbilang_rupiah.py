from __future__ import annotations

import unittest
from decimal import Decimal

from indo_terbilang import TerbilangError, terbilang_rupiah


class TestTerbilangRupiah(unittest.TestCase):
    def test_rupiah_and_sen(self) -> None:
        self.assertEqual(terbilang_rupiah(0), "nol rupiah")
        self.assertEqual(terbilang_rupiah(1000), "seribu rupiah")
        self.assertEqual(
            terbilang_rupiah(Decimal("1250.50")),
            "seribu dua ratus lima puluh rupiah lima puluh sen",
        )
        self.assertEqual(
            terbilang_rupiah("1250.05"),
            "seribu dua ratus lima puluh rupiah lima sen",
        )
        self.assertEqual(terbilang_rupiah("1250.00"), "seribu dua ratus lima puluh rupiah")
        self.assertEqual(terbilang_rupiah("-0.001"), "nol rupiah")
        self.assertEqual(
            terbilang_rupiah("1250.996"),
            "seribu dua ratus lima puluh satu rupiah",
        )
        self.assertEqual(
            terbilang_rupiah("1250.996", rounding="truncate"),
            "seribu dua ratus lima puluh rupiah sembilan puluh sembilan sen",
        )
        self.assertEqual(
            terbilang_rupiah(1250.6, include_sen=False, style="sentence"),
            "Seribu dua ratus lima puluh satu rupiah",
        )

    def test_overflow_after_rounding(self) -> None:
        with self.assertRaises(TerbilangError) as ctx:
            terbilang_rupiah("9" * 36 + ".999")
        self.assertEqual(ctx.exception.code, "OUT_OF_RANGE")


if __name__ == "__main__":
    unittest.main()
