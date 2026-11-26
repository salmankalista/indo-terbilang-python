from __future__ import annotations

import unittest

from indo_terbilang.errors import TerbilangError
from indo_terbilang.rounding import round_decimal


class TestRounding(unittest.TestCase):
    def test_exact_padding_and_half_up(self) -> None:
        self.assertEqual(round_decimal("1500", "50", 2, "half-up"), ("1500", "50"))
        self.assertEqual(round_decimal("1500", "5", 2, "half-up"), ("1500", "50"))
        self.assertEqual(round_decimal("1250", "234", 2, "half-up"), ("1250", "23"))
        self.assertEqual(round_decimal("1250", "235", 2, "half-up"), ("1250", "24"))
        self.assertEqual(round_decimal("1250", "996", 2, "half-up"), ("1251", "00"))
        self.assertEqual(round_decimal("999", "995", 2, "half-up"), ("1000", "00"))
        self.assertEqual(round_decimal("9", "5", 0, "half-up"), ("10", ""))

    def test_truncate_and_invalid_options(self) -> None:
        self.assertEqual(round_decimal("1250", "999", 2, "truncate"), ("1250", "99"))
        self.assertEqual(round_decimal("999", "9", 0, "truncate"), ("999", ""))

        for bad_dec in (-1, True, 1.5):
            with self.assertRaises(TerbilangError):
                round_decimal("10", "5", bad_dec, "half-up")  # type: ignore[arg-type]

        with self.assertRaises(TerbilangError):
            round_decimal("10", "5", 2, "ceil")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
