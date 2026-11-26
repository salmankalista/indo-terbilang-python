# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-26

### Added
- `terbilang(value, ...)`: Konversi angka (`int | float | Decimal | str`) ke kalimat terbilang Bahasa Indonesia baku (EYD V / KBBI) dari `0` hingga skala `desiliun` ($10^{36}-1$).
- `terbilang_rupiah(value, ...)`: Konversi nominal finansial ke kalimat terbilang Rupiah lengkap dengan sen dan pembulatan eksak berbasis string (`half-up` / `truncate`).
- `format_rupiah(value, ...)`: Pemformat mata uang Rupiah deterministik (tanpa ketergantungan locale OS) dengan opsi desimal, format negatif minus/kurung, dan notasi ringkas `compact` (`rb`, `jt`, `M`, `T`).
- `parse_rupiah(value)`: Parser aman untuk mengekstrak string format Rupiah menjadi string numerik kanonik.
- `TerbilangError`: Exception turunan `ValueError` dengan kode terstruktur `INVALID_INPUT`, `NON_FINITE_NUMBER`, dan `OUT_OF_RANGE`.
- Zero runtime dependencies serta dukungan penuh type hints (PEP 561 `py.typed`).
