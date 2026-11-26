from __future__ import annotations

import unittest

from indo_terbilang import TerbilangError, parse_rupiah, terbilang_rupiah


class TestParseRupiah(unittest.TestCase):
    def test_valid_parsing(self) -> None:
        self.assertEqual(parse_rupiah("Rp 1.500.000,50"), "1500000.50")
        self.assertEqual(parse_rupiah("Rp1.500.000"), "1500000")
        self.assertEqual(parse_rupiah("IDR 2.500.000,75"), "2500000.75")
        self.assertEqual(parse_rupiah("-Rp 500.000,25"), "-500000.25")
        self.assertEqual(parse_rupiah("(Rp 500.000,25)"), "-500000.25")
        self.assertEqual(parse_rupiah("(Rp 0,00)"), "0.00")
        self.assertEqual(
            terbilang_rupiah(parse_rupiah("Rp 1.500.000,50")),
            "satu juta lima ratus ribu rupiah lima puluh sen",
        )

    def test_invalid_parsing(self) -> None:
        for bad in ("", "Rp ", "Rp abc", "Rp 1.50.000", "Rp 1.000,", "(-Rp 500)", 123):
            with self.assertRaises(TerbilangError):
                parse_rupiah(bad)  # type: ignore[arg-type]

        with self.assertRaises(TerbilangError) as ctx:
            parse_rupiah("Rp " + "1" * 37)
        self.assertEqual(ctx.exception.code, "OUT_OF_RANGE")


if __name__ == "__main__":
    unittest.main()
