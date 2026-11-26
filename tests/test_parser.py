from __future__ import annotations

import math
import unittest
from decimal import Decimal

from indo_terbilang.errors import TerbilangError
from indo_terbilang.parser import parse_numeric_input


class TestParser(unittest.TestCase):
    def test_int_and_zero_and_huge_int(self) -> None:
        self.assertEqual(
            (parse_numeric_input(0).is_negative, parse_numeric_input(0).integer),
            (False, "0"),
        )
        neg = parse_numeric_input(-9007199254740993)
        self.assertEqual((neg.is_negative, neg.integer, neg.fraction), (True, "9007199254740993", ""))

        big = parse_numeric_input(10**35)
        self.assertEqual(big.integer, "1" + "0" * 35)

        with self.assertRaises(TerbilangError) as ctx:
            parse_numeric_input(10**36)
        self.assertEqual(ctx.exception.code, "OUT_OF_RANGE")

        with self.assertRaises(TerbilangError) as huge_ctx:
            parse_numeric_input(10**5000)
        self.assertEqual(huge_ctx.exception.code, "OUT_OF_RANGE")

    def test_bool_rejected(self) -> None:
        for bad in (True, False):
            with self.assertRaises(TerbilangError) as ctx:
                parse_numeric_input(bad)  # type: ignore[arg-type]
            self.assertEqual(ctx.exception.code, "INVALID_INPUT")

    def test_float_and_decimal(self) -> None:
        z = parse_numeric_input(-0.0)
        self.assertEqual((z.is_negative, z.integer, z.fraction), (False, "0", ""))

        sci = parse_numeric_input(1e21)
        self.assertEqual(sci.integer, "1" + "0" * 21)

        small = parse_numeric_input(1e-7)
        self.assertEqual((small.integer, small.fraction), ("0", "0000001"))

        dec = parse_numeric_input(Decimal("12.50"))
        self.assertEqual((dec.integer, dec.fraction), ("12", "50"))

        dec_neg_zero = parse_numeric_input(Decimal("-0.00"))
        self.assertEqual((dec_neg_zero.is_negative, dec_neg_zero.integer), (False, "0"))

        for bad in (math.nan, math.inf, -math.inf, Decimal("NaN"), Decimal("Infinity")):
            with self.assertRaises(TerbilangError) as ctx:
                parse_numeric_input(bad)
            self.assertEqual(ctx.exception.code, "NON_FINITE_NUMBER")

    def test_string_inputs_and_errors(self) -> None:
        p = parse_numeric_input("  +0001500,05 ")
        self.assertEqual((p.is_negative, p.integer, p.fraction), (False, "1500", "05"))

        dot_lead = parse_numeric_input(".5")
        self.assertEqual((dot_lead.integer, dot_lead.fraction), ("0", "5"))

        sci_str = parse_numeric_input("1.5e6")
        self.assertEqual((sci_str.integer, sci_str.fraction), ("1500000", ""))

        sci_small = parse_numeric_input("12.34E-1")
        self.assertEqual((sci_small.integer, sci_small.fraction), ("1", "234"))

        for bad in ("", "   ", "-", "--5", "abc", "12.", "1.500.000", "1.500,00", "1e2e3", None):
            with self.assertRaises(TerbilangError) as ctx:
                parse_numeric_input(bad)  # type: ignore[arg-type]
            self.assertEqual(ctx.exception.code, "INVALID_INPUT")

        for bad_range in ("1" + "0" * 36, "1e101", "1e-101"):
            with self.assertRaises(TerbilangError) as ctx:
                parse_numeric_input(bad_range)
            self.assertEqual(ctx.exception.code, "OUT_OF_RANGE")


if __name__ == "__main__":
    unittest.main()
