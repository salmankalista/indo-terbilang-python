from __future__ import annotations

import unittest

from indo_terbilang.errors import TerbilangError
from indo_terbilang.style import apply_style_and_affixes


class TestStyle(unittest.TestCase):
    def test_styles_and_affixes(self) -> None:
        sample = "satu juta dua ratus ribu"
        self.assertEqual(apply_style_and_affixes(sample, style="lower"), sample)
        self.assertEqual(
            apply_style_and_affixes(sample, style="upper"),
            "SATU JUTA DUA RATUS RIBU",
        )
        self.assertEqual(
            apply_style_and_affixes(sample, style="title"),
            "Satu Juta Dua Ratus Ribu",
        )
        self.assertEqual(
            apply_style_and_affixes(sample, style="sentence"),
            "Satu juta dua ratus ribu",
        )
        self.assertEqual(
            apply_style_and_affixes(
                "seribu", style="title", prefix="  sejumlah ", suffix=" rupiah  "
            ),
            "Sejumlah Seribu Rupiah",
        )

    def test_invalid_style(self) -> None:
        with self.assertRaises(TerbilangError):
            apply_style_and_affixes("seribu", style="camel")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
